"""
Unit & Integration Tests for Dragon Studios AI Production Studio
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.database.db_manager import init_db, list_projects, get_project
from dragon_studios.agents.script_agent import generate_dark_psychology_script, generate_chitran_manga_script
from dragon_studios.agents.qa_agent import run_qa_check
from dragon_studios.agents.voice_agent import synthesize_speech
from dragon_studios.integrations.google_flow_adapter import GoogleFlowAdapter

class TestDragonStudios(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_script_generation_dark_psychology(self):
        plan = generate_dark_psychology_script()
        self.assertEqual(plan.pillar, "DARK_PSYCHOLOGY")
        self.assertTrue(len(plan.scenes) >= 3)
        self.assertIn("#DragonStudiosIndia", plan.hashtags)

    def test_script_generation_chitran(self):
        plan = generate_chitran_manga_script(chapter_number=1)
        self.assertEqual(plan.pillar, "ORIGINAL_MANGA")
        self.assertTrue(len(plan.scenes) >= 3)
        self.assertIn("AWAKENING", plan.title)

    def test_qa_validation_missing_file(self):
        report = run_qa_check("non_existent_file.mp4")
        self.assertFalse(report["passed"])
        self.assertEqual(report["score"], 0.0)

    def test_google_flow_prompt_optimization(self):
        adapter = GoogleFlowAdapter()
        opt = adapter.optimize_prompt_for_veo(
            scene_description="Warrior awakening dormant energy",
            camera_motion="low angle orbit"
        )
        self.assertIn("low angle orbit", opt["prompt"])
        self.assertIn("negative_prompt", opt)

    def test_google_flow_manifest_creation(self):
        adapter = GoogleFlowAdapter()
        scenes = [
            {"headline": "Scene 1", "subtext": "Opening hook", "camera_angle": "slow dolly in", "duration": 4.0},
            {"headline": "Scene 2", "subtext": "Climax confrontation", "camera_angle": "whip pan", "duration": 5.0}
        ]
        manifest = adapter.create_flow_project_manifest(
            project_id="test_flow_001",
            title="Test Flow Title",
            pillar="DARK_PSYCHOLOGY",
            scenes=scenes
        )
        self.assertEqual(manifest["total_shots"], 2)
        self.assertEqual(manifest["total_estimated_duration"], 9.0)
        self.assertEqual(manifest["timeline"][0]["duration_seconds"], 4.0)

    def test_clean_hook_agent(self):
        from dragon_studios.agents.clean_hook_agent import CleanHookAgent
        agent = CleanHookAgent()
        catalog = agent.load_catalog()
        self.assertTrue(len(catalog) >= 1)
        local_hooks = agent.list_local_hooks()
        self.assertTrue(len(local_hooks) >= 1)
        hook_path = agent.get_clean_hook()
        self.assertTrue(os.path.exists(hook_path))
        self.assertTrue(hook_path.endswith(".mp4"))

    def test_music_agent(self):
        from dragon_studios.agents.music_agent import MusicAgent
        agent = MusicAgent()
        catalog = agent.load_catalog()
        self.assertTrue(len(catalog) >= 10)
        local_tracks = agent.list_local_tracks()
        self.assertTrue(len(local_tracks) >= 5)
        track = agent.get_track_for_project("reel_test_001", pillar="DARK_PSYCHOLOGY")
        self.assertIsNotNone(track)
        self.assertTrue(os.path.exists(track))
        self.assertTrue(track.endswith(".mp3"))

if __name__ == "__main__":
    unittest.main()
