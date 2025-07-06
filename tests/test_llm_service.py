import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import json
from services.llm_service import generate_response
from services.mcp_service import MCPServer
from models.schema import Message

class TestLLMService(unittest.TestCase):
    """Test cases for LLM Service"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mcp_server = MagicMock(spec=MCPServer)
        self.mcp_server.get_tools_for_llm.return_value = [
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "Test tool for unit testing",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Test input"
                            }
                        },
                        "required": ["input"]
                    }
                }
            }
        ]
        self.mcp_server.execute_tool = AsyncMock(return_value={"result": "test_success"})
        
        self.messages = [
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello, can you help me?")
        ]
    
    @patch('services.llm_service.litellm.acompletion')
    async def test_generate_response_no_tool_calls(self, mock_acompletion):
        """Test generating a response with no tool calls"""
        # Create a dictionary that represents the response
        mock_message_dict = {
            "role": "assistant",
            "content": "Hello! I'm here to help. What can I assist you with today?"
        }
        
        # Create a class that simulates a message object with dict() conversion support
        class MockMessage(dict):
            def __init__(self, data):
                super().__init__(data)
                for key, value in data.items():
                    setattr(self, key, value)
            
            def __getitem__(self, key):
                return super().__getitem__(key)
        
        # Create the message and completion objects
        mock_message = MockMessage(mock_message_dict)
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_acompletion.return_value = mock_completion
        
        # Call the function
        result = await generate_response(self.messages, self.mcp_server)
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("role"), "assistant")
        self.assertEqual(result.get("content"), "Hello! I'm here to help. What can I assist you with today?")
    
    @patch('services.llm_service.litellm.acompletion')
    async def test_generate_response_with_tool_calls(self, mock_acompletion):
        """Test generating a response with tool calls"""
        # Create a class that simulates a message object with dict() conversion support
        class MockMessage(dict):
            def __init__(self, data):
                super().__init__(data)
                for key, value in data.items():
                    setattr(self, key, value)
            
            def __getitem__(self, key):
                return super().__getitem__(key)
        
        # First response with tool calls
        first_tool_call = {
            "id": "tool_call_1",
            "function": {
                "name": "test_tool",
                "arguments": json.dumps({"input": "test"})
            }
        }
        
        first_message_dict = {
            "role": "assistant",
            "content": None,
            "tool_calls": [first_tool_call]
        }
        
        # Second response after tool execution
        second_message_dict = {
            "role": "assistant",
            "content": "Based on the tool results, here's your answer."
        }
        
        # Create mock responses
        first_message = MockMessage(first_message_dict)
        first_choice = MagicMock()
        first_choice.message = first_message
        first_completion = MagicMock()
        first_completion.choices = [first_choice]
        
        second_message = MockMessage(second_message_dict)
        second_choice = MagicMock()
        second_choice.message = second_message
        second_completion = MagicMock()
        second_completion.choices = [second_choice]
        
        mock_acompletion.side_effect = [first_completion, second_completion]
        
        # Call the function
        result = await generate_response(self.messages, self.mcp_server)
        
        # Assert tool was executed
        self.mcp_server.execute_tool.assert_called_once_with("test_tool", {"input": "test"})
        
        # Assert final response is returned
        self.assertEqual(result.get("content"), "Based on the tool results, here's your answer.")
    
    @patch('services.llm_service.litellm.acompletion')
    async def test_generate_response_with_api_error(self, mock_acompletion):
        """Test handling of API errors"""
        # Mock API error
        mock_acompletion.side_effect = Exception("API Error")
        
        # Call the function
        result = await generate_response(self.messages, self.mcp_server)
        
        # Assert error is handled gracefully
        self.assertEqual(result.get("role"), "assistant")
        self.assertTrue("Error generating response" in result.get("content"))
    
    @patch('services.llm_service.litellm.acompletion')
    async def test_generate_response_with_tool_execution_error(self, mock_acompletion):
        """Test handling of tool execution errors"""
        # Create a class that simulates a message object with dict() conversion support
        class MockMessage(dict):
            def __init__(self, data):
                super().__init__(data)
                for key, value in data.items():
                    setattr(self, key, value)
            
            def __getitem__(self, key):
                return super().__getitem__(key)
        
        # First response with tool calls
        first_tool_call = {
            "id": "tool_call_1",
            "function": {
                "name": "test_tool",
                "arguments": json.dumps({"input": "test"})
            }
        }
        
        first_message_dict = {
            "role": "assistant",
            "content": None,
            "tool_calls": [first_tool_call]
        }
        
        # Second response after tool execution error
        second_message_dict = {
            "role": "assistant",
            "content": "I encountered an error with the tool."
        }
        
        # Create mock responses
        first_message = MockMessage(first_message_dict)
        first_choice = MagicMock()
        first_choice.message = first_message
        first_completion = MagicMock()
        first_completion.choices = [first_choice]
        
        second_message = MockMessage(second_message_dict)
        second_choice = MagicMock()
        second_choice.message = second_message
        second_completion = MagicMock()
        second_completion.choices = [second_choice]
        
        mock_acompletion.side_effect = [first_completion, second_completion]
        self.mcp_server.execute_tool.side_effect = Exception("Tool execution error")
        
        # Call the function
        result = await generate_response(self.messages, self.mcp_server)
        
        # Assert final response contains error handling message
        self.assertEqual(result.get("content"), "I encountered an error with the tool.")

# Function to convert async tests to sync for unittest
def sync_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

# Apply the decorator to all async test methods
for attr in dir(TestLLMService):
    if attr.startswith('test_') and asyncio.iscoroutinefunction(getattr(TestLLMService, attr)):
        setattr(TestLLMService, attr, sync_test(getattr(TestLLMService, attr)))

if __name__ == "__main__":
    unittest.main()
