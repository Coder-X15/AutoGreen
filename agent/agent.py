import dotenv
import google.genai as genai
from google.genai import types
import os
from .tools import *
from .database_access import DBAccessor
from typing import Dict, Union

# prompts

# 1. Intent identification
INTENT_PROMPT = """
Identify the intent of the user from the given text, according to the following categories:
- Watering: The user is asking to water a specific area of the greenhouse.
- Status: The user is asking for the status of a specific area of the greenhouse.
- None: The user is in a normal conversation
- Fallback: If the user asks for something that is not related to greenhouse maintenance
"""

# 2. Tool call generation
TOOL_CALL_PROMPT = """From the user input, extract the region of the greenhouse that the user has included in their query.
                      If the user is asking to water a specific area, indicated by a number from 0 to 3, call the `water_area` function with the number as an argument.
                      If the user is asking for the status of a specific area, call the `area_status` function with the number as an argument.
"""

# 3. Fallback message
FALLBACK_MESSAGE = """The user is asking for something that is not related to greenhouse maintenance or normal conversation.
                      Please respond with a fallback message, citing you inability to help with it."""

class Agent:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        # load environment variables
        dotenv.load_dotenv()

        # load the Gen-AI client with the API key
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # initialize the database accessor
        self.db_accessor = DBAccessor(
            supabase_url=os.getenv("SUPABASE_URL"), # type: ignore
            supabase_key=os.getenv("SUPABASE_KEY") # type: ignore
        )


        # storing the model name
        self.model = model_name

        # initializing an empty chat history
        self.chat_history = []

    def getIntent(self, user_input: str):
        """
        Identify the intent of the user input.
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents= types.UserContent(
                parts = [user_input]
            ),
            config = types.GenerateContentConfig(
                system_instruction=INTENT_PROMPT
            )
        )
        return response.text.strip() if response.text else None

    def getFunctionCall(self, user_input: str):
        """
        Get the function call based on the user input.
        """
        # append chat to chat history
        self.chat_history.append(
            types.UserContent(
                parts = [user_input]
            )
        )

        # generate the function call
        response = self.client.models.generate_content(
            model=self.model,
            contents= types.UserContent(
                parts = [user_input]
            ),
            config = types.GenerateContentConfig(
                system_instruction=TOOL_CALL_PROMPT,
                tools=[waterCommand, statusCommand],
            )
        )

        # return the function call if it exists
        function_call_part = response.function_calls[0] if response.function_calls else None
        function_call_content = response.candidates[0].content if response.candidates else None

        return function_call_part, function_call_content

    
    def executeFunctionCall(self, function_args: Union[Dict[str, str], None], function_name: str):
        """
        Execute the function call.
        """
       # raise NotImplementedError("Function execution is not implemented yet.")
        if not function_args:
            raise ValueError("Function arguments are required for execution.")
        if function_name == "water_area":
            # print(f"Watering section : {function_args['area']}") # debug line
            # raise RuntimeError("Watering function is not implemented yet.")
            section_id = function_args['area']
            try:
                self.db_accessor.water_section(section_id)
                return f"Section {section_id} has been watered successfully."
            except RuntimeError as e:
                return str(e)
        elif function_name == "area_status":
            # print(f"Fetching status for section : {function_args['area']}") # debug line
            # raise RuntimeError("Status function is not implemented yet.")
            section_id = function_args['area']
            try:
                section_state = self.db_accessor.get_section_state(section_id)
                return f"Section {section_id} status: {'Watered' if section_state['is_watered'] else 'Not Watered'}, Last Watered: {section_state['last_watered']}"
            except RuntimeError as e:  
                return str(e)
        else:
            raise ValueError(f"Unknown function name: {function_name}")
    
    def chat(self, user_input: str):
        """
        Chat with the agent.
        """
        # get the intent of the user input
        intent = self.getIntent(user_input)

        # if the intent is None, continue with normal conversation
        if intent == "None":
            self.chat_history.append(
                types.UserContent(
                    parts = [user_input]
                )
            )

            # generate the response
            reply =  self.client.models.generate_content(
                model=self.model,
                contents=self.chat_history
            ).text

            reply = reply.strip() # type: ignore

            # append model response to chat history
            self.chat_history.append(
                types.ModelContent(
                    parts=[reply]
                )
            )
            return reply
        # if the intent is Fallback, return a fallback message
        elif intent == "Fallback":
            return self.client.models.generate_content(
                model=self.model,
                contents=types.UserContent(
                    parts=[user_input]
                ),
                config=types.GenerateContentConfig(
                    system_instruction=FALLBACK_MESSAGE
                )
            ).text
        
        # if the intent is Watering or Status, get the function call
        elif intent in ["Watering", "Status"]:
            function_call_part, function_call_content = self.getFunctionCall(user_input)
            function_name = function_call_part.name if function_call_part else None
            if function_name:
                # execute the function call
                return self.executeFunctionCall(function_call_part.args, function_name) # type:ignore
            else:
                raise RuntimeError("No function call generated. Please try again.")

if __name__ == "__main__":
    agent = Agent()
    user_input = input("User:")
    response = agent.chat(user_input)
    print("Agent:",response)  # This will print the response from the agent