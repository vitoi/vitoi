- 👋 Hi, I’m @vitoi
- 👀 I’m interested in Python
- 🌱 I’m currently learning Django
- 💞️ I’m looking to collaborate on blog website construction
- 📫 How to reach me: vito-lee@outlook.com

<!---
vitoi/vitoi is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Test Agent

This repository includes a simple testing agent powered by OpenAI. The agent can:

1. Analyze a natural language requirement.
2. Generate a pytest script with help from the language model.
3. Execute the script and collect JSON results.
4. Summarize the report and optionally send it via email.

### Usage

Install dependencies first (requires `openai`, `pytest` and `pytest-json-report`):

```bash
pip install openai pytest pytest-json-report
```

Then run the agent:

```bash
python run_agent.py "your requirement text" --api-key YOUR_OPENAI_KEY
```

Provide SMTP parameters to email the report:

```bash
python run_agent.py "..." --api-key KEY --smtp-host smtp.example.com \
    --smtp-to user@example.com --smtp-user youruser --smtp-password yourpass
```
