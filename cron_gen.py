from cron_descriptor import get_description

def english_to_cron(phrase):
    mappings = {
        "every minute": "* * * * *",
        "every hour": "0 * * * *",
        "every day at 6am": "0 6 * * *",
        "every monday at 9am": "0 9 * * 1",
        "every sunday at midnight": "0 0 * * 0",
    }
    
    cleaned = phrase.strip().lower()
    return mappings.get(cleaned, None)

def run_cron_gen():
    print("Launching cron job generator...")
    # your original script logic here

def main():
    print("Welcome to the Cron Job Generator!\n")
    phrase = input("Enter a schedule (e.g. 'every day at 6am'): ")

    cron_expr = english_to_cron(phrase)
    if cron_expr:
        print(f"\n✅ Cron Expression: `{cron_expr}`")
        print(f"🧠 Description: {get_description(cron_expr)}")
    else:
        print("\n⚠️ Sorry, I don't understand that schedule yet.")
        print("Try one of these:\n  - every minute\n  - every hour\n  - every day at 6am\n  - every monday at 9am\n  - every sunday at midnight")

if __name__ == "__main__":
    main()

