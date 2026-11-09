"""
Unit & Integration Test Suite for DRAGON: HIDDEN REBIRTH
Validates the entire 10-agent autonomous manga production pipeline.
"""

import unittest
import sqlite3
from pathlib import Path
from PIL import Image

import sys
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.production_manager import ProductionManager
from agents.character_agent import CharacterAgent
from agents.storyboard_agent import StoryboardAgent
from scripts.image_generator import MangaImageGenerator

class TestMangaPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_dir = ROOT_DIR
        cls.db_path = ROOT_DIR / "database" / "manga_production.db"
        cls.manager = ProductionManager(ROOT_DIR)

    def test_01_database_seeded(self):
        """Verifies database tables and seeded records."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM characters")
            char_count = cursor.fetchone()[0]
            self.assertGreaterEqual(char_count, 1, "Characters must be seeded.")
            
            cursor.execute("SELECT COUNT(*) FROM panels WHERE page_id='page_001_01'")
            panel_count = cursor.fetchone()[0]
            self.assertEqual(panel_count, 4, "Page 1 must have exactly 4 seeded panels.")

    def test_02_character_agent(self):
        """Verifies character visual prompt construction."""
        char_agent = CharacterAgent(self.db_path)
        char = char_agent.get_character("char_chitran")
        self.assertIsNotNone(char)
        self.assertIn("Chitran", char["name"])
        
        prompt = char_agent.build_conditioned_prompt("char_chitran", "standing over ruined altar")
        self.assertIn("Chitran", prompt)
        self.assertIn("screentone", prompt.lower())

    def test_03_storyboard_layout(self):
        """Verifies Japanese RTL manga layout geometry."""
        sb_agent = StoryboardAgent(self.db_path)
        panels = sb_agent.calculate_standard_layout(page_width=2480, page_height=3508, panel_count=4)
        self.assertEqual(len(panels), 4)
        # Check Panel 2 is on right side (RTL flow)
        self.assertGreater(panels[1]["x"], panels[2]["x"], "In RTL, Panel 2 x should be greater than Panel 3 x.")

    def test_04_procedural_image_generator(self):
        """Verifies zero-cost procedural inking and screentone synthesis."""
        out_dir = self.root_dir / "generated_art"
        gen = MangaImageGenerator(out_dir)
        tone = gen.generate_screentone_pattern(400, 400, dot_spacing=8, dot_radius=2)
        self.assertEqual(tone.size, (400, 400))
        
        speed = gen.generate_speedlines(400, 400, (200, 200))
        self.assertEqual(speed.size, (400, 400))

    def test_05_end_to_end_page_production(self):
        """Executes full production pipeline for Chapter 1 Page 1 and checks QA pass."""
        result = self.manager.produce_page("page_001_01", prefer_cloud=False)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["budget_spent_inr"], 0.0)
        self.assertTrue(Path(result["master_page_path"]).exists())
        
        # Verify master page dimensions
        img = Image.open(result["master_page_path"])
        self.assertEqual(img.size, (2480, 3508), "Master page must be standard 2480x3508 300DPI.")
        
        # Verify QA passed
        qa = result["qa_result"]
        self.assertEqual(qa["verdict"], "PASS")
        self.assertGreaterEqual(qa["overall_score"], 8.5)

if __name__ == "__main__":
    unittest.main()
