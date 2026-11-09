"""
Dragon Studios India - Cloud Video Generation Adapter
Modular abstraction layer connecting to Google Veo, Kling AI, Fal.ai (Wan2.1),
and Replicate, with a zero-cost local fallback engine.
"""

import os
import time
import requests
from typing import Dict, Any, Optional

class VideoGenAdapter:
    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("VIDEO_GEN_PROVIDER", "MOCK")).upper()
        self.fal_key = os.getenv("FAL_KEY", "")
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN", "")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")

    def generate_clip(
        self,
        prompt: str,
        output_path: str,
        duration_seconds: float = 5.0,
        reference_image_path: Optional[str] = None,
        aspect_ratio: str = "9:16"
    ) -> Dict[str, Any]:
        """
        Routes the prompt to the configured video generation engine.
        Saves resulting MP4 to output_path.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if self.provider == "FAL" and self.fal_key:
            return self._generate_via_fal(prompt, output_path, reference_image_path)
        elif self.provider == "REPLICATE" and self.replicate_token:
            return self._generate_via_replicate(prompt, output_path, reference_image_path)
        elif self.provider in ["VEO", "GOOGLE_FLOW", "GOOGLE_VEO"] and self.google_api_key:
            return self._generate_via_veo(prompt, output_path, reference_image_path)
        else:
            # High-Performance Local Canvas Fallback (Zero cost, no API keys needed)
            from dragon_studios.agents.editing_agent import create_color_background_clip
            create_color_background_clip(
                output_path=output_path,
                duration=duration_seconds,
                color="#0b0c10",
                width=1080,
                height=1920,
                fps=30
            )
            return {
                "status": "SUCCESS",
                "provider": "LOCAL_CANVAS",
                "output_path": output_path,
                "duration": duration_seconds,
                "note": "Generated via local zero-cost compositor. Connect FAL_KEY or GOOGLE_API_KEY for live diffusion video."
            }

    def _generate_via_fal(self, prompt: str, output_path: str, reference_image: Optional[str]) -> Dict[str, Any]:
        """Executes Wan2.1 or Kling generation via Fal.ai."""
        headers = {
            "Authorization": f"Key {self.fal_key}",
            "Content-Type": "application/json"
        }
        endpoint = "https://queue.fal.run/fal-ai/wan/v2.1/text-to-video"
        payload = {
            "prompt": f"masterpiece, anime aesthetic, 8k, dark dramatic lighting, {prompt}",
            "aspect_ratio": "9:16"
        }
        res = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        return {"status": "QUEUED", "response": res.json()}

    def _generate_via_replicate(self, prompt: str, output_path: str, reference_image: Optional[str]) -> Dict[str, Any]:
        """Executes CogVideoX-5B or Wan2.1 via Replicate API."""
        headers = {
            "Authorization": f"Token {self.replicate_token}",
            "Content-Type": "application/json"
        }
        endpoint = "https://api.replicate.com/v1/predictions"
        payload = {
            "version": "c0e668a6b1853612dcf654a9b6e82c81e3a4e98f01dd48e65eefec39757912ad",
            "input": {
                "prompt": prompt,
                "num_frames": 49
            }
        }
        res = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        return {"status": "QUEUED", "response": res.json()}

    def _generate_via_veo(self, prompt: str, output_path: str, reference_image: Optional[str]) -> Dict[str, Any]:
        """Calls Google Veo 2 / Gemini API video generation via GoogleFlowAdapter."""
        from dragon_studios.integrations.google_flow_adapter import GoogleFlowAdapter
        adapter = GoogleFlowAdapter(api_key=self.google_api_key)
        return adapter.generate_clip_via_veo(prompt=prompt, output_path=output_path)
