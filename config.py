import os
from dotenv import load_dotenv

# Configuration settings
load_dotenv()  # Load environment variables from .env file

# LLM settings
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3.2")  # Name of local model in Ollama
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:11434")  # Base URL for Ollama API

# API keys for tools
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")
