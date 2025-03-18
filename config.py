# config.py

class Config:
    # Binance API Configs
    BINANCE_API_KEY = ""
    BINANCE_SECRET_KEY = ""

    # OpenAI Configs
    OPENAI_API_KEY = "sk-"
    OPENAI_BASE_URL = "https://api.deepseek.com"

    # Azure OpenAI Configs
    AZURE_API_KEY = ""
    AZURE_API_VERSION = ""
    AZURE_ENDPOINT = ""

    # Local model path / Should be safetensors
    LOCAL_MODEL_PATH = None  # "/path/to/your/model"