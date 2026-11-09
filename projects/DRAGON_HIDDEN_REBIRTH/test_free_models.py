import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image

prompt = "masterpiece, solo leveling manhwa, full color, handsome male with golden eyes in rain"
encoded = urllib.parse.quote(prompt)

# Test 1: Pollinations default (Turbo / SDXL)
url_poll_default = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=1024&nologo=true"
try:
    print("[*] Testing Pollinations default...")
    req = urllib.request.Request(url_poll_default, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
        print(f"[+] Pollinations Default OK: {len(data)} bytes")
except Exception as e:
    print(f"[-] Pollinations Default error: {e}")

# Test 2: Hugging Face with HF_TOKEN
env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
hf_token = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("HF_TOKEN="):
            hf_token = line.split("=", 1)[1].strip().strip('"').strip("'")

print(f"[*] Found HF_TOKEN: {bool(hf_token)}")
if hf_token:
    hf_model = "black-forest-labs/FLUX.1-schnell"
    url_hf = f"https://api-inference.huggingface.co/models/{hf_model}"
    try:
        import json
        req2 = urllib.request.Request(
            url_hf,
            data=json.dumps({"inputs": prompt}).encode("utf-8"),
            headers={"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req2, timeout=25) as resp2:
            data2 = resp2.read()
            print(f"[+] Hugging Face FLUX OK: {len(data2)} bytes")
    except Exception as e:
        print(f"[-] Hugging Face error: {e}")
