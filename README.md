CLI AI Assistant
================

A simple command-line chatbot that answers technical questions using the Google GenAI SDK.

Features
--------
- CLI prompt for questions
- Technical-only guardrail via system instruction
- Environment-based API key loading via `.env`

Requirements
------------
- Python 3.10+ (3.12 recommended)
- An API key for Google GenAI

Local setup
-----------

1) Clone and enter the project

```bash
git clone https://github.com/uttam101/CLI-AI-Assistant.git
cd CLI-AI-Assistant
```

2) Optional: create and activate a virtual environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

3) Install dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

4) Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your API key:

```
GENAI_API_KEY="REPLACE_WITH_YOUR_API_KEY"
```

5) Run the app

```bash
python3 main.py
```

Usage
-----
The app will prompt you with:

```
ask any technical question:
```

If the question is not technical, the assistant replies:

```
Sorry, I can only answer technical questions.
```

Troubleshooting
---------------
- If you see a missing API key error, verify `.env` exists and contains `GENAI_API_KEY`.
- If `python` is not found, use `python3` instead.
- If you are not using a virtual environment, ensure packages are installed in your system Python.

