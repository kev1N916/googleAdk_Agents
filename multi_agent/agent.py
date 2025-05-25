from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .tools import send_email,get_jira_project_issues_and_comments
from .util import load_instruction_from_file

notification_sender_agent = LlmAgent(
    name="NotificationSender",
    model="gemini-2.0-flash-001",
    description="Sends notifications via different channels which can be email,outlook, teams etc using the tools provided to it.",
    instruction=load_instruction_from_file("notification_sender_instruction.txt"),
    tools=[send_email],
)

summarizer_agent = LlmAgent(
    name="Summarizer",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("summarizer_instruction.txt"),
    description="Generates summaries about JIRA issues from their comments using internal logic and reasoning.",
)

jira_interactor_agent = LlmAgent(
    name="JiraInteractor",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("jira_interactor_instruction.txt"),
    description="Interacts with JIRA for various tasks such as fetching issues, comments, and project details, making new comments, creating new issues, deleting issues.",
    tools=[get_jira_project_issues_and_comments],
)


# --- Llm Agent Workflow ---
jira_Automation_Agent = LlmAgent(
    name="jira_Automation_Agent",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("jira_automation_instruction.txt"),
    description="You are an agent that can send make requests to JIRA for issues and comments, summarize these issues and also send notifications to different channels." \
    "You have sub-agents that will help you with these tasks. " ,
    sub_agents=[jira_interactor_agent, summarizer_agent, notification_sender_agent],
)

# The runner will now execute the workflow
root_agent = jira_Automation_Agent