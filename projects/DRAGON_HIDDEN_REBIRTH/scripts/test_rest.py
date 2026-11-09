import requests, json
from pathlib import Path

env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
g_key = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GOOGLE_API_KEY="):
            g_key = line.split("=", 1)[1].strip().strip('"').strip("'")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={g_key}"
payload = {
    "contents": [{"parts": [{"text": "Reply in 1 sentence: Who is Hanirwesh and Antigravity?"}]}]
}
r = requests.post(url, json=payload, timeout=10)
print("Status:", r.status_code)
res = r.json()
print("Answer:", res["candidates"][0]["content"]["parts"][0]["text"].strip())
