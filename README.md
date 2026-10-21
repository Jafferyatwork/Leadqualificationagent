# Lead Qualification AI Agent

An AI agent that chats with website visitors, collects their details, scores each lead (hot / warm / cold), and saves them automatically.

**Live demo:** _add your Streamlit link here after deploying_

## What it does
- Holds a short, friendly conversation, one question at a time
- Collects name, contact, need, budget and timeline
- Scores the lead and saves it using a tool call
- Never quotes prices or promises dates; hands off to a human when unsure

## Tech
- Python
- Claude API (Anthropic)
- Streamlit (demo interface)

## Run it locally
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"   # Windows: setx ANTHROPIC_API_KEY "your-key"

python agent.py          # terminal chat
streamlit run app.py     # browser chat
```

## Customise for a client
Edit the `SYSTEM` prompt in `agent.py` with the client's business, services and FAQs, and adjust the hot/warm/cold rules. Replace `save_lead` to send leads to Google Sheets, a CRM, email or WhatsApp.

## Files
- `agent.py`: the agent logic and tool
- `app.py`: the Streamlit chat interface
- `requirements.txt`: dependencies

Built by Jaffery.
