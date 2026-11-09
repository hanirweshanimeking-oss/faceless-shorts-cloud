import sys
import time
from pathlib import Path

ROOT_DIR = Path(r"c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH")
sys.path.insert(0, str(ROOT_DIR))

from scripts.image_generator import MangaImageGenerator

OUT_DIR = ROOT_DIR / "episodes" / "episode_001" / "panels"
OUT_DIR.mkdir(parents=True, exist_ok=True)

REMAINING_PANELS = [
    # --- SCENE 2: JUBILEE HILLS MASSACRE & THE JACKAL ---
    {
        "id": "ep01_p15_hyderabad_monsoon",
        "title": "Panel 15: Jubilee Hills Estate Monsoon Night",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa aesthetic, full color, wide panoramic establishing shot, massive luxury modern hillside fortress estate in Jubilee Hills Hyderabad at night, torrential monsoon rain, lightning striking purple across stormy sky, neon city lights in distance, cinematic atmosphere, 8k masterpiece"
    },
    {
        "id": "ep01_p16_ike_reading_trusts",
        "title": "Panel 16: 8-Year-Old Ike Dragon on Library Windowsill",
        "width": 768,
        "height": 1024,
        "prompt": "lookism manhwa aesthetic, full color, eight year old young boy Ike Dragon in black traditional kurta sitting on mahogany library windowsill at night, rain beating on window glass, reading corporate financial charts with sharp calculating unchildlike eyes, thin white scar on left temple, raven black hair, 8k"
    },
    {
        "id": "ep01_p20_family_dinner",
        "title": "Panel 20: The Dragon Family Dinner Before Betrayal",
        "width": 1024,
        "height": 768,
        "prompt": "korean manhwa webtoon, full color, grand mahogany dining room, warm crystal chandelier lighting, father Vikram Dragon in charcoal silk shirt smiling, mother Ananya in emerald silk saree, young 8yo Ike sitting observing silently, luxury palace interior, cinematic depth of field, 8k"
    },
    {
        "id": "ep01_p28_raghav_pistol_betrayal",
        "title": "Panel 28: Security Chief Raghav's Treason",
        "width": 768,
        "height": 1024,
        "prompt": "lookism manhwa, full color, dark grand marble dining hall, red emergency LED strips lighting up marble pillars in blood red, security chief in tactical vest aiming suppressed black handgun with sinister smirk, dramatic low angle, cinematic shadow, 8k"
    },
    {
        "id": "ep01_p30_devraj_jackal_arrival",
        "title": "Panel 30: Devraj Rathore ('The Jackal') Entrance",
        "width": 768,
        "height": 1024,
        "prompt": "lookism manhwa, full color, sinister 48yo underworld billionaire boss Devraj Rathore strolling through breached palace door with smoke, tailored charcoal cashmere overcoat, slicked back hair with silver temples, cruel predatory wolfish smirk, gold pinky ring, mercenaries behind, 8k"
    },
    {
        "id": "ep01_p35_ike_lion_eyes",
        "title": "Panel 35: Ike's Unblinking Lion Eyes Staring Down Devraj",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa, full color, extreme close up of eight year old young boy Ike Dragon's face, cold ancient void in his eyes, fearless terrifying expression staring down an underworld boss, thin scar on temple, dramatic red emergency lighting, 8k"
    },

    # --- SCENE 3: GACHIBOWLI HIGHWAY AMBUSH ---
    {
        "id": "ep01_p40_maybach_rpg_flip",
        "title": "Panel 40: Highway Maybach RPG Detonation",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling action manhwa, full color, midnight rainy expressway, massive explosion detonating under black armored luxury Maybach limousine, car flipping upside down in mid-air amidst roaring fire and rain, dynamic kinetic camera angle, flying debris, 8k"
    },
    {
        "id": "ep01_p44_narasimha_naidu_execution",
        "title": "Panel 44: Narasimha Naidu Executioner Arrival",
        "width": 768,
        "height": 1024,
        "prompt": "lookism manhwa, full color, menacing tall muscle syndicate enforcer Narasimha Naidu in immaculate white linen safari suit stepping out of black SUV onto wet highway asphalt, holding shotgun with casual brutality, heavy gold chains, heavy monsoon rain, 8k"
    },

    # --- SCENE 4: CULVERT SURVIVAL & SOVEREIGN REBIRTH ---
    {
        "id": "ep01_p49_ike_in_drainage_sludge",
        "title": "Panel 49: Survival in the Drainage Pipe Sludge",
        "width": 768,
        "height": 1024,
        "prompt": "dark manhwa webtoon, full color, eight year old boy Ike lying hidden flat inside a narrow muddy highway drainage ditch under guardrail, submerged in dark mud and water, clutching a scorched watch, burning car wreckage reflecting in unblinking black eyes, rain pouring, 8k"
    },
    {
        "id": "ep01_p51_sovereign_eye_ignites",
        "title": "Panel 51: The Sovereign Eye Ignites (Climax Splash)",
        "width": 768,
        "height": 1024,
        "prompt": "solo leveling manhwa, full color, vertical webtoon climax splash, eight year old boy standing in rain on empty highway, mud-stained black clothes, left eye blazing with blinding molten sovereign golden fire, 50 meter circular shockwave crater blasted on road, raindrops frozen in mid air, massive phantom shadow of horned dragon rising into storm clouds, 8k"
    }
]

def main():
    print("==================================================")
    print("   DRAGON: HIDDEN REBIRTH — SCENES 2, 3, 4 PRODUCTION")
    print("   Official Cloud FLUX.1-schnell Engine (Zero Canva AI)")
    print("==================================================")
    
    gen = MangaImageGenerator(OUT_DIR)
    
    for idx, panel in enumerate(REMAINING_PANELS, 1):
        p_id = panel["id"]
        out_path = OUT_DIR / f"{p_id}.png"
        
        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"[{idx}/{len(REMAINING_PANELS)}] Already exists: {panel['title']}")
            continue
            
        print(f"\n[{idx}/{len(REMAINING_PANELS)}] Rendering: {panel['title']}...")
        result = gen.generate_panel(
            panel_id=p_id,
            width=panel["width"],
            height=panel["height"],
            shot_type="FULL",
            visual_prompt=panel["prompt"],
            prefer_cloud=True
        )
        if result and Path(result).exists():
            print(f"    [+] Successfully Saved: {Path(result).name} ({panel['width']}x{panel['height']})")
        else:
            print(f"    [-] Warning: Failed to render {panel['title']}")
            
        time.sleep(2) # rate limit courtesy

    print("\n==================================================")
    print(f"[SUCCESS] All Key Panels Rendered Successfully!")
    print(f"Panels directory: {OUT_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
