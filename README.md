# Intern-Hackathon-2025

# 📬 Email-Folder AI Agent Hackathon

Welcome to the **Email-Folder AI Agent Hackathon**! 🎉 In this challenge, you’ll build an intelligent agent that reads customer emails from a folder, understands their content, extracts attachments (mostly PDFs), runs a document extractor, and produces a human-readable summary for confirmation via a simple web front-end.

---

## 🏆 Challenge Overview

Many enterprises receive dozens (or hundreds) of emails per day, each potentially containing valuable documents. Your task is to automate the end-to-end pipeline:

1. **Ingest**: Read raw `.eml` or `.msg` files from a given folder.
2. **Parse**: Extract sender, subject, body text, and all attachments.
3. **Extract**: Invoke a document-extraction API (or your own model) to pull structured content from PDFs.
4. **Summarize & Confirm**: Produce a concise summary of email context and extracted document details, ready for user confirmation on a web front-end.
5. **Deliver**: Package your solution in a GitHub repo, including a flowchart of your architecture and instructions for running locally.

---

## 🎯 What We’re Looking For

- **Correctness & Completeness**  
  - All emails in the folder are processed.  
  - Attachments are successfully passed through the extractor and parsed.  
  - Output includes both email summary and document details in JSON or HTML format.

- **Clarity of Architecture**  
  - A clear flowchart (PNG/SVG/Markdown) illustrating each pipeline stage.  
  - Well-documented README with setup & run instructions.

- **Code Quality & Modularity**  
  - Clean, modular code (Python/Node.js/Java, etc.).  
  - Proper error-handling for missing fields, corrupt PDFs, network failures.

- **Ease of Deployment**  
  - Instructions for local setup (e.g., `npm install`, `pip install -r requirements.txt`).  
  - (Optional) Dockerfile or containerized example.

- **Innovation & UX**  
  - Bonus for a lightweight web front-end (React/Flask/Express) demonstrating the confirmation UI.  
  - Interactive elements: allow user to edit extracted metadata before finalizing.

---

## 🗂️ Dataset

- A ZIP archive containing sample emails:  
  - `emails/sample1.eml`  
  - `emails/sample2.eml`  
  - …  
- Each email may include zero or more attachments (`.pdf`, `.docx`, `.jpeg`).

> **Note:** You may generate your own test emails or use any open-source email-parsing libraries (e.g., [mailparser](https://github.com/mscdex/mailparser), [Apache Tika](https://tika.apache.org/)).

---

## 📦 Deliverables

Your GitHub repo **must** contain:

1. `README.md` (this file)  
2. `flowchart.*` – A diagram (PNG/SVG/Markdown) illustrating your solution pipeline.  
3. Source code under `/src`  
4. A script or instructions to install dependencies and run the pipeline, e.g.:  
   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   pip install -r requirements.txt     # or npm install
   ./run_agent.sh                      # or npm start
