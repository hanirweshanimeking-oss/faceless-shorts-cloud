import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image

def test_pollinations_pipeline():
    prompt = "masterpiece, solo leveling aesthetic, premium korean webtoon manhwa, full color, 8k, handsome 18yo male with messy raven hair, thin white scar on left temple, glowing molten golden eyes, wearing black tactical turtleneck, dramatic cinematic volumetric lighting, volumetric rain drops, atmospheric depth, high contrast shadows"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=1280&model=flux&nologo=true"
    
    out_dir = Path(r"c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH\test_panels")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "test_ike_webtoon_flux.jpg"
    
    print(f"[*] Testing external FLUX webtoon pipeline via Pollinations API...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out_file.write_bytes(resp.read())
        
    print(f"[+] External Image Generated: {out_file} (Size: {out_file.stat().st_size} bytes)")
    img = Image.open(out_file)
    print(f"[+] Verified Image Dimensions: {img.size}, Format: {img.format}")

if __name__ == "__main__":
    try:
        test_pollinations_pipeline()
    except Exception as e:
        print(f"[-] Pipeline error: {e}")
