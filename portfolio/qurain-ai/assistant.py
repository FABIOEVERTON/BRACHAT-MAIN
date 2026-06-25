import json, os, sys
from datetime import datetime, timedelta

SYSTEM_PROMPT = """You are BrightSmile Dental Assistant, a WhatsApp AI assistant for Bright Smile Dental Clinic in Salmiya, Kuwait.

CLINIC INFO:
- Name: Bright Smile Dental
- Location: Salmiya, Kuwait
- Hours: Saturday-Thursday 9:00-21:00, closed Friday
- Services & Prices: Check-up 15 KWD, Cleaning 25 KWD, Whitening 80 KWD, Filling from 30 KWD
- Phone: +965 0000 0000
- Address: Block 3, Street 102, Building 7, Salmiya

RULES:
1. Answer FAQs about hours, prices, services, location clearly and concisely.
2. BOOKING: If patient wants to book, collect their FULL NAME and PREFERRED DATE/TIME. Confirm availability (Sat-Thu 9-21). Save booking data and confirm.
3. MEDICAL ADVICE: NEVER give medical advice. Say: "I'm an assistant and cannot provide medical advice. A dentist from our team will contact you shortly."
4. EMERGENCIES: If patient mentions severe pain, bleeding, swelling, or trauma → respond: "This sounds urgent. Please call us immediately at +965 0000 0000 or go to the nearest emergency room." and flag as EMERGENCY.
5. LANGUAGE: Detect language and reply in the same language (Arabic or English).
6. Keep responses brief and friendly.

OUTPUT FORMAT: Respond with JSON:
{"response": "your reply to patient", "action": "faq|booking|medical_handoff|emergency|other", "booking": null or {"name": "...", "time": "..."}}
"""

BOOKINGS_FILE = "bookings.json"

def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE) as f: return json.load(f)
    return []

def save_booking(name, time_slot):
    bookings = load_bookings()
    bookings.append({"name": name, "time": time_slot, "created": datetime.now().isoformat()})
    with open(BOOKINGS_FILE, "w") as f: json.dump(bookings, f, indent=2)
    return bookings

def llm_respond(message, history=None):
    """Calls an LLM (OpenAI-compatible API). Replace URL/key as needed."""
    import requests
    api_key = os.environ.get("OPENAI_API_KEY", "")
    endpoint = os.environ.get("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for h in history: messages.append(h)
    messages.append({"role": "user", "content": message})
    try:
        resp = requests.post(endpoint, json={"model": model, "messages": messages, "temperature": 0.1}, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        content = resp.json()["choices"][0]["message"]["content"]
        content = content.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(content)
    except Exception as e:
        return {"response": f"Error: {e}", "action": "other", "booking": None}

def handle_message(message, history=None):
    result = llm_respond(message, history)
    if result.get("action") == "booking" and result.get("booking"):
        b = result["booking"]
        save_booking(b["name"], b["time"])
    return result

def show_help():
    print("Available commands:")
    print("  <your message>  - Chat with the assistant")
    print("  /test           - Run automated test cases")
    print("  /cost           - Show cost estimate for ~1000 chats")
    print("  /prompt         - Show system prompt")
    print("  /bookings       - Show saved bookings")
    print("  /quit           - Exit")

def run_tests():
    tests = [
        ("Normal booking", "I want to book an appointment for tomorrow at 10am. My name is Ahmed."),
        ("Typo tolerance", "I wanna make a apointment for checkup pls. Name: Sara"),
        ("Arabic", "أريد حجز موعد يوم السبت الساعة 11 صباحاً. اسمي محمد"),
        ("Medical advice refusal", "My tooth hurts, what medicine should I take?"),
        ("Emergency escalation", "I have severe pain and bleeding after a fall"),
        ("FAQ hours", "What are your working hours?"),
        ("FAQ price", "How much is teeth cleaning?"),
    ]
    results = []
    for label, msg in tests:
        print(f"\n--- {label} ---")
        print(f"  User: {msg}")
        r = handle_message(msg)
        print(f"  Assistant [{r.get('action')}]: {r.get('response')[:120]}")
        results.append({"test": label, "input": msg, "output": r})
    print(f"\n{'='*50}")
    print(f"Tests completed: {len(tests)}")
    print(f"Bookings saved: {len(load_bookings())}")
    return results

def cost_estimate():
    return {
        "llm": {"model": "gpt-4o-mini", "cost_per_1k_input": 0.00015, "cost_per_1k_output": 0.0006, "avg_input_tokens": 300, "avg_output_tokens": 100, "monthly_input": 450000, "monthly_output": 150000, "llm_cost_monthly": 0.0675 + 0.09},
        "hosting": {"platform": "Render/Railway free tier", "cost": 0},
        "total_monthly": 0.16,
        "note": "~1000 chats/month. LLM costs ~$0.16. Hosting free on Render/Railway. With n8n self-hosted: $0 additional."
    }

def main():
    print("="*50)
    print("  BrightSmile Dental WhatsApp Assistant")
    print("  Qurain AI Technical Challenge")
    print("="*50)
    history = []
    show_help()
    while True:
        msg = input("\n> ").strip()
        if not msg: continue
        if msg == "/quit": break
        if msg == "/help": show_help()
        elif msg == "/test": run_tests()
        elif msg == "/cost": print(json.dumps(cost_estimate(), indent=2))
        elif msg == "/prompt": print(SYSTEM_PROMPT)
        elif msg == "/bookings": print(json.dumps(load_bookings(), indent=2))
        else:
            r = handle_message(msg, history)
            print(f"\n[{r.get('action')}] {r.get('response')}")
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": r.get("response", "")})

if __name__ == "__main__":
    main()
