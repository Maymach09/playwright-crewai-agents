import os
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

class FilesystemMCP:
    """Automated persistent connector to local Filesystem MCP server using stdio transport."""

    def __init__(self, directory_path=None):
        if directory_path is None:
            directory_path = "/Users/maymach09/Documents/GenAI09/MacOS/Playwright/playwright_agents"
        # Command to launch Filesystem MCP server subprocess with given directory path(s)
        self.server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", directory_path],
            env={**os.environ}
        )
        self.adapter = None
        self.tools = None

    def connect(self):
        """Start MCP filesystem server subprocess and connect via stdio."""
        try:
            self.adapter = MCPServerAdapter(self.server_params, connect_timeout=30)
            self.tools = self.adapter.__enter__()
            tool_names = [t.name for t in self.tools] if hasattr(self.tools, "__iter__") else []
            #print(f"✅ Persistent MCP Filesystem server connection established over stdio. Tools: {tool_names}")
            return self.tools
        except Exception as e:
            print(f"❌ Failed to connect to Filesystem MCP server: {e}")
            return []

    def disconnect(self):
        if self.adapter:
            try:
                self.adapter.__exit__(None, None, None)
                print("🔌 Disconnected from Filesystem MCP server.")
            except Exception as e:
                print(f"⚠️ Error during MCP disconnect: {e}")
# Example usage
if __name__ == "__main__":
    mcp = FilesystemMCP()
    tools = mcp.connect()
    mcp.disconnect()