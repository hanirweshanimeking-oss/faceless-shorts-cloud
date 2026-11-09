# SSS+ MANGA PRODUCTION — CLOUD GPU WORKFLOW GUIDE
## How to Run Free Unlimited High-Res Diffusion for DRAGON: HIDDEN REBIRTH

Because our local GPU is an NVIDIA GT 710 (2 GB Kepler VRAM), we route diffusion generation through free cloud GPUs for ₹0.

---

### METHOD 1: Free Hugging Face Token (Fastest — 30 Seconds)
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (log in or create a free account).
2. Click **Create new token**, name it `MangaStudio`, role `Read`.
3. Copy the token (`hf_...`).
4. In PowerShell, set it:
   ```powershell
   $env:HF_TOKEN = "hf_your_token_here"
   ```
5. Run the production command:
   ```powershell
   & "C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe" DRAGON_HIDDEN_REBIRTH\scripts\produce_chapter_002.py
   ```

---

### METHOD 2: Free Google Colab ComfyUI T4 GPU (100% Unlimited Runs)
If you want completely unlimited 1024x1024 panel generations with custom LoRAs:
1. Open [Google Colab](https://colab.research.google.com).
2. Upload [`DRAGON_HIDDEN_REBIRTH/workflows/CHITRAN_ComfyUI_Colab.ipynb`](CHITRAN_ComfyUI_Colab.ipynb).
3. Set Runtime → Change runtime type → **T4 GPU** (Free).
4. Run the single cell. It downloads ComfyUI, *Animagine XL 3.1*, and starts a public tunnel.
5. Copy the generated `https://...trycloudflare.com` URL.
6. Pass the tunnel URL to the studio CLI:
   ```powershell
   & "C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe" DRAGON_HIDDEN_REBIRTH\scripts\cli.py produce-page --page-id page_002_01 --comfy-url "https://your-tunnel.trycloudflare.com"
   ```
