import sys
from anyio import run

from common.config import MCP_TRANSPORT
from common.client import TelegramClientManager
from common.server import mcp

import tools.server_management

class TelegramMCPServer:
    def __init__(self):
        print("Starting the TelegramMCPServer", file=sys.stderr)

    def run(self):
        mcp.run(transport=MCP_TRANSPORT)

async def authenticate_telegram():
    """Handle Telegram authentication separately"""
    is_authenticated = await TelegramClientManager.is_authenticated()
    if not is_authenticated:
        print("Telegram client is not authenticated. Please authenticate first.", file=sys.stderr)
        sys.exit(1)
    print("Authentication successful. Starting MCP server...", file=sys.stderr)

def main():
    
    run(authenticate_telegram)
    
    server = TelegramMCPServer()
    server.run()
    print("TelegramMCPServer has been started successfully.", file=sys.stderr)

if __name__ == "__main__":
    main()
    print("TelegramMCPServer has been stopped.", file=sys.stderr)