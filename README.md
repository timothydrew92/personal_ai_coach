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

You need **Python 3.10 or newer** on your machine. If you’ve never installed Python, follow the steps below for your operating system.

#### Option A: macOS

1. **Check if Python is already installed**  
   Open **Terminal** (Applications → Utilities → Terminal, or press `Cmd + Space`, type `Terminal`, press Enter). Run:
   ```bash
   python3 --version
   ```
   If you see something like `Python 3.10.x` or higher, you’re done with this step. If you see “command not found” or a version below 3.10, continue.

2. **Install Python** (choose one):
   - **From python.org (recommended if you don’t use Homebrew):**  
     - Go to [python.org/downloads](https://www.python.org/downloads/).  
     - Download the latest **macOS** installer (e.g. “macOS 64-bit universal2 installer”).  
     - Run the installer and follow the prompts (you can leave the default options checked).  
     - When finished, close and reopen Terminal, then run `python3 --version` again to confirm.
   - **Using Homebrew (if you already use it):**  
     - In Terminal, run: `brew install python`  
     - Then run: `python3 --version` to confirm.

#### Option B: Windows

1. **Check if Python is already installed**  
   Open **PowerShell** (press `Win + X` and choose “Windows PowerShell”, or search for “PowerShell” in the Start menu). Run:
   ```powershell
   python --version
   ```
   If you see `Python 3.10.x` or higher, you’re done. If you see “not recognized” or a version below 3.10, continue.

2. **Install Python from python.org**  
   - Go to [python.org/downloads](https://www.python.org/downloads/).  
   - Download the latest **Windows** installer (e.g. “Windows installer (64-bit)”).  
   - Run the installer.  
   - **Important:** On the first screen, check **“Add python.exe to PATH”**, then click “Install Now” (or “Customize installation” if you prefer, but still ensure “Add Python to PATH” is enabled).  
   - When the installer finishes, close PowerShell, open a **new** PowerShell window, and run `python --version` to confirm.

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

