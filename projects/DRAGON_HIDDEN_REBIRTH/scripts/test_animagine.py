from gradio_client import Client
import time
from pathlib import Path

env_path = Path(r"c:\Users\DESKTOP\Downloads\money\.env")
hf_token = None
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("HF_TOKEN="):
            hf_token = line.split("=", 1)[1].strip().strip('"').strip("'")

client = Client("Asahina2K/animagine-xl-3.1", token=hf_token)
print("Calling animagine-xl-3.1 with positional arguments...")
prompt = "1boy, ike dragon, 8yo, raven black hair, sharp calculating golden eyes, black kurta, rain, cinematic lighting, masterpiece, high quality manhwa"
neg_prompt = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"

res = client.predict(
    prompt,
    neg_prompt,
    42,
    832,
    1216,
    7.0,
    25,
    "Euler a",
    "832 x 1216",
    "Cinematic",
    "Standard v3.1",
    False,
    0.5,
    1.0,
    True,
    api_name="/run"
)
print("Success! Result from Animagine:", res)
