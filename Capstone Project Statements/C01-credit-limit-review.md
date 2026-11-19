# **Capstone Project: Existing Customer Credit Limit Review Assistant**

## **1. Project Statement**

Create a multi-agent AI assistant that reviews existing customers' financial information and recommends appropriate credit limit actions: **Increase, Maintain, Reduce, or Suspend**.

The assistant should analyze customer financial data, evaluate applicable credit policy rules, and generate recommendations with supporting explanations.

## **2. Technical Requirements**

Use the **existing Microsoft Foundry project and its already-deployed models**. Create and configure the required agents, tools, and workflows within the same project.

### **Agent 1: Financial Analysis Agent**

- Analyze two years of customer financial data.
- Calculate the following financial ratios:
  - Current Ratio
  - Debt-to-Equity Ratio
  - Net Profit Margin
- Identify financial trends, risks, and changes in the customer's financial position.
- Provide a summary of the customer's financial health.

### **Agent 2: Credit Policy Agent**

- Use the provided credit policy PDF as the knowledge source.
- Implement Retrieval-Augmented Generation (RAG) to retrieve relevant credit policy rules.
- Evaluate customer eligibility against the applicable policy criteria.
- Provide relevant policy references and explanations.

### **Multi-Agent Workflow**

Create a multi-agent workflow that:

1. Accepts existing customer financial information as input.
2. Sends the financial data to the Financial Analysis Agent.
3. Sends the relevant customer information to the Credit Policy Agent.
4. Combines the outputs from both agents.
5. Generates a consolidated credit limit review with:
   - Financial analysis and key ratios.
   - Identified financial risks and trends.
   - Relevant credit policy rules and references.
   - Recommended action: Increase, Maintain, Reduce, or Suspend.
   - Proposed credit limit.
   - Supporting explanation for the recommendation.

## **3. Deliverables**

**ZIP file:** A complete project package containing all the following:

- Complete source code (excluding the virtual environment and `.env` file).
- Sample financial data.
- Credit policy PDF.
- README file with project setup instructions and usage details.
- PowerPoint presentation covering:
  - Project overview.
  - System architecture.
  - Agent responsibilities.
  - Multi-agent workflow.
- Screenshots of the working application showing:
  - Customer input data.
  - Financial analysis and calculated ratios.
  - Retrieved credit policy rules.
  - Final credit limit recommendations.

## **4. ZIP Folder Structure and Naming Convention**

Before creating the ZIP file, organize all deliverables inside a folder named `agenticuser99`. Replace `99` with your assigned number.

**Example folder structure:** follow https://github.com/UnDerl4Y/capstone-project-template

*The structure can be adapted to your actual implementation.*

**Important instructions:**

1. Exclude the virtual environment (`venv`, `.venv`) and actual `.env` file.
2. Keep `.env.example` with placeholder values only. Do not include API keys, passwords, or other secrets.
3. Ensure all required source files, data, presentation, and screenshots are inside the `agenticuser99` folder.
4. Compress the entire `agenticuser99` folder into a ZIP file named `agenticuser99.zip`.
5. Keep `agenticuser99` as the root folder inside the ZIP file.
6. Upload the ZIP file to the designated SharePoint folder.

**Example:** If your assigned username is `agenticuser5`, your folder must be named `agenticuser5` and your ZIP file must be `agenticuser5.zip`.

## **5. Submission Checklist**

- Financial Analysis Agent implemented and tested.
- Credit Policy Agent implemented with RAG.
- Multi-agent workflow configured and tested.
- Credit limit recommendations generated with supporting explanations.
- Complete source code and sample data included.
- Credit policy PDF included.
- README included.
- PowerPoint presentation included.
- Required application screenshots included.
- ZIP folder and filename follow the assigned username convention.
- ZIP file uploaded to the designated SharePoint folder.

**Note:** Video Demo is optional (Under 1-2 mins).
