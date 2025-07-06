from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any

from models.schema import AgentRequest, AgentResponse
from services.llm_service import generate_response
from services.mcp_service import MCPServer

app = FastAPI(title="Agent AI with Tool-calling")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP Server
mcp_server = MCPServer()

# Register tools on startup
@app.on_event("startup")
async def startup_event():
    print("Loading tools during server startup...")
    mcp_server.load_tools_from_modules()
    print(f"Loaded {len(mcp_server.tools)} tools successfully")

@app.get("/")
async def root():
    return {"message": "Agent AI with Tool-calling API"}

@app.post("/agent/chat", response_model=AgentResponse)
async def agent_chat(request: AgentRequest):
    try:
        # Process the request through the LLM and get response
        response = await generate_response(request.messages, mcp_server)
        return AgentResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/tools")
async def list_tools():
    """List all available tools in the MCP Server"""
    return {"tools": mcp_server.list_tools()}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
