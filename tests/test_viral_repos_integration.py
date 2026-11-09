"""
Dragon Studios India - Tests for 12 Integrated Viral Repositories
Validates ReelMimic, Hypit SVML, Paradee 1.2 TTS, Virality Predictor, and OpenMontage adapters.
"""

import os
import sys
import unittest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.integrations.reelmimic_adapter import ReelMimicAdapter
from dragon_studios.integrations.hypit_adapter import HypitAdapter
from dragon_studios.integrations.paradee_voice import ParadeeVoiceEngine
from dragon_studios.integrations.virality_predictor import ViralityPredictorEngine
from dragon_studios.integrations.openmontage_adapter import OpenMontageAdapter
from dragon_studios.integrations import get_integrations_health_check

class TestViralReposIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.reelmimic = ReelMimicAdapter()
        self.hypit = HypitAdapter()
        self.paradee = ParadeeVoiceEngine()
        self.predictor = ViralityPredictorEngine()
        self.openmontage = OpenMontageAdapter()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reelmimic_deconstruction(self):
        blueprint = self.reelmimic.deconstruct_viral_style(
            reference_topic="The Art of Stoic Silence",
            pillar="DARK_PSYCHOLOGY"
        )
        self.assertEqual(blueprint.total_shots, 5)
        self.assertGreater(blueprint.total_duration_seconds, 20.0)
        self.assertIn("Obsidian", blueprint.dominant_color_mood)
        self.assertIn("orbital_push", [s.camera_movement for s in blueprint.shots])
        self.assertTrue(len(blueprint.reusable_prompt_formula) > 20)

    def test_hypit_svml_conversion(self):
        dialogue = "Never let an enemy see you react. Silence is your greatest weapon."
        scene = self.hypit.convert_to_svml(
            scene_index=1,
            dialogue=dialogue,
            duration=4.5,
            pillar="DARK_PSYCHOLOGY"
        )
        self.assertEqual(scene.scene_index, 1)
        self.assertEqual(scene.duration_seconds, 4.5)
        self.assertGreaterEqual(len(scene.word_nodes), 10)
        # Verify emphasis on power words like 'never' and 'silence'
        emphasized = [wn.word.lower().strip(".,") for wn in scene.word_nodes if wn.emphasis]
        self.assertIn("never", emphasized)
        self.assertIn("silence", emphasized)

    def test_hypit_viral_variants(self):
        variants = self.hypit.generate_viral_variants(
            base_topic="Psychological Manipulation in Office Politics",
            pillar="DARK_PSYCHOLOGY"
        )
        self.assertEqual(len(variants), 4)
        types = [v.hook_type for v in variants]
        self.assertIn("curiosity_gap", types)
        self.assertIn("confrontational", types)
        self.assertIn("identity_threat", types)
        self.assertIn("data_driven", types)

    def test_paradee_voices_registry(self):
        voices = self.paradee.list_voices()
        self.assertEqual(len(voices), 4)
        self.assertIn("af_heart", voices)
        self.assertIn("am_puck", voices)
        self.assertIn("bf_isabella", voices)
        self.assertIn("bm_fable", voices)

    def test_virality_predictor(self):
        forecast = self.predictor.predict(
            title="How to Destroy an Enemy with Silence",
            hook_text="If you react to an insult, you have already lost the war.",
            pillar="DARK_PSYCHOLOGY"
        )
        self.assertGreaterEqual(forecast.viral_potential_score, 7.0)
        self.assertGreaterEqual(forecast.predicted_3s_hold_rate, 60.0)
        self.assertGreater(forecast.hook_strength_score, 60.0)
        self.assertTrue(len(forecast.optimization_recommendations) >= 1)

    def test_openmontage_pipelines(self):
        pipelines = self.openmontage.list_pipelines()
        self.assertEqual(len(pipelines), 4)
        pipeline_ids = [p.pipeline_id for p in pipelines]
        self.assertIn("sci_fi_cinematic_trailer", pipeline_ids)
        self.assertIn("animated_explainer_3d", pipeline_ids)
        self.assertIn("dark_psychology_documentary", pipeline_ids)
        self.assertIn("ai_tool_showcase", pipeline_ids)

    def test_integrations_health_check(self):
        check = get_integrations_health_check()
        self.assertGreaterEqual(check["total_repositories"], 12)
        self.assertGreaterEqual(check["installed_count"], 10)
        self.assertIn("reelmimic", check["repositories"])
        self.assertTrue(check["repositories"]["reelmimic"]["installed"])

if __name__ == "__main__":
    unittest.main()
