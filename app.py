import streamlit as st
from langchain_openai import ChatOpenAI
from jiratool import JiraAgent
from workflow import create_workflow, AgentState
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, date

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("jira_agent.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="V3 AI | Jira Ticket Creator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://v3-ai.com',
        'Report a bug': 'https://github.com/williavs',
        'About': 'Created by V3 AI - Visit v3-ai.com for more AI solutions'
    }
)

# Initialize session state
if 'credentials_submitted' not in st.session_state:
    st.session_state.credentials_submitted = False
if 'jira_server_url' not in st.session_state:
    st.session_state.jira_server_url = ""
if 'jira_email' not in st.session_state:
    st.session_state.jira_email = ""
if 'jira_api_token' not in st.session_state:
    st.session_state.jira_api_token = ""
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""

# Helper function to parse date string
def parse_date(date_string):
    if date_string and isinstance(date_string, str):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None

def handle_login(jira_server_url, jira_email, jira_api_token, openai_api_key):
    """Handle the login process and return success status"""
    if not all([jira_server_url, jira_email, jira_api_token, openai_api_key]):
        st.error("Please fill in all fields")
        return False
    
    # Test connection with new credentials
    try:
        jira_agent = JiraAgent(
            server_url=jira_server_url,
            email=jira_email,
            api_token=jira_api_token
        )
        result = jira_agent.test_connection()
        if "successful" in result.lower():
            # Save credentials to session state
            st.session_state.jira_server_url = jira_server_url
            st.session_state.jira_email = jira_email
            st.session_state.jira_api_token = jira_api_token
            st.session_state.openai_api_key = openai_api_key
            st.session_state.credentials_submitted = True
            return True
        else:
            st.error(f"Connection failed: {result}")
            return False
    except Exception as e:
        st.error(f"Error connecting to Jira: {str(e)}")
        return False

def show_welcome_page():
    try:
        st.image("assets/logo.png", width=200)
    except:
        st.warning("Logo not found. Please add logo.png to the assets directory.")
        
    st.title("V3 AI Jira Ticket Creator")
    st.markdown("""
    ### Welcome to the Future of Ticket Creation
    
    Transform your requirements into well-structured Jira tickets using AI.
    Simply describe what you need, and let our AI handle the rest.
    
    #### Security & Transparency
    - 🔒 Your API keys are stored securely in session state only
    - 💻 [Open source code](https://github.com/williavs) - inspect how we handle your data
    - 🚫 No data persistence - everything is cleared when you close the app
    - ⚡ Run it locally or deploy it in your secure environment
    
    *This is a demonstration tool to showcase AI-powered ticket creation. Perfect for testing and evaluation. For enterprise deployments or custom solutions, [contact us](https://v3-ai.com).*
    
    #### To get started, you'll need:
    - Your Jira Server URL
    - Jira Email
    - Jira API Token
    - OpenAI API Key
    """)
    
    with st.form("credentials_form", clear_on_submit=False):
        jira_server_url = st.text_input(
            "Jira Server URL",
            value=st.session_state.jira_server_url,
            placeholder="https://your-domain.atlassian.net"
        )
        jira_email = st.text_input(
            "Jira Email",
            value=st.session_state.jira_email,
            placeholder="your.email@company.com"
        )
        jira_api_token = st.text_input(
            "Jira API Token",
            value=st.session_state.jira_api_token,
            type="password",
            help="Generate from https://id.atlassian.com/manage-profile/security/api-tokens"
        )
        openai_api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Get from https://platform.openai.com/api-keys"
        )
        
        if st.form_submit_button("Login", use_container_width=True):
            if handle_login(jira_server_url, jira_email, jira_api_token, openai_api_key):
                st.success("Connection successful!")
                st.balloons()
                st.rerun()

def main_app():
    # Initialize Jira Agent with session state credentials
    jira_agent = JiraAgent(
        server_url=st.session_state.jira_server_url,
        email=st.session_state.jira_email,
        api_token=st.session_state.jira_api_token
    )

    # Initialize LLM with session state OpenAI key
    os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")

    # Create workflow
    app = create_workflow(llm)

    # Custom sidebar header
    with st.sidebar:
        try:
            st.image("assets/logo.png", width=150)
        except:
            pass
        st.title("V3 AI")
        
        # Navigation section
        st.markdown("### Navigation")
        
        # About page link
        if st.button("ℹ️ About V3 AI", use_container_width=True):
            st.switch_page("pages/about.py")
            
        if st.button("🌐 Visit v3-ai.com", use_container_width=True):
            st.markdown('<meta http-equiv="refresh" content="0;url=https://v3-ai.com">', unsafe_allow_html=True)
        
        # Logout button at the bottom of sidebar
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    # Initialize session state for app data
    if 'state' not in st.session_state:
        st.session_state.state = 'input'
    if 'jira_ticket' not in st.session_state:
        st.session_state.jira_ticket = None
    if 'ai_response' not in st.session_state:
        st.session_state.ai_response = None
    if 'projects' not in st.session_state:
        st.session_state.projects = jira_agent.get_projects()

    # Main content area title
    st.title("V3 AI Jira Ticket Creator")
    st.markdown("""
    Transform your requirements into well-structured Jira tickets using AI. 
    Simply describe what you need, and let our intelligent system handle the formatting and organization.
    
    *Created by [V3 AI](https://v3-ai.com) - Enterprise AI Solutions*
    """)
    
    # Sidebar for Jira settings
    with st.sidebar:
        st.header("Jira Settings")
        
        # Initialize variables
        project_key = None
        selected_issue_type = None
        assignee_username = None
        parent_key = None
        
        # Project selection
        project_options = {f"{p['key']} - {p['name']}": p['key'] for p in st.session_state.projects}
        if project_options:
            selected_project = st.selectbox(
                "Select Project",
                options=list(project_options.keys()),
                key="project_select"
            )
            project_key = project_options[selected_project]
            
            # Get issue types for selected project
            issue_types = jira_agent.get_issue_types(project_key)
            if issue_types:
                issue_type_options = [it['name'] for it in issue_types]
                if not issue_type_options:
                    st.error("No issue types available for this project")
                    selected_issue_type = None
                else:
                    selected_issue_type = st.selectbox(
                        "Issue Type",
                        options=issue_type_options,
                        key="issue_type_select",
                        help="Select the type of issue to create"
                    )
                    # Show subtask warning if parent selected
                    if parent_key and selected_issue_type.lower() == 'sub-task':
                        st.info("This will be created as a subtask of the selected parent issue")
                    elif parent_key:
                        st.info("This will be created as a linked issue to the selected parent")
            else:
                st.error("Failed to load issue types")
                selected_issue_type = None
            
            # Parent issue selection
            st.subheader("Parent Issue (Optional)")
            
            # Get all issues for the project
            if 'project_issues' not in st.session_state or st.session_state.get('last_project') != project_key:
                st.session_state.project_issues = jira_agent.search_issues(project_key)
                st.session_state.last_project = project_key
            
            # Create a formatted list of issues for the dropdown
            issue_options = ["No Parent"]
            issue_keys = {"No Parent": None}
            
            for issue in st.session_state.project_issues:
                # Format: KEY - TYPE - STATUS: Summary
                display_text = f"{issue['key']} - {issue['type']} - {issue['status']}: {issue['summary'][:100]}..."
                issue_options.append(display_text)
                issue_keys[display_text] = issue['key']
            
            selected_issue = st.selectbox(
                "Select Parent Issue",
                options=issue_options,
                help="Select an existing issue as parent"
            )
            
            parent_key = issue_keys[selected_issue]
            if parent_key:
                parent_issue = jira_agent.get_issue(parent_key)
                if parent_issue:
                    with st.expander("Parent Issue Details"):
                        st.info(f"""
                        **Key:** {parent_issue['key']}
                        **Type:** {parent_issue['type']}
                        **Status:** {parent_issue['status']}
                        **Summary:** {parent_issue['summary']}
                        """)
            
            # Optional filter to search within dropdown
            filter_issues = st.text_input(
                "Filter Issues",
                placeholder="Type to filter issues list",
                help="Filter the issues dropdown by typing part of the key or summary"
            )
            if filter_issues:
                filtered_options = [opt for opt in issue_options 
                                  if filter_issues.lower() in opt.lower()]
                if filtered_options:
                    selected_issue = st.selectbox(
                        "Filtered Issues",
                        options=filtered_options,
                        key="filtered_parent"
                    )
                    parent_key = issue_keys[selected_issue]
                    if parent_key:
                        parent_issue = jira_agent.get_issue(parent_key)
                        if parent_issue:
                            with st.expander("Parent Issue Details"):
                                st.info(f"""
                                **Key:** {parent_issue['key']}
                                **Type:** {parent_issue['type']}
                                **Status:** {parent_issue['status']}
                                **Summary:** {parent_issue['summary']}
                                """)
                else:
                    st.warning("No matching issues found")

            # Assignee search
            st.subheader("Assignee")
            assignee_query = st.text_input("Search Assignee", 
                                         placeholder="Type to search users",
                                         key="assignee_search")
            if assignee_query:
                users = jira_agent.search_users(assignee_query)
                if users:
                    selected_assignee = st.selectbox(
                        "Select Assignee",
                        options=[f"{u['displayName']} ({u['name']})" for u in users],
                        key="assignee_select"
                    )
                    assignee_username = users[st.session_state.assignee_select]['name']
                else:
                    st.warning("No users found")
                    assignee_username = None
            else:
                assignee_username = None
        else:
            st.error("No projects found. Please check your Jira connection.")
            project_key = None
            selected_issue_type = None
            assignee_username = None
            parent_key = None

    # Rest of your existing main app code...
    # Test Jira connection
    if st.button("Test Jira Connection", key="test_connection"):
        result = jira_agent.test_connection()
        logger.info(f"Jira connection test result: {result}")
        st.write(result)

    # User input
    input_type = st.selectbox(
        "Select Input Type",
        ["Technical Task", "Business Requirement", "Process Change"]
    )

    user_input = st.text_area("Enter your Jira ticket details:")

    if st.button("Generate Ticket", key="generate_ticket") and user_input:
        if not project_key:
            st.error("Please select a project first")
            return
            
        logger.info("Generate Ticket button clicked.")
        with st.spinner("Generating ticket..."):
            state = AgentState(
                human_input=user_input,
                input_type=input_type,
                ai_response="",
                jira_ticket={},
                messages=[]
            )
            for output in app.stream(state, {"configurable": {"thread_id": "1"}}, stream_mode="values"):
                logger.debug(f"Stream output: {output}")
                if "jira_ticket" in output and output["jira_ticket"]:
                    st.session_state.jira_ticket = output["jira_ticket"]
                    st.session_state.ai_response = output.get("ai_response", "AI response not available")
                    st.session_state.state = 'review'
                else:
                    st.session_state.ai_response = output.get("ai_response", "AI response not available")
        st.rerun()

    # Display and edit the generated ticket
    if st.session_state.state == 'review' and st.session_state.jira_ticket:
        st.write("Generated Jira Ticket:")
        st.write(f"Summary: {st.session_state.jira_ticket['summary']}")
        st.write(f"Description: {st.session_state.jira_ticket['description']}")
        st.write(f"Due Date: {st.session_state.jira_ticket.get('due_date', 'Not set')}")

        with st.form(key='edit_ticket'):
            new_summary = st.text_input("Edit Summary", value=st.session_state.jira_ticket['summary'])
            new_description = st.text_area("Edit Description", value=st.session_state.jira_ticket['description'])
            new_due_date = st.date_input("Edit Due Date", value=parse_date(st.session_state.jira_ticket.get('due_date')) or date.today())
            
            submit_button = st.form_submit_button(label='Update Ticket')
            if submit_button:
                st.session_state.jira_ticket['summary'] = new_summary
                st.session_state.jira_ticket['description'] = new_description
                st.session_state.jira_ticket['due_date'] = new_due_date.isoformat() if new_due_date else None
                st.rerun()

        # Human review
        st.write("Please review the generated ticket:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Approve and Create Ticket"):
                if not selected_issue_type:
                    st.error("Please select an issue type")
                    return
                    
                try:
                    issue = jira_agent.create_issue(
                        project_key=project_key,
                        summary=st.session_state.jira_ticket['summary'],
                        description=st.session_state.jira_ticket['description'],
                        issue_type=selected_issue_type,
                        assignee=assignee_username,
                        parent_key=parent_key,
                        due_date=st.session_state.jira_ticket.get('due_date')
                    )
                    st.success(f"Created Jira issue: [{issue.key}]({st.session_state.jira_server_url}/browse/{issue.key})")
                    if parent_key:
                        st.info(f"Linked to parent issue: [{parent_key}]({st.session_state.jira_server_url}/browse/{parent_key})")
                    st.session_state.state = 'input'
                    st.session_state.jira_ticket = None
                    st.session_state.ai_response = None
                except ValueError as e:
                    st.error(f"Invalid input: {str(e)}")
                except Exception as e:
                    st.error(f"Error creating Jira issue: {str(e)}")
                    logger.error(f"Detailed error creating issue: {e}", exc_info=True)
        with col2:
            if st.button("Reject and Start Over"):
                st.session_state.state = 'input'
                st.session_state.jira_ticket = None
                st.session_state.ai_response = None
                st.rerun()

    # Display AI response
    if st.session_state.ai_response:
        st.write("AI Response (XML):")
        st.code(st.session_state.ai_response, language='xml')

    # Clear button to reset the app state
    if st.button("Clear", key="clear_button"):
        logger.info("Clear button pressed. Resetting all states")
        st.session_state.state = 'input'
        st.session_state.jira_ticket = None
        st.session_state.ai_response = None
        st.rerun()

    if not user_input and st.session_state.state == 'input':
        st.warning("Please enter ticket details before generating.")

# Main app flow using tabs for better organization
if not st.session_state.credentials_submitted:
    show_welcome_page()
else:
    main_app()
