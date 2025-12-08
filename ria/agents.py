import importlib
from langchain.agents import create_agent
from langchain_core.tools import tool

from .models import get_model
from .tools import get_tools
from .prompts import SUPERVISOR_PROMPT, WORKERS

# ===================================== #
#               MODEL
# ===================================== #

# The model is the reasoning engine of your agent.
llm = get_model()

# ===================================== #
#               PROMPTS
# ===================================== #

def _get_prompts():
    """Get the prompts for each agent"""

    prompts_module_str = "ria.prompts"
    prompts_module = importlib.import_module(prompts_module_str)

    for worker in WORKERS:
        globals()[f"{worker}_agent_prompt"] = lambda worker=worker : getattr(prompts_module, f"{worker}_agent_prompt")
        globals()[f"{worker}_subagent_description"] = lambda worker=worker : getattr(prompts_module, f"{worker}_subagent_description")

# You can shape how your agent approaches tasks by providing a prompt.
_get_prompts()

# ===================================== #
#               TOOLS
# ===================================== #

# Tools give agents the ability to take actions.
tools = get_tools()

# ===================================== #
#               AGENTS
# ===================================== #

agents = []

# create_agent builds a graph-based agent runtime using LangGraph. 
# A graph consists of nodes (steps) and edges (connections) that define how your agent processes information. 
# The agent moves through this graph, executing nodes like the model node (which calls the model), the tools node (which executes tools), or middleware.
def _create_agents():
    """Create the agents"""
    for worker in WORKERS:
        globals()[f"{worker}_agent"] = lambda worker=worker : create_agent(
            model=llm,
            tools=tools[f"mcp_{worker}_tools"],
            system_prompt=globals()[f"{worker}_agent_prompt"]()
        )
        agents.append(globals()[f"{worker}_agent"]())

# Agents combine language models with tools to create systems that can reason about tasks,
# decide which tools to use, and iteratively work towards solutions.
# An LLM Agent runs tools in a loop to achieve a goal.
_create_agents()

# ===================================== #
#     SUBAGENTS AS SUPERVISOR TOOLS
# ===================================== #

supervisor_tools = []

def _create_supervisor_tools():
    """Create subagent tools from agents"""

    def create_subagent_tool(agent_func, tool_name: str, description: str):
        """Create a subagent tool from an agent function"""
        @tool(name_or_callable=tool_name, description=description)
        async def subagent_tool(request: str) -> str:
            result = await agent_func().ainvoke({
                "messages": [{"role": "user", "content": request}]
            })
            return result["messages"][-1].text
        return subagent_tool

    for worker in WORKERS:
        globals()[f"{worker}_subagent"] = create_subagent_tool(
            agent_func=globals()[f"{worker}_agent"],
            tool_name=f"{worker}_subagent",
            description=globals()[f"{worker}_subagent_description"]()
        )
        supervisor_tools.append(globals()[f"{worker}_subagent"])

_create_supervisor_tools()

# ===================================== #
#           SUPERVISOR AGENT
# ===================================== #

def create_supervisor():
    """Create the supervisor that manages the agents"""
    supervisor = create_agent(
        model=llm,
        tools=supervisor_tools,
        system_prompt=SUPERVISOR_PROMPT
    )
    return supervisor

# ===================================== #
#  SUBAGENT TOOL DEFINITIONS (ALTERNATIVE)
# ===================================== #
# def create_subagent_tool(agent_func, tool_name: str, description: str):
#         """Create a subagent tool from an agent function"""
#         @tool(name_or_callable=tool_name, description=description)
#         async def subagent_tool(request: str) -> str:
#             result = await agent_func().ainvoke({
#                 "messages": [{"role": "user", "content": request}]
#             })
#             return result["messages"][-1].text
#         return subagent_tool

# devops_subagent = create_subagent_tool(
#     agent_func=devops_agent,
#     tool_name="devops_subagent",
#     description="""read metrics, read logs, download logs from mc-dope (devops) servers.
#     Use this when the user wants to read logs, read metrics, download logs, loook for canaries etc from mc_devops server.
#     Input: Natural language devops request (e.g., 'Are there any canary failures in mpaasoicnative tenancy of us-phoenix-1 region for the phonebook oracle integration cloud?')"""
#     )
# atlassian_subagent = create_subagent_tool(
#     agent_func=atlassian_agent,
#     tool_name="atlassian_subagent",
#     description="""read, update comments, re-assign jira issues.
#     Input: Natural language request related to jira issue (e.g., 'Get the details of jira id EHRM-3552 the EHRM project queue')"""
#     )

# subagents_definitions = """
# @tool
# async def devops_subagent(request: str) -> str:
#     \"""read metrics, read logs, download logs from mc-dope (devops) servers.

#     Use this when the user wants to read logs, read metrics, download logs, loook for canaries etc from mc_devops server.

#     Input: Natural language devops request (e.g., 'Are there any canary failures in mpaasoicnative tenancy of us-phoenix-1 region for the phonebook oracle integration cloud?')
#     \"""
#     result = await devops_agent().ainvoke({
#         "messages": [{"role": "user", "content": request}]
#     })
#     return result["messages"][-1].text

# @tool
# async def atlassian_subagent(request: str) -> str:
#     \"""read, update comments, re-assign jira issues.

#     Input: Natural language request related to jira issue (e.g., 'Get the details of jira id EHRM-3552 the EHRM project queue')
#     \"""
#     result = await atlassian_agent().ainvoke({
#         "messages": [{"role": "user", "content": request}]
#     })
#     return result["messages"][-1].text
# """

#exec(subagents_definitions)
# Now, devops_subagent and atlassian_subagent are available in the current scope

# @tool
# async def devops_subagent(request: str) -> str:
#     """read metrics, read logs, download logs from mc-dope (devops) servers.

#     Use this when the user wants to read logs, read metrics, download logs, loook for canaries etc from mc_devops server.

#     Input: Natural language devops request (e.g., 'Are there any canary failures in mpaasoicnative tenancy of us-phoenix-1 region for the phonebook oracle integration cloud?')
#     """
#     result = await devops_agent().ainvoke({
#         "messages": [{"role": "user", "content": request}]
#     })
#     return result["messages"][-1].text

# @tool
# async def atlassian_subagent(request: str) -> str:
#     """read, update comments, re-assign jira issues.

#     Input: Natural language request related to jira issue (e.g., 'Get the details of jira id EHRM-3552 the EHRM project queue')
#     """
#     result = await atlassian_agent().ainvoke({
#         "messages": [{"role": "user", "content": request}]
#     })
#     return result["messages"][-1].text
