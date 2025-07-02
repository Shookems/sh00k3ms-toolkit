import os
from datetime import datetime

results = []
loot_keywords = ["password", "token", "secret", "key", "auth", "credential"]

def index_loot_file(filepath):
    info = {
        "file": filepath,
        "size_bytes": os.path.getsize(filepath),
        "modified": datetime.utcfromtimestamp(os.path.getmtime(filepath)).isoformat(),
        "created": datetime.utcfromtimestamp(os.path.getctime(filepath)).isoformat(),
        "keywords_found": []
    }

    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read().lower()
            for keyword in loot_keywords:
                if keyword in content:
                    info["keywords_found"].append(keyword)
    except Exception as e:
        info["error"] = str(e)

    return info

def run_loot_indexer():
    print("\n--- Loot Indexer ---")
    path = input("Enter the directory containing loot to index: ").strip()

    if not os.path.isdir(path):
        print("[!] Invalid directory.")
        return

    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                result = index_loot_file(full_path)
                results.append(result)
            except Exception as e:
                results.append({"file": full_path, "error": str(e)})

    with open("loot_index_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Loot index complete. Results saved to loot_index_results.txt.")

