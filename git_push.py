import subprocess
import argparse

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip()

def get_commit_message(cli_msg=None):
    if cli_msg:
        return cli_msg
    msg = input("💬 Enter a commit message (leave blank to auto-generate): ").strip()
    return msg or "Auto-commit from sh00k3ms toolkit"

def main():
    parser = argparse.ArgumentParser(description="Git push helper for Sh00k3ms Toolkit")
    parser.add_argument("-m", "--message", help="Commit message")
    args = parser.parse_args()

    print("📦 Checking for changes...")
    stdout, stderr = run_cmd("git status --short")
    if not stdout:
        print("✅ No changes to commit.")
        return

    print("📝 You have the following changes:\n")
    print(stdout)

    message = get_commit_message(args.message)

    print("\n📂 Staging all changes...")
    run_cmd("git add .")

    print(f"🔐 Committing with message: \"{message}\"")
    run_cmd(f'git commit -m "{message}"')

    print("🚀 Pushing to origin...")
    run_cmd("git push origin HEAD")

    print("✅ Push complete.")

if __name__ == "__main__":
    main()

