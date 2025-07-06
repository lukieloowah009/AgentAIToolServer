# This file makes the tools directory a Python package
# It also serves as an entry point for loading all tools

# Import all tool registration functions here
from tools.weather import register_weather_tool
from tools.time_tool import register_time_tool
from tools.calculator import register_calculator_tool
from tools.currency import register_currency_tool

__all__ = [
    "register_weather_tool",
    "register_time_tool",
    "register_calculator_tool",
    "register_currency_tool"
]
