import os

MODULE_DIR = "modules"
MAIN_FILE = "main.py"

def extract_function_name(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if line.strip().startswith("def "):
                return line.strip().split()[1].split("(")[0]
    return None

def build_main():
    entries = []
    imports = []
    calls = []

    for filename in sorted(os.listdir(MODULE_DIR)):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            filepath = os.path.join(MODULE_DIR, filename)
            function_name = extract_function_name(filepath)

            if not function_name:
                continue

            imports.append(f"from modules.{module_name} import {function_name}")
            entries.append(f"{len(entries)+1}. {function_name.replace('_', ' ').title()}")
            calls.append(f"    elif choice == \"{len(entries)}\":\n        {function_name}()")

    # Build the new main.py content
    main_lines = [
        *imports,
        "",
        "def main():",
        "    print(\"=== Sh00k3ms Toolkit ===\")",
    ]
    for i, entry in enumerate(entries, 1):
        main_lines.append(f"    print(\"{i}. {entry}\")")
    main_lines.append("    choice = input(\"Select a tool: \")")
    main_lines.append("    if choice == \"0\":\n        return")
    main_lines.extend(calls)
    main_lines.append("    else:\n        print(\"Invalid selection.\")\n")
    main_lines.append("if __name__ == \"__main__\":")
    main_lines.append("    main()")
    main_lines.append("    if input(\"Would you like to push to Git now? [y/N]: \").lower() == \"y\":")
    main_lines.append("        import git_push\n        git_push.main()")

    with open(MAIN_FILE, "w") as f:
        f.write("\n".join(main_lines))

    print(f"✅ Rebuilt {MAIN_FILE} with {len(entries)} tool(s).")

if __name__ == "__main__":
    build_main()

