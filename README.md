# Sentinels of Truth

Sentinels of Truth is a lightweight multi-agent fact-checking prototype built with Streamlit, LangGraph, Tavily search, and SQLite. A user submits a claim, the app gathers web evidence, assigns a verification status, and decides whether the result should be stored, discarded, or flagged for review.

## Overview

This project is designed as a simple end-to-end fact-checking workflow:

1. A user enters a claim in the Streamlit interface.
2. Agent Alpha searches the web for supporting evidence.
3. The system applies a keyword-based heuristic to label the claim.
4. Agent Beta checks the local SQLite archive and decides what to do next.

## Features

- Streamlit UI for entering and verifying claims
- LangGraph workflow with two agent steps
- Tavily-powered web search for evidence gathering
- SQLite archive for storing verified claims
- Duplicate and contradiction detection before insert

## Architecture

```text
User Claim
   |
   v
Streamlit UI (app.py)
   |
   v
LangGraph Workflow (graph.py)
   |
   +--> Agent Alpha / Investigator (agents.py)
   |      - searches the web
   |      - labels claim as VERIFIED or FAKE
   |
   +--> Agent Beta / Archivist (agents.py)
          - checks existing records
          - returns INSERT, DISCARD, or FLAG_REVIEW
          - stores verified claims in SQLite
```

## Project Structure

```text
sentinels_of_truth/
├── app.py           # Streamlit interface
├── graph.py         # LangGraph workflow definition
├── agents.py        # Agent logic and decision rules
├── tools.py         # Tavily search integration
├── database.py      # SQLite schema initialization
├── requirements.txt # Python dependencies
├── README.md
└── facts.db         # Local SQLite database
```

## Prerequisites

- Python 3.10 or newer
- A Tavily API key

## Installation

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If the repository already contains a `venv`, you can activate that instead of creating a new one.

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Initialize the database

Run this once before starting the app on a fresh setup:

```powershell
python -c "from database import init_db; init_db()"
```

This creates the `facts` table used by the archivist agent.

## Running the App

```powershell
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## How the Workflow Works

### Agent Alpha: Investigator

Defined in `agents.py`, Agent Alpha:

- receives the claim
- calls Tavily search through `tools.py`
- combines the top search snippets into evidence text
- assigns `VERIFIED` or `FAKE` using a keyword heuristic

### Agent Beta: Archivist

Also defined in `agents.py`, Agent Beta:

- checks whether the claim already exists in `facts.db`
- returns `DISCARD` for an exact duplicate with the same status
- returns `FLAG_REVIEW` if the same claim appears with a different status
- inserts only new `VERIFIED` claims into the database

## Output Meanings

### Verification Status

- `VERIFIED`: the heuristic found supporting signals in the evidence
- `FAKE`: the heuristic found contradicting signals, insufficient support, or a search failure

### Decision

- `INSERT`: a new verified claim was stored
- `DISCARD`: the claim was already present with the same status
- `FLAG_REVIEW`: the claim needs manual attention

## Example Use Case

Enter a claim such as:

```text
India won ICC Champions Trophy 2025
```

The app will:

1. search for recent supporting sources
2. show the gathered evidence
3. label the claim
4. decide whether it should be stored or reviewed

## Current Limitations

- Claim verification is heuristic-based, not a robust fact-checking model.
- `FAKE` currently covers both false claims and claims with weak or missing evidence.
- Search evidence is stored as plain text snippets without source scoring.
- Database initialization is manual on a fresh setup.
- `langchain` and `langchain-openai` are installed, but the current flow does not directly use an LLM-driven reasoning step.

## Future Improvements

- Add confidence scores and source-level citations
- Distinguish false claims from unsupported claims
- Auto-initialize the database at app startup
- Add a manual review queue for flagged claims
- Replace keyword heuristics with stronger claim verification logic

## Tech Stack

- Streamlit
- LangGraph
- Tavily
- SQLite
- Python

## License

This project currently has no license file. Add a license before distributing it publicly.
