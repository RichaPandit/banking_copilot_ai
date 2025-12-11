from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn

mcp = FastMCP("Banking MCP", json_response=True, streamable_http_path="/mcp")

@mcp.tool()
def add(a: int, b:int) -> int:
    return a+b

# Expose via FastAPI (HTTP)
app = FastAPI(title="Banking MCP Demo")

# 3) Diagnostics (remain in main app)
@app.get("/health")
def health():
    return {"ok": True, "service": "Banking MCP Demo"}

@app.get("/whoami")
def whoami():
    return {"app": "main_http:app", "mounted_paths": ["/mcp"]}

app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    # Run locally: http://127.0.0.1:8000
    uvicorn.run("main_http:app", host="127.0.0.1", port=8000, reload=True)