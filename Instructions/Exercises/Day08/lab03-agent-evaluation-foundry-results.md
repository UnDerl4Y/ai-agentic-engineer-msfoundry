---
lab:
  title: 'Evaluate an Azure AI agent using the Python SDK'
  description: 'Learn how to evaluate an existing Azure AI agent using the Python SDK and review evaluation results in Microsoft Foundry.'
  level: 300
  duration: 40
  islab: true
  status: 'released'
---

# Evaluate an Azure AI agent using the Python SDK

In this exercise, you'll use the Azure AI Projects SDK to evaluate an existing Credit Risk Assessment agent. You'll prepare a JSONL test dataset, configure built-in evaluators, run the evaluation, and review the results in Microsoft Foundry.

This exercise takes approximately **40 minutes** to complete.

## Learning objectives

By the end of this exercise, you'll be able to:

- Prepare a JSONL dataset for agent evaluation.
- Connect to a Microsoft Foundry project using the Python SDK.
- Configure built-in evaluators.
- Run an evaluation against an Azure AI agent.
- Review evaluation results in Microsoft Foundry.
- Identify weak test cases and suggest improvements.

## Prerequisites

Before starting this exercise, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.12.10](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed.
- Access to the Microsoft Foundry project and a model deployment within the same project.

## Create the agent

1. Return to [Microsoft Foundry](https://ai.azure.com/?utm_source=chatgpt.com) and select your project if you haven't been automatically redirected to the home page.

2. Click on **Create an agent**.

3. A dialog box will appear. Enter your agent name in the following format: `<your_unique_prefix>-cra`.

4. Leave the other settings unchanged. Click **Create**.

5. Replace the default instructions with the following:

   ```text
   You are a Credit Risk Assessment Agent. Help users understand factors that may affect credit risk and provide clear, concise responses based on the information provided.
   ```

6. After creating the agent, note its name in Notepad, as you will need to use the same name in the `.env` file shortly:

   ```env
   AGENT_NAME="<your_unique_prefix>-credit-risk-assessment-agent"
   ```

## Get the application files from GitHub

### 1. Clean Up Previous Downloads

Before downloading the latest repository version, remove the previous downloaded files and extracted folders to avoid using an outdated copy.

1. Open your **Downloads** folder.
2. Delete the previously downloaded `AgenticAIEngineer-main.zip` file.
3. Delete the previously extracted `AgenticAIEngineer-main` folder and any duplicate extracted folders, such as `AgenticAIEngineer-main (1)`.
4. Make sure the old copies have been removed before proceeding.

> [!TIP]
> Make sure to download the latest repository ZIP file, as it contains the current lab files and instructions required to complete the steps in this exercise.

### 2. Download and Extract the Latest Repository

The application files for the Credit Risk RAG application are provided in the [training repository](https://github.com/Kiran-255666/AgenticAIEngineer).

1. Open the [training repository](https://github.com/Kiran-255666/AgenticAIEngineer) in a browser.

2. Select **Code** and then select **Download ZIP**.

3. Once the ZIP file has downloaded, open the **Downloads** folder.

4. Right-click the ZIP file and select **Extract All**.

> **Important:** Do not run the application directly from the deeply nested extracted folder in `Downloads`. The long Windows path can cause path-related problems in the VM.

5. After extracting the repository, open **PowerShell** and run these commands.

   ```powershell
   Copy-Item "C:\Users\agenticuser\Downloads\AgenticAIEngineer-main\AgenticAIEngineer-main\labfiles\Day08\lab03-agent-evaluation-foundry-results" "$env:USERPROFILE\Desktop\lab02-agent-evaluation-foundry-results" -Recurse
   ```

6. Run the following command to open the copied lab folder from your Desktop in Visual Studio Code:

   ```powershell
   code "$env:USERPROFILE\Desktop\lab03-agent-evaluation-foundry-results"
   ```

7. In Visual Studio Code, select **Terminal > New Terminal**.

8. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

9. Install the required Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

### Configure the environment

> [!TIP]
> `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME` are already prefilled. You only need to replace the `AGENT_NAME` value with the agent name you saved earlier in Notepad.

1. The lab includes a `.env` file with the configuration required by the evaluation script.

2. Use the agent name you saved in Notepad in the previous step to replace `<your_unique_prefix>-cra`.

```env
AZURE_AI_PROJECT_ENDPOINT="https://hakunamatata11.services.ai.azure.com/api/projects/hakunamatata"

AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-5.4-mini"

AGENT_NAME="<your_unique_prefix>-cra"
```

## Sign in to Azure

1. In the terminal, run:

   ```powershell
   az account show
   ```

2. If your account details are displayed, continue to the next step, [Review the lab files](#review-the-lab-files). Otherwise, run `az login` followed by `az account show` to sign in and verify your Azure account.

## Review the lab files

The lab contains the following files:

```text
lab04-agent-evaluation-foundry-results/

├── .env
├── requirements.txt
├── evaluate_agent_advanced.py
├── data/
│   └── credit_risk_test_queries.jsonl
└── results/
```

The files have the following purpose:

- **`.env`** contains the Microsoft Foundry project and agent configuration.
- **`requirements.txt`** contains the required Python packages.
- **`credit_risk_test_queries.jsonl`** contains the test queries.
- **`evaluate_agent_advanced.py`** contains the evaluation workflow.
- **`results/`** stores the local evaluation summary created by the script.

## Review the test dataset

Open:

```text
data/credit_risk_test_queries.jsonl
```

The file contains one JSON object per line.

For example:

```json
{"query": "What factors are usually considered when assessing a customer's credit risk?"}
```

The evaluation script uses the `query` field to send each test case to the Credit Risk Assessment agent.

The dataset contains questions covering different aspects of credit risk assessment.

> [!Note] 
> You can add or replace test queries with questions relevant to your Credit Risk Assessment agent. Keep the `query` field in each JSON object.

## Review the evaluation script

Open:

```text
evaluate_agent_advanced.py
```

The script performs the complete evaluation workflow.

### Connect to Microsoft Foundry

The script loads the project configuration from `.env` and creates an authenticated Microsoft Foundry client.

The Azure identity is provided through `DefaultAzureCredential`.

This allows the script to use the Azure account authenticated through Azure CLI.

### Upload the test dataset

The script uploads:

```text
data/credit_risk_test_queries.jsonl
```

to the Microsoft Foundry project as an evaluation dataset.

Each `query` is used as an input to the agent.

### Configure built-in evaluators

The evaluation uses built-in Azure AI evaluators:

- **Coherence**: Evaluates whether the response is clear and logically consistent.
- **Violence**: Evaluates the response against the configured safety criteria.
- **Task Adherence**: Evaluates whether the response follows the expected task.

The evaluators are configured directly in the evaluation script.

The configured model deployment is used by the model-based evaluators that require a judge model.

### Create and run the evaluation

The script creates an evaluation using the uploaded dataset and configured evaluators.

The evaluation target is the existing Credit Risk Assessment agent.

The script then monitors the evaluation run until it reaches a terminal state.

## Run the evaluation

1. In terminal use

   ```powershell
   python evaluate_agent_advanced.py
   ```

2. The script performs the following operations:

   1. Uploads the credit risk test dataset.
   2. Configures the built-in evaluators.
   3. Creates the evaluation.
   4. Runs the evaluation against the agent.
   5. Monitors the evaluation until it completes.
   6. Displays the Microsoft Foundry report URL.
   7. Saves a local evaluation summary.

3. When the evaluation completes, the terminal displays the evaluation status, evaluation ID, run ID, report URL, and result counts.

The local summary is saved to:

```text
results/evaluation_run_summary.json
```

A successful run displays a result similar to:

```text
Status: completed
Result counts: ResultCounts(errored=0, failed=0, passed=7, total=7, skipped=0)
```

> **Note:** The number of test cases and evaluation results depends on the dataset and evaluation run.

> **Note:** Evaluation output can vary slightly between runs because model-generated responses and evaluator results can differ.

## Review the evaluation results in Microsoft Foundry

1. Open the report URL displayed in the terminal.

2. If the URL is not available, open [Microsoft Foundry](https://ai.azure.com/).

3. Select the Microsoft Foundry project used by the lab.

4. Open **Evaluations**.

5. Select the evaluation run created by the script.

6. Review the evaluation results.

Review the following information:

- Overall evaluation status.
- Individual test case results.
- Coherence results.
- Violence safety results.
- Task Adherence results.
- Evaluator reasoning.
- Failed or weak test cases.

### Review individual test cases

Open individual test cases to compare:

- The original query.
- The agent response.
- The evaluator result.
- The evaluator reasoning.

Pay particular attention to test cases where the agent receives a low score or where an evaluator identifies a quality issue.

## Improve the agent and re-evaluate

Choose one weak or failed test case.

Review the result and determine whether the issue is related to:

- Agent instructions.
- Agent knowledge.
- Agent tools.
- Test query.
- Response quality.

Make one improvement to the agent and run the evaluation again.

Compare the new evaluation run with the previous run.

Consider whether the change improved the result without introducing problems in other test cases.

## Summary

In this exercise, you used the Azure AI Projects SDK to evaluate an existing Credit Risk Assessment agent.

You prepared a JSONL test dataset, configured built-in evaluators, ran the evaluation, and reviewed the results in Microsoft Foundry.

You also identified weak test cases and re-evaluated the agent after making improvements.