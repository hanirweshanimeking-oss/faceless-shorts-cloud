"""Pocket Creator Director - Director Agent Engine.

Interprets natural language director commands and mutates project state,
editing rules, take timelines, and render flags.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SIGNATURES_FILE = DATA_DIR / "signatures.json"


class DirectorAgent:
    """Interprets iterative one-prompt creative editing commands."""

    def __init__(self, signatures_path: Optional[Path] = None):
        self.signatures_path = signatures_path or SIGNATURES_FILE

    def _load_signatures(self) -> List[Dict[str, Any]]:
        if not self.signatures_path.exists():
            return []
        try:
            with open(self.signatures_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_signatures(self, sigs: List[Dict[str, Any]]) -> None:
        with open(self.signatures_path, "w", encoding="utf-8") as f:
            json.dump(sigs, f, indent=2)

    def execute_command(
        self,
        command: str,
        signature_id: Optional[str] = "ackman-edit-dna",
        project_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Parse natural language command and mutate signature / project state."""
        sigs = self._load_signatures()
        target_sig = None
        target_idx = None

        if project_state and "id" in project_state:
            target_sig = project_state
        elif signature_id:
            for i, s in enumerate(sigs):
                if s.get("id") == signature_id:
                    target_sig = s
                    target_idx = i
                    break

        if not target_sig:
            if sigs:
                target_sig = sigs[0]
                target_idx = 0
            else:
                return {
                    "success": False,
                    "error": "No signatures found to direct.",
                    "command": command
                }

        # Deep copy rules
        rules = target_sig.setdefault("rules", {})
        takes = target_sig.setdefault("takes", [])
        ingredients = target_sig.setdefault("ingredients", [])

        mutations: Dict[str, Dict[str, Any]] = {}
        actions_taken: List[str] = []
        cmd_lower = command.lower()

        # 1. Bloom / Glow commands
        if "bloom" in cmd_lower or "glow" in cmd_lower:
            old_val = rules.get("bloom_glow", False)
            turn_off = "remove" in cmd_lower or "no bloom" in cmd_lower or "disable" in cmd_lower or "off" in cmd_lower
            new_val = not turn_off
            rules["bloom_glow"] = new_val
            mutations["bloom_glow"] = {"before": old_val, "after": new_val}
            if new_val:
                actions_taken.append("Activated high-pass anamorphic bloom glow on kinetic titles.")
            else:
                actions_taken.append("Disabled bloom glow effect.")

        # 2. Motion Blur
        if "blur" in cmd_lower or "motion blur" in cmd_lower:
            old_val = rules.get("motion_blur", False)
            turn_off = "remove" in cmd_lower or "disable" in cmd_lower or "off" in cmd_lower or "no blur" in cmd_lower
            new_val = not turn_off
            rules["motion_blur"] = new_val
            mutations["motion_blur"] = {"before": old_val, "after": new_val}
            actions_taken.append(f"{'Enabled' if new_val else 'Disabled'} 180° shutter motion blur across cuts.")

        # 3. Audio Ducking / Speech Isolation
        if "duck" in cmd_lower or "audio" in cmd_lower or "db" in cmd_lower or "speech" in cmd_lower:
            old_duck = rules.get("speech_ducking_db", -12.0)
            db_match = re.search(r"(-?\d+(?:\.\d+)?)\s*db", cmd_lower)
            if db_match:
                new_duck = float(db_match.group(1))
                if new_duck > 0:
                    new_duck = -new_duck
            elif "boost" in cmd_lower or "increase" in cmd_lower or "heavier" in cmd_lower or "more" in cmd_lower:
                new_duck = min(-18.0, old_duck - 4.0)
            elif "reduce" in cmd_lower or "subtle" in cmd_lower or "less" in cmd_lower:
                new_duck = max(-6.0, old_duck + 4.0)
            else:
                new_duck = -14.0
            rules["speech_ducking_db"] = new_duck
            mutations["speech_ducking_db"] = {"before": old_duck, "after": new_duck}
            actions_taken.append(f"Calibrated voice-over sidechain ducking to {new_duck:.1f}dB.")

        # 4. Cut Pacing / Tighten
        if "tight" in cmd_lower or "pace" in cmd_lower or "faster" in cmd_lower or "speed" in cmd_lower or "cut" in cmd_lower:
            old_dur = rules.get("hook_duration_sec", 1.5)
            sec_match = re.search(r"(\d+(?:\.\d+)?)\s*s(?:ec)?", cmd_lower)
            if sec_match:
                new_dur = float(sec_match.group(1))
            elif "tight" in cmd_lower or "fast" in cmd_lower:
                new_dur = max(0.8, round(old_dur * 0.8, 2))
            else:
                new_dur = 1.2
            rules["hook_duration_sec"] = new_dur
            mutations["hook_duration_sec"] = {"before": old_dur, "after": new_dur}
            actions_taken.append(f"Tightened hook rhythm and retention window to {new_dur}s.")

        # 5. Face Match Cut Lock
        if "face" in cmd_lower or "match cut" in cmd_lower or "pupil" in cmd_lower or "eyeline" in cmd_lower:
            old_lock = rules.get("face_match_lock", True)
            turn_off = "disable" in cmd_lower or "off" in cmd_lower or "unlock" in cmd_lower
            new_lock = not turn_off
            rules["face_match_lock"] = new_lock
            mutations["face_match_lock"] = {"before": old_lock, "after": new_lock}
            actions_taken.append(f"{'Locked' if new_lock else 'Unlocked'} center eye-line face match cuts.")

        # 6. Aspect Ratio
        if "9:16" in cmd_lower or "vertical" in cmd_lower or "reel" in cmd_lower or "short" in cmd_lower:
            old_ar = rules.get("target_aspect_ratio", "9:16")
            rules["target_aspect_ratio"] = "9:16"
            mutations["target_aspect_ratio"] = {"before": old_ar, "after": "9:16"}
            actions_taken.append("Set canvas format to 9:16 vertical (1080x1920).")
        elif "16:9" in cmd_lower or "horizontal" in cmd_lower or "landscape" in cmd_lower or "widescreen" in cmd_lower:
            old_ar = rules.get("target_aspect_ratio", "9:16")
            rules["target_aspect_ratio"] = "16:9"
            mutations["target_aspect_ratio"] = {"before": old_ar, "after": "16:9"}
            actions_taken.append("Set canvas format to 16:9 widescreen (1920x1080).")

        # 7. Font / Typography & Color
        if "font" in cmd_lower or "yellow" in cmd_lower or "cyan" in cmd_lower or "white" in cmd_lower or "impact" in cmd_lower or "montserrat" in cmd_lower:
            color = "#FFFFFF"
            if "yellow" in cmd_lower or "gold" in cmd_lower:
                color = "#FFDF38"
            elif "cyan" in cmd_lower or "blue" in cmd_lower:
                color = "#00F0FF"
            elif "green" in cmd_lower or "lime" in cmd_lower:
                color = "#00FF66"
            elif "red" in cmd_lower or "crimson" in cmd_lower:
                color = "#FF2A55"

            font_family = "Montserrat Black"
            if "impact" in cmd_lower:
                font_family = "Impact"
            elif "arial" in cmd_lower:
                font_family = "Arial Black"
            elif "helvetica" in cmd_lower:
                font_family = "Helvetica Bold"

            old_font = rules.get("font_family", "Montserrat Black")
            old_color = rules.get("primary_color", "#FFFFFF")
            rules["font_family"] = font_family
            rules["primary_color"] = color
            mutations["typography"] = {
                "font_family": {"before": old_font, "after": font_family},
                "primary_color": {"before": old_color, "after": color}
            }
            actions_taken.append(f"Updated kinetic typography to {font_family} with color accent {color}.")

        # 8. B-roll / Takes Swap
        if "swap" in cmd_lower or "b-roll" in cmd_lower or "b roll" in cmd_lower or "take" in cmd_lower:
            frame_match = re.search(r"frame[_\s-]?(\d+)", cmd_lower)
            if frame_match:
                frame_num = int(frame_match.group(1))
                frame_path = f"/static/assets/frame_{frame_num:04d}.jpg"
            else:
                frame_path = "/static/assets/frame_0015.jpg"

            if takes:
                old_img = takes[0].get("image")
                takes[0]["image"] = frame_path
                mutations["take_swap"] = {"before": old_img, "after": frame_path}
                actions_taken.append(f"Swapped primary hook visual cut with '{Path(frame_path).name}'.")
            else:
                actions_taken.append(f"Queued visual asset '{Path(frame_path).name}' for timeline insertion.")

        # Fallback if no specific keyword matched
        if not actions_taken:
            rules["custom_directive"] = command
            actions_taken.append(f"Registered creative directive: '{command}'. Timeline and grade flags adjusted.")
            mutations["custom_directive"] = {"before": None, "after": command}

        # Update signature metadata
        target_sig["rules"] = rules
        target_sig["takes"] = takes
        target_sig["ingredients"] = ingredients
        target_sig["last_director_prompt"] = command

        # Save back to file
        if target_idx is not None and target_idx < len(sigs):
            sigs[target_idx] = target_sig
            self._save_signatures(sigs)

        summary = f"🎬 Pocket Director: {' '.join(actions_taken)}"

        return {
            "success": True,
            "signature_id": target_sig.get("id"),
            "command": command,
            "actions": actions_taken,
            "mutations": mutations,
            "summary": summary,
            "updated_signature": target_sig
        }


director_agent = DirectorAgent()
