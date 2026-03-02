## Personal AI Coach – Minimal Streamlit App (Including Prompts & Instructions for use with Cursor IDE)

A minimal Streamlit application that turns OpenAI's chat models into a small **personal AI coach**, with selectable personas and a simple evaluation script.

The project is intentionally small so it is easy to read, fork, and adapt.

### Files

- **app.py**: Main Streamlit application and all application logic.
- **prompts.py**: Prompt templates and persona definitions (no application logic).
- **evaluation.py**: Simple script that runs three test cases against the prompts and prints a short report.
- **requirements.txt**: Python dependencies (streamlit, openai).
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

### 2. Download Cursor and create the project folder

1. **Download and install Cursor**  
   - Go to [cursor.com](https://cursor.com) and download Cursor for your OS (Mac or Windows).  
   - Run the installer and open Cursor when it’s ready.

2. **Create a folder named `personal_ai_coach`**  
   - On your Mac or Windows PC, create a new folder called `personal_ai_coach` (e.g. on your Desktop or in Documents).  
   - This folder will hold the project files.

3. **Open the folder in Cursor**  
   - In Cursor, go to **File → Open Folder** (Mac: `Cmd + O`; Windows: `Ctrl + K` then `Ctrl + O`).  
   - Select the `personal_ai_coach` folder you created.  
   - You’ll do the rest of the setup (venv, dependencies, running the app) inside this folder.

---

### 3. Generate the project files, then create and activate a virtual environment

#### 3a. Add your first prompt to Cursor to create the file structure

With the `personal_ai_coach` folder open in Cursor, open the AI chat (e.g. **Cursor Chat** or **Composer**) and paste the prompt below. Cursor will create the required files in this folder.

```
Create a minimal Streamlit project in this folder with these files: app.py, prompts.py, evaluation.py, requirements.txt, README.md, .gitignore.
Constraints: keep the application logic in a single file (app.py). prompts.py should only store prompt templates and persona options. evaluation.py should be a simple script that runs 3 test cases against the prompt and prints a short report.
Use OpenAI API via environment variable OPENAI_API_KEY. Do not hardcode any secrets.
Make the README include Python install notes, venv setup, pip install, and streamlit run command.
```

When Cursor is done, you should see these files in your folder: **app.py**, **prompts.py**, **evaluation.py**, **requirements.txt**, **README.md**, and **.gitignore**. You can then continue with the venv and run steps below.

#### 3b. Create and activate a virtual environment

From the project root (`personal_ai_coach`):

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Once activated, your shell prompt should show `(.venv)` or similar.

---

### 4. Install dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

---

### 5. Configure OpenAI API key

The app and evaluation script both read your OpenAI API key from the `OPENAI_API_KEY` environment variable. **Do not** hardcode secrets in the code.

This application connects to a live language model using an API key. You can create a key from:

**OpenAI Platform:** [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

If you are using an enterprise environment, you may instead use:
- Azure OpenAI
- Google Vertex AI
- Your organization's approved LLM provider

A valid API key is required to generate real responses from the model.

You do not need a ChatGPT subscription. This uses the developer API, not the ChatGPT web interface.

**Set the key in your environment:**

**macOS / Linux**

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Windows (PowerShell)**

```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

Replace `sk-your-key-here` with your actual key.

---

### 6. Run the Streamlit app

From the project root (with the virtual environment activated and `OPENAI_API_KEY` set):

```bash
streamlit run app.py
```

This will open the Personal AI Coach interface in your browser. Enter your goal (and optional constraints), choose a coach style, and click **Generate Plan**.

---

### 7. Run the evaluation script

To quickly test the prompt and personas without the UI, run:

```bash
python evaluation.py
```

This will execute three predefined test cases and print a short report containing each test name, persona, the user input, and a truncated model response.

