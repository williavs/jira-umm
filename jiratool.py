import os
from jira import JIRA
from jira.resources import Issue
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class JiraAgent:
    """Basic Jira API wrapper to read, create, or update Jira issues"""

    def __init__(self, server_url=None, email=None, api_token=None):
        # Use parameters if provided, otherwise fall back to env vars
        self.jira = JIRA(
            server=server_url or os.getenv("JIRA_SERVER_URL"),
            basic_auth=(email or os.getenv("JIRA_EMAIL"), 
                       api_token or os.getenv("JIRA_API_TOKEN"))
        )

    def get_projects(self) -> List[Dict]:
        """Get list of available projects"""
        try:
            projects = self.jira.projects()
            return [{"key": project.key, "name": project.name} for project in projects]
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}")
            return []

    def get_issue_types(self, project_key: str) -> List[Dict]:
        """Get available issue types for a project"""
        try:
            project = self.jira.project(project_key)
            # Get issue types specific to the project
            metadata = self.jira.createmeta(
                projectKeys=project_key,
                expand='projects.issuetypes'
            )
            project_meta = metadata['projects'][0]
            return [{"id": it['id'], "name": it['name']} for it in project_meta['issuetypes']]
        except Exception as e:
            logger.error(f"Error fetching issue types: {str(e)}")
            return []

    def search_users(self, query: str = "") -> List[Dict]:
        """Search for users in Jira"""
        try:
            users = self.jira.search_users(query)
            return [{"name": user.name, "displayName": user.displayName} for user in users]
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            return []

    def search_issues(self, project_key: str, query: str = "", max_results: int = 1000) -> List[Dict]:
        """Get all issues in a project that can be used as parents"""
        try:
            # JQL to get all issues in project, sorted by key descending (newest first)
            jql = f'project = "{project_key}" ORDER BY key DESC'
            if query:  # Only add summary filter if query provided
                jql = f'project = "{project_key}" AND summary ~ "{query}" ORDER BY key DESC'
                
            issues = self.jira.search_issues(jql, maxResults=max_results)
            return [{
                "key": issue.key,
                "summary": issue.fields.summary,
                "type": issue.fields.issuetype.name,
                "status": issue.fields.status.name,
                "created": issue.fields.created,
                "updated": issue.fields.updated
            } for issue in issues]
        except Exception as e:
            logger.error(f"Error searching issues: {str(e)}")
            return []

    def get_issue(self, key: str) -> Optional[Dict]:
        """Fetch and return a Jira issue"""
        try:
            logger.info(f"Fetching Jira issue with key: {key}")
            issue = self.jira.issue(key)
            return {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "type": issue.fields.issuetype.name,
                "status": issue.fields.status.name,
                "parent": getattr(issue.fields, 'parent', None) and {
                    "key": issue.fields.parent.key,
                    "summary": issue.fields.parent.fields.summary
                }
            }
        except Exception as e:
            logger.error(f"Error fetching issue: {str(e)}")
            return None

    def create_issue(self, project_key: str, summary: str, description: str, 
                    issue_type: str = "Task", assignee: str = None, 
                    parent_key: str = None, due_date: str = None) -> Issue:
        """Create an issue with the given fields."""
        # Get issue type ID
        issue_types = self.get_issue_types(project_key)
        issue_type_match = next((it for it in issue_types if it['name'].lower() == issue_type.lower()), None)
        
        if not issue_type_match:
            raise ValueError(f"Issue type '{issue_type}' not found in project {project_key}")
        
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'id': issue_type_match['id']}  # Use ID instead of name
        }
        
        # Add parent link if provided
        if parent_key:
            # Check if the issue type supports parent field directly
            if issue_type.lower() in ['sub-task', 'subtask']:
                issue_dict['parent'] = {'key': parent_key}
            else:
                # For other issue types, we'll create a link after creation
                pass

        if assignee:
            issue_dict['assignee'] = {'name': assignee}
        if due_date:
            issue_dict['duedate'] = due_date

        logger.info(f"Creating Jira issue with the following fields: {issue_dict}")
        issue = self.jira.create_issue(fields=issue_dict)

        # If parent_key was provided but issue type doesn't support direct parent field,
        # create a link
        if parent_key and issue_type.lower() not in ['sub-task', 'subtask']:
            try:
                self.jira.create_issue_link(
                    type="Relates",  # or other link types like "Blocks", "is blocked by", etc.
                    inwardIssue=issue.key,
                    outwardIssue=parent_key
                )
            except Exception as e:
                logger.warning(f"Failed to create issue link: {str(e)}")

        return issue

    def get_available_link_types(self) -> List[Dict]:
        """Get available issue link types"""
        try:
            link_types = self.jira.issue_link_types()
            return [{
                "name": lt.name,
                "inward": lt.inward,
                "outward": lt.outward
            } for lt in link_types]
        except Exception as e:
            logger.error(f"Error fetching link types: {str(e)}")
            return []

    def modify_issue(self, issue_key: str, **fields) -> Issue:
        """Modify an issue with the given key using the keyworded arguments.
        Returns the issue just modified.
        """
        issue = self.jira.issue(issue_key)
        logger.info(f"Modifying Jira issue with key: {issue_key} and the following fields: {fields}")
        issue.update(fields=fields)
        return issue

    def test_connection(self):
        """Test the Jira connection"""
        try:
            projects = self.jira.projects()
            return f"Connection successful. Found {len(projects)} projects."
        except Exception as e:
            return f"Connection failed: {str(e)}"


# Test the Jira connection
if __name__ == "__main__":
    jira_agent = JiraAgent()
    print(jira_agent.test_connection())
