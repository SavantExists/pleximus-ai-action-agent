# Pleximus AI Action Agent

An autonomous, tool-calling AI agent built for the Pleximus Inc. AI Hackathon. Driven by **Gemini 3.6 Flash**, the agent translates natural language instructions into concrete real-world execution by invoking local tools and external REST APIs.

---

## Key Features & Tool Suite

The agent includes all 3 core functional tools plus an integrated extension tool:

* **🧮 Calculator (`calculate`)**: Evaluates mathematical expressions locally (addition, multiplication, complex numeric parsing).


* **🌤️ Weather Lookup (`get_weather`)**: Fetches live current weather conditions and metadata for any city.


* **🔤 Text Utility (`text_utility`)**: Operates local string transformations, including word counts, character counts, uppercase, lowercase, and text reversing.


* **𒒱 Currency Converter (`convert_currency`)** *(Extension Tool)*: Fetches live foreign exchange rates to convert values between global currencies (e.g., USD to INR).



---

## System Architecture

```text
User Input ──► Gemini 3.6 Flash (Function Calling) ──► Tool Execution Engine ──► Final Natural Language Response

```

* **Parallel Action Execution**: If a user submits multiple distinct requests in a single prompt (e.g., *"Check the weather in Mumbai and convert 100 USD to INR"*), the agent identifies, invokes, and aggregates results from multiple tools simultaneously before composing its final reply.


* **Graceful Exception Handling**: Built-in try-catch wrappers intercept API connection issues or execution failures, passing execution status back to the LLM without crashing the chat session.



---

## Directory Structure

```text
AI-Hackathon/
├── agent.py              # Main Agent logic, Gemini schema declarations & tool dispatcher
├── main.py               # CLI interactive loop entry point
├── test_tools.py         # Verification suite for individual tool functions
├── requirements.txt      # Python library dependencies
├── frontend/             # Visual Command Center UI (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── app.js
└── tools/                # Execution modules for tools
    ├── calculator.py
    ├── weather.py
    ├── text_utils.py
    └── currency.py

```

---

## Quickstart & Local Setup

### 1. Prerequisites

Ensure **Python 3.10+** is installed on your system.

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd AI-Hackathon
pip install -r requirements.txt

```

### 3. Environment Variables

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here

```

### 4. Running the Agent

**CLI Interface:**
Run the interactive console agent:

```bash
python main.py

```

**Testing Tools Directly:**
Run unit tests across all integrated tools:

```bash
python test_tools.py

```

**Frontend Command Center:**
Open `frontend/index.html` directly in any web browser to view the Command Center user interface.

---

## Judging Checklist Evaluation

* **Tool Selection Precision**: Configured via Gemini's native function calling schema to ensure deterministic execution.


* **Multi-Intent Handling**: System instructions force execution of all relevant actions before generating output.


* **Error Resilience**: Explicit failure reporting handles API timeouts, bad input strings, or unknown tool calls gracefully.
