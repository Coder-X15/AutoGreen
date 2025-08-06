from google.genai import types

# function declarations & tool definitions

# this tool is called when the agent is asked to water a specific region
# of the greenhouse
water_function = types.FunctionDeclaration(
    name="water_area",
    description="Water the specified area of the greenhouse.",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties={
            "area": types.Schema(
                type=types.Type.STRING,
                description="The section of the greenhouse to water."
            )
        },
        required=["area"]
    )
)

# this tool is called when the agent is asked to fetch the status of 
# a specific region of the greenhouse
status_function = types.FunctionDeclaration(
    name="area_status",
    description="To fetch the status of the specified area of the greenhouse.",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties={
            "area": types.Schema(
                type=types.Type.STRING,
                description="The section of the greenhouse to query for \
                (e.g., 'north', 'south', 'east', 'west')."
            )
        },
        required=["area"]
    )
)


# tool declarations
waterCommand = types.Tool(function_declarations=[water_function]) # water command
statusCommand = types.Tool(function_declarations=[status_function]) # status command
