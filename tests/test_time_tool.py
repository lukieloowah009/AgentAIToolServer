import unittest
from unittest.mock import patch, MagicMock
import asyncio
import datetime
from tools.time_tool import get_time

class TestTimeTool(unittest.TestCase):
    """Test cases for the time tool"""

    @patch('tools.time_tool.datetime')
    async def test_get_time_no_timezone(self, mock_datetime):
        # Mock datetime to return a fixed date/time
        mock_now = datetime.datetime(2025, 7, 6, 12, 0, 0)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.strftime = datetime.datetime.strftime
        
        # Call the function without timezone
        result = await get_time()
        
        # Assertions
        self.assertIn("current_time", result)
        self.assertIn("timezone", result)
        self.assertEqual(result["timezone"], "UTC")  # Default timezone
    
    @patch('tools.time_tool.datetime')
    @patch('tools.time_tool.pytz')
    async def test_get_time_with_timezone(self, mock_pytz, mock_datetime):
        # Mock timezone
        mock_tz = MagicMock()
        mock_pytz.timezone.return_value = mock_tz
        
        # Mock datetime with timezone
        mock_now = datetime.datetime(2025, 7, 6, 12, 0, 0)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.strftime = datetime.datetime.strftime
        
        # Mock localize to return the same datetime
        mock_tz.localize.return_value = mock_now
        mock_now.strftime.return_value = "2025-07-06 12:00:00"
        
        # Call the function with timezone
        result = await get_time("America/New_York")
        
        # Assertions
        self.assertIn("current_time", result)
        self.assertEqual(result["timezone"], "America/New_York")
    
    @patch('tools.time_tool.pytz')
    async def test_get_time_invalid_timezone(self, mock_pytz):
        # Mock pytz to raise exception for invalid timezone
        mock_pytz.timezone.side_effect = Exception("Invalid timezone")
        
        # Call with invalid timezone
        result = await get_time("Invalid/Timezone")
        
        # Assertions
        self.assertIn("error", result)
        self.assertTrue("Invalid timezone" in result["error"])

# Allow running the tests directly
if __name__ == "__main__":
    unittest.main()
