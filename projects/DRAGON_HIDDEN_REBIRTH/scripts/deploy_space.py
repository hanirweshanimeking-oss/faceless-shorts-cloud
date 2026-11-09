import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

DIR = Path(r"c:\Users\DESKTOP\Downloads\money")
ENV_PATH = DIR / ".env"
BOT_DIR = DIR / "cloud_telegram_bot"

hf_token = None
google_api_key = None

if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("HF_TOKEN="):
            hf_token = line.split("=", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("GOOGLE_API_KEY="):
            google_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

if not hf_token:
    print("[-] Missing HF_TOKEN")
    sys.exit(1)

api = HfApi(token=hf_token)
user = api.whoami()["name"]
repo_id = f"{user}/antigravity-studio-bot"

print(f"[*] Deploying to Hugging Face Space: {repo_id}...")

# 1. Create Space repo if not exists
try:
    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
        private=False,
        exist_ok=True
    )
    print(f"[+] Space repository verified: {repo_id}")
except Exception as e:
    print(f"[*] Repo create notice: {e}")

# 2. Configure Space Secrets
secrets = {
    "TELEGRAM_BOT_TOKEN": "8768392597:AAEXtwLn-wShMTceDfYopQfR0wpySmtsA5A",
    "TELEGRAM_CHAT_ID": "7527497140",
    "GOOGLE_API_KEY": google_api_key or "",
    "HF_TOKEN": hf_token
}

for k, v in secrets.items():
    if v:
        try:
            api.add_space_secret(repo_id=repo_id, key=k, value=v)
            print(f"[+] Secret configured: {k}")
        except Exception as e:
            print(f"[-] Secret {k} notice: {e}")

# 3. Upload all files from cloud_telegram_bot/
print(f"[*] Uploading cloud bot package from {BOT_DIR}...")
try:
    api.upload_folder(
        folder_path=str(BOT_DIR),
        repo_id=repo_id,
        repo_type="space",
        commit_message="Deploy Antigravity Cloud Studio & Telegram Remote Hub"
    )
    print(f"[SUCCESS] Upload complete! Space building live at: https://huggingface.co/spaces/{repo_id}")
except Exception as e:
    print(f"[-] Upload error: {e}")
    sys.exit(1)
