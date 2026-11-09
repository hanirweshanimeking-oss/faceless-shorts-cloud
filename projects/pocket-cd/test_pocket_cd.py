"""Pocket Creator Director (Pocket CD) - End-to-End Verification Test Suite.

Tests all engines, REST API endpoints, FFmpeg rendering, and script exports.
Must pass with exit code 0.
"""

import asyncio
import json
import os
import sys
import unittest
from pathlib import Path

# Force utf-8 encoding for Windows console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from server import app
from engine.dna_extractor import dna_extractor, INGREDIENT_TEMPLATES
from engine.director_agent import director_agent
from engine.storyteller import storyteller
from engine.compositor import compositor
from engine.exporters import exporters

client = TestClient(app)


class TestPocketCreatorDirector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n========================================================")
        print("🧪 RUNNING POCKET CREATOR DIRECTOR VERIFICATION SUITE")
        print("========================================================")

    # -------------------------------------------------------------
    # 1. DNA Extractor Tests
    # -------------------------------------------------------------
    def test_01_dna_extractor_prompt(self):
        print("\n[TEST 1] DNA Extractor: Prompt Decompilation...")
        prompt = "High contrast finance documentary with yellow kinetic titles and face match cuts"
        sig = dna_extractor.extract_from_prompt(prompt, title="Wall Street Bio Test")

        self.assertIsNotNone(sig)
        self.assertEqual(sig.get("title"), "Wall Street Bio Test")
        self.assertEqual(len(sig.get("ingredients", [])), 11)
        self.assertTrue(sig.get("rules", {}).get("bloom_glow"))
        self.assertEqual(sig.get("rules", {}).get("target_aspect_ratio"), "9:16")

        # Verify all 11 canonical ingredients exist
        names = [ing["title"] for ing in sig["ingredients"]]
        self.assertTrue(any("Flash Open" in n for n in names))
        self.assertTrue(any("Poster Title Punch" in n for n in names))
        self.assertTrue(any("Screen Name Reveal" in n for n in names))
        self.assertTrue(any("Difference Pull Back" in n for n in names))
        self.assertTrue(any("Face Match Cut" in n for n in names))
        self.assertTrue(any("Grid Cut List" in n for n in names))
        self.assertTrue(any("Quantity Or Quality" in n for n in names))
        self.assertTrue(any("Flip Stack" in n for n in names))
        self.assertTrue(any("Viewfinder REC" in n for n in names))
        self.assertTrue(any("Counter Rate" in n for n in names))
        self.assertTrue(any("Granular SFX" in n for n in names))
        print("   ✅ Extracted all 11 modular ingredients successfully.")

    def test_02_dna_extractor_video(self):
        print("\n[TEST 2] DNA Extractor: Video Decompilation...")
        sig = dna_extractor.decompile(video_path="ackman_reference.mp4", title="Ackman Reference Test")
        self.assertIsNotNone(sig)
        self.assertEqual(len(sig.get("ingredients", [])), 11)
        self.assertIn("video_meta", sig)
        print(f"   ✅ Video probed: {sig['video_meta'].get('width')}x{sig['video_meta'].get('height')} @ {sig['video_meta'].get('fps')}fps")

    # -------------------------------------------------------------
    # 2. Director Agent Tests
    # -------------------------------------------------------------
    def test_03_director_agent_commands(self):
        print("\n[TEST 3] Director Agent: Natural Language Commands...")
        # Command 1: Add intense bloom
        res1 = director_agent.execute_command("Add intense bloom and neon yellow subtitles", signature_id="ackman-edit-dna")
        self.assertTrue(res1.get("success"))
        self.assertTrue(res1["updated_signature"]["rules"]["bloom_glow"])
        self.assertEqual(res1["updated_signature"]["rules"]["primary_color"], "#FFDF38")

        # Command 2: Tighten cuts to 0.8s
        res2 = director_agent.execute_command("Tighten cuts to 0.8s", signature_id="ackman-edit-dna")
        self.assertTrue(res2.get("success"))
        self.assertEqual(res2["updated_signature"]["rules"]["hook_duration_sec"], 0.8)

        # Command 3: Set ducking to -15dB
        res3 = director_agent.execute_command("Increase speech ducking to -15dB", signature_id="ackman-edit-dna")
        self.assertTrue(res3.get("success"))
        self.assertEqual(res3["updated_signature"]["rules"]["speech_ducking_db"], -15.0)

        # Command 4: Swap B-roll with frame 0015
        res4 = director_agent.execute_command("Swap B-roll with frame 0015", signature_id="ackman-edit-dna")
        self.assertTrue(res4.get("success"))
        self.assertIn("frame_0015.jpg", res4["updated_signature"]["takes"][0]["image"])
        print(f"   ✅ Director Agent executed 4 iterative mutations with voice feedback: {res4.get('summary')}")

    # -------------------------------------------------------------
    # 3. Storyteller & Voice Engine Tests
    # -------------------------------------------------------------
    def test_04_storyteller_script_generation(self):
        print("\n[TEST 4] Storyteller: ElevenLabs V4 Script Generation...")
        script = storyteller.generate_vsl_script(
            topic="Pocket Creator Director Launch",
            style="carl_voice",
            target_duration_sec=22
        )
        self.assertIsNotNone(script)
        self.assertIn("[emotion:", script["content"])
        self.assertIn("[pause:", script["content"])
        self.assertEqual(script["model"], "ElevenLabs v4")
        print("   ✅ ElevenLabs V4 script formatted with pauses and emotion brackets.")

    def test_05_storyteller_voice_synthesis(self):
        print("\n[TEST 5] Storyteller: Edge-TTS Neural Synthesis...")
        text = "Hello Carl, relaxed hi. Pocket Creative Director is active and operational."
        res = storyteller.synthesize_speech(
            text=text,
            voice_key="carl",
            output_filename="test_verification_narration.mp3"
        )
        self.assertTrue(res.get("success"))
        audio_file = Path(res.get("absolute_path"))
        self.assertTrue(audio_file.exists())
        self.assertGreater(audio_file.stat().st_size, 5000)
        print(f"   ✅ Synthesized MP3 ({audio_file.stat().st_size} bytes): {audio_file.name}")

    # -------------------------------------------------------------
    # 4. Gyan FFmpeg Compositor Tests
    # -------------------------------------------------------------
    def test_06_compositor_real_render(self):
        print("\n[TEST 6] Gyan FFmpeg Compositor: 9:16 Vertical Reel Rendering...")
        res = compositor.render_vertical_reel(
            signature_id="ackman-edit-dna",
            title_text="AUTONOMOUS REEL",
            subtitle_text="POCKET CREATOR DIRECTOR",
            counter_label="VALUATION",
            target_value=2500000000,
            duration_sec=3.0,
            resolution="720x1280",
            fps=30,
            rules={
                "bloom_glow": True,
                "motion_blur": True,
                "speech_ducking_db": -12.0,
                "hook_duration_sec": 0.8,
                "primary_color": "#FFDF38"
            }
        )
        self.assertTrue(res.get("success"), msg=res.get("error"))
        mp4_path = Path(res.get("render_path"))
        self.assertTrue(mp4_path.exists())
        self.assertGreater(mp4_path.stat().st_size, 10000)
        print(f"   ✅ Composited MP4 reel: {mp4_path.name} ({res.get('size_mb')} MB) in {res.get('render_time_sec')}s")

    # -------------------------------------------------------------
    # 5. Multi-Engine Exporters Tests
    # -------------------------------------------------------------
    def test_07_exporters(self):
        print("\n[TEST 7] Multi-Engine Exporters: JSX, Python, Lua, JSON...")
        sample_sig = {
            "id": "test_sig_export",
            "title": "Test Signature Reel",
            "rules": {"bloom_glow": True, "motion_blur": True, "speech_ducking_db": -14.0}
        }
        # JSX
        jsx_path = Path(exporters.generate_after_effects_jsx(sample_sig))
        self.assertTrue(jsx_path.exists())
        with open(jsx_path, "r", encoding="utf-8") as f:
            jsx_content = f.read()
        self.assertIn("app.beginUndoGroup", jsx_content)
        self.assertIn("ADBE Glow2", jsx_content)

        # Python Resolve
        py_path = Path(exporters.generate_davinci_resolve_py(sample_sig))
        self.assertTrue(py_path.exists())
        with open(py_path, "r", encoding="utf-8") as f:
            py_content = f.read()
        self.assertIn("DaVinciResolveScript", py_content)
        self.assertIn("1080x1920", py_content)

        # Lua REAPER
        lua_path = Path(exporters.generate_reaper_lua(sample_sig))
        self.assertTrue(lua_path.exists())
        with open(lua_path, "r", encoding="utf-8") as f:
            lua_content = f.read()
        self.assertIn("ReaComp (Cockos)", lua_content)
        self.assertIn("reaper.Undo_BeginBlock()", lua_content)

        # JSON Manifest
        json_path = Path(exporters.generate_style_dna_manifest_json(sample_sig))
        self.assertTrue(json_path.exists())
        print(f"   ✅ Exported After Effects JSX, DaVinci Python, REAPER Lua, and JSON Manifest.")

    # -------------------------------------------------------------
    # 6. REST API Endpoints Tests
    # -------------------------------------------------------------
    def test_08_rest_api_endpoints(self):
        print("\n[TEST 8] FastAPI REST API Endpoints Verification...")

        # GET /api/health
        r = client.get("/api/health")
        self.assertEqual(r.status_code, 200)

        # GET /
        r_index = client.get("/")
        self.assertEqual(r_index.status_code, 200)
        self.assertIn("Pocket Creator Director", r_index.text)

        # GET /api/signatures
        r = client.get("/api/signatures")
        self.assertEqual(r.status_code, 200)
        sigs = r.json()
        self.assertGreater(len(sigs), 0)

        # GET /api/signatures/{id}
        sig_id = sigs[0]["id"]
        r = client.get(f"/api/signatures/{sig_id}")
        self.assertEqual(r.status_code, 200)

        # POST /api/signatures/{id}/rules
        r = client.post(f"/api/signatures/{sig_id}/rules", json={"rules": {"motion_blur": True, "speech_ducking_db": -13.5}})
        self.assertEqual(r.status_code, 200)

        # GET /api/library & POST /api/library
        r = client.get("/api/library")
        self.assertEqual(r.status_code, 200)
        r = client.post("/api/library", json={
            "title": "API Test Item",
            "category": "Sound",
            "type": "SFX Preset",
            "description": "Test verification item"
        })
        self.assertEqual(r.status_code, 201)

        # GET /api/scripts & POST /api/scripts/generate
        r = client.get("/api/scripts")
        self.assertEqual(r.status_code, 200)
        r = client.post("/api/scripts/generate", json={"topic": "REST API Test VSL", "style": "carl_voice"})
        self.assertEqual(r.status_code, 201)

        # POST /api/voice/synthesize
        r = client.post("/api/voice/synthesize", json={"text": "Quick API voice test", "voice": "carl"})
        self.assertEqual(r.status_code, 200)

        # GET /api/boards & POST /api/boards/{id}/cards
        r = client.get("/api/boards")
        self.assertEqual(r.status_code, 200)
        r = client.post("/api/boards/board_1/cards", json={"title": "Test Card", "type": "notes", "content": "Sample note"})
        self.assertEqual(r.status_code, 201)

        # POST /api/dna/extract
        r = client.post("/api/dna/extract", json={"prompt": "Rapid fire commercial reel with strobe flash"})
        self.assertEqual(r.status_code, 200)

        # POST /api/director/command
        r = client.post("/api/director/command", json={"command": "Tighten cuts and add bloom", "signature_id": sig_id})
        self.assertEqual(r.status_code, 200)

        # POST /api/render
        r = client.post("/api/render", json={
            "signature_id": sig_id,
            "title_text": "API VERIFICATION",
            "duration_sec": 2.0,
            "resolution": "720x1280"
        })
        self.assertEqual(r.status_code, 200)

        # GET /api/export/{format}/{signature_id}
        for fmt in ["jsx", "py", "lua", "json"]:
            r = client.get(f"/api/export/{fmt}/{sig_id}")
            self.assertEqual(r.status_code, 200, msg=f"Failed for format: {fmt}")

        print("   ✅ All REST API endpoints passed with code 200/201.")


if __name__ == "__main__":
    unittest.main()
