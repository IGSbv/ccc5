# mcp_connectors.py
import os
from dotenv import load_dotenv
from atlassian import Jira
from notion_client import Client
# Load environment variables from .env file
load_dotenv()

def get_jira_tickets(project_key: str):
    """
    This is our first MCP Connector.
    It connects to Jira and fetches the 5 most recent tickets from a project.
    """
    try:
        jira = Jira(
            url=os.getenv("JIRA_SERVER_URL"),
            username=os.getenv("JIRA_USERNAME"),
            password=os.getenv("JIRA_API_TOKEN"),
            cloud=True
        )
        
        # JQL to get issues from a project, ordered by creation date
        jql_query = f'project = "{project_key}" ORDER BY created DESC'
        
        issues = jira.jql(jql_query, limit=5)
        
        # Format the data into a clean string
        formatted_tickets = "Here are the 5 most recent Jira tickets:\n"
        for issue in issues['issues']:
            ticket_id = issue['key']
            summary = issue['fields']['summary']
            status = issue['fields']['status']['name']
            formatted_tickets += f"- {ticket_id} ({status}): {summary}\n"
            
        return formatted_tickets
        
    except Exception as e:
        print(f"Error connecting to Jira: {e}")
        return "Sorry, I couldn't connect to Jira at the moment."
def get_notion_page_content(page_id: str):
    """
    This is our second MCP Connector.
    It connects to Notion and fetches the text content from a page.
    """
    try:
        notion = Client(auth=os.getenv("NOTION_API_KEY"))
        response = notion.blocks.children.list(block_id=page_id)

        content = ""
        for block in response["results"]:
            if "type" in block and block["type"] == "paragraph":
                for rich_text in block["paragraph"]["rich_text"]:
                    content += rich_text["plain_text"]

        return content
    except Exception as e:
        print(f"Error connecting to Notion: {e}")
        return "Sorry, I couldn't connect to Notion."