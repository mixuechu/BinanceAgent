# BinanceAgent

BinanceAgent is a Flask-based conversational service designed to execute Binance API operations through user dialogue. It integrates multiple Binance API tools to automatically invoke the appropriate function based on user requests and return relevant results.

## Features

BinanceAgent provides the following functionalities:

1. **Get Current Price**: Retrieve the latest price of a specified trading pair using the `get_symbol_price` tool.
2. **Get Account Balance**: Check the balance of a specified cryptocurrency using the `get_account_balance` tool.
3. **Place Market Order**: Execute a market order using the `place_market_order` tool.
4. **Retrieve Trade History**: Fetch the trade history of a specified trading pair using the `get_trade_history` tool.
5. **Check Open Orders**: Get a list of open orders for a specified trading pair using the `get_open_orders` tool.
6. **Cancel an Order**: Cancel a specific order using the `cancel_order` tool.

## Project Structure

```
📂 BinanceAgent/
├── 📜 model.py       - Manages models, handles dialogue logic
├── ⚙️ config.py       - Configuration parameters, such as API keys
├── 🔧 tool.py        - Trading tools and their registration process
├── 🚀 service.py     - Flask service, runs the dialogue system
├── 🧪 test.py        - Test cases, simulates API calls
└── 📄 README.md      - Project documentation
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/BinanceAgent.git
cd BinanceAgent
```

### 2. Install Dependencies

Ensure you have Python 3.7 or higher installed. Then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Set up your Binance API keys in the `config.py` file:

```python
API_KEY = 'your-binance-api-key'
API_SECRET = 'your-binance-api-secret'
```

### 4. Start the Service

Run `service.py` to launch the Flask service:

```bash
python service.py
```

Once the service is running, you can interact with BinanceAgent via `http://127.0.0.1:5000/chat`.

### 5. Testing

You can test the conversation service using the sample cases in `test.py`:

```bash
python test.py
```

## Example Conversations

Here are some sample interactions with BinanceAgent:

```plaintext
User: What is the current price of BTC?
Function Calling: {'content': 'Tool call result: BTCUSDT current price is: 83271.73000000 USDT', 'name': 'get_symbol_price', 'role': 'function'}
AI: The current price of BTC is 83,271.73 USDT.
--------------------------------------------------
User: What is my BTC balance?
Function Calling: {'content': 'Tool call result: BTC balance is: 0.00000000', 'name': 'get_account_balance', 'role': 'function'}
AI: Your BTC balance is 0.00000000 BTC.
--------------------------------------------------
User: What are the five trades in my history for BTCUSDT?
Function Calling: {'content': 'Tool call result: []', 'name': 'get_trade_history', 'role': 'function'}
AI: You currently have no trades in your history for BTCUSDT.
--------------------------------------------------
User: What are my open orders for BTCUSDT?
Function Calling: {'content': 'Tool call result: []', 'name': 'get_open_orders', 'role': 'function'}
AI: You currently have no open orders for BTCUSDT.
--------------------------------------------------
User: Cancel order 123456789, I think the currency is BTCUSDT.
Function Calling: {'content': 'Tool call result: Failed to cancel order: {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action."}', 'name': 'cancel_order', 'role': 'function'}
AI: It seems that I am unable to cancel the order due to an invalid API key, IP, or insufficient permissions for this action. You may want to check your API settings or try to cancel the order directly through your trading platform.
--------------------------------------------------
```


![chat-ui-preview](./image.png)



## Frontend

I didn’t have time to implement a frontend framework, so I ensured our agent works well with ChatUI.

https://github.com/huggingface/chat-ui

Start the service, replace the .env file in the chat-ui folder with the one I provided, then run:
```
npm run dev
```
And you’re good to go! 🚀

## Contribution

Contributions are welcome! If you have suggestions or find any issues, feel free to submit an Issue or a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
