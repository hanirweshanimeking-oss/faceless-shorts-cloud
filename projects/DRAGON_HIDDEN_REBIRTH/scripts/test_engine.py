import os
from gradio_client import Client
from pathlib import Path

env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
hf_token = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("HF_TOKEN="):
            hf_token = line.split("=", 1)[1].strip().strip('"').strip("'")

print("Checking Asahina2K/animagine-xl-3.1...")
try:
    client = Client("Asahina2K/animagine-xl-3.1", token=hf_token)
    print("Successfully connected!")
    print("Endpoints:", client.view_api(all_endpoints=True))
except Exception as e:
    print("Animagine error:", e)

print("\nChecking FLUX.1-schnell cooldown status...")
try:
    c_flux = Client("black-forest-labs/FLUX.1-schnell", token=hf_token)
    res = c_flux.predict(
        prompt="quick test",
        seed=0,
        randomize_seed=True,
        width=768,
        height=1024,
        num_inference_steps=4,
        api_name="/infer"
    )
    print("FLUX cooldown finished! Success:", res)
except Exception as e:
    print("FLUX status:", e)
