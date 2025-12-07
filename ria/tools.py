import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from typing import Dict, List

mcpServers = {
    "mcp_devops": {
      "timeout": 60,
      "transport": "sse",
      "url": "http://localhost:8081/sse"
    },
    "mcp_atlassian": {
      "timeout": 60,
      "transport": "sse",
      "url": "http://localhost:8082/sse"
    },
    "mcp_math": {
         "command": "python",
         "args": ["mcp_server.py"],
         "transport": "stdio",
     }
}

async def get_tools_by_server_name() -> Dict[str, List[BaseTool]]:
    client = MultiServerMCPClient(
      connections = mcpServers
    )
    tools_by_server = {}
    for server_name in mcpServers.keys():
        tools = await client.get_tools(server_name=server_name)
        tools_by_server[server_name + "_tools"] = tools
    return tools_by_server

def get_tools():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop, so create and run a new one
        print("No running loop found, creating a new one.")
        return asyncio.run(get_tools_by_server_name())
    else:
        # Loop is running, use run_until_complete
        print("Running loop found, using run_until_complete.")
        return loop.run_until_complete(get_tools_by_server_name())

