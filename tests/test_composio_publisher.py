"""
Tests for Dragon Studios Composio Multi-Platform Publisher & Alert Hub
"""

import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.agents.composio_publisher import ComposioPublisherHub, ComposioPublishResult
from dragon_studios.agents.publishing_agent import PublishingAgent

class TestComposioPublisher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.hub = ComposioPublisherHub()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_composio_status_detection(self):
        status = self.hub.check_status()
        self.assertTrue(status["composio_sdk_installed"])
        self.assertIn("api_key_configured", status)
        self.assertIn("discord_webhook_configured", status)
        self.assertIn("slack_webhook_configured", status)
        self.assertIn("notion_database_configured", status)

    def test_youtube_shorts_fallback_payload(self):
        dummy_video = os.path.join(self.temp_dir, "test_video.mp4")
        with open(dummy_video, "w") as f:
            f.write("dummy video data")

        res = self.hub.publish_youtube_shorts(
            video_path=dummy_video,
            title="Cold Stoicism & Power",
            description="The ego is fragile.",
            tags=["Dark Psychology", "Anime"]
        )

        self.assertTrue(res.success)
        self.assertEqual(res.platform, "YOUTUBE_SHORTS")
        self.assertTrue(res.fallback_used)
        self.assertIn("#Shorts", res.response_data["title"])
        self.assertEqual(res.response_data["privacy_status"], "public")

    def test_instagram_reel_fallback_payload(self):
        dummy_video = os.path.join(self.temp_dir, "test_video.mp4")
        with open(dummy_video, "w") as f:
            f.write("dummy video data")

        res = self.hub.publish_instagram_reel(
            video_path=dummy_video,
            caption="Rule #1: Zero Reaction",
            hashtags="#DarkPsychology #DragonStudios"
        )

        self.assertTrue(res.success)
        self.assertEqual(res.platform, "INSTAGRAM_REELS")
        self.assertTrue(res.fallback_used)
        self.assertIn("Rule #1: Zero Reaction", res.response_data["caption"])
        self.assertIn("#DarkPsychology", res.response_data["caption"])

    def test_notion_sync_payload(self):
        res = self.hub.sync_to_notion(
            project_id="PROJ_TEST_NOTION",
            title="THE ART OF COLD APATHY",
            pillar="DARK_PSYCHOLOGY",
            concept="Ego breakdown",
            hook="Silence is lethal.",
            master_video_path="output/master.mp4",
            qa_score=94.5
        )

        self.assertTrue(res.success)
        self.assertEqual(res.platform, "NOTION")
        self.assertEqual(res.response_data["project_id"], "PROJ_TEST_NOTION")
        self.assertEqual(res.response_data["qa_score"], 94.5)

    @patch("requests.post")
    def test_discord_alert_webhook_success(self, mock_post):
        mock_post.return_value = MagicMock(status_code=204)
        res = self.hub.send_discord_alert(
            project_id="PROJ_DISCORD_01",
            title="COLD SILENCE",
            qa_score=92.0,
            pillar="DARK_PSYCHOLOGY",
            video_path="output/master.mp4",
            webhook_url="https://discord.com/api/webhooks/mock"
        )
        self.assertTrue(res.success)
        self.assertEqual(res.platform, "DISCORD")
        self.assertFalse(res.fallback_used)
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_slack_alert_webhook_success(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        res = self.hub.send_slack_alert(
            project_id="PROJ_SLACK_01",
            title="COLD SILENCE",
            qa_score=92.0,
            pillar="DARK_PSYCHOLOGY",
            video_path="output/master.mp4",
            webhook_url="https://hooks.slack.com/services/mock"
        )
        self.assertTrue(res.success)
        self.assertEqual(res.platform, "SLACK")
        self.assertFalse(res.fallback_used)
        mock_post.assert_called_once()

    def test_syndicate_all_end_to_end(self):
        dummy_video = os.path.join(self.temp_dir, "master.mp4")
        with open(dummy_video, "w") as f:
            f.write("mock video bytes")

        res = self.hub.syndicate_all(
            project_id="PROJ_SYNDICATE_TEST",
            title="CHITRAN: CHAPTER ONE",
            pillar="ORIGINAL_MANGA",
            caption="The seal has fractured.",
            hashtags="#DragonStudios #Anime",
            master_video_path=dummy_video,
            qa_score=96.0,
            output_dir=self.temp_dir
        )

        self.assertIn("youtube_shorts", res)
        self.assertIn("instagram_reels", res)
        self.assertIn("notion", res)
        self.assertIn("discord", res)
        self.assertIn("slack", res)
        self.assertTrue(os.path.exists(res["manifest_path"]))

    def test_publishing_agent_integration(self):
        dummy_video = os.path.join(self.temp_dir, "master.mp4")
        with open(dummy_video, "w") as f:
            f.write("mock video bytes")

        bundle = PublishingAgent.prepare_release_bundle(
            project_id="PROJ_AGENT_TEST",
            title="NEVER PAY FOR VIDEO EDITING",
            pillar="AI_TOOLS",
            caption="Stop paying monthly subscriptions.",
            hashtags="#AITools #Code",
            master_video_path=dummy_video,
            output_dir=self.temp_dir,
            qa_score=98.0
        )

        self.assertEqual(bundle["status"], "PACKAGED_FOR_DISTRIBUTION")
        self.assertIn("composio_syndication", bundle)
        self.assertIn("NOTION", bundle["platforms"])
        self.assertIn("DISCORD", bundle["platforms"])

if __name__ == "__main__":
    unittest.main()
