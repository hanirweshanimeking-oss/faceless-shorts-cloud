"""
Dragon Studios India - 10-Stage Autonomous Creator Studio Test Suite
Verifies: RESEARCH -> IDEATE -> SCRIPT -> STORYBOARD -> GENERATE -> EDIT -> REVIEW -> PUBLISH -> ANALYZE -> IMPROVE
"""

import os
import sys
import unittest
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.database.db_manager import init_db, list_projects, get_project
from dragon_studios.agents.research_agent import ResearchAgent
from dragon_studios.agents.ideate_agent import IdeateAgent
from dragon_studios.agents.script_agent import (
    generate_dark_psychology_script,
    generate_ai_tools_script,
    generate_chitran_manga_script
)
from dragon_studios.agents.storyboard_agent import StoryboardAgent
from dragon_studios.agents.generation_agent import GenerationEngine
from dragon_studios.agents.qa_agent import run_qa_check
from dragon_studios.agents.publishing_agent import PublishingAgent
from dragon_studios.agents.analytics_agent import evaluate_reels_performance
from dragon_studios.agents.improve_agent import ImproveAgent
from dragon_studios.pipeline.orchestrator import StudioOrchestrator

class TestCreatorStudio10Stages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_stage_1_research(self):
        agent = ResearchAgent()
        dossier = agent.conduct_research(topic="Video Editing", pillar="AI_TOOLS")
        self.assertEqual(dossier.pillar, "AI_TOOLS")
        self.assertTrue(len(dossier.proven_hooks) >= 2)
        self.assertGreaterEqual(dossier.market_opportunity_score, 5.0)

    def test_stage_2_ideate(self):
        concepts = IdeateAgent.brainstorm_concepts(topic="Mindset", pillar="DARK_PSYCHOLOGY")
        self.assertTrue(len(concepts) >= 2)
        self.assertGreaterEqual(concepts[0].viral_potential_score, 8.0)
        self.assertIn("THE", concepts[0].title)

    def test_stage_3_script(self):
        plan_ai = generate_ai_tools_script(title="NEVER PAY FOR VIDEO EDITING", topic="Video Pipeline")
        self.assertEqual(plan_ai.pillar, "AI_TOOLS")
        self.assertTrue(len(plan_ai.scenes) >= 3)

        plan_dp = generate_dark_psychology_script()
        self.assertEqual(plan_dp.pillar, "DARK_PSYCHOLOGY")
        self.assertIn("#DragonStudiosIndia", plan_dp.hashtags)

    def test_stage_4_storyboard(self):
        plan = generate_dark_psychology_script()
        storyboard = StoryboardAgent.generate_storyboard(plan)
        self.assertEqual(storyboard.aspect_ratio, "9:16")
        self.assertEqual(storyboard.resolution, "1080x1920")
        self.assertEqual(len(storyboard.panels), len(plan.scenes))
        self.assertIn("--ar 9:16", storyboard.panels[0].visual_prompt_midjourney)

    def test_stage_5_generate_canvas(self):
        frame = GenerationEngine.render_procedural_scene_frame(
            width=1080,
            height=1920,
            headline="RULE #1: ZERO REACTION",
            subtext="Silence is your weapon",
            pillar="DARK_PSYCHOLOGY",
            scene_num=1
        )
        self.assertEqual(frame.size, (1080, 1920))

    def test_stage_8_publishing_bundle(self):
        test_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
        bundle = PublishingAgent.prepare_release_bundle(
            project_id="test_bundle_proj",
            title="TEST VIDEO TITLE",
            pillar="DARK_PSYCHOLOGY",
            caption="Test Caption",
            hashtags="#Test",
            master_video_path="",
            output_dir=test_out
        )
        self.assertTrue(os.path.exists(bundle["bundle_dir"]))
        self.assertTrue(os.path.exists(bundle["copy_paste_file"]))

    def test_stage_9_and_10_analytics_and_improve(self):
        metrics = evaluate_reels_performance(
            views=10000, reach=9000, likes=1200, comments=50,
            shares=250, saves=350, watch_time_seconds=20.0, video_duration=24.0
        )
        self.assertGreater(metrics["overall_score"], 0)

        feedback = ImproveAgent.analyze_and_optimize(
            project_id="test_proj_analytics",
            analytics_data=metrics,
            pillar="DARK_PSYCHOLOGY"
        )
        self.assertTrue(len(feedback.next_topic_recommendation) > 5)
        self.assertTrue(feedback.recommended_duration_seconds > 0)

    def test_full_10_stage_integration_run(self):
        orchestrator = StudioOrchestrator()
        result = orchestrator.execute_10_stage_run(
            topic="Cold Stoicism & Power",
            pillar="DARK_PSYCHOLOGY",
            auto_approve=True
        )
        self.assertEqual(len(result["stages_completed"]), 10)
        self.assertTrue(result["stages_completed"][0] == "STAGE_1_RESEARCH")
        self.assertTrue(result["stages_completed"][-1] == "STAGE_10_IMPROVE")
        self.assertTrue(os.path.exists(result["master_video_path"]))
        self.assertTrue(os.path.exists(result["capcut_draft"]))

if __name__ == "__main__":
    unittest.main()
