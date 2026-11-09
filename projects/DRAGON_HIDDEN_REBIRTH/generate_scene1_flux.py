import sys
import time
from pathlib import Path

ROOT_DIR = Path(r"c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH")
sys.path.insert(0, str(ROOT_DIR))

from scripts.image_generator import MangaImageGenerator

OUT_DIR = ROOT_DIR / "episodes" / "episode_001" / "panels"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENE_1_PANELS = [
    {
        "id": "ep01_p01_cosmic_throne",
        "title": "Panel 01: The Cosmic Throne",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa webtoon aesthetic, full color, center of collapsing multiverse, spiral galaxies folding into violet static fissures like burning parchment, gigantic colossal black throne carved from dead stars, titanic dark entity silhouette sitting on throne, deep cosmic dread, volumetric cinematic lighting, 8k masterpiece"
    },
    {
        "id": "ep01_p03_four_sovereigns",
        "title": "Panel 03: The Four Sovereigns",
        "width": 1024,
        "height": 768,
        "prompt": "solo leveling manhwa, full color, wide shot, four divine anime sovereigns standing shoulder to shoulder on cracked obsidian stone floating in space, shattered divine armor, leaking liquid golden ether and roaring crimson bloodfire flame, defiant posture, volumetric cosmic lighting, 8k digital painting"
    },
    {
        "id": "ep01_p04_hanirwesh_feral",
        "title": "Panel 04: Hanirwesh Kaivalya Feral Grin",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa, full color, close up of massive muscular anime warrior Hanirwesh, crimson scar tribal tattoos, blood dripping from fangs, wiping jaw with cracked gauntlet, wild unhinged feral grin, burning red eyes, dramatic chiaroscuro lighting, 8k"
    },
    {
        "id": "ep01_p07_siddhartha_supernova",
        "title": "Panel 07: Siddhartha (Golden Sovereign)",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa style, full color, handsome anime sovereign Siddhartha, macro face close up, unblinking eyes burning like twin molten golden supernovas, threads of molten gold glowing in raven black hair, cold calm smile, cracked divine armor collar, volumetric cinematic lighting, 8k"
    },
    {
        "id": "ep01_p10_sovereign_annihilation",
        "title": "Panel 10: Sovereign Annihilation Strike",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa, full color, cataclysmic double splash impact, gold quasar explosion, crimson bloodfire, azure lightning, and black void event horizon braided into a single world-cleaving helix striking an obsidian throne, shockwave rings, 8k masterpiece"
    },
    {
        "id": "ep01_p14_memory_keys_sealed",
        "title": "Panel 14: 20 Memory Reclamation Keys",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa webtoon, full color, cosmic chains driving into an anime sovereign's body, golden soul ripping into twenty glowing crystalline golden keys sealing into his bone marrow, blinding golden sacred runes, deep space void background, dramatic cinematic lighting, 8k"
    }
]

def main():
    print("==================================================")
    print("   DRAGON: HIDDEN REBIRTH — SCENE 1 FLUX PRODUCTION")
    print("   Official Cloud FLUX.1-schnell Engine (Zero Canva AI)")
    print("==================================================")
    
    gen = MangaImageGenerator(OUT_DIR)
    
    for idx, panel in enumerate(SCENE_1_PANELS, 1):
        p_id = panel["id"]
        out_path = OUT_DIR / f"{p_id}.png"
        
        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"[{idx}/{len(SCENE_1_PANELS)}] Already exists: {panel['title']}")
            continue
            
        print(f"\n[{idx}/{len(SCENE_1_PANELS)}] Rendering: {panel['title']}...")
        result = gen.generate_flux_panel(
            panel_id=p_id,
            width=panel["width"],
            height=panel["height"],
            visual_prompt=panel["prompt"]
        )
        if result and Path(result).exists():
            print(f"    [+] Successfully Saved: {Path(result).name} ({panel['width']}x{panel['height']})")
        else:
            print(f"    [-] Warning: Failed to render {panel['title']}")
            
        time.sleep(2) # rate limit courtesy

    print("\n==================================================")
    print(f"[SUCCESS] Scene 1 FLUX Artwork Generation Complete!")
    print(f"Panels directory: {OUT_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
