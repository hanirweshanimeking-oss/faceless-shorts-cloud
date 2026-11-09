import os
from pathlib import Path
import urllib.request, json

env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
g_key = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GOOGLE_API_KEY="):
            g_key = line.split("=", 1)[1].strip().strip('"').strip("'")

print("GOOGLE_API_KEY present:", bool(g_key))
if g_key:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={g_key}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            models = [m["name"] for m in data.get("models", []) if "gemini" in m["name"]]
            print(f"Gemini API working! Total Gemini models: {len(models)}")
            print("Examples:", models[:4])
    except Exception as e:
        print("Gemini API error:", e)
