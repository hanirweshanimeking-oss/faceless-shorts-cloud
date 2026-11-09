import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragon_studios.integrations.ayanokoji_voice import (
    synthesize_ayanokoji_hindi,
    RVC_MODEL_DIR
)

class TestAyanokojiVoice(unittest.TestCase):
    def test_model_files_exist(self):
        """Verify downloaded RVC v2 model files exist on disk."""
        nss_model = os.path.join(RVC_MODEL_DIR, "NSS-Dragon_Ayanokojiv2", "ayanokouji_experiment.pth")
        nss_index = os.path.join(RVC_MODEL_DIR, "NSS-Dragon_Ayanokojiv2", "added_IVF314_Flat_nprobe_1_ayanokouji_experiment_v2.index")
        dub_model = os.path.join(RVC_MODEL_DIR, "JombysAright_Ayanokouji_Dub", "Ayanokouji Kiyotaka (Dub).pth")
        
        self.assertTrue(os.path.exists(nss_model), "NSS-Dragon RVC model missing")
        self.assertTrue(os.path.exists(nss_index), "NSS-Dragon RVC index missing")
        self.assertTrue(os.path.exists(dub_model), "JombysAright Dub RVC model missing")

    def test_synthesize_ayanokoji_hindi(self):
        """Verify Hindi speech synthesis with Ayanokoji mastering."""
        test_out = "output/test_ayanokoji_unit.mp3"
        result = synthesize_ayanokoji_hindi(
            text="जीत ही सब कुछ है।",
            output_path=test_out,
            apply_rvc=False,
            apply_mastering=True
        )
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["character"], "Kiyotaka Ayanokoji")
        self.assertTrue(os.path.exists(test_out))
        self.assertGreater(os.path.getsize(test_out), 1000)

    def test_synthesize_ayanokoji_true_rvc(self):
        """Verify full end-to-end RVC v2 40kHz conversion pipeline."""
        test_out = "output/test_ayanokoji_rvc_unit.mp3"
        result = synthesize_ayanokoji_hindi(
            text="जीत ही सब कुछ है।",
            output_path=test_out,
            apply_rvc=True,
            apply_mastering=True,
            index_rate=0.75
        )
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["rvc_converted"])
        self.assertIn("RVC_v2_40k", result["pipeline"])
        self.assertTrue(os.path.exists(test_out))
        self.assertGreater(os.path.getsize(test_out), 2000)

    def test_synthesize_ayanokoji_english_dub(self):
        """Verify English Dub RVC v2 conversion pipeline."""
        from dragon_studios.integrations.ayanokoji_voice import synthesize_ayanokoji_voice
        test_out = "output/test_ayanokoji_dub_unit.mp3"
        result = synthesize_ayanokoji_voice(
            text="Winning is everything.",
            output_path=test_out,
            language="en",
            model_choice="dub",
            apply_rvc=True,
            apply_mastering=True
        )
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["rvc_converted"])
        self.assertTrue(os.path.exists(test_out))
        self.assertGreater(os.path.getsize(test_out), 2000)

if __name__ == "__main__":
    unittest.main()
