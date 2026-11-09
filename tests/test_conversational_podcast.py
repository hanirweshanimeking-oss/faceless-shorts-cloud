"""
Tests for Conversational Podcast & Interrogation Video Pipeline Pillar (Raj Shamani Format).
"""

import unittest
import os
import shutil
from dragon_studios.agents.script_agent import (
    generate_conversational_podcast_script,
    VideoProductionPlan
)
from dragon_studios.agents.generation_agent import GenerationEngine
from dragon_studios.pipeline.orchestrator import StudioOrchestrator

class TestConversationalPodcastPipeline(unittest.TestCase):
    def test_conversational_script_generation(self):
        plan: VideoProductionPlan = generate_conversational_podcast_script(
            title="IS YOUR FIRST 1 CRORE WORTHLESS?",
            topic="The First Crore Wealth Trap"
        )
        self.assertEqual(plan.pillar, "CONVERSATIONAL_PODCAST")
        self.assertGreaterEqual(len(plan.scenes), 5)
        self.assertIn("CRORE", plan.hook.upper())
        self.assertIn("FiguringOut", plan.hashtags)
        self.assertIn("DROP", plan.scenes[-1].subtitle_text.upper())

    def test_procedural_frame_conversational_gold(self):
        engine = GenerationEngine()
        img = engine.render_procedural_scene_frame(
            headline="WAIT... IS 1 CRORE WORTHLESS?",
            subtext="Look at the math. In Mumbai or Delhi, one crore gets you half an apartment.",
            pillar="CONVERSATIONAL_PODCAST",
            scene_num=1
        )
        self.assertEqual(img.size, (1080, 1920))

    def test_orchestrator_integration_conversational(self):
        orchestrator = StudioOrchestrator()
        result = orchestrator.execute_10_stage_run(
            topic="Is Your First Crore Overrated?",
            pillar="CONVERSATIONAL_PODCAST",
            auto_approve=True
        )
        self.assertIn("STAGE_1_RESEARCH", result["stages_completed"])
        self.assertIn("STAGE_3_SCRIPT", result["stages_completed"])
        self.assertIn("STAGE_5_GENERATE", result["stages_completed"])
        self.assertIn("STAGE_6_EDIT", result["stages_completed"])
        self.assertTrue(os.path.exists(result["master_video_path"]))
        self.assertGreater(os.path.getsize(result["master_video_path"]), 1000)

if __name__ == "__main__":
    unittest.main()
