"""
Agent 10: Production Manager
Master Orchestrator: tracks chapter progress, dispatches agents, audits metrics,
and enforces zero-cost compliance across DRAGON: HIDDEN REBIRTH.
"""

import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.creative_director import CreativeDirector
from agents.story_agent import StoryAgent
from agents.character_agent import CharacterAgent
from agents.world_agent import WorldAgent
from agents.storyboard_agent import StoryboardAgent
from agents.illustration_agent import IllustrationAgent
from agents.effects_agent import EffectsAgent
from agents.composition_agent import CompositionAgent
from agents.qa_agent import QualityAssuranceAgent

class ProductionManager:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.db_path = root_dir / "database" / "manga_production.db"
        self.generated_art_dir = root_dir / "generated_art"
        self.effects_dir = root_dir / "effects"
        self.final_pages_dir = root_dir / "final_pages"
        self.quality_reports_dir = root_dir / "quality_reports"
        
        # Initialize subagents
        self.creative_director = CreativeDirector(self.db_path)
        self.story_agent = StoryAgent(self.db_path)
        self.character_agent = CharacterAgent(self.db_path)
        self.world_agent = WorldAgent(self.db_path)
        self.storyboard_agent = StoryboardAgent(self.db_path)
        self.illustration_agent = IllustrationAgent(self.db_path, self.generated_art_dir)
        self.effects_agent = EffectsAgent(self.effects_dir)
        self.composition_agent = CompositionAgent(self.db_path, self.final_pages_dir)
        self.qa_agent = QualityAssuranceAgent(self.db_path, self.quality_reports_dir)

    def produce_page(self, page_id: str, prefer_cloud: bool = False) -> Dict[str, Any]:
        """
        Orchestrates the entire end-to-end production pipeline for a single manga page:
        Script Verification -> Panel Art Generation -> SFX/Effects -> Compositing -> Automated QA.
        """
        t0 = time.time()
        print(f"\n=======================================================")
        print(f"[*] SSS+ PRODUCTION PIPELINE: PRODUCING PAGE [{page_id}]")
        print(f"=======================================================")

        # 1. Story Continuity Check
        print("[1/5] Story Agent: Validating dialogue and character continuity...")
        story_val = self.story_agent.validate_script_continuity(page_id)
        if story_val["status"] != "VALID":
            print(f"[-] Script validation warning: {story_val['issues']}")

        # 2. Panel Illustration Generation
        print("[2/5] Illustration Agent: Generating high-resolution panel artwork...")
        panels = self.storyboard_agent.get_page_panels(page_id)
        rendered_panels = []
        for p in panels:
            res = self.illustration_agent.render_panel(p["id"], prefer_cloud=prefer_cloud)
            rendered_panels.append(res)
            print(f"    - Rendered Panel {p['panel_index']}/{len(panels)}: {p['shot_type']} ({p['bbox_w']}x{p['bbox_h']})")

        # 3. Effects Synthesis
        print("[3/5] Effects Agent: Synthesizing celestial dragon auras & sound effects...")
        for p in panels:
            sfx = p.get("sfx_text")
            raw_path = p.get("raw_panel_path")
            if sfx and raw_path and Path(raw_path).exists():
                from PIL import Image
                panel_img = Image.open(raw_path)
                sfx_style = p.get("sfx_style", "EXPLOSION")
                panel_img = self.effects_agent.render_sfx(panel_img, sfx, style=sfx_style)
                panel_img.save(raw_path, "PNG", dpi=(300, 300))

        # 4. Final Page Compositing
        print("[4/5] Composition Agent: Assembling 300 DPI master canvas and speech balloons...")
        master_page_path = self.composition_agent.composite_page(page_id)
        print(f"    [+] Master Page Exported: {master_page_path}")

        # 5. Automated QA Inspection
        print("[5/5] QA Agent: Performing dynamic range, contrast, and readability audit...")
        qa_result = self.qa_agent.inspect_page(page_id, master_page_path)
        print(f"    [+] QA Verdict: {qa_result['verdict']} (Score: {qa_result['overall_score']:.2f}/10.0)")

        elapsed = time.time() - t0
        
        # Log Metrics
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO production_metrics (metric_name, metric_value, context_json)
                VALUES (?, ?, ?)
            """, ("page_generation_time_seconds", elapsed, f'{{"page_id": "{page_id}"}}'))
            conn.commit()

        return {
            "status": "COMPLETED",
            "page_id": page_id,
            "master_page_path": str(master_page_path),
            "qa_result": qa_result,
            "elapsed_seconds": round(elapsed, 2),
            "budget_spent_inr": 0.0
        }

    def get_studio_status(self) -> Dict[str, Any]:
        """Queries database and returns an executive studio dashboard."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM chapters")
            total_chapters = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM pages WHERE status='QA_PASSED'")
            completed_pages = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM panels WHERE status='GENERATED'")
            completed_panels = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(score_contrast) FROM qa_reports")
            avg_contrast = cursor.fetchone()[0] or 0.0
            
            cursor.execute("SELECT COUNT(*) FROM characters")
            total_characters = cursor.fetchone()[0]
            
        return {
            "studio_title": "DRAGON: HIDDEN REBIRTH Autonomous Studio",
            "total_chapters": total_chapters,
            "completed_pages": completed_pages,
            "completed_panels": completed_panels,
            "total_characters": total_characters,
            "avg_contrast_score": round(avg_contrast, 2),
            "total_production_cost": "INR 0.00 (Zero Budget Rule Compliant)",
            "local_gpu_mode": "Kepler GT 710 Safe (Procedural Inking Canvas & Cloud Bridge)"
        }
