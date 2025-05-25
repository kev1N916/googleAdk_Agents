from google.adk.agents import Agent
from .mail_sender import MailSender
from .jira_api import JiraClient

jiraClient=JiraClient()
mailSender=MailSender()


def get_jira_project_issues_and_comments() -> dict:
    """Retrieves all ISSUES and their associated COMMENTS for SPRINTS of PROJECTS  within JIRA
    These PROJECTS all belong to the user.
    If the user is not using JIRA, this function should not be invoked.
    This function is specifically designed to interact with Jira instances to fetch sprint and project-related data.
    It should ONLY be used when the user needs to find issues and their corresponding comments
    for a sprint of a project that resides within Jira. If the project or its tracking system is not Jira,
    this function will not be applicable and should not be invoked.

    Returns:
        dict: A dictionary containing the status of the operation and the retrieved data or an error message.
              - If successful, the 'status' key will be "success" and the 'result' key will contain
                a dictionary where keys are issue keys (e.g., "PROJ-123") and values are dictionaries
                containing issue details,which sprint the issue belongs to and a list of comments.
                Example success structure:
                {
                    "status": "success",
                    "result": {
                        "PROJ-1": {
                            "summary": "Implement user authentication",
                            "description": "As a user, I want to log in securely.",
                            "status": "Open",
                            "sprint_name": "Sprint 1",
                            "sprint_goal": "Complete user authentication feature",
                            "comments": [
                                {"author": "john.doe", "created": "2023-10-26T10:00:00Z", "body": "Initial thoughts on implementation."},
                                {"author": "jane.smith", "created": "2023-10-26T14:30:00Z", "body": "Assigned to development team."}
                            ]
                        },
                        "PROJ-2": {
                            "summary": "Fix UI bug on login page",
                            "description": "Button is misaligned in Chrome.",
                            "status": "In Progress",
                            "comments": []
                        }
                    }
                }
              - If an error occurs (e.g., project not found, Jira API issues, or invalid project key),
                the 'status' key will be "error" and the 'error_message' key will provide details
                about the failure.
                Example error structure:
                {
                    "status": "error",
                    "error_message": "Project with key 'NONEXISTENT' not found in Jira."
                }
    """

    return jiraClient.getSummary()   


def send_email(recipient: str, subject: str, body: str) -> dict:
    """Sends an email to a specified recipient with the given subject and body.

    This function facilitates the sending of email messages. It's a general-purpose
    email utility and can be used whenever there's a need to dispatch an email
    to an individual or a group of recipients.

    Args:
        recipient (str): The email address of the primary recipient (e.g., "john.doe@example.com").
                         For multiple recipients, this could be a comma-separated string
                         or a list of strings, depending on the underlying email sending library's
                         expected format.
        subject (str): The subject line of the email. This will appear in the recipient's inbox
                       as the title of the email.
        body (str): The main content of the email message.

    Returns:
        dict: A dictionary indicating the status of the email sending operation.
              - If the email is sent successfully, the 'status' key will be "success".
                Example success structure:
                {
                    "status": "success",
                    "message": "Email successfully sent to john.doe@example.com."
                }
              - If an error occurs during the sending process (e.g., invalid recipient address,
                connection issues with the email server, authentication failure), the 'status' key
                will be "error" and the 'error_message' key will provide details about the failure.
                Example error structure:
                {
                    "status": "error",
                    "error_message": "Failed to connect to email server. Please check network settings."
                }
    """

    mailSender.sendMail(
        subject=subject,
        recipient=recipient,
        body=body
    )

    return {
        "status": "success",
        "message": f"Email successfully sent to {recipient}."
    }

system_prompt = """
You are an intelligent automation agent specialized in monitoring and reporting on Jira project progress.
Your primary goal is to analyze Jira issue data, summarize development progress, identify potential blockers, and communicate this summary via email.

Here's your precise workflow:

1. You will be provided with a dictionary containing detailed information about Jira issues, including their summaries, 
descriptions, statuses, and importantly, their associated comments. This data will be retrieved using the `get_jira_project_issues_and_comments` tool.

2. Analyze and Summarize Progress By Yourself:
    NO EXTERNAL TOOLS ARE TO BE USED FOR THIS STEP.
    Thoroughly examine the `comments` for each issue.
    For each issue, determine and summarize the following:
        Current Progress: What has been done or discussed since the last update or since the issue was created?
        On Track/Off Track:Based on the comments and issue status, is the issue progressing as expected, or is it falling behind schedule?
        Blockers/Delays:*Identify any specific individuals, teams, external dependencies, or technical hurdles mentioned in the comments that are causing or are likely to cause delays.
        If no explicit blockers are mentioned, state that.
        Next Steps (if discernible): What are the immediate next actions mentioned or implied for the issue?

    SYNTHESIZE a concise, professional, and informative summary for the entire set of issues provided.
    This summary should be suitable for a stakeholder who needs a quick overview of the project's health.
    The summary DOES NOT have to be a single a single, cohesive text block.
    SEPARATE it into individual issue summaries.
    NOTHING HAS TO BE IN BOLD. SO WHILE GENERATING THE SUMMARY DONT USE ** TO MAKE ANY WORK OR HEADING BOLD.
    MAKE sure for a single project, the different issues are clearly delineated.
    The summary should be clear, actionable, and devoid of unnecessary jargon.
    

3. Construct Email Content: The summary you generate in step 2 will serve as the entire `body` of the email.

4. Send Email: You will then use the `send_email` tool to dispatch this summary to a specified recipient.

Constraints and Best Practices:

Tool Usage:
    Use `get_jira_project_issues_and_comments()` ONLY when you need to retrieve Jira issues and their comments for the user's projects.
    Use `send_email(recipient: str, subject: str, body: str)` ONLY for sending the generated summary.
    
Summarization Logic:Your summarization must rely *solely* on the provided Jira data and your internal reasoning capabilities. 
Do not attempt to query external APIs, perform web searches, or use any other tools for this analysis.
Ensure your summary is easy to understand and provides actionable insights without excessive jargon.

Error Handling:If the `get_jira_project_issues_and_comments` tool returns an error, report the error message clearly and do not attempt to summarize or send an email. 
If the `send_email` tool returns an error, report that error as well.
Recipient and Subject: The recipient email address and the email subject will be provided to you separately, or you will infer them from the user's request. 
Always confirm the recipient and subject before attempting to send the email.

Example Interaction Flow:

User: "Summarize progress for my JIRA projects and send it to manager@example.com with the subject 'Project Progress Update'."

* Agent Action: Call `get_jira_project_issues_and_comments()`.
* Agent Observation: (Receives Jira data, e.g., `{"status": "success", "result": {"Sprint-1": {...}, "Sprint-2": {...}}}`)
* Agent Thought: Analyze the received Jira data, focusing on comments for progress, blockers, etc.
Agen t Action:Generate summary (e.g., "Overall progress on Project is steady... Sprint-1 is on track... Sprint-2 is blocked by external API...")
Agent Action: Call `send_email(recipient="manager@example.com", subject="Project Progress Update", body="[Generated Summary]")`.
Agent Observation: (Receives email sending status, e.g., `{"status": "success", "message": "Email sent."}`)
Agent Response: "Jira progress summary sent successfully to manager@example.com."

**Remember, your success hinges on accurate analysis of the provided Jira data and precise use of the `send_email` tool.**
"""


root_agent = Agent(
    name="Jira_Automation_Agent",
    model="gemini-2.0-flash",
    description=(
        "Agent which is used to automate tasks related to Jira projects and issues, "
        "including retrieving project issues and their comments, and sending emails."
    ),
    instruction=(
        system_prompt
    ),
    tools=[send_email, get_jira_project_issues_and_comments],
)

