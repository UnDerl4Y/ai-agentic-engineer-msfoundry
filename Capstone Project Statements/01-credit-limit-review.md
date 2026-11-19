# Capstone Project: Existing Customer Credit Limit Review Assistant

## 1. Project Statement

Create a multi-agent AI assistant that reviews existing customers' financial information and recommends appropriate credit limit actions: **Increase, Maintain, Reduce, or Suspend**.

The system must analyze customer financial data, check applicable credit policy rules, and generate recommendations with supporting explanations.

## 2. Technical Requirements

- Use the existing Microsoft Foundry project and its deployed models.
- Create and configure the required agents, tools, and workflows in Microsoft Foundry.
- Test the agents using the Foundry Playground.
- Implement the complete application using Python, including a separate user interface.
- Connect the Python application to the existing Foundry project using its endpoint and API key.
- Test the application and capture screenshots of the Foundry portal and Python application.

### Agent 1: Financial Analysis Agent

- Analyze two years of customer financial data.
- Calculate the following financial ratios:
  - Current Ratio
  - Debt-to-Equity Ratio
  - Net Profit Margin
- Identify financial trends and risks.
- Summarize the customer's financial health.

### Agent 2: Credit Policy Agent

- Use the provided credit policy document (`.md` or `.txt`) as the knowledge source.
- Use RAG to retrieve relevant credit policy rules.
- Check customer eligibility against the applicable policy criteria.
- Provide relevant policy references and explanations.

### Multi-Agent Workflow

Create a workflow that connects **Agent 1 (Financial Analysis Agent)** and **Agent 2 (Credit Policy Agent)**.

1. Accept customer financial information.
2. Send the data to Agent 1 for financial analysis.
3. Send the relevant information to Agent 2 for credit policy checks.
4. Combine the outputs from both agents.
5. Generate one final credit review with financial analysis, policy findings, recommended action, proposed credit limit, and supporting explanation.

**Note:** Create only two agents. The workflow must make both agents work together. A third agent is not required.

## 3. Deliverables and Submission

Submit one ZIP file containing:

- Complete Python source code and application UI.
- Sample customer financial data.
- Credit policy document.
- README with setup and usage instructions.
- PowerPoint presentation.
- Screenshots of the Foundry configuration, agent testing, workflow execution, and Python application.

### Required Folder Structure

Create a folder using your assigned name, such as `agenticuser99`.

```text
agenticuser99/
├── src/
├── data/
├── screenshots/
├── presentation/
├── README.md
└── .env.example
```

You can organize the folders and files according to your implementation.

**Folder guidelines:**

- `src/`: Complete codebase. Organize agents, tools, workflows, application files, and other source files as required.
- `data/`: Sample customer data (`.csv`), credit policy documents (`.md` or `.txt`), and other required input files.
- `screenshots/`: Screenshots (`.png`) of the Foundry portal, agent configurations, Playground testing, workflow execution, and application results.
- `presentation/`: PowerPoint presentation (`.pptx`).
- `README.md`: Project overview, architecture, prerequisites, setup instructions, configuration, and execution steps.
- `.env.example`: Environment variable template with placeholder values only.

### PowerPoint Presentation

Your presentation should cover:

1. Project overview and problem statement.
2. System architecture.
3. Responsibilities of both agents.
4. Multi-agent workflow showing how both agents work together.
5. Technology stack.
6. Application demonstration and sample results.

### **Environment Configuration**

Include an `.env.example` file with the environment variables required by your application.

Example:

```env
AZURE_AI_PROJECT_ENDPOINT=your_project_endpoint
AZURE_AI_API_KEY=your_api_key
AZURE_AI_MODEL=your_deployed_model
AGENT_1_NAME=financial_analysis_agent
AGENT_2_NAME=credit_policy_agent
```

The example shows common configuration values. You can add other environment variables based on your project requirements, such as agent names, model deployment names, API settings, or other configuration values.

Use the variable names required by your application. Include placeholder values only. **Never include actual API keys, passwords, or other secrets.**

### ZIP and Submission Instructions

1. Exclude the virtual environment (`venv`, `.venv`) and actual `.env` file.
2. Include all required source code, data, screenshots, documentation, and presentation files.
3. Compress the entire project folder into a ZIP file.
4. Keep your assigned project folder as the root folder inside the ZIP file.
5. Name the ZIP file using your assigned folder name. For example, `agenticuser99.zip`.
6. Upload the ZIP file to your designated SharePoint submission folder.

**Important: Do not upload the project to GitHub. Submit the ZIP file through SharePoint only.**

**Optional Video Demonstration:** A video demonstration is optional. A duration of less than 90 seconds is ideal.
