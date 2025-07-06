import requests
from typing import Dict, Any
import config
from models.schema import Tool

async def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """
    Convert an amount from one currency to another
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
        
    Returns:
        Dictionary containing conversion result
    """
    try:
        # Using ExchangeRate-API (free tier available)
        # Replace with your preferred currency API
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data["result"] != "success":
            return {"error": "Failed to fetch exchange rates"}
        
        # Get the exchange rate for the target currency
        to_currency = to_currency.upper()
        if to_currency not in data["rates"]:
            return {"error": f"Currency '{to_currency}' not found"}
        
        exchange_rate = data["rates"][to_currency]
        converted_amount = int(amount) * exchange_rate
        
        return {
            "from": from_currency.upper(),
            "to": to_currency,
            "amount": amount,
            "converted_amount": converted_amount,
            "rate": exchange_rate,
            "timestamp": data["time_last_update_unix"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching exchange rates: {str(e)}"}
    except (KeyError, ValueError) as e:
        return {"error": f"Error processing conversion: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def register_currency_tool(mcp_server):
    """Register the currency conversion tool with the MCP server"""
    currency_tool = Tool(
        name="convert_currency",
        description="Convert an amount from one currency to another",
        parameters={
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code, e.g., 'USD', 'EUR', 'JPY'"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code, e.g., 'USD', 'EUR', 'JPY'"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        },
        function=convert_currency
    )
    
    mcp_server.register_tool(currency_tool)
