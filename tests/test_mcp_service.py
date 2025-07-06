import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import json
from services.mcp_service import MCPServer
from models.schema import Tool

class TestMCPService(unittest.TestCase):
    """Test cases for MCP Server service"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mcp_server = MCPServer()
        
        # Create a test tool
        self.test_tool = Tool(
            name="test_tool",
            description="Test tool for unit testing",
            parameters={
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Test input"
                    }
                },
                "required": ["input"]
            },
            function=AsyncMock(return_value={"result": "test_success"})
        )
        
    def test_register_tool(self):
        """Test tool registration"""
        # Register the test tool
        self.mcp_server.register_tool(self.test_tool)
        
        # Verify tool was registered
        self.assertIn("test_tool", self.mcp_server.tools)
        self.assertEqual(self.mcp_server.tools["test_tool"], self.test_tool)
    
    def test_list_tools(self):
        """Test listing registered tools"""
        # Register a test tool
        self.mcp_server.register_tool(self.test_tool)
        
        # Get the list of tools
        tool_list = self.mcp_server.list_tools()
        
        # Verify the test tool is in the list
        self.assertEqual(len(tool_list), 1)
        self.assertEqual(tool_list[0]["name"], "test_tool")
        self.assertEqual(tool_list[0]["description"], "Test tool for unit testing")
    
    def test_get_tools_for_llm(self):
        """Test getting tools formatted for LLM"""
        # Register a test tool
        self.mcp_server.register_tool(self.test_tool)
        
        # Get tools for LLM
        llm_tools = self.mcp_server.get_tools_for_llm()
        
        # Verify format is correct for LLM
        self.assertEqual(len(llm_tools), 1)
        self.assertEqual(llm_tools[0]["type"], "function")
        self.assertEqual(llm_tools[0]["function"]["name"], "test_tool")
        self.assertEqual(llm_tools[0]["function"]["description"], "Test tool for unit testing")
        self.assertIn("parameters", llm_tools[0]["function"])
    
    async def test_execute_tool(self):
        """Test tool execution"""
        # Register the test tool
        self.mcp_server.register_tool(self.test_tool)
        
        # Execute the tool
        result = await self.mcp_server.execute_tool("test_tool", {"input": "test"})
        
        # Verify correct function was called with right arguments
        self.test_tool.function.assert_called_once_with(input="test")
        self.assertEqual(result, {"result": "test_success"})
    
    async def test_execute_nonexistent_tool(self):
        """Test executing a tool that doesn't exist"""
        with self.assertRaises(ValueError):
            await self.mcp_server.execute_tool("nonexistent_tool", {})
    
    async def test_execute_tool_with_exception(self):
        """Test tool execution that raises an exception"""
        # Create a tool that raises an exception
        error_tool = Tool(
            name="error_tool",
            description="Tool that raises an exception",
            parameters={},
            function=AsyncMock(side_effect=Exception("Test error"))
        )
        
        # Register the error tool
        self.mcp_server.register_tool(error_tool)
        
        # Execute the tool and expect exception to be raised
        with self.assertRaises(Exception):
            await self.mcp_server.execute_tool("error_tool", {})

# Function to convert async tests to sync for unittest
def sync_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

# Apply the decorator to all async test methods
for attr in dir(TestMCPService):
    if attr.startswith('test_') and asyncio.iscoroutinefunction(getattr(TestMCPService, attr)):
        setattr(TestMCPService, attr, sync_test(getattr(TestMCPService, attr)))

if __name__ == "__main__":
    unittest.main()
