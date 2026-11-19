# **Capstone Project: AI-Powered Legal Document Review System**

## **1. Project Statement**

Create a multi-agent AI-powered legal document review system that analyzes legal documents, extracts important clauses, identifies potential compliance issues, and generates structured review reports.

The system should use Retrieval-Augmented Generation (RAG) to retrieve relevant legal rules and reference documents to support its analysis and provide grounded explanations.

## **2. Technical Requirements**

Use the **existing Microsoft Foundry project and its already-deployed model**. Create and configure the required agents and workflows within the same project.

Use Python for application development and a simple vector-based knowledge base for document retrieval.

### **Agent 1: Document Analysis Agent**

- Accept legal documents in PDF or TXT format.
- Extract and process document text.
- Identify document type and important information.
- Extract key legal clauses, including:
  - Confidentiality.
  - Termination.
  - Indemnification.
  - Liability.
  - Payment Terms.
  - Dispute Resolution.
  - Governing Law.
- Identify missing, unclear, or potentially problematic clauses.
- Generate a structured document summary.

### **Agent 2: Legal Compliance Agent**

- Use sample legal rules, regulations, and reference documents as the knowledge source.
- Implement Retrieval-Augmented Generation (RAG) to retrieve relevant information.
- Compare extracted clauses against the retrieved legal references.
- Identify potential compliance issues and risks.
- Provide supporting explanations and references to the retrieved documents.
- Highlight issues that require further human review.

### **Multi-Agent Workflow**

Create a multi-agent workflow that:

1. Accepts a legal document as input.
2. Sends the document to the Document Analysis Agent.
3. Extracts important clauses and document information.
4. Sends the extracted clauses to the Legal Compliance Agent.
5. Retrieves relevant legal references using RAG.
6. Evaluates the clauses against the retrieved information.
7. Combines the outputs from both agents.
8. Generates a consolidated legal document review report containing:
   - Document overview.
   - Extracted legal clauses.
   - Missing or potentially problematic clauses.
   - Retrieved legal references.
   - Identified compliance issues and risks.
   - Supporting explanations.
   - Recommended areas for further review.
   - Final review summary.

### **Agent Orchestration**

- Use Microsoft Agent Framework to coordinate the agents.
- Implement a straightforward sequential workflow.
- Pass outputs between agents using structured data.
- Maintain the document context throughout the review process.
- Handle basic errors during document processing and agent execution.

## **3. Deliverables**

**Complete Project Package:** A complete project package containing:

- Complete source code (excluding the virtual environment and `.env` file).
- Sample legal documents (PDF or TXT).
- Sample legal rules and reference documents for the RAG knowledge base.
- RAG implementation and document retrieval functionality.
- Agent configurations and orchestration workflow.
- README file with project setup instructions and usage details.
- PowerPoint presentation covering:
  - Project overview.
  - System architecture.
  - Agent responsibilities.
  - RAG implementation.
  - Multi-agent workflow.
  - Expected system outputs.
- Screenshots of the working application showing:
  - Legal document upload.
  - Extracted document content and clauses.
  - Retrieved legal references.
  - Identified compliance issues.
  - Final legal document review report.

## **4. Project Folder Structure and Naming Convention**

Before creating the ZIP file, organize all deliverables inside a folder named `agenticuser99`. Replace `99` with your assigned number.

**Example folder structure:** Follow the project template:

https://github.com/UnDerl4Y/capstone-project-template

The structure can be adapted to your actual implementation.

**Recommended folder structure:**

```text
agenticuser99/
│
├── agents/
│   ├── document_analysis_agent.py
│   └── legal_compliance_agent.py
│
├── rag/
│   ├── document_loader.py
│   ├── embeddings.py
│   └── retrieval.py
│
├── orchestration/
│   └── workflow.py
│
├── data/
│   ├── sample_legal_documents/
│   └── legal_references/
│
├── app/
│   └── main.py
│
├── screenshots/
│
├── presentation/
│   └── project_presentation.pptx
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

**Important instructions:**

1. Exclude the virtual environment (`venv`, `.venv`) and actual `.env` file.
2. Keep `.env.example` with placeholder values only. Do not include API keys, passwords, or other secrets.
3. Ensure all source code, sample documents, RAG resources, presentation, README, and screenshots are inside the `agenticuser99` folder.
4. Compress the entire `agenticuser99` folder into a ZIP file named `agenticuser99.zip`.
5. Keep `agenticuser99` as the root folder inside the ZIP file.
6. Upload the ZIP file and PowerPoint presentation to the designated public Google Drive folder.
7. Ensure the Google Drive folder has the required public access permissions.

**Example:** If your assigned username is `agenticuser5`, your folder must be named `agenticuser5` and your ZIP file must be named `agenticuser5.zip`.

## **5. Submission Checklist**

- Document Analysis Agent implemented and tested.
- Legal Compliance Agent implemented and tested.
- RAG implemented with sample legal reference documents.
- Document retrieval and clause comparison working.
- Multi-agent workflow implemented using Microsoft Agent Framework.
- Existing Microsoft Foundry project and deployed model integrated.
- Legal documents successfully processed.
- Compliance issues identified with supporting references.
- Final legal document review reports generated.
- Complete source code and sample data included.
- README included.
- PowerPoint presentation included.
- Required application screenshots included.
- ZIP folder and filename follow the assigned username convention.
- ZIP file uploaded to the designated public Google Drive folder.

**Note:** Video demonstration is optional (1–2 minutes).
