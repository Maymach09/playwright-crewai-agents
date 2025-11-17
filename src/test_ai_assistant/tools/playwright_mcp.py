from crewai_tools import MCPServerAdapter

class PlaywrightMCP:
    """Persistent connector to Playwright MCP server using CrewAI MCPServerAdapter."""

    def __init__(self, server_url="http://localhost:5174/sse"):
        self.server_params = [{"url": server_url, "transport": "sse"}]
        self.adapter = None
        self.tools = None

    def connect(self):
        """Keep the MCP connection alive for the entire Crew run."""
        try:
            self.adapter = MCPServerAdapter(self.server_params, connect_timeout=30)
            self.tools = self.adapter.__enter__()
            tool_names = [t.name for t in self.tools] if hasattr(self.tools, "__iter__") else []
            #print(f"✅ Persistent MCP connection established. Tools: {tool_names}")
            return self.tools
        except Exception as e:
            print(f"❌ Failed to connect to Playwright MCP server: {e}")
            return []

    def disconnect(self):
        if self.adapter:
            try:
                self.adapter.__exit__(None, None, None)
                print("🔌 Disconnected from MCP server.")
            except Exception as e:
                print(f"⚠️ Error during MCP disconnect: {e}")


if __name__ == "__main__":
    mcp = PlaywrightMCP()
    tools = mcp.connect()
    mcp.disconnect()
