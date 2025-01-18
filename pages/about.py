import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About | V3 AI Ticket Creator",
    page_icon="👋",
    layout="wide"
)

# Header
st.title("About the Creator")
try:
    st.image("assets/logo.png", width=150)
except:
    pass

# Main content section
st.markdown("""
## William VanSickle III
### Founder, V3 AI | Product Manager @ Justworks

Based in Brooklyn, I bridge the worlds of AI engineering and product management. 
Currently shaping the future of HR tech at Justworks while building innovative AI solutions through V3 AI.

### Expertise
- 🤖 AI/ML Integration & Development
- 🔄 Workflow Automation
- 🛠️ Custom Tool Development
- 📊 Data Analytics & Visualization
- 🌐 Full-Stack Development

### Connect With Me
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/williavs)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/willyv3/)
[![Website](https://img.shields.io/badge/Website-FF4B4B?style=for-the-badge&logo=safari&logoColor=white)](https://v3-ai.com)
""")

# Featured Solutions section
st.header("Featured Solutions")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("V3 AI Platform")
    st.write("Enterprise AI solutions and consulting services, helping businesses leverage cutting-edge AI technology for practical solutions.")
    st.write("*Technologies: AI/ML, Enterprise Integration, Custom Development*")
    st.markdown("[Learn More →](https://v3-ai.com)")

with col2:
    st.subheader("PM Feels")
    st.write("Master the human side of product management. Transform how you handle stakeholders with emotional intelligence and get your ideas championed.")
    st.write("*Features: EQ Development, Stakeholder Intelligence, Strategic Impact*")
    st.markdown("[Start Building Influence →](https://pmfeels.com)")

with col3:
    st.subheader("Sagedoc")
    st.write("YOUR IDEAS ARE MID 🦆 (until they meet our AI). Generate documentation so fire your IDE starts sweating. From API specs to design systems made for AI/Human Pair Programming.")
    st.write("*Features: Visual Design Specs, System Architecture, API Docs, DB Schema*")
    st.markdown("[Get Started →](https://sagedoc.me)")

# Demo Projects section
st.header("Demo Projects")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Terminal Agent")
    st.write("A terminal-based Langgraph Agent with chat capabilities and memory management.")
    st.write("*Technologies: Python, LangChain, LangGraph, CLI*")
    st.markdown("[View Code →](https://github.com/williavs/terminal_agent)")

with col2:
    st.subheader("CODE PROMPT PRO")
    st.write("AI-powered code prompt engineering tool for developers to generate better, more precise prompts.")
    st.write("*Technologies: LangChain, Python, React, OpenAI*")

with col3:
    st.subheader("ColdCallProX")
    st.write("AI-powered sales training platform with real-time feedback and coaching for sales professionals.")
    st.write("*Technologies: OpenAI, React, Node.js, WebSocket*")

# Enterprise AI Solutions section
with st.expander("🛠️ Enterprise AI Solutions"):
    st.markdown("""
    ### What V3 AI Can Build For You

    1. **Enterprise AI Integration**
       - Custom LLM solutions
       - Workflow automation
       - Document processing & analysis
       - Intelligent data pipelines

    2. **AI-Powered Tools**
       - Custom GPT integrations
       - Natural language interfaces
       - Automated reporting
       - Predictive analytics

    3. **Specialized Solutions**
       - Industry-specific AI tools
       - Custom AI platforms
       - Integration with existing systems
       - Scalable AI infrastructure

    ### Our Process
    1. Free Consultation
    2. Solution Design
    3. Proof of Concept
    4. Development & Testing
    5. Deployment & Training
    6. Ongoing Support

    [**Schedule a Consultation →**](https://v3-ai.com)
    """)

# Contact section
st.header("Get in Touch")
st.markdown("""
Ready to transform your business with AI? Let's discuss how V3 AI can help you:
- Build custom AI solutions for your specific needs
- Integrate AI into your existing workflows
- Scale your AI capabilities efficiently

Visit [v3-ai.com](https://v3-ai.com) to learn more!
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Website\n🌐 [v3-ai.com](https://v3-ai.com)")

with col2:
    st.markdown("### GitHub\n💻 [github.com/williavs](https://github.com/williavs)")

with col3:
    st.markdown("### LinkedIn\n👔 [linkedin.com/in/willyv3](https://www.linkedin.com/in/willyv3/)")

# Footer
st.markdown("---")
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("© 2024 V3 AI | Created by William VanSickle III")
    st.markdown("[v3-ai.com](https://v3-ai.com)")
with col2:
    try:
        st.image("assets/profile.jpeg", width=50)
    except:
        pass 