import os

from jira import JIRA
from jira.exceptions import JIRAError
import re


# Replace these variables with your own
jira_server = os.environ["JIRA_SERVER"]
jira_token = os.environ["JIRA_TOKEN"]
pr_url = os.environ["PR_URL"]
branch_name = os.environ["BRANCH_NAME"]
branch_url = os.environ["BRANCH_URL"]

jira_ticket_id = (
    re.search(r"[a-zA-Z0-9]{3,5}-\d+", branch_name, re.IGNORECASE).group(0)
    if re.search(r"[a-zA-Z0-9]{3,5}-\d+", branch_name, re.IGNORECASE)
    else None
)

if not jira_ticket_id:
    print("ERROR: No JIRA ticket ID found in the branch name.")
    exit(1)

print(f"JIRA Ticket ID: {jira_ticket_id}")

# Create a JIRA instance with bearer token
jira = JIRA(jira_server, token_auth=jira_token)

try:
    # Fetch the issue using the JIRA ticket ID
    issue = jira.issue(jira_ticket_id)

    print(f"DEBUG: Issue ID: {issue.id}")
    print(f"DEBUG: Summary: {issue.fields.summary}")
    print(f"DEBUG: Status: {issue.fields.status.name}")

    # Check if a pull request comment already exists
    existing_comments = jira.comments(issue)
    comment_exists = any(pr_url in comment.body for comment in existing_comments)

    if comment_exists:
        print("DEBUG: Pull request comment already exists.")
    else:
        print("DEBUG: Adding new pull request comment.")
        comment = f"Pull request linked: {pr_url} for branch {branch_name} ({branch_url}) from GitHub Actions"
        jira.add_comment(issue, comment)
except JIRAError as e:
    if e.status_code == 404:
        print(f"ERROR: Issue {jira_ticket_id} not found.")
    else:
        print(f"ERROR: An error occurred: {e.text}")
