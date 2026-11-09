import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

OUT_DIR = Path(r"c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH\episodes\episode_001\panels")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Master Full-Colour Korean Webtoon Visual Prompts for Episode 1
PANEL_SPECS = [
    {
        "id": "ep01_p01_cosmic_throne",
        "title": "Panel 01: The Cosmic Throne",
        "width": 800,
        "height": 1280,
        "prompt": "masterpiece, solo leveling aesthetic, premium korean webtoon manhwa, full color, 8k, center of collapsing multiverse, spiral galaxies folding into violet static fissures like burning parchment, gigantic colossal black throne carved from dead stars, titanic dark entity silhouette sitting on throne, deep cosmic dread, cinematic lighting, volumetric purple aura"
    },
    {
        "id": "ep01_p03_four_sovereigns",
        "title": "Panel 03: The Four Sovereigns",
        "width": 800,
        "height": 1100,
        "prompt": "masterpiece, solo leveling manhwa, full color, four divine anime sovereigns standing shoulder to shoulder on cracked obsidian stone floating in space, shattered divine armor, leaking liquid golden ether and roaring crimson bloodfire flame, defiant posture, volumetric cosmic lighting, 8k digital painting"
    },
    {
        "id": "ep01_p07_siddhartha_supernova",
        "title": "Panel 07: Siddhartha (Golden Sovereign)",
        "width": 800,
        "height": 1000,
        "prompt": "masterpiece, solo leveling manhwa style, full color, handsome anime sovereign Siddhartha, macro face close up, unblinking eyes burning like twin molten golden supernovas, threads of molten gold glowing in raven black hair, cold calm smile, cracked divine armor collar, volumetric cinematic lighting, 8k"
    },
    {
        "id": "ep01_p14_memory_keys_sealed",
        "title": "Panel 14: The 20 Memory Keys",
        "width": 800,
        "height": 1280,
        "prompt": "masterpiece, solo leveling webtoon, full color, cosmic chains driving into an anime sovereign's body, golden soul ripping into twenty glowing crystalline golden keys sealing into his bone marrow, blinding golden sacred runes, deep space void background, dramatic cinematic lighting, 8k"
    },
    {
        "id": "ep01_p15_hyderabad_monsoon",
        "title": "Panel 15: Jubilee Hills Estate Monsoon",
        "width": 800,
        "height": 1100,
        "prompt": "masterpiece, korean manhwa, full color, wide panoramic establishing shot, massive luxury modern hillside fortress estate in Jubilee Hills Hyderabad at night, torrential monsoon rain, lightning striking across stormy sky, neon city lights in distance, cinematic atmosphere, 8k"
    },
    {
        "id": "ep01_p16_ike_reading_trusts",
        "title": "Panel 16: 8-Year-Old Ike in Library",
        "width": 800,
        "height": 1000,
        "prompt": "masterpiece, lookism manhwa aesthetic, full color, eight year old young boy Ike Dragon in black traditional kurta sitting on mahogany library windowsill at night, rain beating on window glass, reading corporate charts with sharp calculating unchildlike eyes, thin white scar on left temple, 8k"
    },
    {
        "id": "ep01_p28_raghav_pistol_betrayal",
        "title": "Panel 28: Raghav's Pistol Betrayal",
        "width": 800,
        "height": 1100,
        "prompt": "masterpiece, lookism manhwa, full color, dark grand marble dining hall, red emergency LED strips lighting up marble pillars in blood red, security chief in tactical vest aiming suppressed black handgun with sinister smirk, dramatic low angle, cinematic shadow, 8k"
    },
    {
        "id": "ep01_p30_devraj_jackal_arrival",
        "title": "Panel 30: Devraj Rathore ('The Jackal')",
        "width": 800,
        "height": 1280,
        "prompt": "masterpiece, lookism manhwa, full color, sinister 48yo underworld billionaire boss Devraj Rathore strolling through breached palace door with smoke, tailored charcoal cashmere overcoat, slicked back hair with silver temples, cruel predatory wolfish smirk, gold pinky ring, mercenaries behind, 8k"
    },
    {
        "id": "ep01_p35_ike_lion_eyes",
        "title": "Panel 35: The Lion's Cold Gaze",
        "width": 800,
        "height": 900,
        "prompt": "masterpiece, solo leveling manhwa, full color, extreme close up of eight year old young boy Ike Dragon's face, cold ancient void in his eyes, fearless terrifying expression staring down a criminal boss, thin scar on temple, dramatic red emergency lighting, 8k"
    },
    {
        "id": "ep01_p40_maybach_rpg_flip",
        "title": "Panel 40: Highway Maybach RPG Detonation",
        "width": 800,
        "height": 1280,
        "prompt": "masterpiece, solo leveling action manhwa, full color, midnight rainy expressway, massive explosion detonating under black armored luxury Maybach limousine, car flipping upside down in mid-air amidst roaring fire and rain, dynamic kinetic camera angle, flying debris, 8k"
    },
    {
        "id": "ep01_p49_ike_in_drainage_sludge",
        "title": "Panel 49: Survival in the Sludge",
        "width": 800,
        "height": 1100,
        "prompt": "masterpiece, dark manhwa webtoon, full color, eight year old boy Ike lying hidden flat inside a narrow muddy highway drainage ditch under guardrail, submerged in dark mud and water, clutching a scorched watch, burning car wreckage reflecting in unblinking black eyes, rain pouring, 8k"
    },
    {
        "id": "ep01_p51_sovereign_eye_ignites",
        "title": "Panel 51: The Sovereign Eye Ignites",
        "width": 800,
        "height": 1400,
        "prompt": "masterpiece, solo leveling manhwa, full color, vertical webtoon climax splash, eight year old boy standing in rain on empty highway, mud-stained black clothes, left eye blazing with blinding molten sovereign golden fire, 50 meter circular shockwave crater blasted on road, raindrops frozen in mid air, massive phantom shadow of horned dragon rising into storm clouds, 8k"
    }
]

def generate_panel(spec: dict) -> Path:
    panel_id = spec["id"]
    out_file = OUT_DIR / f"{panel_id}.jpg"
    
    if out_file.exists() and out_file.stat().st_size > 10000:
        print(f"  [✓] {spec['title']} already exists ({out_file.name})")
        return out_file

    print(f"  [...] Generating {spec['title']} ({spec['width']}x{spec['height']}) via FLUX...")
    encoded_prompt = urllib.parse.quote(spec["prompt"])
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={spec['width']}&height={spec['height']}&model=flux&nologo=true"
    
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
                if len(data) > 10000:
                    out_file.write_bytes(data)
                    # Verify image
                    with Image.open(out_file) as img:
                        print(f"    [+] Saved & Verified: {out_file.name} ({img.size})")
                    return out_file
                else:
                    print(f"    [-] Attempt {attempt}: Received small response ({len(data)} bytes), retrying...")
        except Exception as e:
            print(f"    [-] Attempt {attempt} error: {e}")
            time.sleep(3)
            
    raise RuntimeError(f"Failed to generate {spec['title']} after 3 attempts.")

def main():
    print("==================================================")
    print("   DRAGON: HIDDEN REBIRTH — EPISODE 1 ARTWORK")
    print("   Full-Colour Korean Webtoon FLUX Engine (Zero Canva AI)")
    print("==================================================")
    
    generated_count = 0
    for idx, spec in enumerate(PANEL_SPECS, 1):
        print(f"\n[{idx}/{len(PANEL_SPECS)}] Processing: {spec['title']}")
        p = generate_panel(spec)
        if p.exists():
            generated_count += 1
        time.sleep(1) # respectful pacing
        
    print("\n==================================================")
    print(f"[SUCCESS] All {generated_count} key manhwa panels generated successfully!")
    print(f"Output directory: {OUT_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
