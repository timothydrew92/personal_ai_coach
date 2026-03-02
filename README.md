## Personal AI Coach – Minimal Streamlit App

A minimal Streamlit application that turns OpenAI's chat models into a small **personal AI coach**, with selectable personas and a simple evaluation script.

The project is intentionally small so it is easy to read, fork, and adapt.

### Files

- **app.py**: Main Streamlit application and all application logic.
- **prompts.py**: Prompt templates and persona definitions (no application logic).
- **evaluation.py**: Simple script that runs three test cases against the prompts and prints a short report.
- **requirements.txt**: Python dependencies.
- **.gitignore**: Ignore rules for Python / virtualenv / local files.

---

## Setup

### 1. Install Python

- **Recommended**: Python 3.10 or newer.
- On macOS, you can install via Homebrew:

```bash
brew install python
```

Verify the version:

```bash
python3 --version
```

---

## Create and activate a virtual environment

From the project root (`personal_ai_coach`):

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Once activated, your shell prompt should show `(.venv)` or similar.

---

## Install dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configure OpenAI API key

The app and evaluation script both read your OpenAI API key from the `OPENAI_API_KEY` environment variable. **Do not** hardcode secrets in the code.

### macOS / Linux

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

Replace `sk-your-key-here` with your actual key.

---

## Run the Streamlit app

From the project root (with the virtual environment activated and `OPENAI_API_KEY` set):

```bash
streamlit run app.py
```

This will open the Personal AI Coach interface in your browser. Choose a persona, enter your question or goal, and click **"Get coaching"**.

---

## Run the evaluation script

To quickly test the prompt and personas without the UI, run:

```bash
python evaluation.py
```

This will execute three predefined test cases and print a short report containing each test name, persona, the user input, and a truncated model response.

