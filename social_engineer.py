import random
from datetime import datetime

results = []

pretexts = {
    "sms": [
        "Your package is delayed. Please verify delivery info: {link}",
        "We've detected suspicious login activity. Reset your password: {link}",
        "You have an unpaid toll. Pay now to avoid fees: {link}",
        "Claim your reward before it expires: {link}"
    ],
    "voice": [
        "Hi, this is IT support. We need you to verify your credentials for a scheduled update.",
        "This is the security desk. We've noticed unusual account activity and require urgent confirmation.",
        "Hey, I’m calling from HR. We need to validate some payroll details before processing."
    ]
}

def generate_pretext(method, link=None):
    template = random.choice(pretexts.get(method, []))
    return template.replace("{link}", link) if link and "{link}" in template else template

def run_social_engineer():
    print("\n--- Social Engineering Toolkit ---")
    sms_link = input("Enter phishing link to embed in SMS (e.g., http://short.link/alert): ").strip()
    sms_msg = generate_pretext("sms", sms_link)
    voice_script = generate_pretext("voice")

    results.append({
        "type": "SMS Phish",
        "message": sms_msg,
        "link": sms_link,
        "timestamp": datetime.utcnow().isoformat()
    })

    results.append({
        "type": "Voice Pretext",
        "script": voice_script,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open("social_engineer_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Social engineering pretexts saved to social_engineer_results.txt.")

