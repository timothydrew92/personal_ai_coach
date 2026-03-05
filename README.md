## Personal AI Coach (Minimal Streamlit Project)

This is a minimal Streamlit app that acts as a simple **personal AI coach** using the OpenAI API.  
All application logic lives in `app.py`, prompt templates and persona options live in `prompts.py`, and a small evaluation script lives in `evaluation.py`.

### Files

- `app.py` – Streamlit application and OpenAI call logic.
- `prompts.py` – Prompt templates and persona definitions (no application logic).
- `evaluation.py` – Simple script that runs 3 test cases against the prompt and prints a short report.
- `requirements.txt` – Python dependencies.
- `README.md` – This documentation.
- `.gitignore` – Basic Python and virtual environment ignores.

### Prerequisites

- **Python**: Recommended Python 3.9 or newer.
- An OpenAI API key available as the environment variable **`OPENAI_API_KEY`**.

### Create and activate a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (if you ever run this there), activation would look like:

```bash
.venv\Scripts\activate
```

### Install dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure OpenAI API key

Set the `OPENAI_API_KEY` environment variable (replace `YOUR_KEY_HERE` with your actual key):

```bash
export OPENAI_API_KEY="YOUR_KEY_HERE"
```

Optionally, you can override the default model by setting:

```bash
export OPENAI_MODEL="gpt-4o"
```

If `OPENAI_MODEL` is not set, the app defaults to `gpt-4o`.

### Run the Streamlit app

From the project root, with your virtual environment active:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the personal AI coach UI in your browser.

### Run the evaluation script

To run the three simple test cases against the prompt and print a short report:

```bash
python evaluation.py
```

Make sure `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`) are set in your environment before running this script.

