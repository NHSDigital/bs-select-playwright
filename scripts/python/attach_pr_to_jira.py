import os

from jira import JIRA
from jira.exceptions import JIRAError
import re


# Replace these variables with your own
jira_server = "https://nhsd-jira.digital.nhs.uk/"
jira_token = os.environ["JIRA_TOKEN"]
pr_url = os.environ["PR_URL"]
branch_name = os.environ["BRANCH_NAME"]
branch_url = os.environ["BRANCH_URL"]


jira_ticket_id = (
    re.search(r"bss2-\d+", branch_name, re.IGNORECASE).group(0)
    if re.search(r"bss2-\d+", branch_name, re.IGNORECASE)
    else None
)
if not jira_ticket_id:
    print("No JIRA ticket ID found in the branch name.")
    exit(1)

print(f"JIRA Ticket ID: {jira_ticket_id}")

# Create a JIRA instance with bearer token
jira = JIRA(jira_server, token_auth=jira_token)

try:
    # Fetch the issue using the JIRA ticket ID
    issue = jira.issue(jira_ticket_id)

    print(f"Issue ID: {issue.id}")
    print(f"Summary: {issue.fields.summary}")
    print(f"Status: {issue.fields.status.name}")

    # Check if a pull request comment already exists
    existing_comments = jira.comments(issue)
    comment_exists = any(pr_url in comment.body for comment in existing_comments)

    if comment_exists:
        print("Pull request comment already exists.")
    else:
        print("Adding new pull request comment.")
        comment = (
            f"Pull request linked: {pr_url} for branch {branch_name} ({branch_url}) from GitHub Actions"
        )
        jira.add_comment(issue, comment)
except JIRAError as e:
    if e.status_code == 404:
        print(f"Issue {jira_ticket_id} not found.")
    else:
        print(f"An error occurred: {e.text}")
