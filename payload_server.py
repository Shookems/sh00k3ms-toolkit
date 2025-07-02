import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime

LOG_FILE = "payload_server_requests.txt"
PAYLOAD_DIR = "payloads"
PORT = 8000

class LoggingHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args,
        )
        with open(LOG_FILE, "a") as f:
            f.write(msg)
        print(msg.strip())

def run_payload_server():
    print("\n--- Payload Server ---")

    if not os.path.exists(PAYLOAD_DIR):
        os.makedirs(PAYLOAD_DIR)
        print(f"[+] Created payloads directory: {PAYLOAD_DIR}")

    os.chdir(PAYLOAD_DIR)
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, LoggingHandler)

    print(f"[+] Hosting files from '{PAYLOAD_DIR}' on http://0.0.0.0:{PORT}")
    print("[*] Press Ctrl+C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Payload server stopped.")

