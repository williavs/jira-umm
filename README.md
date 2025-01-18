# V3 AI Jira Ticket Creator 🤖

Transform your requirements into well-structured Jira tickets using AI. This tool leverages GPT-4 to help you create detailed, properly formatted Jira tickets from natural language descriptions.

## 🌟 Features

- 🧠 **AI-Powered Ticket Generation**: Convert natural language into structured Jira tickets
- 🔄 **Smart Issue Type Detection**: Automatically suggests appropriate issue types
- 👥 **Assignee Management**: Search and assign tickets to team members
- 🔗 **Parent Issue Linking**: Create subtasks or linked issues with ease
- 🎯 **Multiple Input Types**: Support for Technical Tasks, Business Requirements, and Process Changes
- 🔒 **Secure API Handling**: No data persistence, all credentials stored in session state only
- 🎨 **Modern UI**: Clean, intuitive interface built with Streamlit

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jira account with API access
- OpenAI API key
- Git (for cloning the repository)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/williavs/jira-umm.git
cd jira-umm
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

You'll need the following credentials:
- Jira Server URL (e.g., https://your-domain.atlassian.net)
- Jira Email
- Jira API Token (Generate from https://id.atlassian.com/manage-profile/security/api-tokens)
- OpenAI API Key (Get from https://platform.openai.com/api-keys)

## 🎮 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter your credentials in the welcome page
3. Select your project and issue type
4. Describe your ticket requirements in natural language
5. Review and edit the generated ticket
6. Approve and create the ticket in Jira

## 🔐 Security

- No credentials are stored persistently
- All API keys and tokens are kept in session state only
- The application can be run locally in your secure environment
- Open source code for full transparency

## 🛠️ Technical Details

### Architecture

- **Frontend**: Streamlit
- **AI Integration**: LangChain + GPT-4
- **Jira Integration**: Custom JiraAgent class
- **State Management**: Streamlit session state
- **Error Handling**: Comprehensive logging and user feedback

### Key Components

- `app.py`: Main application and UI
- `jiratool.py`: Jira integration and API handling
- `workflow.py`: LangChain workflow configuration
- `pages/about.py`: About page with developer info

## 🤝 Contributing

This is a demonstration project to showcase AI capabilities in workflow automation. Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Links

- [V3 AI Website](https://v3-ai.com)
- [GitHub Repository](https://github.com/williavs/jira-umm)
- [Report Issues](https://github.com/williavs/jira-umm/issues)

## 👨‍💻 Author

**William VanSickle III**
- Founder, V3 AI
- Product Manager @ Justworks
- [GitHub](https://github.com/williavs)
- [LinkedIn](https://www.linkedin.com/in/willyv3/)
- [Website](https://v3-ai.com)

## 🙋‍♂️ Support

Need enterprise-grade AI solutions or custom development?
- Visit [v3-ai.com](https://v3-ai.com)
- Email: [william@v3-ai.com](mailto:william@v3-ai.com)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/williavs/jira-umm?style=social)
![GitHub forks](https://img.shields.io/github/forks/williavs/jira-umm?style=social)
![GitHub issues](https://img.shields.io/github/issues/williavs/jira-umm)
![GitHub license](https://img.shields.io/github/license/williavs/jira-umm)

---

*Built with ❤️ by [V3 AI](https://v3-ai.com)* 