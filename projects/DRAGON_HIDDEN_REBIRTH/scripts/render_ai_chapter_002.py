"""
AI Panel Renderer for Chapter 2
Fetches high-fidelity AI-generated manga panels via the free open endpoint (Tier 2),
crops watermarks, resizes to target panel bounding boxes, and composites into Master 300 DPI Canvas.
"""

import urllib.request
import urllib.parse
import time
import os
import sys
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.composition_agent import CompositionAgent
from agents.qa_agent import QualityAssuranceAgent

DB_PATH = ROOT_DIR / "database" / "manga_production.db"
OUTPUT_DIR = ROOT_DIR / "generated_art"
FINAL_PAGES_DIR = ROOT_DIR / "final_pages"
QA_DIR = ROOT_DIR / "quality_reports"

PANELS_TO_GENERATE = [
    (
        "panel_002_01_01", 2280, 950,
        "masterpiece anime manhwa wide panoramic establishing shot, vast subterranean ancient Hindu temple library beneath river ghats, ancient Sanskrit carved stone arches, high stone jali lattice with moonlight streaming down, warm golden oil lamps glowing, dust particles, cinematic lighting, 8k, detailed architecture",
        42
    ),
    (
        "panel_002_01_02", 1120, 1100,
        "masterpiece anime manhwa portrait close up, Indian teenage boy Aarav with messy layered black hair and red scarf, glowing amber eyes looking at a hovering glowing golden diamond crystal relic with ancient Sanskrit runes, warm atmospheric lighting, cinematic, 8k",
        108
    ),
    (
        "panel_002_01_03", 1120, 1100,
        "masterpiece anime manhwa portrait close up, beautiful Indian young woman Ananya with expressive brown eyes, delicate gold jhumkas and maang tikka, white jasmine flowers in long wavy dark hair, wearing purple and gold silk saree, warm temple lamp light, 8k",
        777
    ),
    (
        "panel_002_01_04", 2280, 1150,
        "masterpiece anime manhwa dynamic action panel, terrifying black smoke shadow monster with glowing red eyes rising from ground, Indian teenage boy Aarav with red scarf thrusting hands forward unleashing swirling golden celestial solar fire shockwave, explosive sparks, dynamic combat composition, 8k",
        999
    )
]

def generate_ai_panels():
    print("[*] Generating AI Manhwa Panels matching Hanirwesh benchmark...")
    
    for panel_id, w, h, prompt, seed in PANELS_TO_GENERATE:
        out_file = OUTPUT_DIR / f"{panel_id}.png"
        print(f"\n[*] Generating {panel_id} ({w}x{h})...")
        
        # Pollinations Free Endpoint
        encoded = urllib.parse.quote(prompt)
        # Fetch at 1024x1024 or ratio
        req_w = 1024 if w >= h else 768
        req_h = 768 if w >= h else 1024
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={req_w}&height={req_h}&nologo=true&seed={seed}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req, timeout=35) as resp:
                if resp.status == 200:
                    img = Image.open(resp).convert("RGB")
                    # Crop bottom 36px to ensure no watermark
                    iw, ih = img.size
                    img = img.crop((0, 0, iw, ih - 36))
                    # Resize to target panel dimensions with Lanczos
                    img_final = img.resize((w, h), Image.Resampling.LANCZOS)
                    # Add clean manga black border
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(img_final)
                    draw.rectangle([0, 0, w - 1, h - 1], outline=(15, 15, 20), width=6)
                    
                    img_final.save(out_file, "PNG", dpi=(300, 300))
                    print(f"    [+] Successfully generated and saved {out_file} ({w}x{h})")
                else:
                    print(f"    [-] Server returned status: {resp.status}")
        except Exception as e:
            print(f"    [-] Error generating {panel_id}: {e}")
            
        time.sleep(1.5)

    print("\n[*] Compositing Chapter 2 Page 1 Master Canvas...")
    composer = CompositionAgent(DB_PATH, FINAL_PAGES_DIR)
    master_path = composer.composite_page("page_002_01")
    print(f"[+] Master Page 1 Exported to: {master_path}")

    print("\n[*] Running Quality Assurance Inspection...")
    qa = QualityAssuranceAgent(DB_PATH, QA_DIR)
    qa_res = qa.inspect_page("page_002_01", master_path)
    print(f"[+] QA Verdict: {qa_res['verdict']} (Score: {qa_res['overall_score']:.2f}/10)")
    print(f"[+] Report: {qa_res['report_path']}")

if __name__ == "__main__":
    generate_ai_panels()
