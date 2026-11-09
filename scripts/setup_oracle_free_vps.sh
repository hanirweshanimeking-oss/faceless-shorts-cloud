#!/bin/bash
# ==============================================================================
# 🐉 ANTIGRAVITY 1-COMPUTER DEDICATED VPS BOOTSTRAP SCRIPT
# For Oracle Cloud Always Free Tier (4 ARM64 OCPUs, 24GB RAM, 200GB NVMe SSD)
# Or Any Ubuntu 22.04 / 24.04 LTS Cloud Machine (DigitalOcean, Hetzner, AWS)
# ==============================================================================

set -e

echo "===> [1/6] Updating Ubuntu System & Installing Core Toolchains..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    ffmpeg \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-noto-cjk \
    tmux \
    htop \
    tree \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    docker.io \
    docker-compose

sudo systemctl enable --now docker
sudo usermod -aG docker $USER

echo "===> [2/6] Setting Up Workspace Directory & Swapping..."
# Add 8GB swap if needed
if [ $(free -m | awk '/^Swap:/ {print $2}') -lt 4000 ]; then
    echo "Creating 8GB swap file for high-memory workflows..."
    sudo fallocate -l 8G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

WORKSPACE_DIR="/home/$USER/antigravity_cloud"
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

echo "===> [3/6] Cloning Antigravity Cloud Repository..."
if [ ! -d "$WORKSPACE_DIR/faceless-shorts-cloud" ]; then
    git clone https://github.com/hanirweshanimeking-oss/faceless-shorts-cloud.git
fi

cd "$WORKSPACE_DIR/faceless-shorts-cloud"

echo "===> [4/6] Setting Up Python 3.11 Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "===> [5/6] Creating Persistent Systemd 24/7 Agent Daemon..."
DAEMON_SCRIPT="$WORKSPACE_DIR/faceless-shorts-cloud/antigravity_cloud_daemon.py"

cat << 'EOF' > "$DAEMON_SCRIPT"
"""
Antigravity 24/7 Persistent Cloud Host Daemon
Listens directly to Hanirwesh on Telegram via Long-Polling (No Webhook required!)
Executes root commands, clones any repo, runs full studio pipelines.
"""
import os
import sys
import time
import requests
from antigravity_cloud_agent import execute_autonomous_agent, send_telegram

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8768392597:AAEXtwLn-wShMTceDfYopQfR0wpySmtsA5A")
AUTHORIZED_CHAT_ID = 7527497140

print("===> Antigravity 24/7 Dedicated Cloud Daemon Started.")
send_telegram("🐉 *ANTIGRAVITY 24/7 DEDICATED CLOUD COMPUTER ACTIVE!*\n\nReady for unrestricted commands, git clones, and studio production.")

last_update_id = 0
while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
        resp = requests.get(url, timeout=40).json()
        for update in resp.get("result", []):
            last_update_id = update["update_id"]
            msg = update.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "").strip()

            if chat_id != AUTHORIZED_CHAT_ID or not text:
                continue

            print(f"[RECV] From Hanirwesh: {text}")
            if text.startswith("/clone"):
                repo = text.replace("/clone", "").strip()
                execute_autonomous_agent(f"Clone repository '{repo}', install dependencies, inspect architecture, and report features.")
            elif text.startswith("/run"):
                cmd = text.replace("/run", "").strip()
                execute_autonomous_agent(f"Run shell command: {cmd}")
            elif text.startswith("/agent") or text.startswith("/task") or text.startswith("/code"):
                task = text.replace("/agent", "").replace("/task", "").replace("/code", "").strip()
                execute_autonomous_agent(task)
            elif text.startswith("/reel") or text.startswith("/dark") or text.startswith("/manga"):
                from unified_cloud_dispatcher import dispatch
                execute_autonomous_agent(f"Produce reel for: {text}")
    except Exception as e:
        print(f"Polling loop notice: {e}")
        time.sleep(2)
EOF

# Create Systemd Service
sudo tee /etc/systemd/system/antigravity.service > /dev/null << EOF
[Unit]
Description=Antigravity 24/7 Autonomous Cloud Computer Daemon
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORKSPACE_DIR/faceless-shorts-cloud
Environment=PATH=$WORKSPACE_DIR/faceless-shorts-cloud/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=TELEGRAM_BOT_TOKEN=8768392597:AAEXtwLn-wShMTceDfYopQfR0wpySmtsA5A
Environment=TELEGRAM_CHAT_ID=7527497140
ExecStart=$WORKSPACE_DIR/faceless-shorts-cloud/venv/bin/python antigravity_cloud_daemon.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable antigravity.service
sudo systemctl start antigravity.service

echo "===> [6/6] Bootstrap Complete! Antigravity Service is Running 24/7."
echo "Check logs with: sudo journalctl -u antigravity.service -f"
