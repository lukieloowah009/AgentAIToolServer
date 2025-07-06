# Agent AI with Tool-calling MCP Server

A proof-of-concept implementation of an Agent AI system with tool-calling capabilities through an MCP (Model-Controller-Provider) server architecture.

## Features

- FastAPI backend server
- Integration with local Llama 3.2 model via LiteLLM
- MCP Server for managing tool calls
- Implemented tools:
  1. Current Weather
  2. Time
  3. Calculator
  4. Currency Conversion

## Getting Started

### Prerequisites

- Python 3.9+
- Local Llama 3.2 model running
- API keys for external services (e.g., weather API)

### Installation

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Set up environment variables or update config.py with your settings
4. Run the server:
```
uvicorn main:app --reload
```

## Usage

Once the server is running, you can access the API documentation at `http://localhost:8000/docs` and interact with the Agent AI through API calls.

## Architecture

This project follows a microservice-like architecture:
- FastAPI provides the HTTP interface
- LiteLLM handles communication with the LLM
- MCP Server manages tool registration and execution
- Each tool is implemented as a separate module

## Project Structure

```
AgentAI-POC/
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration settings
├── models/                   # Data models
│   └── schema.py             # Pydantic models for requests/responses
├── services/
│   ├── llm_service.py        # LiteLLM integration
│   └── mcp_service.py        # MCP Server implementation
└── tools/
    ├── __init__.py
    ├── weather.py            # Weather tool
    ├── time_tool.py          # Time tool 
    ├── calculator.py         # Calculator tool
    └── currency.py           # Currency conversion tool
```
