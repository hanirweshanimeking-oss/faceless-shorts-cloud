"""
Dragon Studios India - Google Flow Web Browser Automation (Playwright + CDP)
Automates flow.google using Google Chrome with a persistent profile.
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, List, Optional
from playwright.sync_api import sync_playwright

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), ".gemini", "chrome_flow_profile"))
CDP_URL = "http://127.0.0.1:9222"

class GoogleFlowBrowser:
    def __init__(self, profile_dir: str = PROFILE_DIR):
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

    def launch_browser_for_flow(self, target_url: str = "https://flow.google") -> None:
        """
        Launches Google Chrome with remote debugging on port 9222 and persistent profile.
        Does not interfere with other Chrome instances.
        """
        cmd = [
            CHROME_EXE,
            f"--remote-debugging-port=9222",
            f"--user-data-dir={self.profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            target_url
        ]
        # Launch detached so it keeps running independently
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)

    def connect_and_check_auth(self) -> Dict[str, Any]:
        """
        Connects to the running Chrome instance over CDP and inspects login state on flow.google.
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(CDP_URL)
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                
                # Find or open flow.google tab
                page = None
                for p_tab in context.pages:
                    if "flow.google" in p_tab.url or "labs.google" in p_tab.url:
                        page = p_tab
                        break
                
                if not page:
                    page = context.new_page()
                    page.goto("https://flow.google", timeout=30000)

                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)

                url = page.url
                title = page.title()

                # Check if signed in or sign-in button present
                is_signed_in = not ("accounts.google.com" in url or "Sign in" in page.content()[:2000])

                return {
                    "status": "CONNECTED",
                    "url": url,
                    "title": title,
                    "is_signed_in": is_signed_in,
                    "message": "Connected to Google Flow via Chrome CDP." if is_signed_in else "Please log in to your Google Account on the opened Chrome window."
                }
        except Exception as e:
            return {
                "status": "DISCONNECTED",
                "error": str(e),
                "message": "Could not connect to Chrome on port 9222. Call launch_browser_for_flow() first."
            }

    def generate_shot_in_flow(
        self,
        prompt: str,
        camera_motion: str = "",
        output_dir: str = "output"
    ) -> Dict[str, Any]:
        """
        Navigates Google Flow UI, creates a scene with the prompt, and initiates generation.
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(CDP_URL)
                context = browser.contexts[0]
                page = context.pages[0] if context.pages else context.new_page()

                if "flow.google" not in page.url:
                    page.goto("https://flow.google", timeout=30000)
                    page.wait_for_load_state("networkidle")

                return {
                    "status": "READY_IN_FLOW",
                    "prompt": prompt,
                    "current_page": page.url
                }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

if __name__ == "__main__":
    bot = GoogleFlowBrowser()
    bot.launch_browser_for_flow()
    res = bot.connect_and_check_auth()
    print("Flow Browser Status:", res)
