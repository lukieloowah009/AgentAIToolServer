import unittest
from unittest.mock import patch, MagicMock
import asyncio
from tools.currency import convert_currency

class TestCurrencyTool(unittest.TestCase):
    """Test cases for currency conversion tool"""

    @patch('tools.currency.requests.get')
    async def test_convert_currency_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "time_last_update_unix": 1625076000,
            "base_code": "USD",
            "rates": {
                "EUR": 0.85,
                "GBP": 0.73,
                "JPY": 110.45
            }
        }
        mock_get.return_value = mock_response
        
        # Call the function
        result = await convert_currency(100, "USD", "EUR")
        
        # Assertions
        self.assertEqual(result["from"], "USD")
        self.assertEqual(result["to"], "EUR")
        self.assertEqual(result["amount"], 100)
        self.assertEqual(result["converted_amount"], 85.0)
        self.assertEqual(result["rate"], 0.85)
    
    @patch('tools.currency.requests.get')
    async def test_convert_currency_invalid_from_currency(self, mock_get):
        # Mock API response for invalid from_currency
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "error",
            "error-type": "invalid-base-currency"
        }
        mock_get.return_value = mock_response
        
        # Call with invalid from_currency
        result = await convert_currency(100, "INVALID", "EUR")
        
        # Assertions
        self.assertIn("error", result)
    
    @patch('tools.currency.requests.get')
    async def test_convert_currency_invalid_to_currency(self, mock_get):
        # Mock API response with valid base but invalid target currency
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "time_last_update_unix": 1625076000,
            "base_code": "USD",
            "rates": {
                "EUR": 0.85,
                "GBP": 0.73
            }
        }
        mock_get.return_value = mock_response
        
        # Call with invalid to_currency
        result = await convert_currency(100, "USD", "INVALID")
        
        # Assertions
        self.assertIn("error", result)
        self.assertIn("not found", result["error"])
    
    @patch('tools.currency.requests.get')
    async def test_convert_currency_api_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = Exception("API connection error")
        
        # Call the function
        result = await convert_currency(100, "USD", "EUR")
        
        # Assertions
        self.assertIn("error", result)
        self.assertTrue("API connection error" in result["error"])
    
    @patch('tools.currency.requests.get')
    async def test_convert_string_amount(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "time_last_update_unix": 1625076000,
            "base_code": "USD",
            "rates": {
                "EUR": 0.85
            }
        }
        mock_get.return_value = mock_response
        
        # Call the function with string amount
        result = await convert_currency("100", "USD", "EUR")
        
        # Assertions
        self.assertEqual(result["amount"], "100")
        self.assertEqual(result["converted_amount"], 85.0)

# Function to convert async tests to sync for unittest
def sync_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

# Apply the decorator to all async test methods
for attr in dir(TestCurrencyTool):
    if attr.startswith('test_'):
        setattr(TestCurrencyTool, attr, sync_test(getattr(TestCurrencyTool, attr)))

if __name__ == "__main__":
    unittest.main()
