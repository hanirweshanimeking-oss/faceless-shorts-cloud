import os
import sys
import json
import urllib.request
from pathlib import Path

env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
hf_token = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("HF_TOKEN="):
            hf_token = line.split("=", 1)[1].strip().strip('"').strip("'")

print(f"HF Token present: {bool(hf_token)}")
if not hf_token:
    print("[-] Missing HF_TOKEN in .env")
    sys.exit(1)

req = urllib.request.Request(
    "https://huggingface.co/api/whoami-v2",
    headers={"Authorization": f"Bearer {hf_token}", "User-Agent": "Antigravity/1.0"}
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print(f"[+] Authenticated as HF User: {data.get('name')}")
        print(f"[+] Account Email: {data.get('email')}")
        print(f"[+] Token Type: {data.get('auth', {}).get('type')}")
        print(f"[+] Organizations: {[org.get('name') for org in data.get('orgs', [])]}")
except Exception as e:
    print(f"[-] Whoami error: {e}")
