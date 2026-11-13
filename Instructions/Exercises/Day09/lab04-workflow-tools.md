---
lab:
  title: Use workflows as tools
  module: Incorporate workflows to enhance agent behavior
  description: In this lab, you will use Copilot to create an agent, create workflows, and add workflows as tools to the agent and to a topic.
  duration: 60 minutes
  level: 200
  islab: true
  primarytopics:
    - Microsoft Copilot Studio
---

# Use workflows as tools

## Scenario

In this exercise, you will:

- Create an agent
- Create workflows
- Add workflows as tools
- Use tools in the agent and in topics
- Test the agent

This exercise will take approximately **60** minutes to complete.

## What you will learn

- How workflows enable agents to perform deterministic actions
- How to configure workflows as tools
- How to use workflows in a topic

## High-level lab steps

- Create an agent using Copilot
- Create a workflow to send a message to Mail
- Add the workflow as a tool to the agent
- Create a workflow and add to a topic
  
## Prerequisites

- Have a Microsoft Entra ID account
- Have a Copilot Studio license or have signed up for a [free trial](https://go.microsoft.com/fwlink/p/?linkid=2252605).
- Have access to a Power Platform environment and a solution where you can create agents and related assets.
- Have access to Microsoft Outlook (Mail) and permission to send email messages.
- You can use:
  - the environment and **Lab Exercises** solution created in the **ILT Setup** lab, or
  - your own existing environment and solution.
- If you do not already have an environment and solution prepared, complete the steps in the **ILT Setup** lab before continuing.
  
> [!IMPORTANT]
> You may notice a new Copilot Studio experience that is currently in preview. These labs use the current Copilot Studio interface, so some steps and screenshots may not match the preview experience. To follow the lab instructions successfully, use the Classic Copilot Studio UI experience throughout these exercises.

## Key concept: Agent components and behavior

When generative orchestration is enabled, the agent can use instructions, knowledge, topics, and tools to generate responses dynamically. The agent can use tools to perform actions in external systems, retrieve data, and send messages. Tools are typically used for performing actions or retrieving external data, while topics guide structured conversational flows.

## Exercise 1 - Create an agent

In this exercise, you will create a new agent using natural language to analyze, categorize, and prioritize tasks.

### Task 1.1 – Create an agent to analyze tasks

1. Navigate to the **Copilot Studio** home page `https://copilotstudio.microsoft.com/`.

1. Make sure you are in the **Copilot Studio** classic experience. If you are not, switch to the classic experience before proceeding.

1. At the top of the page, verify that you are working in the environment you want to use for this exercise.

1. Select **Agents** in the left-hand navigation.

1. In the bottom-left of the *Start building by describing what your agent needs to do* text box, select the **Agent Settings** icon, which is displayed as a **⚙️** icon.

   ![Screenshot of the agent settings dialog.](../media/agent-settings-dialog.png)

1. Leave **English (United States)** set as the primary language for the agent.

1. In the **Solution** drop-down, select **Lab Exercises**.

1. Enter `taskagent` for the *Schema name*.

1. Select **Update**.

1. In the *Start building by describing what your agent needs to do* text box, Enter the following prompt:

   ```prompt
   You are an agent that analyzes, categorizes, and prioritizes tasks.
   ```
   
1. Select the **Send** **→** icon .

   Once your agent has been provisioned, you may proceed with configuring your agent.

1. In the agent overview page, under the Details section, select Edit.

1. Change the agent name to **`Task Agent`**.

1. Select Save.

## Exercise 2 - Create a workflow tool

In this exercise, you create a workflow that sends a message to Mail. You will add this workflow to the agent.
> [!NOTE]
> Agent responses, orchestration behavior, and tool usage may vary slightly from the screenshots shown in this lab depending on your tenant configuration and model behavior.

### Task 2.1 – Create the Send Message to Mail workflow

1. In Copilot Studio, select **Tools** in the left-hand navigation.

   ![Screenshot of Tools registry page.](../media/copilot-studio-tools-registry.png)

1. Select **+ New tool**.

1. In the **New Tool** dialog, select the **Agent flow** tile.

1. Verify that the **When an agent calls the flow** trigger and the **Respond to the agent** action have been added to the workflow.

   ![Screenshot of a new workflow.](../media/workflow-new.png)

1. Select the trigger step **When an agent calls the flow** and select **+ Add an input**.

   ![Screenshot of a new workflow.](../media/workflow-new1.png)

1. Select **Text**.

1. Enter **Task Summary** by replacing the default text **Text**, and enter **Analyzed tasks** by replacing **Please enter your input**.

   ![Screenshot of trigger properties of the flow.](../media/workflow-trigger-step.png)

1. Select **Save draft** near the upper-right of the page.

1. Select the **Overview** tab.

1. In the **Details** section, select **Edit**.

   ![Screenshot of details properties of the flow.](../media/workflow-details.png)

1. Replace the default **Flow name** value `Untitled` with `Send Summary to Mail`.

1. Replace the default **Description** text with `Send a mail with the summary of the task analysis`.

1. Select **Save**.

### Task 2.2 - Send mail action

1. Select the **Designer** tab.

1. Select the **+** icon between the two steps in the workflow to insert a new action.

1. Enter `Send an email (V2)` in the **Search** field.

1. Select the **Send an email (V2)** action.

1. In the Connection name field, enter **`OutlookConnection`**.

1. Verify that Authentication Type is set to Office 365 (sign in as user).

1. Select **Sign in**.

1. Select the account provided by your instructor.

1. If the **Confirmation required** dialog appears, select the **I have verified this request and trust the source** checkbox, then select **Allow access**.

1. **For To**, enter your email address or the account provided by your instructor.

1. **For Subject**, enter **Task Analysis Summary**.

1. In the **Body** field, enter `/`, click **Insert dynamic content**, and select **Task Summary** from the dynamic content list.

   ![Screenshot of Mail action in the workflow.](../media/workflow-teams-action11.gif)

1. Leave **Sensitivity** and **Advanced parameters** unchanged.

1. Verify that **Task Summary** appears in the **Body** field.

   ![Screenshot of Mail action in the workflow.](../media/workflow-teams-action11.png)

### Task 2.3 - Response action

1. Select the **Respond to the agent** node in the authoring canvas and select **+ Add an output**.

1. Select **Text**.

1. For *Enter a name*, enter `Message`.

1. For **Enter a value to respond with**, enter `Summary sent to mail`.

1. Select **Save draft** near the upper-right of the page.

1. Select **Publish** near the upper-right of the page.

1. In Copilot Studio, select **Tools** in the left-hand navigation to verify the workflow status is **Ready**.

### Task 2.4 - Add workflow as a tool to the agent

1. Select **Agents** from the left navigation pane.

1. Open the **Task Agent** agent by clicking it.

1. Select the **Tools** tab.

1. Select **+ Add a tool**.

1. In the **Add tool** dialog, select the **Flow** filter.

   ![Screenshot of adding a workflow as a tool.](../media/workflow-add-tool.png)

1. Select the **Send Summary to Mail** workflow.

1. Select **Add and configure**.

1. In the **Details** section, for **Description**, replace `Send Summary to Mail` by entering `Sends a summary of the completed task analysis by mail`.

1. Expand **Additional details**, then select and enter the following:

   - **When this tool may be used**: Agent may use this tool at any time
   - **Ask the end user before running**: No
   - **Credentials to use**: End user credentials
   - **Description**: `Please sign in to send mail`

1. In the **Inputs** section, for *Fill using* select **Dynamically fill with AI**.
  
   This allows the agent to determine the appropriate input value dynamically from the conversation context.

1. In the **Completion** section, for **After running**, select **Write the response with generative AI**.

   ![Screenshot of the configuration of workflow as a tool.](../media/workflow-tool-configuration.png)

1. Select **Save**.

### Task 2.5 - Update agent instructions

> [!IMPORTANT]
> The instructions that Copilot generates when it creates an agent vary, and they're often long and general. Those instructions can cause the agent to answer from knowledge or ask the user for a list of tasks instead of calling your topics and tools. In this task, you replace the generated instructions with a specific set of instructions so that the agent behaves predictably in the remaining exercises.

1. Select the **Overview** tab.

2. In the **Instructions** section, select **Edit**.

3. Select all of the existing text in the **Instructions** box and delete it.

4. Enter the following instructions.

   ```prompt
   # Purpose

   The purpose of this agent is to analyze, categorize, and prioritize tasks, and to send a summary of the analysis by mail.

   # General guidelines

   - Maintain a professional and supportive tone.
   - Always use the topics and tools listed below. Don't answer from your own knowledge.

   # Skills

   - Use the <Send Summary to Mail> tool to send a summary of the task analysis by mail.

   # Step-by-step instructions

   1. Analyze tasks
      - Categorize and prioritize the tasks that the user provides.
      - Determine a recommended execution order.
      - Create a clear and structured task analysis summary.

   2. Send the results
      - Use the <Send Summary to Mail> tool when the task analysis is complete.
   ```

5. In the **Skills** and **Send the results** sections, locate the placeholder `<Send Summary to Mail>` and delete it. Type `/` and select the **Send Summary to Mail** tool from the list to insert it as a tool reference.

   ![Screenshot of referencing the workflow tool in the agent instructions.](../media/workflow-add-tool-to-instructions111.gif)

6. Select **Save**.

### Task 2.6 - Test the workflow tool in the agent

1. Select the **Test** icon in the upper-right of the page to open the testing pane.

1. In the **Test** pane, select the ellipsis (**...**) next to the variables **{x}** icon, and toggle **Show activity map when testing** to **On** and **Track between topics** to **Off**.

   ![Show activity map.](../media/show-activity-map1.png)

1. At the top of the **Test** pane, select the **Start new test session** icon **+**.

1. When the **Conversation Start** message appears, your agent will start a conversation. In response, let's try to trigger the topic that you've created:

   `Analyze this list of tasks 1. Build an agent, 2. Test an agent, 3. Deploy an agent`

1. If prompted to connect to Office 365 Outlook, select **Allow**.

   ![Screenshot of the workflow tool used when testing the agent.](../media/workflow-test-agent-tool.png)

1. In a new browser tab, navigate to `https://outlook.office.com/mail` and sign in if prompted.

1. Open the inbox of the email address you entered earlier in the workflow and verify the task analysis summary was received in the mail.

   ![Screenshot of the message in Mail.](../media/workflow-test-agent-mail.png)

> [!NOTE] 
>
> The formatting of the email may vary. **Focus on verifying that the workflow successfully sent the task analysis summary to the specified email address** .

## Exercise 3 - Create a workflow tool that analyzes an Excel file in a topic

In this exercise, you will use Copilot to create a topic from a description, create a workflow tool that analyzes the tasks in an Excel file, and call the tool from a topic.

### Task 3.1 - Create an Excel file

> [!NOTE]
>
> If you encounter any issues creating the spreadsheet, you can download a copy from the following link: [Download the file](https://github.com/Kiran-255666/AccelerateAgenticAI/blob/main/labfiles/Operations%20tasks.xlsx).

1. In Copilot Studio, select the **App launcher** icon in the upper-left corner, then select **OneDrive**.

   ![Screenshot of App Launcher.](../media/copilot-studio-app-launcher.png)

1. If prompted, skip any welcome messages.

1. Select **+ Create or upload**.

1. Select **Excel workbook**.

   ![Screenshot of creating a file in OneDrive.](../media/onedrive-create.png)

1. In the upper-left of the **Excel workbook**, rename the file by selecting **Book** and entering `Operations tasks`.

   ![Screenshot of renaming a file in OneDrive.](../media/onedrive-rename.png)

1. Create the following columns in the first row:

   - `Reference`
   - `Title`
   - `Description`
   - `Requested by`
   - `Priority`
   - `Status`

1. In the second row, enter for the first task:

   - `OPS-001`
   - `Server Patch Update`
   - `Apply monthly security patches to production servers`
   - `IT Operations`
   - `High`
   - `Open`

1. In the third row, enter for the second task:

   - `OPS-002`
   - `Backup Validation`
   - `Verify nightly backups completed successfully`
   - `Infrastructure Team`
   - `Medium`
   - `In Progress`

1. In the fourth row, enter for the third task:

   - `OPS-003`
   - `Access Review`
   - `Review and remove inactive user accounts`
   - `Security Team`
   - `High`
   - `Open`

1. In the fifth row, enter for the fourth task:

   - `OPS-004`
   - `Incident Report`
   - `Document root cause for recent service outage`
   - `Service Desk`
   - `Medium`
   - `Completed`

   ![Screenshot of tasks in a file in OneDrive.](../media/onedrive-tasks.png)

1. Select the rows and columns containing data (A1:F5), and in the toolbar select the **Insert** tab, and select **Table**, check the box **My table has headers**, then select **OK**.

1. Select the **Table Design** tab and in the upper-left change the name of the table from *Table1* to **`Tasks`**.

   ![Screenshot of tasks as a table in a file in OneDrive.](../media/onedrive-tasks-table.png)

1. Close the browser tab containing the Excel workbook.

1. In OneDrive, select **My files** and verify that the Operations tasks Excel workbook is listed.

1. Close the OneDrive browser tab.

### Task 3.2 – Create the Analyze Excel tasks workflow

1. In Copilot Studio, in the left-hand navigation, select **Tools**.

1. Select **+ New tool**.

1. In the **New tool** dialog, select the **Agent flow** tile.

1. Verify that the **When an agent calls the flow** trigger and the **Respond to the agent** action have been added to the workflow.

1. Select the trigger step **When an agent calls the flow** and select **+ Add an input**.

1. Select **Text**.

1. Replace the default **Input** name with **`Priority`** and replace **Please enter your input** with **`Priority of Tasks`**.

1. Select **Save draft** near the upper-right of the page.

1. Select the **Overview** tab.

1. In the **Details** section, select **Edit**.

1. In the **Details** pane, update **Flow name** to `Get Task List`.

1. For **Details** pane, update **Description** to `Retrieve a list of tasks with a matching priority`.

1. Select **Save**.

1. Select the **Designer** tab.

1. Select the **+** icon between the two steps in the workflow to insert a new action.

1. In the **Search** field, enter `List rows present in a table`.

2. Select the **List rows present in a table** action under **Excel Online (Business)**.

1. Select **Sign in** to create a connection.

1. In the **Sign into your account** dialog, select the account you are using for this lab environment.

1. For **Location** select **OneDrive for Business**.

1. For **Document library** select **OneDrive**.

1. For **File** browse and select the **Operations tasks** workbook.

1. For **Table** select **Tasks**.

   ![Screenshot of Excel action in the workflow.](../media/onedrive-action.png)

1. Select **Show all**.

1. For **Filter query**, enter `Priority eq ''`.

1. Move the cursor between the two single quotes and use **Dynamic content** to insert the **Priority** input parameter.

   ![Screenshot of Excel filter in the workflow.](../media/onedrive-action-filter.gif)

1. Select the **Respond to the agent** node in the authoring canvas and select **+ Add an output**.

1. Select **Text**.

1. For *Enter a name*, enter `Task list`.

1. For *Enter a value to respond with*, select the field, and then select the **Expression** (**fx**) option. Enter the following expression to convert the returned rows into text that matches the **Text** output type, and then select **Add**:

   `string(outputs('List_rows_present_in_a_table')?['body/value'])`
   
   ![Screenshot of Excel filter in the workflow.](../media/onedrive-action-filter2.gif)

1. Select **Save draft** near the upper-right of the page.

1. Select **Publish** near the upper-right of the page.

1. Select **Tools** in the left-hand navigation to verify the workflow status is **Ready**.

### Task 3.3 – Add a topic to the agent

1. Select **Agents** from the left navigation pane.

1. Open the **Task Agent** agent.

1. Select the **Topics** tab.

1. Select **+ Add a topic** and select **Add from description with Copilot**. A new dialog window appears.

1. In the **Name your topic** text box, enter **`Priority Tasks`**.

1. In the **Create a topic to...** text box, enter `Ask the user to choose a priority from a list containing High, Medium, and Low`.

1. Select **Create**.

   ![Screenshot of topic with a question node.](../media/topic-question-node.png)

1. Select the **Priority** variable in the bottom of the question node to open **Variables properties**.

1. Under **Usage** select **Global (any topic can access)**.

   ![Screenshot of global variable for a question node.](../media/variable-global.png)

1. Select **Save**.

### Task 3.4 - Add workflow as a tool

1. Select **Agents** from the left navigation pane.

1. Open the **Task Agent** agent.

1. Select the **Tools** tab.

1. Select **+ Add a tool**.

1. In the **Add tool** dialog, select the **Flow** filter.

1. Select the **Get Task List** workflow.

1. Select **Add and configure**.

1. In the **Details** section, for **Description** enter `Retrieves a list of tasks for a specified priority`.

1. Expand **Additional details** and select or enter the following:

   - **When this tool may be used**: Only when referenced by topics or agents
   - **Ask the end user before running**: No
   - **Credentials to use**: End user credentials
   - **Description**: *`Please sign in to retrieve tasks`*

1. In the **Inputs** section, for **Fill using** select **Custom value** and select the **Priority** global variable.

   ![Screenshot of the inputs of workflow as a tool.](../media/workflow-tool-inputs.png)

1. Select the ellipsis (**...**) next to the **Global.Priority** value, select **Formula** (**fx**), enter `Text(Global.Priority)`, and then select **Insert**. The **Priority** question stores a choice value, and the workflow requires text, so this formula converts the value and prevents a type mismatch error.

1. In the **Completion** section, for **After running**, select **Write the response with generative AI**.

1. Select **Save**.

### Task 3.5 - Add workflow tool to the topic

1. Select the **Topics** tab.

1. Select the **Priority Tasks** topic.

1. Under the **Question** node, select the **+** icon, select **Add a tool**, select the **Tool** tab, and then select the **Get Task List** tool.

   ![Screenshot of adding a workflow as a tool to a topic.](../media/topic-add-tool.png)

1. Select **Save**.

### Task 3.6 - Update agent instructions with the topic

1. Select the **Overview** tab.

1. In the **Instructions** section, select **Edit**.

1. In the *# Skills* section, add a new line, enter `- Use the `, type `/`, select the **Priority Tasks** topic, and then enter ` topic to get the task list.`

1. In the *# Step-by-step instructions* section, under **1. Analyze tasks**, add a new line, enter `- Use the `, type `/`, select the **Priority Tasks** topic, and then enter ` topic to get the task list.`

1. Select **Save**.

### Task 3.7 - Test the workflow tools

1. Select the **Test** icon in the upper-right of the page to open the testing pane.

1. In the **Test** pane, select the ellipsis (**...**) next to the variables **{x}** icon, and toggle **Show activity map when testing** to **Off** and **Track between topics** to **On**.

1. At the top of the **Test** pane, select the **Start new test session** icon **+**.

1. When the **Conversation Start** message appears, your agent will start a conversation. In response, let's try to trigger the topic that you've created:

   `Analyze the task list`

1. The **Priority Tasks** topic will be shown.

   > [!NOTE]
   > If the agent answers without opening the **Priority Tasks** topic, verify on the **Overview** tab that the agent instructions reference the **Priority Tasks** topic and the **Send Summary to Mail** tool as inserted references, and then start a new test session.

1. Select **Medium**.

1. If prompted to connect to **Excel Online (Business)**, select **Allow**.

1. The **test** pane should contain two tasks.

   ![Screenshot of the workflow tool used when testing the agent.](../media/workflow-test-topic-tool.png)

1. In a new browser tab, navigate to `https://outlook.office.com/mail` and sign in if prompted.

1. Open the inbox of the email address you entered earlier and review the mail containing the two tasks.

   ![Screenshot of the message in Mail.](../media/workflow-test-topic-teams.png)

## Summary

In this lab, you created workflow tools that are called by the agent using generative AI and from a topic.