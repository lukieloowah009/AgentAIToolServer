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
2. Run the setup script:
```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The setup script will:
- Create and activate a virtual environment (.venv)
- Install all dependencies
- Initialize the application

3. Set up environment variables in the .env file

4. Activate the virtual environment (if not already activated):
```bash
source .venv/bin/activate
```

5. Run the server:
```bash
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

## Testing

The project includes a comprehensive test suite for all components. You can run the tests using any of the following methods:

### Run All Tests

```bash
# Run all tests using the provided test runner
python tests/run_tests.py

# Alternatively, use Python's unittest module
python -m unittest discover tests
```

### Run Specific Test Files

```bash
# Run tests for a specific component
python -m unittest tests/test_calculator.py
python -m unittest tests/test_currency.py
python -m unittest tests/test_weather.py
python -m unittest tests/test_time_tool.py
python -m unittest tests/test_mcp_service.py
python -m unittest tests/test_llm_service.py
```

### Run Individual Test Cases

```bash
# Run a specific test class
python -m unittest tests.test_calculator.TestCalculator

# Run a specific test method
python -m unittest tests.test_calculator.TestCalculator.test_basic_addition
```

### Using pytest (if installed)

```bash
# Install pytest
pip install pytest

# Run all tests with detailed output
pytest tests/ -v
```

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
