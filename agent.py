import csv
import os
import anthropic

# Reads your key from an environment variable. Never paste the key in this file.
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-sonnet-5-5"

SYSTEM = """You are the assistant for [Client Business], which offers [services].
Your job: have a friendly, short conversation to learn the visitor's name,
contact details, what they need, budget, and timeline. Ask one question at a time.
Never quote prices or promise dates. If you don't know something, say a team
member will follow up. Once you have name, contact and need, call save_lead.
Score the lead: hot = clear need, budget and wants to start soon;
warm = interested but unsure on budget or timing; cold = just browsing."""

TOOLS = [{
    "name": "save_lead",
    "description": "Save a lead once name, contact and need are collected.",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "contact": {"type": "string"},
            "need": {"type": "string"},
            "budget": {"type": "string"},
            "timeline": {"type": "string"},
            "score": {"type": "string", "enum": ["hot", "warm", "cold"]},
        },
        "required": ["name", "contact", "need", "score"],
    },
}]

FIELDS = ["name", "contact", "need", "budget", "timeline", "score"]


def save_lead(**lead):
    new_file = not os.path.exists("leads.csv")
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerow(lead)


def chat(history):
    while True:
        r = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM,
            tools=TOOLS,
            messages=history,
        )
        history.append({"role": "assistant", "content": r.content})

        if r.stop_reason != "tool_use":
            return "".join(b.text for b in r.content if b.type == "text")

        results = []
        for b in r.content:
            if b.type == "tool_use":
                save_lead(**b.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": "Lead saved.",
                })
        history.append({"role": "user", "content": results})


if __name__ == "__main__":
    history = []
    print("Lead agent ready. Type 'quit' to exit.")
    while True:
        text = input("You: ")
        if text.lower() in ("quit", "exit"):
            break
        history.append({"role": "user", "content": text})
        print("Agent:", chat(history))
