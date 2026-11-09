"""
Tests for Dragon Studios Higgsfield Integration
Validates WebGPU scene construction, physical materials, 38-model catalog adapter,
faceless video blueprint generation, and fallback rendering.
"""

import os
import sys
import unittest
import tempfile
import shutil
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.agents.higgsfield_engine import HiggsfieldWebGPUEngine
from dragon_studios.agents.higgsfield_skills import HiggsfieldSkillsAdapter
from dragon_studios.agents.generation_agent import GenerationEngine

class TestHiggsfieldIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.gpu_engine = HiggsfieldWebGPUEngine()
        self.skills_adapter = HiggsfieldSkillsAdapter()
        self.gen_engine = GenerationEngine()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_engine_scene_blueprint_dark_psychology(self):
        scene = self.gpu_engine.build_cinematic_scene(
            pillar="DARK_PSYCHOLOGY",
            scene_num=1,
            width=540,
            height=960,
            spp=16
        )
        self.assertEqual(scene["version"], 1)
        self.assertEqual(scene["render"]["width"], 540)
        self.assertEqual(scene["render"]["height"], 960)
        self.assertEqual(scene["render"]["post"]["tonemap"], "agx")
        self.assertTrue(len(scene["materials"]) >= 2)
        self.assertTrue(len(scene["meshes"]) >= 2)
        self.assertTrue(len(scene["lights"]) >= 2)
        self.assertIn("environment", scene)

    def test_engine_scene_blueprint_ai_tools(self):
        scene = self.gpu_engine.build_cinematic_scene(
            pillar="AI_TOOLS",
            scene_num=2,
            width=540,
            height=960,
            spp=16
        )
        self.assertEqual(scene["render"]["width"], 540)
        self.assertEqual(scene["render"]["height"], 960)
        self.assertTrue(any("transmission" in m for m in scene["materials"]))

    def test_engine_scene_blueprint_original_manga(self):
        scene = self.gpu_engine.build_cinematic_scene(
            pillar="ORIGINAL_MANGA",
            scene_num=3,
            width=540,
            height=960,
            spp=16
        )
        self.assertEqual(scene["render"]["width"], 540)
        self.assertEqual(scene["render"]["height"], 960)
        self.assertEqual(len(scene["meshes"]), 3)

    def test_composite_frame_generation_with_fallback(self):
        out_png = os.path.join(self.temp_dir, "test_composite.png")
        # Run with allow_webgpu=False to test instant deterministic fallback rendering
        result_path = self.gpu_engine.render_composite_frame(
            headline="THE SILENT GAZE",
            subtext="Power is demonstrated in stillness.",
            pillar="DARK_PSYCHOLOGY",
            scene_num=1,
            output_path=out_png,
            allow_webgpu=False
        )
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(os.path.getsize(result_path) > 5000)

    def test_model_catalog_filtering(self):
        all_models = self.skills_adapter.get_catalog_models()
        video_models = self.skills_adapter.get_catalog_models(kind="video")
        image_models = self.skills_adapter.get_catalog_models(kind="image")

        self.assertGreaterEqual(len(all_models), 15)
        self.assertGreaterEqual(len(video_models), 10)
        self.assertGreaterEqual(len(image_models), 5)

        model_ids = [m.id for m in all_models]
        self.assertIn("soul-2", model_ids)
        self.assertIn("kling-3-pro", model_ids)
        self.assertIn("wan-3-prime", model_ids)
        self.assertIn("flux-2", model_ids)

    def test_faceless_video_blueprint_manifest(self):
        sample_scenes = [
            {"duration_seconds": 4.0, "subtitle_text": "HOOK OF CURIOSITY", "dialogue": "Notice how they speak."},
            {"duration_seconds": 5.0, "subtitle_text": "THE PSYCHOLOGICAL PIVOT", "dialogue": "Observe the reaction."}
        ]
        manifest = self.skills_adapter.build_faceless_video_blueprint(
            topic="Power Dynamics in Negotiation",
            pillar="DARK_PSYCHOLOGY",
            scenes=sample_scenes,
            model_id="soul-2"
        )
        self.assertEqual(manifest["project_type"], "higgsfield_faceless_explainer")
        self.assertEqual(manifest["total_blocks"], 2)
        self.assertEqual(manifest["total_duration_seconds"], 9.0)
        self.assertEqual(manifest["aspect_ratio"], "9:16")
        self.assertGreater(manifest["estimated_credits"], 0)
        self.assertIn("blocks", manifest)
        self.assertEqual(manifest["blocks"][0]["model"], "soul-2")

    def test_budget_estimation(self):
        budget = self.skills_adapter.estimate_production_budget(scene_count=4, model_id="kling-3-pro")
        self.assertEqual(budget["model_id"], "kling-3-pro")
        self.assertEqual(budget["scene_count"], 4)
        self.assertEqual(budget["estimated_credits"], 12.0)
        self.assertGreater(budget["cost_usd"], 0)
        self.assertGreater(budget["cost_inr"], 0)
        self.assertIn("Local GPU", budget["zero_cost_local_alternative"])

    def test_generation_engine_integration(self):
        # Test GenerationEngine renders scene frames using procedural fallback or WebGPU
        frame = self.gen_engine.render_scene_frame(
            headline="NEURAL SYNERGY",
            subtext="Autonomous systems collaborating in harmony.",
            pillar="AI_TOOLS",
            scene_num=1,
            width=1080,
            height=1920,
            use_higgsfield_webgpu=False
        )
        self.assertIsNotNone(frame)
        self.assertEqual(frame.size, (1080, 1920))

if __name__ == "__main__":
    unittest.main()
