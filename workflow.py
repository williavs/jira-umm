from langgraph.graph import StateGraph, END
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated, List
import operator
import logging
import json
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    human_input: str
    input_type: str  # Add this line
    jira_ticket: dict
    ai_response: str

def create_workflow(llm: ChatOpenAI):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an advanced AI assistant specializing in creating comprehensive Jira tickets for the AI Pod at Justworks. Your role is to analyze various types of input and create detailed, well-structured Jira issues that capture both technical and non-technical requirements effectively.

Input Analysis Guidelines:
1. For technical inputs (code, APIs, architecture docs):
   - Include specific technical requirements and dependencies
   - List potential technical challenges and constraints
   - Specify development environment requirements
   - Add relevant technical acceptance criteria
   - Include performance considerations
   - Reference related technical documentation

2. For business/non-technical inputs (PRDs, requirements):
   - Focus on business objectives and success metrics
   - Include stakeholder requirements
   - Outline business impact and value proposition
   - Add relevant business context and background
   - Include user story format where appropriate
   - Reference related business documents

3. For process/operational inputs:
   - Detail workflow changes and process impacts
   - Include operational requirements
   - Specify training or documentation needs
   - List affected teams or departments
   - Include timeline considerations
   - Reference related process documentation

Key Areas to Consider:
- AI/ML Components: Model requirements, training data needs, performance metrics
- Integration Points: APIs, services, databases, external systems
- Security Requirements: Data handling, authentication, authorization
- Scalability Considerations: Performance requirements, load handling
- Testing Requirements: Unit tests, integration tests, acceptance criteria
- Documentation Needs: Technical docs, user guides, API documentation
- Dependencies: Other tickets, systems, or team dependencies
- Resource Requirements: Computing resources, tools, licenses

Your response MUST be in the following XML format:

<jira_ticket>
    <summary>Clear, specific title describing the core task (max 80 chars)</summary>
    
    <description>
    h2. Background
    [Provide detailed context and background information here]

    h2. Objective
    [Provide clear statement of what needs to be accomplished]

    h2. Technical Details
    [Provide technical specifications, requirements, and constraints if applicable]

    h2. Requirements
    * [List detailed functional requirements]
    * [List technical requirements if applicable]
    * [List integration requirements if applicable]
    * [List security requirements if applicable]

    h2. Acceptance Criteria
    * [List specific, measurable criteria for completion]
    * [List testing requirements]
    * [List performance requirements if applicable]

    h2. Dependencies
    * [List dependencies and prerequisites]
    * [List related tickets or projects]

    h2. Additional Information
    * [List any other relevant details]
    * [Add links to relevant documentation]
    * [Add notes on implementation approach]
    </description>

    <start_date>YYYY-MM-DD</start_date>
    <due_date>YYYY-MM-DD</due_date>
    <priority>High/Medium/Low</priority>
    <labels>Comma-separated list of relevant labels (e.g., AI, Technical, Business, Process)</labels>
    <epic_link>Name of the related epic if applicable</epic_link>
    <story_points>Estimated story points (if applicable)</story_points>
    <components>Relevant components (comma-separated)</components>
</jira_ticket>

Analyze the input carefully to determine its type (technical, business, or process) and adjust the detail level and focus accordingly. Ensure all relevant sections are filled with appropriate detail while maintaining clarity and structure."""),
        ("human", "Input Type: {input_type}"),
        ("human", "Content: {human_input}"),
        ("human", "Create a detailed Jira ticket based on this input, ensuring appropriate depth and focus based on the input type.")
    ])

    # Define the LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    def process_input(state: AgentState) -> AgentState:
        # Pass both input_type and human_input to the chain
        response = llm_chain.run(
            input_type=state["input_type"],
            human_input=state["human_input"]
        )
        logger.debug(f"AI response: {response}")
        
        try:
            jira_ticket = extract_ticket_info_from_xml(response)
            if not jira_ticket:
                raise ValueError("Failed to extract ticket info from XML")
            
            return {**state, "jira_ticket": jira_ticket, "ai_response": response}
        except Exception as e:
            logger.error(f"Failed to process AI response: {str(e)}")
            return {**state, "ai_response": f"Failed to process AI response: {str(e)}", "jira_ticket": {}}

    def extract_ticket_info_from_xml(xml_string):
        ticket = {}
        fields = [
            'summary', 'description', 'start_date', 'due_date',
            'priority', 'labels', 'epic_link', 'story_points', 'components'
        ]
        
        for field in fields:
            pattern = f"<{field}>(.*?)</{field}>"
            match = re.search(pattern, xml_string, re.DOTALL)
            if match:
                ticket[field] = match.group(1).strip()
        
        # Ensure required fields are present
        if 'summary' not in ticket or 'description' not in ticket:
            return None
        
        return ticket

    # Define the graph
    workflow = StateGraph(AgentState)

    # Define the nodes
    workflow.add_node("process_input", process_input)

    # Set the entrypoint as `process_input`
    workflow.set_entry_point("process_input")

    # Add edge to END
    workflow.add_edge("process_input", END)

    # Compile the graph
    app = workflow.compile()

    return app
