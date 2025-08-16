from __future__ import annotations
import os
from typing import Iterable, List
import jwt

WORDLIST_CANDIDATES: List[str] = [
    "jwt_secrets_wordlist.txt",
    os.path.join(os.path.dirname(__file__), "..", "jwt_secrets_wordlist.txt"),
]

ALGS = ["HS256", "HS384", "HS512"]

def _load_wordlist() -> Iterable[str]:
    for path in WORDLIST_CANDIDATES:
        path = os.path.abspath(path)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    w = line.strip()
                    if w:
                        yield w
            return
    # fallback small set
    for w in ("secret", "password", "changeme", "admin", "jwtsecret"):
        yield w

def run_jwt_cracker(token: str | None = None) -> None:
    if not token:
        print("Usage: sh00k3ms jwt crack <token>")
        return

    print(f"[+] Token length: {len(token)}")
    tried = 0
    for key in _load_wordlist():
        tried += 1
        for alg in ALGS:
            try:
                jwt.decode(token, key, algorithms=[alg])
                print(f"[✓] KEY FOUND: '{key}' (alg={alg})")
                print("[i] NOTE: works only for HMAC (HS*) tokens, not RS*/ES* public-key JWTs.")
                return
            except jwt.InvalidTokenError:
                continue
    print(f"[x] No key found after {tried} guesses.")
