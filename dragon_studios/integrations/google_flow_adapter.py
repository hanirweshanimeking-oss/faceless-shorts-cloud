"""
Dragon Studios India - Google Flow & Veo 2/3 Filmmaking Integration Adapter
Enables multi-scene conversational storyboarding, character consistency continuity,
and cloud video generation via Google Veo / Google Flow.
"""

import os
import json
import time
import requests
from typing import Dict, Any, List, Optional

class GoogleFlowAdapter:
    """
    Direct interface to Google Flow workspace formats and Google Veo video generation.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        # Google AI Studio / Vertex AI Veo endpoint
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    @staticmethod
    def optimize_prompt_for_veo(
        scene_description: str,
        camera_motion: str = "slow cinematic push-in",
        lighting: str = "volumetric dark moody rim light, high contrast chiaroscuro",
        style: str = "dark anime cinematic masterpiece, Ufotable aesthetic, 8k",
        negative_prompt: str = "blurry, low quality, distorted anatomy, text artifacts, watermark"
    ) -> Dict[str, str]:
        """
        Enhances scene prompts with Google Veo / Flow directorial tokens.
        """
        full_prompt = (
            f"{style}. {scene_description}. "
            f"Camera: {camera_motion}. "
            f"Lighting: {lighting}."
        )
        return {
            "prompt": full_prompt,
            "negative_prompt": negative_prompt,
            "camera_motion": camera_motion,
            "lighting": lighting
        }

    def create_flow_project_manifest(
        self,
        project_id: str,
        title: str,
        pillar: str,
        scenes: List[Dict[str, Any]],
        aspect_ratio: str = "9:16"
    ) -> Dict[str, Any]:
        """
        Constructs a Google Flow-compatible multi-shot project specification.
        """
        flow_shots = []
        for idx, scene in enumerate(scenes, 1):
            cam = scene.get("camera_movement") or scene.get("camera_angle") or "medium close-up, subtle pan"
            visual = scene.get("visual_prompt") or scene.get("headline", "")
            dialogue = scene.get("dialogue") or scene.get("dialogue_text") or scene.get("subtitle_text") or scene.get("script_text") or scene.get("subtext", "")
            duration = scene.get("duration_seconds") or scene.get("duration", 5.0)

            veo_prompt = self.optimize_prompt_for_veo(
                scene_description=visual,
                camera_motion=cam,
                lighting="dark moody neon rim lighting" if pillar == "DARK_PSYCHOLOGY" else "cinematic golden studio glow",
                style="Japanese dark fantasy anime, 8k, sharp focus" if pillar != "CONVERSATIONAL_PODCAST" else "ultra-sharp 4k studio podcast broadcast"
            )

            flow_shots.append({
                "shot_index": idx,
                "scene_name": f"Shot {idx}: {scene.get('headline', 'Scene')}",
                "duration_seconds": duration,
                "veo_prompt": veo_prompt["prompt"],
                "negative_prompt": veo_prompt["negative_prompt"],
                "camera_direction": cam,
                "dialogue_audio_cue": dialogue,
                "continuity_tokens": [pillar, f"char_ref_{project_id}"]
            })

        manifest = {
            "flow_version": "1.0",
            "project_id": project_id,
            "title": title,
            "pillar": pillar,
            "target_aspect_ratio": aspect_ratio,
            "recommended_model": "Google Veo 2 / Veo 3",
            "total_shots": len(flow_shots),
            "total_estimated_duration": sum(s["duration_seconds"] for s in flow_shots),
            "timeline": flow_shots
        }
        return manifest

    def export_flow_project(
        self,
        project_id: str,
        title: str,
        pillar: str,
        scenes: List[Dict[str, Any]],
        output_dir: str = "output"
    ) -> str:
        """
        Saves the Google Flow project file and markdown director guide.
        """
        manifest = self.create_flow_project_manifest(project_id, title, pillar, scenes)
        proj_dir = os.path.join(output_dir, project_id)
        os.makedirs(proj_dir, exist_ok=True)

        json_path = os.path.join(proj_dir, f"{project_id}_google_flow.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Also write a ready-to-paste Director's Script for Flow Studio
        md_path = os.path.join(proj_dir, f"{project_id}_flow_director_board.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Google Flow Director Blueprint: {title}\n\n")
            f.write(f"- **Project ID**: `{project_id}`\n")
            f.write(f"- **Pillar**: {pillar}\n")
            f.write(f"- **Aspect Ratio**: {manifest['target_aspect_ratio']}\n")
            f.write(f"- **Recommended Engine**: Google Veo 2 / 3 via Google Flow (`flow.google`)\n\n")
            f.write("## Shot-by-Shot Prompts for Google Flow Studio\n\n")
            for shot in manifest["timeline"]:
                f.write(f"### Shot {shot['shot_index']}: {shot['scene_name']} ({shot['duration_seconds']}s)\n")
                f.write(f"- **Veo Prompt**: `{shot['veo_prompt']}`\n")
                f.write(f"- **Camera Motion**: {shot['camera_direction']}\n")
                f.write(f"- **Voiceover / Dialogue Cue**: \"{shot['dialogue_audio_cue']}\"\n\n")

        return json_path

    def generate_clip_via_veo(
        self,
        prompt: str,
        output_path: str,
        duration_seconds: float = 5.0,
        aspect_ratio: str = "9:16"
    ) -> Dict[str, Any]:
        """
        Dispatches prompt to Google Veo via Google Cloud / AI Studio REST API.
        Falls back cleanly if GOOGLE_API_KEY is not set or quota is limited.
        """
        if not self.api_key:
            return {
                "status": "CONFIG_REQUIRED",
                "provider": "GOOGLE_VEO",
                "message": "GOOGLE_API_KEY is not configured in .env. Falling back to local zero-cost compositor."
            }

        headers = {
            "Content-Type": "application/json"
        }
        
        # Endpoint for Google Veo video generation
        endpoint = f"{self.base_url}/models/veo-2.0-generate-001:predictLongRunning?key={self.api_key}"
        payload = {
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "aspectRatio": "9:16" if aspect_ratio == "9:16" else "16:9",
                "sampleCount": 1,
                "durationSeconds": int(duration_seconds)
            }
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            if response.status_code in [200, 202]:
                data = response.json()
                operation_name = data.get("name")
                return {
                    "status": "QUEUED",
                    "provider": "GOOGLE_VEO",
                    "operation": operation_name,
                    "prompt": prompt,
                    "output_path": output_path
                }
            else:
                return {
                    "status": "API_ERROR",
                    "provider": "GOOGLE_VEO",
                    "code": response.status_code,
                    "details": response.text
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "provider": "GOOGLE_VEO",
                "error": str(e)
            }
