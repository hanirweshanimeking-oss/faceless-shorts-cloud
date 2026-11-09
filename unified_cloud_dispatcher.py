"""
Dragon Studios Cloud - Master Unified Production Dispatcher
Unifies the 10-Stage Dragon Studios Creator Lifecycle with the Faceless 3D Director Engine.
"""
import os
import sys
import shutil
import argparse
import logging
from pathlib import Path

# Ensure UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add current workspace directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("UnifiedDispatcher")

DRAGON_PILLARS = [
    "DARK_PSYCHOLOGY",
    "ORIGINAL_MANGA",
    "AI_TOOLS",
    "CONVERSATIONAL_PODCAST",
    "RAJ_SHAMANI"
]

def dispatch(prompt: str, mode: str, target: str, voice: str = "auto", slug: str = "reel_output"):
    output_dir = Path("output/final")
    output_dir.mkdir(parents=True, exist_ok=True)
    master_path = output_dir / f"{slug}_master.mp4"

    target_upper = target.upper().replace(" ", "_")
    is_dragon_pillar = mode == "DRAGON_PILLAR" or target_upper in DRAGON_PILLARS or any(p in target_upper for p in DRAGON_PILLARS)

    if is_dragon_pillar:
        # Match exact pillar
        matched_pillar = "DARK_PSYCHOLOGY"
        for p in DRAGON_PILLARS:
            if p in target_upper:
                matched_pillar = p
                break

        logger.info(f"==> Launching Dragon Studios 10-Stage Lifecycle for Pillar: {matched_pillar}")
        logger.info(f"==> Topic: {prompt}")

        from dragon_studios.pipeline.orchestrator import StudioOrchestrator
        orchestrator = StudioOrchestrator(output_dir=str(Path("output") / slug))
        
        result = orchestrator.execute_10_stage_run(
            topic=prompt,
            pillar=matched_pillar,
            auto_approve=True,
            use_clean_hook=True
        )

        generated_master = result.get("master_video_path")
        if not generated_master or not os.path.exists(generated_master):
            # Search for any master mp4 generated
            for root, dirs, files in os.walk(str(Path("output") / slug)):
                for f in files:
                    if f.endswith("_master.mp4") or f.endswith(".mp4"):
                        candidate = os.path.join(root, f)
                        if os.path.getsize(candidate) > 100000:
                            generated_master = candidate
                            break

        if generated_master and os.path.exists(generated_master):
            shutil.copy2(generated_master, str(master_path))
            logger.info(f"✓ 10-Stage Dragon Studios lifecycle complete: {master_path}")
            print(f"\n[UNIFIED_DISPATCHER_SUCCESS] Master Video: {master_path}")
            return {"status": "SUCCESS", "video_path": str(master_path)}
        else:
            raise RuntimeError(f"Dragon Studios orchestrator output missing: {result}")

    else:
        # Faceless 3D Engine
        logger.info(f"==> Launching Faceless 3D Adaptive Engine for Style: {target}")
        logger.info(f"==> Prompt: {prompt}")
        from faceless_engine.pipeline import create_faceless_short
        
        result = create_faceless_short(
            prompt=prompt,
            style=target,
            voice=None if voice == "auto" else voice,
            project_slug=slug
        )
        if result.get("status") == "SUCCESS":
            generated_master = result.get("final_video_path")
            shutil.copy2(generated_master, str(master_path))
            logger.info(f"✓ Faceless 3D short generation complete: {master_path}")
            print(f"\n[UNIFIED_DISPATCHER_SUCCESS] Master Video: {master_path}")
            return {"status": "SUCCESS", "video_path": str(master_path)}
        else:
            raise RuntimeError(f"Faceless engine failed: {result}")

def main():
    parser = argparse.ArgumentParser(description="Dragon Studios Master Unified Cloud Dispatcher")
    parser.add_argument("--prompt", type=str, required=True, help="Video topic or story prompt")
    parser.add_argument("--mode", type=str, default="DRAGON_PILLAR", help="DRAGON_PILLAR or FACELESS_3D")
    parser.add_argument("--target", type=str, default="DARK_PSYCHOLOGY", help="Pillar or Visual Style")
    parser.add_argument("--voice", type=str, default="auto", help="Voice override")
    parser.add_argument("--slug", type=str, default="cloud_reel", help="Project slug")

    args = parser.parse_args()
    dispatch(
        prompt=args.prompt,
        mode=args.mode,
        target=args.target,
        voice=args.voice,
        slug=args.slug
    )

if __name__ == "__main__":
    main()
