"""
Batch Art Generator for CHITRAN Chapter 2
Calibrated to Hanirwesh's exact Anime Manhwa Aesthetic:
- Consistent Aarav: messy black hair, warm amber eyes, red scarf, black mandala tunic, tan skin
- Consistent Neel: majestic male celestial sovereign, dark indigo blue skin, glowing blue trishul on forehead, cobalt eyes, gold jewelry
- Consistent Ananya: traditional Indian maiden, dark hazel eyes, jasmine blossoms, violet silk saree, gold jewelry
- Consistent Void Stalkers: formless smoky black tendrils, burning crimson slit eyes
- Indian Vedic Temple Architecture: carved sandstone pillars, Sanskrit runes, warm oil lamps, chiaroscuro lighting
"""

import os
import sys
import time
import shutil
from pathlib import Path
from gradio_client import Client

ROOT_DIR = Path(__file__).parent.parent
ART_DIR = ROOT_DIR / "generated_art" / "chapter_002_hd"
ART_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR = Path("C:/Users/DESKTOP/.gemini/antigravity/brain/d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3")

PANEL_PROMPTS = {
    # ========== PAGE 1: THE SANCTUARY AT MIDNIGHT ==========
    "p1_1_sanctum_wide": (
        "masterpiece, 2D anime manhwa illustration, vast ancient Indian subterranean temple library, "
        "carved sandstone arches and towering pillars covered in Sanskrit and Brahmi inscriptions, "
        "warm golden oil lamps casting long shadows, soft moonlight streaming through an overhead stone jali lattice grille, "
        "shelves filled with thousands of ancient palm-leaf manuscripts and scrolls, cinematic chiaroscuro, 8k"
    ),
    "p1_2_aarav_ananya_altar": (
        "masterpiece, 2D anime manhwa illustration, Indian teenage boy Aarav with messy black hair and red scarf "
        "standing beside Indian maiden Ananya with jasmine flowers in hair and purple saree, "
        "examining ancient scrolls on a massive carved stone reading altar inside a moonlit temple library, "
        "warm candlelight, highly detailed anime linework, 8k"
    ),
    "p1_3_ananya_concern": (
        "masterpiece, 2D anime manhwa illustration, beautiful Indian teenage maiden Ananya, close-up portrait, "
        "large expressive dark hazel anime eyes, soft blush on cheeks, long dark wavy hair decorated with white jasmine blossoms, "
        "antique gold jhumka earrings, violet silk saree, worried gentle expression, warm golden lamp glow, 8k"
    ),
    "p1_4_aarav_determined": (
        "masterpiece, 2D anime manhwa illustration, mature Indian teenage boy Aarav, close-up portrait, "
        "messy windswept black anime hair, warm luminous amber-gold eyes, red scarf draped around neck, "
        "black tunic with gold embroidery, intense focused expression, cinematic side lighting, 8k"
    ),
    "p1_5_sanskrit_scroll": (
        "masterpiece, 2D anime manhwa illustration, close-up macro of an ancient weathered Sanskrit palm-leaf manuscript scroll, "
        "intricate glowing golden Devanagari Sanskrit calligraphy letters, floating golden dust motes, magical amber embers, 8k"
    ),
    "p1_6_fragment_hover": (
        "masterpiece, 2D anime manhwa illustration, a sacred glowing diamond-shaped golden crystal relic fragment "
        "levitating in mid-air, spinning gently with concentric golden light rings, glowing Sanskrit runes inscribed on the crystal, "
        "sparkling golden ember trail, dark temple background, 8k"
    ),
    "p1_7_aarav_macro_eye": (
        "masterpiece, 2D anime manhwa illustration, extreme macro close-up of a handsome Indian boy's eye, "
        "intricate glowing amber-gold anime iris with radiant solar flecks and bright highlights, messy black hair strands, "
        "glowing reflection of golden fire in the pupil, intense awe, 8k"
    ),
    "p1_8_shadows_creeping": (
        "masterpiece, 2D anime manhwa illustration, ancient carved stone temple floor, "
        "creeping shadowy liquid black ink tendrils detaching from the ground and reaching upward, "
        "sinister glowing crimson red eyes glowing in the dark smoke, cold violet-blue mist, ominous horror atmosphere, 8k"
    ),

    # ========== PAGE 2: THE DEVOURER OF STORIES ==========
    "p2_1_void_erupt": (
        "masterpiece, 2D anime manhwa illustration, terrifying gigantic cosmic Void Stalker monster "
        "erupting from stone floor, formless swirling black smoke tendrils, sharp shadowy claws, "
        "burning fierce crimson red slit eyes, destroying ancient scrolls into black ash, dramatic low angle, 8k"
    ),
    "p2_2_void_fangs": (
        "masterpiece, 2D anime manhwa illustration, extreme close-up of a menacing shadowy Void beast's demonic visage, "
        "glowing sharp crimson slit eyes, formless gaping black mouth of smoke, inky tentacles reaching toward viewer, horror anime, 8k"
    ),
    "p2_3_ananya_fear": (
        "masterpiece, 2D anime manhwa illustration, Indian maiden Ananya backing away in fear against a stone temple pillar, "
        "wide terrified hazel eyes, hands clasped tightly to chest, jasmine flowers in dark hair, violet silk saree, "
        "shadowy smoke closing in, dramatic lighting, 8k"
    ),
    "p2_4_aarav_protect": (
        "masterpiece, 2D anime manhwa illustration, Indian teenage boy Aarav stepping forward bravely, "
        "one arm outstretched shielding the girl behind him, red scarf billowing violently, messy black hair, "
        "amber eyes blazing, black tunic with gold trim, heroic dynamic anime pose, 8k"
    ),
    "p2_5_aarav_eyes_ignite": (
        "masterpiece, 2D anime manhwa illustration, extreme close-up of Aarav's face, "
        "his amber eyes exploding with blinding solar fire and glowing yellow runes, determined fierce shouting expression, "
        "heat waves and golden sparks whipping through his spiky black hair, 8k"
    ),
    "p2_6_celestial_flame_burst": (
        "masterpiece, 2D anime manhwa illustration, dynamic wide action shot, "
        "massive concentric spherical shockwave of radiant golden celestial fire bursting outward from Aarav's palms, "
        "intricate Vedic mandala fire rings repelling shadowy beasts, blinding light, sparks and explosion, 8k"
    ),
    "p2_7_fire_vs_shadow": (
        "masterpiece, 2D anime manhwa illustration, epic clash between swirling radiant golden solar fire and dark smoky Void tentacles, "
        "thousands of golden sparks showering across ancient temple stone walls, high contrast chiaroscuro, 8k"
    ),
    "p2_8_shadow_overwhelm": (
        "masterpiece, 2D anime manhwa illustration, shadowy black ink tendrils constricting tightly around a cracking golden energy shield, "
        "Aarav gritting teeth in exhaustion, sweat on brow, red scarf frayed, struggling to maintain the barrier, dramatic tension, 8k"
    ),

    # ========== PAGE 3: THE SOVEREIGN'S JUDGMENT ==========
    "p3_1_lightning_crash": (
        "masterpiece, 2D anime manhwa illustration, a massive blinding bolt of brilliant celestial cyan-blue lightning "
        "tearing through the stone ceiling of the temple library, shattering rock into floating debris, intense azure light, 8k"
    ),
    "p3_2_neel_arrival": (
        "masterpiece, 2D anime manhwa illustration, handsome male Indian celestial sovereign deity Neel, "
        "descending gracefully through moonlight and blue lightning, radiant dark indigo celestial blue skin, "
        "glowing electric-blue trishul trident crest shining on forehead, intense glowing cobalt blue eyes, "
        "long flowing dark wavy hair with ornate gold ornaments and jewelry, midnight robes, calm sovereign aura, 8k"
    ),
    "p3_3_neel_vortex_hand": (
        "masterpiece, 2D anime manhwa illustration, close-up macro of Neel's slender blue hand, "
        "a miniature swirling cosmic galaxy vortex spinning above his palm, radiating intricate electric-blue light arcs and stardust, "
        "gold ring on finger, ornate gold wrist cuff, 8k"
    ),
    "p3_4_vortex_shockwave": (
        "masterpiece, 2D anime manhwa illustration, vast expanding dome of ethereal cyan and deep blue cosmic energy, "
        "instantly disintegrating the shadow Void beasts into harmless dissipating mist, sparkling starlight filling the hall, 8k"
    ),
    "p3_5_aarav_shocked": (
        "masterpiece, 2D anime manhwa illustration, Indian teenage boy Aarav kneeling on stone floor, "
        "gasping for breath, faint golden embers drifting off his hands, looking up in complete awe and astonishment, "
        "red scarf, messy black hair, amber eyes wide, 8k"
    ),
    "p3_6_neel_close": (
        "masterpiece, 2D anime manhwa illustration, majestic close-up portrait of male blue deity Neel, "
        "calm ancient piercing cobalt blue eyes looking down, glowing cyan trishul mark on brow, "
        "ornate gold earrings and collar, moonlit silver highlights on long dark hair, enigmatic aura, 8k"
    ),
    "p3_7_aarav_resolve": (
        "masterpiece, 2D anime manhwa illustration, Aarav rising to his feet, gripping his fist tight, "
        "a graceful ribbon of golden celestial fire swirling around his forearm, confident resolute amber eyes, "
        "answering the sovereign with unyielding determination, 8k"
    ),
    "p3_8_temple_roof_constellation": (
        "masterpiece, 2D anime manhwa illustration, panoramic wide shot, "
        "silhouettes of Aarav, Ananya, and Neel standing upon the highest moonlit temple terrace, "
        "looking out across the vast ancient temple city towards jagged mountain peaks, "
        "in the starry night sky a giant glowing constellation of a celestial dragon shines with golden-blue light, 8k"
    )
}

def generate_all():
    token_path = Path.home() / ".cache" / "huggingface" / "token"
    token = token_path.read_text().strip() if token_path.exists() else None
    
    print("[*] Connecting to AP123/SDXL-Lightning...")
    client = Client("AP123/SDXL-Lightning", token=token)
    print("[+] Connected!")

    # Check already existing files
    for name, prompt in PANEL_PROMPTS.items():
        target_path = ART_DIR / f"{name}.png"
        if target_path.exists() and target_path.stat().st_size > 50000:
            print(f"[SKIP] {name} already exists.")
            continue

        print(f"\n[*] Generating panel: {name}...")
        t0 = time.time()
        try:
            res = client.predict(prompt, "4-Step", api_name="/generate_image")
            shutil.copy(res, str(target_path))
            # Also copy to artifacts dir
            shutil.copy(res, str(ARTIFACTS_DIR / f"{name}.png"))
            dt = time.time() - t0
            print(f"[+] Done {name} in {dt:.1f}s -> {target_path.name}")
        except Exception as e:
            print(f"[!] Error generating {name}: {e}")
            time.sleep(3)

    print("\n[=== ALL PANELS GENERATED SUCCESSFULLY ===]")

if __name__ == "__main__":
    generate_all()
