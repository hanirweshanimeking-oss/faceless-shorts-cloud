"""
Faceless Shorts CLI Entrypoint
Run: python -m faceless_engine.cli --prompt "..." --style "Tall Tale 3D"
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
from faceless_engine.pipeline import create_faceless_short

def main():
    parser = argparse.ArgumentParser(description="Zero-Cost Faceless Shorts Automation CLI")
    parser.add_argument("--prompt", type=str, default="The man who bought an entire bank for $1", help="Video concept or story prompt")
    parser.add_argument("--style", type=str, default="Tall Tale 3D", help="Visual style: Tall Tale 3D, Deep Dive 3D, Inside Out, Stick Story, Night File 3D, Paper Atlas")
    parser.add_argument("--voice", type=str, default="am_adam", help="Kokoro voice name (am_adam, am_michael, af_bella, etc.)")
    parser.add_argument("--slug", type=str, default="bank_for_one_dollar", help="Output project slug")

    args = parser.parse_args()
    result = create_faceless_short(
        prompt=args.prompt,
        style=args.style,
        voice=args.voice,
        project_slug=args.slug
    )
    if result.get("status") == "SUCCESS":
        print(f"\n[Faceless CLI] Successfully created video: {result['final_video_path']}")
        sys.exit(0)
    else:
        print(f"\n[Faceless CLI] Error creating video: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
