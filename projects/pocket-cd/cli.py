"""Pocket Creator Director (Pocket CD) - Command Line Interface (CLI).

Fast autonomous control for DNA extraction, director commands,
audio synthesis, FFmpeg composition, and NLE/DAW script generation.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Force utf-8 encoding for Windows console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure pocket-cd directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from engine.compositor import compositor
from engine.director_agent import director_agent
from engine.dna_extractor import dna_extractor
from engine.exporters import exporters
from engine.storyteller import storyteller

DATA_DIR = BASE_DIR / "data"
SIGNATURES_FILE = DATA_DIR / "signatures.json"


def cmd_extract(args):
    """Decompile video or style prompt into 11 modular ingredients."""
    print("🧬 [DNA EXTRACTOR] Reverse-engineering creative DNA...")
    sig = dna_extractor.decompile(
        video_path=args.video,
        prompt=args.prompt,
        title=args.title
    )
    print(f"✨ Extracted Signature: {sig.get('title')} ({sig.get('id')})")
    print(f"   Category: {sig.get('category')} | Engines: {sig.get('engines')}")
    print(f"   Rules: {json.dumps(sig.get('rules'), indent=2)}")
    print("   11 Modular Ingredients:")
    for ing in sig.get("ingredients", []):
        print(f"   • {ing.get('id')}: {ing.get('title')} [{ing.get('category')}] ({ing.get('duration')})")


def cmd_director(args):
    """Execute natural language editing directive."""
    print(f"🎬 [DIRECTOR AGENT] Executing directive: '{args.command}'...")
    res = director_agent.execute_command(
        command=args.command,
        signature_id=args.signature_id
    )
    if res.get("success"):
        print(f"✅ {res.get('summary')}")
        print("   Mutations:")
        for k, v in res.get("mutations", {}).items():
            print(f"   - {k}: {v.get('before')} -> {v.get('after')}")
    else:
        print(f"❌ Error: {res.get('error')}")


def cmd_script(args):
    """Generate VSL script with ElevenLabs V4 syntax."""
    print(f"🎙️ [STORYTELLER] Generating script for topic: '{args.topic}'...")
    script = storyteller.generate_vsl_script(
        topic=args.topic,
        style=args.style,
        target_duration_sec=args.duration
    )
    print(f"✅ Created Script: {script.get('title')} ({script.get('id')})")
    print(f"   Voice: {script.get('voice')} | Model: {script.get('model')}")
    print("\n--- SCRIPT CONTENT ---")
    print(script.get("content"))
    print("----------------------\n")


def cmd_voice(args):
    """Synthesize neural audio via Edge-TTS."""
    print(f"🔊 [VOICE SYNTHESIS] Synthesizing speech with voice: {args.voice}...")
    res = storyteller.synthesize_speech(
        text=args.text,
        voice_key=args.voice,
        output_filename=args.output
    )
    print(f"✅ Audio generated successfully!")
    print(f"   File: {res.get('audio_filename')}")
    print(f"   Path: {res.get('absolute_path')}")
    print(f"   Duration: ~{res.get('duration_sec')}s ({res.get('word_count')} words)")


def cmd_render(args):
    """Execute FFmpeg to composite 9:16 vertical reel."""
    print(f"🎞️ [COMPOSITOR] Rendering vertical reel with Gyan FFmpeg 9.0.2...")
    res = compositor.render_vertical_reel(
        signature_id=args.signature_id,
        title_text=args.title,
        subtitle_text=args.subtitle,
        counter_label=args.counter_label,
        target_value=args.target_value,
        resolution=args.resolution,
        duration_sec=args.duration,
        fps=args.fps
    )
    if res.get("success"):
        print(f"✅ Master reel rendered in {res.get('render_time_sec')}s!")
        print(f"   Output: {res.get('render_path')}")
        print(f"   Web URL: {res.get('web_url')}")
        print(f"   Resolution: {res.get('resolution')} @ {res.get('fps')}fps ({res.get('size_mb')} MB)")
    else:
        print(f"❌ Render failed: {res.get('error')}")


def cmd_export(args):
    """Generate After Effects JSX, DaVinci Resolve Python, REAPER Lua, or JSON Manifest."""
    print(f"💾 [EXPORTER] Exporting '{args.format}' for signature: {args.signature_id}...")
    sigs = dna_extractor.load_signatures()
    target = next((s for s in sigs if s.get("id") == args.signature_id), None)
    if not target:
        if sigs:
            target = sigs[0]
        else:
            print("❌ No signatures available to export.")
            return

    fmt = args.format.lower()
    if fmt in ["jsx", "ae", "aftereffects"]:
        path = exporters.generate_after_effects_jsx(target)
    elif fmt in ["py", "resolve", "davinci"]:
        path = exporters.generate_davinci_resolve_py(target)
    elif fmt in ["lua", "reaper"]:
        path = exporters.generate_reaper_lua(target)
    elif fmt in ["json", "dna", "manifest"]:
        path = exporters.generate_style_dna_manifest_json(target)
    else:
        print(f"❌ Unknown format: {fmt}. Choose from jsx, py, lua, json.")
        return

    print(f"✅ Generated script: {path}")


def cmd_serve(args):
    """Launch FastAPI server with Uvicorn."""
    import uvicorn
    print(f"🚀 [SERVER] Launching Pocket Creator Director API on http://{args.host}:{args.port}...")
    uvicorn.run("server:app", host=args.host, port=args.port, reload=args.reload)


def cmd_test(args):
    """Run verification test suite across all modules."""
    print("🧪 [TEST] Running Pocket Creator Director verification test suite...")
    import subprocess
    test_script = BASE_DIR / "test_pocket_cd.py"
    py_bin = r"C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe"
    proc = subprocess.run([py_bin, str(test_script)], capture_output=False)
    sys.exit(proc.returncode)


def main():
    parser = argparse.ArgumentParser(description="Pocket Creator Director (Pocket CD) CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # extract
    p_extract = subparsers.add_parser("extract", help="Reverse-engineer video or prompt into 11 ingredients")
    p_extract.add_argument("--video", "-v", type=str, help="Path to video file")
    p_extract.add_argument("--prompt", "-p", type=str, default="Viral commercial reel with yellow kinetic titles and face match cuts", help="Style description prompt")
    p_extract.add_argument("--title", "-t", type=str, help="Signature title")

    # director
    p_dir = subparsers.add_parser("director", help="Execute natural language director command")
    p_dir.add_argument("command_text", type=str, help="Command prompt (e.g. 'Add bloom and tighten cuts')")
    p_dir.add_argument("--signature-id", "-s", type=str, default="ackman-edit-dna", help="Target signature ID")

    # script
    p_script = subparsers.add_parser("script", help="Generate ElevenLabs V4 script")
    p_script.add_argument("--topic", "-t", type=str, default="Pocket Creative Director Launch VSL")
    p_script.add_argument("--style", "-s", type=str, default="carl_voice")
    p_script.add_argument("--duration", "-d", type=int, default=22)

    # voice
    p_voice = subparsers.add_parser("voice", help="Synthesize neural audio via Edge-TTS")
    p_voice.add_argument("--text", "-t", type=str, required=True, help="Text to speak")
    p_voice.add_argument("--voice", "-v", type=str, default="carl", help="Voice preset")
    p_voice.add_argument("--output", "-o", type=str, help="Output filename")

    # render
    p_render = subparsers.add_parser("render", help="Render vertical reel via Gyan FFmpeg")
    p_render.add_argument("--title", type=str, default="BILL ACKMAN")
    p_render.add_argument("--subtitle", type=str, default="PERSHING SQUARE CAPITAL")
    p_render.add_argument("--counter-label", type=str, default="AUM")
    p_render.add_argument("--target-value", type=int, default=18000000000)
    p_render.add_argument("--signature-id", "-s", type=str, default="ackman-edit-dna")
    p_render.add_argument("--resolution", "-r", type=str, default="720x1280")
    p_render.add_argument("--duration", "-d", type=float, default=6.0)
    p_render.add_argument("--fps", type=int, default=30)

    # export
    p_export = subparsers.add_parser("export", help="Generate AE .jsx, Resolve .py, REAPER .lua")
    p_export.add_argument("--format", "-f", type=str, choices=["jsx", "py", "lua", "json"], default="jsx")
    p_export.add_argument("--signature-id", "-s", type=str, default="ackman-edit-dna")

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch FastAPI server")
    p_serve.add_argument("--host", type=str, default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--reload", action="store_true")

    # test
    p_test = subparsers.add_parser("test", help="Run verification test suite")

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "director":
        args.command = args.command_text
        cmd_director(args)
    elif args.command == "script":
        cmd_script(args)
    elif args.command == "voice":
        cmd_voice(args)
    elif args.command == "render":
        cmd_render(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "serve":
        cmd_serve(args)
    elif args.command == "test":
        cmd_test(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
