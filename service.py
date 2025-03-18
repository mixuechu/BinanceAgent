from flask import Flask, request, Response
import json
import time
import random

from model import ModelManager
from tool import tool_manager

app = Flask(__name__)

# Initialize ModelManager
model_manager = ModelManager()


# Initialize SessionManager
class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        self.sessions[session_id] = {"history": []}

    def add_to_history(self, session_id, message):
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id]["history"].append(message)

    def get_history(self, session_id):
        return self.sessions.get(session_id, {}).get("history", [])


session_manager = SessionManager()


def handle_chat(prompt, session_id, model_manager, tool_manager):
    """
    Process user input, determine whether a tool needs to be called, and generate a response.
    :param prompt: User input
    :param session_id: Session ID
    :param model_manager: Model management module
    :param tool_manager: Tool management module
    :return: AI-generated response
    """
    # Retrieve session history
    history = session_manager.get_history(session_id)
    messages = history.copy()
    tool_prompt = (
            "You are a helpful AI assistant. You have access to the following tools:\n"
            + "\n".join(
        [f"- {tool['name']}: {tool['description']} - parameters: arguments: {tool['parameters']}" for tool in
         tool_manager.get_tool_descriptions()])
            + "\n\n"
              "If you need to use a tool, respond with a JSON object containing the following fields:\n"
              "1. `function_call`: A dictionary with `name` (the tool name) and `arguments` (a JSON string of the tool's input parameters).\n"
              "2. `content`: A brief explanation of why you are calling the tool.\n"
              "Remember, if some argument is missing, and the argument itself is rather trivial, you can fill it with a default value. For example, if the argument LIMIT is missing, put a 5 or 1."
              "Example:\n"
              "```json\n"
              "{\n"
              '  "function_call": {\n'
              '    "name": "get_symbol_price",\n'
              '    "arguments": "{\"symbol\": \"BTCUSDT\"}"\n'
              "  },\n"
              '  "content": "I need to get the current price of BTC."\n'
              "}\n"
              "```\n"
              "If you do not need to use a tool, respond with a normal message in the `content` field.\n"
              "Example:\n"
              "```json\n"
              "{\n"
              '  "content": "The current price of BTC is 50000 USDT."\n'
              "}\n"
              "```"
    )
    messages.append({"role": "system", "content": tool_prompt})
    messages.append({"role": "user", "content": prompt})

    # Call the model, passing in the tool descriptions
    response_data = model_manager.call_azure(messages)

    # Save session history
    session_manager.add_to_history(session_id, {"role": "user", "content": prompt})

    function_call_step = {}

    # Check if a tool needs to be called
    if "function_call" in response_data:
        # Extract tool name and parameters
        function_name = response_data["function_call"]["name"]
        function_args = response_data["function_call"]["arguments"]

        # Parse parameters
        if isinstance(function_args, str):
            function_args = json.loads(function_args)
        elif not isinstance(function_args, dict):
            raise ValueError("function_args must be a dictionary or JSON string")

        # Call the tool
        tool_result = tool_manager.use_tool(function_name, **function_args)

        function_call_step = {
            "role": "function",
            "name": function_name,
            "content": f"Tool call result: {tool_result}"
        }

        print(f"This is the function call step: {function_call_step}")

        # Add tool result to session history
        messages.append(function_call_step)

        final_reply = model_manager.call_azure(messages).get("content", "The model did not return a valid response")

        session_manager.add_to_history(session_id, function_call_step)
    else:
        # If no tool call is needed, return AI's response directly
        final_reply = response_data.get("content", "The model did not return a valid response")

    session_manager.add_to_history(session_id, {"role": "assistant", "content": final_reply})

    return final_reply, function_call_step


# Flask route
def chat_stream(response_text):
    gen_text = ""
    tok_cnt = 0
    words = response_text.split()

    for word in words:
        tok_cnt += 1
        gen_text += word + " "
        tok = {
            "token": {
                "id": random.randrange(0, 2 ** 32),
                "text": word,
                "logprob": 0,
                "special": False,
            },
            "generated_text": None,
            "details": None
        }
        yield f"data:{json.dumps(tok, separators=(',', ':'))}\n\n"
        time.sleep(0.1)
    final_tok = {
        "token": {
            "id": random.randrange(0, 2 ** 32),
            "text": None,
            "logprob": 0,
            "special": True,
        },
        "generated_text": gen_text.strip(),
        "details": {
            "finish_reason": "stop",
            "generated_tokens": tok_cnt,
            "seed": None
        }
    }
    yield f"data:{json.dumps(final_tok, separators=(',', ':'))}\n\n\n"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id', "root_session")
    prompt = data.get('inputs')

    response, _ = handle_chat(prompt, session_id, model_manager, tool_manager)

    return Response(chat_stream(response), content_type='text/event-stream',
                    headers={"Content-Type": "text/event-stream"})


if __name__ == '__main__':
    app.run(debug=True)
