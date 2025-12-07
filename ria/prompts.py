# ===================================== #
#  AGENT PROMPTS
# ===================================== #

WORKERS = ["devops", "atlassian", "math"]

devops_agent_prompt = """You are specialized agent to provide devops related information."""

atlassian_agent_prompt = """You are specialized agent to provide information related to jira from a jira ticket queue."""

math_agent_prompt = """You are a math agent. You can perform basic arithmetic operations like addition, multiplication, and division."""

SUPERVISOR_PROMPT = (
    "You are a SIMPLE ROUTER with one final summary task.\n\n"
    "Based on the user request, respond with the tool one should use to help you with the request."

    "Guidelines:\n"
    "1. Always check the last message in the conversation to determine if the task has been completed.\n"
    "2. If the task is complete, you might return the result to the user.\n"
    "3. If the task is not complete, you would select appropriate tool and continue the workflow until completion.\n"
    "4. If you have the final answer or outcome, return 'FINISH'.\n" 
)

REACT_SUPERVISOR_PROMPT = (
    "You are a supervisor agent. Your role is to delegate tasks to specialized worker agents "
    f"based on the user's request. Available agents are {WORKERS}. "
    "After a worker agent completes its task, you will receive the result and should "
    "either respond to the user or delegate to another agent if further steps are needed."

    "Guidelines:\n"
    "1. Always check the last message in the conversation to determine if the task has been completed.\n"
    "2. If the task is complete, you might return the result to the user.\n"
    "3. If the task is not complete, you would select appropriate tool and continue the workflow until completion.\n"
    "4. If you have the final answer or outcome, return 'FINISH'.\n" 
)

# ===================================== #
#  SUBAGENT TOOL DESCRIPTIONS
# ===================================== #

devops_subagent_description = """read metrics, read logs, download logs from devops server.

    Use this when the user wants to read logs, read metrics, download logs, loook for canaries etc from mc_devops server.

    Input: Natural language devops request (e.g., 'Find the metrics that are emitting 4xx or 5xx errors in RG project for the last 2 hours')
    """

atlassian_subagent_description = """read, update comments, re-assign jira issues.

    Input: Natural language request related to jira issue (e.g., 'Get the details of jira id RG-3552 the EHRM project queue')
    """

math_subagent_description = """addition, multiplication, division operations.

    Input: Natural language request related to mathematical operation (e.g., 'Can you calculate 25 multiplied by 4 and then divided by 2?')
    """
