import importlib
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from .models import get_model
from .tools import get_tools
from .prompts import REACT_SUPERVISOR_PROMPT, WORKERS

# ===================================== #
#               MODEL
# ===================================== #

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

_get_prompts()

# ===================================== #
#               TOOLS
# ===================================== #

tools = get_tools()

# ===================================== #
#               AGENTS
# ===================================== #

agents = []

def _create_react_agents():
    """Create the agents"""
    for worker in WORKERS:
        globals()[f"{worker}_agent"] = lambda worker=worker: create_react_agent(
            model=llm,
            tools=tools[f"mcp_{worker}_tools"],
            prompt=globals()[f"{worker}_agent_prompt"](),
            name=f"{worker}_agent"
        )
        agents.append(globals()[f"{worker}_agent"]())

_create_react_agents()

# ===================================== #
#           SUPERVISOR AGENT
# ===================================== #

def create_react_supervisor():
    """Create the supervisor that manages the agents"""
    
    supervisor = create_supervisor(
        model=llm,
        agents=agents,
        prompt=REACT_SUPERVISOR_PROMPT,
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

    return supervisor