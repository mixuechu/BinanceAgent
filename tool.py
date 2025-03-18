# tool.py

import requests
import hmac
import hashlib
import time
from config import Config
from functools import lru_cache


class ToolManager:
    def __init__(self):
        self.tools = {}
        self.tool_descriptions = []

    def register_tool(self, tool_name, tool_function, description, parameters):
        """
        Register a tool.
        :param tool_name: Name of the tool
        :param tool_function: Function of the tool
        :param description: Description of the tool
        :param parameters: Parameters of the tool
        """
        self.tools[tool_name] = tool_function
        self.tool_descriptions.append({
            "name": tool_name,
            "description": description,
            "parameters": parameters
        })

    def use_tool(self, tool_name, *args, **kwargs):
        """
        Use a tool.
        :param tool_name: Name of the tool
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Result of the tool call
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found.")
        return self.tools[tool_name](*args, **kwargs)

    def get_tool_descriptions(self):
        """
        Get descriptions of all tools.
        :return: List of tool descriptions
        """
        return self.tool_descriptions


# Tool registration decorator
def register_tool(description, parameters):
    def decorator(func):
        tool_manager.register_tool(
            tool_name=func.__name__,
            tool_function=func,
            description=description,
            parameters=parameters
        )
        return func

    return decorator


# Initialize ToolManager
tool_manager = ToolManager()


# Tool 1: Get cryptocurrency pair price
@register_tool(
    description="Get the current price of a cryptocurrency pair.",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The cryptocurrency pair, e.g., BTCUSDT."}
        },
        "required": ["symbol"]
    }
)
@lru_cache(maxsize=100)
def get_symbol_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return f"{symbol} current price is: {data['price']} USDT"
    else:
        return f"Failed to get {symbol} price: {response.text}"


# Tool 2: Get account balance
@register_tool(
    description="Get the balance of a specific cryptocurrency in the account.",
    parameters={
        "type": "object",
        "properties": {
            "asset": {"type": "string", "description": "The cryptocurrency symbol, e.g., BTC."}
        },
        "required": ["asset"]
    }
)
def get_account_balance(asset):
    url = "https://api.binance.com/api/v3/account"
    timestamp = int(time.time() * 1000)
    params = {"timestamp": timestamp}
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(Config.BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": Config.BINANCE_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        balances = response.json().get("balances", [])
        for balance in balances:
            if balance["asset"] == asset:
                return f"{asset} balance is: {balance['free']}"
        return f"No balance found for {asset}"
    else:
        return f"Failed to get account balance: {response.text}"


# Tool 3: Place a market order
@register_tool(
    description="Place a market order to buy or sell a cryptocurrency.",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The cryptocurrency pair, e.g., BTCUSDT."},
            "side": {"type": "string", "description": "The order side, either BUY or SELL."},
            "quantity": {"type": "string", "description": "The quantity to buy or sell."}
        },
        "required": ["symbol", "side", "quantity"]
    }
)
def place_market_order(symbol, side, quantity):
    url = "https://api.binance.com/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(Config.BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": Config.BINANCE_API_KEY}
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        return f"{side} {quantity} {symbol} order has been placed"
    else:
        return f"Failed to place order: {response.text}"


# Tool 4: Get trade history
@register_tool(
    description="Get the recent trade history for a cryptocurrency pair.",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The cryptocurrency pair, e.g., BTCUSDT."},
            "limit": {"type": "integer", "description": "The number of trades to return."}
        },
        "required": ["symbol"]
    }
)
def get_trade_history(symbol, limit=10):
    url = "https://api.binance.com/api/v3/myTrades"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "limit": limit,
        "timestamp": timestamp
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(Config.BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": Config.BINANCE_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        trades = response.json()
        return [f"{trade['time']}: {trade['side']} {trade['qty']} {symbol} @ {trade['price']}" for trade in trades]
    else:
        return f"Failed to get trade history: {response.text}"


# Tool 5: Get open orders
@register_tool(
    description="Get the current open orders for a cryptocurrency pair.",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The cryptocurrency pair, e.g., BTCUSDT."}
        },
        "required": ["symbol"]
    }
)
def get_open_orders(symbol):
    url = "https://api.binance.com/api/v3/openOrders"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "timestamp": timestamp
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(Config.BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": Config.BINANCE_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        orders = response.json()
        return [f"{order['side']} {order['origQty']} {symbol} @ {order['price']}" for order in orders]
    else:
        return f"Failed to get open orders: {response.text}"


# Tool 6: Cancel an order
@register_tool(
    description="Cancel an open order for a cryptocurrency pair.",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The cryptocurrency pair, e.g., BTCUSDT."},
            "order_id": {"type": "string", "description": "The ID of the order to cancel."}
        },
        "required": ["symbol", "order_id"]
    }
)
def cancel_order(symbol, order_id):
    url = "https://api.binance.com/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "orderId": order_id,
        "timestamp": timestamp
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(Config.BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": Config.BINANCE_API_KEY}
    response = requests.delete(url, headers=headers, params=params)
    if response.status_code == 200:
        return f"Order {order_id} has been canceled"
    else:
        return f"Failed to cancel order: {response.text}"
