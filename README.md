```markdown
# BinanceAgent

BinanceAgent 是一个基于 Flask 的对话服务，旨在通过与用户的对话来执行币安（Binance）API 的相关操作。它集成了多个币安 API 工具，能够根据用户的需求自动调用相应的工具并返回结果。

## 功能概述

BinanceAgent 提供了以下功能：

1. **获取当前价格**：通过 `get_symbol_price` 工具获取指定交易对的当前价格。
2. **获取账户余额**：通过 `get_account_balance` 工具获取指定币种的账户余额。
3. **下达市价单**：通过 `place_market_order` 工具下达市价单。
4. **获取交易历史**：通过 `get_trade_history` 工具获取指定交易对的交易历史。
5. **获取未成交订单**：通过 `get_open_orders` 工具获取指定交易对的未成交订单。
6. **取消订单**：通过 `cancel_order` 工具取消指定订单。

## 文件结构

```
BinanceAgent/
├── model.py          # 管理模型，处理对话逻辑
├── config.py         # 配置参数，如 API 密钥等
├── tool.py           # 交易工具及其注册流程
├── service.py        # Flask 服务，启动对话服务
├── test.py           # 测试样例，模拟调用对话接口
└── README.md         # 项目说明文档
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/BinanceAgent.git
cd BinanceAgent
```

### 2. 安装依赖

确保你已经安装了 Python 3.7 或更高版本。然后安装所需的依赖：

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

在 `config.py` 文件中配置你的币安 API 密钥：

```python
API_KEY = 'your-binance-api-key'
API_SECRET = 'your-binance-api-secret'
```

### 4. 启动服务

运行 `service.py` 启动 Flask 服务：

```bash
python service.py
```

服务启动后，你可以通过 `http://127.0.0.1:5000/chat` 与 BinanceAgent 进行对话。

### 5. 测试

你可以使用 `test.py` 中的样例来测试对话服务：

```bash
python test.py
```

## 示例对话

以下是 BinanceAgent 的示例对话流程：

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

## 贡献

欢迎贡献代码！如果你有任何建议或发现问题，请提交 Issue 或 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
```

### 说明：
1. **文件结构**：你可以根据实际的文件结构进行调整。
2. **API 密钥配置**：确保在 `config.py` 中正确配置 API 密钥。
3. **示例对话**：你可以根据实际测试结果更新示例对话。
4. **依赖**：如果你有 `requirements.txt` 文件，确保在 `README.md` 中提到它。

希望这个 `README.md` 文件能帮助你更好地展示你的项目！如果有任何需要调整的地方，请告诉我。