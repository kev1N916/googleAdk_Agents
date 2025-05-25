import os
from dotenv import load_dotenv
from atlassian import Jira
import json

class JiraClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.jira = Jira(
            url=os.getenv('JIRA_URL'),
            username=os.getenv('JIRA_EMAIL'),
            password=os.getenv('JIRA_API_TOKEN'),
        )

    def getSummary(self) -> dict:
            """
             Returns a dictionary summarizing all issues from JIRA sprints
             mapped by issue keys. Each entry contains:
             - summary
             - description
             - status
             - sprint name
             - sprint goal
             - comments: list of {author, created, body}
             """
            
            result = {}
            
            boards = self.jira.get_all_agile_boards()
            for board in boards.get("values", []):
                sprints = self.jira.get_all_sprints_from_board(board_id=board['id'])
                for sprint in sprints.get("values", []):
                    sprint_name = sprint.get('name', 'N/A')
                    sprint_goal = sprint.get('goal', 'N/A')
                    
                    issues = self.jira.get_sprint_issues(sprint_id=sprint['id'], start=0, limit=50)
                    for issue in issues.get("issues", []):
                        key = issue['key']
                        fields = issue['fields']
                        issue_summary = fields.get('summary', 'N/A')
                        issue_description = fields.get('description', 'N/A')
                        issue_status = fields.get('status', {}).get('name', 'N/A')
                        
                        comments_list = []
                        for comment in fields.get('comment', {}).get('comments', []):
                            comments_list.append({
                                "author": comment.get('author', {}).get('displayName', 'N/A'),
                                "created": comment.get('created', 'N/A'),
                                "body": comment.get('body', '')
                                })
                        result[key] = {
                             "summary": issue_summary,
                             "description": issue_description,
                             "status": issue_status,
                             "sprint_name": sprint_name,
                             "sprint_goal": sprint_goal,
                             "comments": comments_list
                             }
                    
            return result

    # def getSummary(self):
    #     boards = self.jira.get_all_agile_boards()
    #     for board in boards.get("values", []):
    #         print(f"Board Name: {board['name']}")
    #         print(f"Board Type: {board['type']}")
    #         print(f"Project Key: {board['location']['projectKey']}")
            
    #         sprints = self.jira.get_all_sprints_from_board(board_id=board['id'])
    #         for sprint in sprints.get("values", []):
    #             print(f"  Sprint Name: {sprint['name']}")
    #             print(f"  Sprint State: {sprint['state']}")
    #             print(f"  Sprint Start Date: {sprint.get('startDate', 'N/A')}")
    #             print(f"  Sprint End Date: {sprint.get('endDate', 'N/A')}")
    #             print(f"  Sprint Goal: {sprint.get('goal', 'N/A')}")
                
    #             issues = self.jira.get_sprint_issues(sprint_id=sprint['id'], start=0, limit=50)
    #             for issue in issues.get("issues", []):
    #                 print(f"    Issue Key: {issue['key']}")
    #                 fields = issue['fields']
    #                 print(f"    Issue Summary: {fields.get('summary', 'N/A')}")
    #                 print(f"    Issue Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
    #                 print(f"    Issue Status: {fields.get('status', {}).get('name', 'N/A')}")
    #                 print(f"    Issue Resolution: {fields.get('resolution', 'N/A')}")
                    
    #                 for comment in fields.get('comment', {}).get('comments', []):
    #                     print(f"      Comment ID: {comment['id']}")
    #                     print(f"      Comment Author: {comment['author']['displayName']}")
    #                     print(f"      Comment Body: {comment['body']}")
    #                     print(f"      Comment Created: {comment['created']}")


# Example usage:
# if __name__ == "__main__":
#     jiraClient = JiraClient()
#     result = jiraClient.getSummary()
#     print(json.dumps(result, indent=4))












    # print(sprints)

        # issueDetails=jira2.get_issue(issue_id_or_key=issue["id"])
        # print(issueDetails['key'])
        # print(issueDetails['fields']['summary'])
        # print(issueDetails['fields']['issueType']['name'])

 ##   sprints=jira2.get_all_sprints_from_board(board_id=board['id'])
  ##  for sprint in sprints["values"]:
 ##   print(f"  Sprint ID: {sprint['id']}")
        # print(f"  Sprint Name: {sprint['name']}")
        # print(f"  Sprint State: {sprint['state']}")
        # print(f"  Sprint Start Date: {sprint['startDate']}")
        # print(f"  Sprint End Date: {sprint['endDate']}")
        # print(f"  Sprint Complete Date: {sprint.get('completeDate', 'N/A')}")

        # issues=jira2.get_issue(sprint_id=sprint['id'])
    # print("---")

