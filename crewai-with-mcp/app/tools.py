# tools.py
from crewai_tools import MCPServerAdapter

server_params_list = [
    {"url": "http://localhost:8001/mcp", "transport": "streamable-http"},
    {"url": "http://localhost:8002/mcp", "transport": "streamable-http"},
]

def get_tools():
    try:
        with MCPServerAdapter(server_params_list) as aggregated_tools:
            tools = list(aggregated_tools)
            print("Loaded tools:", [t.name for t in tools])
            return tools
    except Exception as e:
        print(f"Error loading tools: {e}")
        return []
