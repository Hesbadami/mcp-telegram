from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(
    "Telegram MCP Server",
    dependencies=["telethon", "dotenv", "numpy"]
)