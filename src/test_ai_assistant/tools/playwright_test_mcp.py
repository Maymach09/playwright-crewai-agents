from crewai_tools import MCPServerAdapter

class PlaywrightTestMCP:
    """Persistent connector to Playwright MCP server using CrewAI MCPServerAdapter."""

    def __init__(self, server_url="http://localhost:8931/sse"):
        self.server_params = [{"url": server_url, "transport": "sse"}]
        self.adapter = None
        self.tools = None

    def connect(self):
        """Connects to MCP server and returns list of tool instances."""
        try:
            self.adapter = MCPServerAdapter(self.server_params, connect_timeout=30)
            self.tools = self.adapter.__enter__()
            
            # Debug: print all tool names and objects
            # print(f"✅ Persistent MCP server connection established. Tools:")
            # for tool in self.tools:
            #     print(f"  - {tool.name} ({type(tool)})")
            
            # Return full tool instances, not just names
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

# Example usage
if __name__ == "__main__":
    mcp = PlaywrightTestMCP()
    tool_names = mcp.connect()
    mcp.disconnect()