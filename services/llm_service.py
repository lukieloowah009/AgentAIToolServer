from typing import List, Dict, Any
import json
import litellm
from models.schema import Message
from services.mcp_service import MCPServer
import config

async def generate_response(messages: List[Message], mcp_server: MCPServer) -> Dict[str, Any]:
    """
    Generate a response from the LLM, handling potential tool calls
    
    Args:
        messages: List of message objects
        mcp_server: MCP Server instance for tool handling
        
    Returns:
        Dictionary containing the assistant's response and any tool calls/results
    """
    # Convert messages to the format expected by litellm
    llm_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
    
    # Get available tools from MCP server
    tools = mcp_server.get_tools_for_llm()
    
    try:
        # Call the LLM with tool calling capabilities
        completion = await litellm.acompletion(
            model=f"ollama/{config.LLM_MODEL_NAME}",  # Format for Ollama models in LiteLLM
            messages=llm_messages,
            api_base=config.LLM_API_BASE_URL,
            tools=tools,
            tool_choice="auto"  # Let the model decide when to call tools
        )
        
        response = completion.choices[0].message
        
        # Process tool calls if present
        if "tool_calls" in dict(response) and response["tool_calls"]:
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                try:
                    # Parse tool call arguments
                    arguments = json.loads(tool_call["function"]["arguments"])
                    
                    # Execute the tool call
                    tool_result = await mcp_server.execute_tool(tool_name, arguments)
                    
                    # Add tool result to the conversation
                    llm_messages.append(response)
                    llm_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    })
                    
                except Exception as e:
                    # Handle tool execution errors
                    error_message = f"Error executing tool {tool_name}: {str(e)}"
                    llm_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": tool_name,
                        "content": json.dumps({"error": error_message})
                    })
            
            # Add a system message to instruct the LLM to provide a user-friendly summary
            llm_messages.append({
                "role": "system",
                "content": "Based on the previous messages and tool results, provide a clear, concise, and user-friendly summary. Use natural language and avoid technical details unless necessary."
            })
            
            # Get a new response after tool calls
            final_completion = await litellm.acompletion(
                model=f"ollama/{config.LLM_MODEL_NAME}",  # Format for Ollama models in LiteLLM
                messages=llm_messages,
                api_base=config.LLM_API_BASE_URL
            )
            
            return dict(final_completion.choices[0].message)
        
        # Return the original response if no tool calls
        return dict(response)
    
    except Exception as e:
        return {"role": "assistant", "content": f"Error generating response: {str(e)}"}
