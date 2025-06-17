from modules.reflected_tester import run_reflected_tester

def main():
    print("=== Sh00k3ms Toolkit ===")
    print("1. Reflected XSS / CSS Injection Tester")
    choice = input("Select a tool: ")

    if choice == "1":
        run_reflected_tester()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()

