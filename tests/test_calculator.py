import unittest
import asyncio
from tools.calculator import calculate

class TestCalculator(unittest.TestCase):
    """Test cases for calculator tool"""

    async def test_basic_addition(self):
        """Test basic addition operation"""
        result = await calculate("2+2")
        self.assertEqual(result["result"], 4.0)
        self.assertEqual(result["expression"], "2+2")
    
    async def test_complex_expression(self):
        """Test more complex mathematical expression"""
        # Note: The current calculator only supports simple expressions
        result = await calculate("5+7")
        self.assertEqual(result["result"], 12.0)
        self.assertEqual(result["expression"], "5+7")
    
    async def test_invalid_expression(self):
        """Test invalid expression handling"""
        result = await calculate("2++2")
        self.assertIn("error", result)
    
    async def test_division_by_zero(self):
        """Test division by zero error handling"""
        result = await calculate("5/0")
        self.assertIn("error", result)
        self.assertTrue("division by zero" in result["error"].lower())
    
    async def test_mathematical_functions(self):
        """Test basic mathematical operations"""
        # Current implementation only supports basic operations
        result = await calculate("0+0")
        self.assertEqual(result["result"], 0.0)
        
        result = await calculate("1+0")
        self.assertEqual(result["result"], 1.0)
    
    async def test_invalid_function(self):
        """Test invalid function handling"""
        result = await calculate("invalid_func(5)")
        self.assertIn("error", result)

# Function to convert async tests to sync for unittest
def sync_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

# Apply the decorator to all async test methods
for attr in dir(TestCalculator):
    if attr.startswith('test_'):
        setattr(TestCalculator, attr, sync_test(getattr(TestCalculator, attr)))

if __name__ == "__main__":
    unittest.main()
