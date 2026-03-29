# SQL Agent

Ask questions about your database in plain English and get answers back — no SQL needed.

## What it does

You type a question, the agent figures out the SQL, runs it, and gives you the answer.

## Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd sql-react
```

### 2. Install dependencies

This project uses `uv` for package management.

```bash
pip install uv
uv sync
```

### 3. Add your environment variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key (or any other)
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
```

### 4. Run

```bash
uv run main.py
```

Then type your question when prompted.
