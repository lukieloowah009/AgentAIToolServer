from typing import Dict, Any, List, Callable, Optional
import inspect
import json
from models.schema import Tool

class MCPServer:
    """
    Model-Controller-Provider (MCP) Server for managing tool calls.
    This class handles tool registration, listing, and execution.
    """
    
    def __init__(self):
        """Initialize the MCP server with an empty tools registry"""
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """
        Register a tool with the MCP server
        
        Args:
            tool: Tool object to register
        """
        self.tools[tool.name] = tool
        print(f"Tool '{tool.name}' registered successfully")
    
    def unregister_tool(self, tool_name: str) -> bool:
        """
        Unregister a tool from the MCP server
        
        Args:
            tool_name: Name of the tool to unregister
            
        Returns:
            True if tool was unregistered, False if tool was not found
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            print(f"Tool '{tool_name}' unregistered successfully")
            return True
        return False
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all registered tools
        
        Returns:
            List of tool information dictionaries
        """
        return [
            {"name": name, "description": tool.description, "parameters": tool.parameters}
            for name, tool in self.tools.items()
        ]
    
    def get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """
        Get tools in the format expected by LLMs for function calling
        
        Returns:
            List of tool definitions in OpenAI function calling format
        """
        llm_tools = []
        for name, tool in self.tools.items():
            llm_tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })
        return llm_tools
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool with the given arguments
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            Result of the tool execution
            
        Raises:
            ValueError: If tool is not found
            Exception: If tool execution fails
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        
        try:
            # Check if the function is async
            if inspect.iscoroutinefunction(tool.function):
                result = await tool.function(**arguments)
            else:
                result = tool.function(**arguments)
            
            return result
        except Exception as e:
            raise Exception(f"Error executing tool '{tool_name}': {str(e)}")
    
    def load_tools_from_modules(self) -> None:
        """
        Load and register all tools from the tools directory
        This method should be called during application startup
        """
        # Import here to avoid circular imports
        from tools.weather import register_weather_tool
        from tools.time_tool import register_time_tool
        from tools.calculator import register_calculator_tool
        from tools.currency import register_currency_tool
        
        # Register all tools
        register_weather_tool(self)
        register_time_tool(self)
        register_calculator_tool(self)
        register_currency_tool(self)
