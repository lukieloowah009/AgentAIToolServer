import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from tests.test_weather import TestWeatherTool
from tests.test_time_tool import TestTimeTool
from tests.test_calculator import TestCalculator
from tests.test_currency import TestCurrencyTool
from tests.test_mcp_service import TestMCPService
from tests.test_llm_service import TestLLMService

def run_all_tests():
    """Run all test cases"""
    # Create a test loader
    loader = unittest.TestLoader()
    
    # Create test suite and add all test cases
    test_suite = unittest.TestSuite([
        loader.loadTestsFromTestCase(TestWeatherTool),
        loader.loadTestsFromTestCase(TestTimeTool),
        loader.loadTestsFromTestCase(TestCalculator),
        loader.loadTestsFromTestCase(TestCurrencyTool),
        loader.loadTestsFromTestCase(TestMCPService),
        loader.loadTestsFromTestCase(TestLLMService)
    ])
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    return result

if __name__ == "__main__":
    result = run_all_tests()
    # Exit with appropriate code for CI/CD systems
    sys.exit(not result.wasSuccessful())
