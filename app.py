from agent.agent import Agent
from flask import Flask, request, jsonify
from flask_cors import CORS
# defining the agent instance
agent = Agent()

# defining the Flask app
app = Flask(__name__)

# enabling CORS for the app
CORS(app)

# defining the route for the chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to chat with the agent.
    Expects a JSON payload with a 'user' field.
    """
    data = request.get_json()
    user_input = data.get('user', '')

    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    try:
        response = agent.chat(user_input)
        return jsonify({"assistant": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')