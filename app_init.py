import uvicorn
from main import app, mcp_server

def initialize_application():
    """Initialize the application by loading all tools and configurations"""
    print("Initializing Agent AI application...")
    
    # Load all tools from the tools directory
    mcp_server.load_tools_from_modules()
    
    print(f"Loaded {len(mcp_server.tools)} tools:")
    for tool_name in mcp_server.tools:
        print(f"  - {tool_name}")
    
    print("\nAgent AI application initialized successfully!")
    print("Run the server with: uvicorn main:app --reload")

if __name__ == "__main__":
    initialize_application()
