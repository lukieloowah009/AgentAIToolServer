from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class Message(BaseModel):
    """Message model representing a chat message"""
    role: str = Field(..., description="Role of the message sender (e.g., 'user', 'assistant', 'system')")
    content: str = Field(..., description="Content of the message")
    
class AgentRequest(BaseModel):
    """Request model for agent chat endpoint"""
    messages: List[Message] = Field(..., description="List of message objects")

class SimpleAgentRequest(BaseModel):
    """Simplified request model for agent chat endpoint that takes just the message content"""
    message: str = Field(..., description="The user's message content")
    
class AgentResponse(BaseModel):
    """Response model for agent chat endpoint"""
    response: Dict[str, Any] = Field(..., description="Agent response with potential tool calls")

class ToolCall(BaseModel):
    """Model for a tool call"""
    tool_name: str = Field(..., description="Name of the tool to call")
    parameters: Dict[str, Any] = Field(..., description="Parameters for the tool call")

class ToolResponse(BaseModel):
    """Model for a tool response"""
    tool_name: str = Field(..., description="Name of the tool that was called")
    response: Any = Field(..., description="Response from the tool")
    error: Optional[str] = Field(None, description="Error message if tool call failed")

class Tool(BaseModel):
    """Model for tool registration"""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool")
    parameters: Dict[str, Any] = Field(..., description="Parameters schema for the tool")
    function: Any = Field(None, description="Function to call when tool is invoked")
