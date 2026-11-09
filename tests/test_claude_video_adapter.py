"""
Tests for Dragon Studios Claude-Video (/watch) Perception Adapter & System Integrations.
Validates AI video perception, frame extraction, viral deconstruction,
QA visual inspection, and research agent integration.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.integrations.claude_video_adapter import (
    ClaudeVideoAdapter,
    VideoPerceptionDossier
)
from dragon_studios.integrations import get_integrations_health_check
from dragon_studios.agents.research_agent import ResearchAgent
from dragon_studios.agents.qa_agent import run_qa_check

SAMPLE_VIDEO = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "output", "viral_edits", "nikhil_kamath_viral_edit.mp4")
)


class TestClaudeVideoAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = ClaudeVideoAdapter()

    def test_claude_video_readiness(self):
        """Verifies that the claude-video engine and system tools (ffmpeg, ffprobe) are ready."""
        readiness = self.adapter.check_readiness()
        self.assertTrue(readiness["ready"])
        self.assertIn("tools", readiness)
        self.assertIn("ffmpeg", readiness["tools"])
        self.assertTrue(readiness["tools"]["ffmpeg"]["ok"])

    def test_watch_local_video_perception(self):
        """Verifies watching a real vertical reel extracts timestamped frames and metadata."""
        if not os.path.exists(SAMPLE_VIDEO):
            self.skipTest(f"Sample video not found at {SAMPLE_VIDEO}")

        dossier = self.adapter.watch(SAMPLE_VIDEO, detail="efficient", max_frames=4)

        self.assertIsInstance(dossier, VideoPerceptionDossier)
        self.assertEqual(dossier.status, "success")
        self.assertGreater(dossier.duration_seconds, 20.0)
        self.assertTrue("1080x1920" in dossier.resolution or "1920" in dossier.resolution)
        self.assertGreater(dossier.frame_count, 0)
        self.assertEqual(len(dossier.frames), dossier.frame_count)

        # Verify frame file exists
        first_frame = dossier.frames[0]
        self.assertTrue(os.path.exists(first_frame.path))
        self.assertIsNotNone(first_frame.timestamp)

    def test_watch_resilient_error_handling(self):
        """Verifies that invalid files fail gracefully without raising uncaught exceptions."""
        dossier = self.adapter.watch("non_existent_fake_video.mp4")

        self.assertIsInstance(dossier, VideoPerceptionDossier)
        self.assertEqual(dossier.status, "error")
        self.assertIsNotNone(dossier.error_message)

    def test_deconstruct_for_recreation(self):
        """Verifies reverse-engineering video pacing into a blueprint with scene breakdowns."""
        if not os.path.exists(SAMPLE_VIDEO):
            self.skipTest(f"Sample video not found at {SAMPLE_VIDEO}")

        blueprint = self.adapter.deconstruct_for_recreation(SAMPLE_VIDEO)

        self.assertIn("total_duration_seconds", blueprint)
        self.assertGreater(blueprint["total_duration_seconds"], 20.0)
        self.assertIn("average_seconds_per_shot", blueprint)
        self.assertGreater(blueprint["average_seconds_per_shot"], 0)
        self.assertIn("pacing_category", blueprint)
        self.assertIn("reconstructed_scenes", blueprint)
        self.assertGreater(len(blueprint["reconstructed_scenes"]), 0)
        self.assertIn("recreation_strategy", blueprint)
        self.assertIn("hook_rule", blueprint["recreation_strategy"])

    def test_research_agent_with_video_perception(self):
        """Verifies that Stage 1 ResearchAgent can research directly from a video file."""
        if not os.path.exists(SAMPLE_VIDEO):
            self.skipTest(f"Sample video not found at {SAMPLE_VIDEO}")

        agent = ResearchAgent()
        dossier = agent.research_video(SAMPLE_VIDEO)

        self.assertIsNotNone(dossier.topic)
        self.assertGreaterEqual(len(dossier.proven_hooks), 3)
        self.assertGreaterEqual(len(dossier.suggested_angles), 3)
        self.assertGreaterEqual(len(dossier.reference_reels), 1)
        self.assertEqual(dossier.reference_reels[0].url, SAMPLE_VIDEO)

    def test_qa_agent_visual_perception(self):
        """Verifies that Stage 7 QA Agent includes visual perception verification in reports."""
        if not os.path.exists(SAMPLE_VIDEO):
            self.skipTest(f"Sample video not found at {SAMPLE_VIDEO}")

        qa_report = run_qa_check(SAMPLE_VIDEO)

        self.assertIn("visual_inspection", qa_report)
        inspection = qa_report["visual_inspection"]
        self.assertTrue(inspection["verified"])
        self.assertGreater(inspection["frame_count"], 0)
        self.assertGreater(len(inspection["sample_frames"]), 0)

    def test_integrations_health_check_includes_claude_video(self):
        """Verifies that the unified ecosystem hub includes claude-video and reports 14/14 ready."""
        health = get_integrations_health_check()
        self.assertEqual(health["total_repositories"], 14)
        self.assertEqual(health["installed_count"], 14)
        self.assertTrue(health["all_ready"])
        self.assertIn("claude-video", health["repositories"])
        self.assertTrue(health["repositories"]["claude-video"]["installed"])


if __name__ == "__main__":
    unittest.main()
