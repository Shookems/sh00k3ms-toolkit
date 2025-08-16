import sys, importlib

def main() -> int:
    try:
        root_main = importlib.import_module("main")  # your repo-root main.py
    except Exception as e:
        sys.stderr.write(f"[sh00k3ms] failed to import main.py: {e}\n")
        return 1
    if not hasattr(root_main, "main"):
        sys.stderr.write("[sh00k3ms] main.py must define main()\n")
        return 2
    return int(root_main.main() or 0)

if __name__ == "__main__":
    raise SystemExit(main())
