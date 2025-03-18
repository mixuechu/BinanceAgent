import requests

# Flask service URL
BASE_URL = "http://127.0.0.1:5000"  # Default Flask runs on local port 5000


def chat(session_id, prompt):
    """
    Call the /chat endpoint to interact with AI.
    :param session_id: Session ID
    :param prompt: User input
    :return: AI response
    """
    url = f"{BASE_URL}/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "session_id": session_id,
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"


if __name__ == "__main__":
    # Test conversation
    session_id = "test_session_123"  # Session ID
    prompts = [
        "What is the current price of BTC?",
        # "Buy 0.01 BTC.",
        "What is my BTC balance?",
        "What are the five trades in my history for BTCUSDT?",
        "What are my open orders for BTCUSDT?",
        "Cancel order 123456789, I think the currency is BTCUSDT."
    ]

    for prompt in prompts:
        print(f"User: {prompt}")
        response = chat(session_id, prompt)

        print(f"Function Calling: {response.get('function_call_step')}")

        print(f"AI: {response.get('response')}")
        print("-" * 50)
