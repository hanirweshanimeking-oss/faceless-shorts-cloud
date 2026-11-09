"""
Faceless Shorts Automation Pipeline
Orchestrates end-to-end zero-cost video generation:
Prompt -> Script -> Neural Voiceover -> Whisper Alignment -> 3D Animation -> Foley/Ducking -> Master .MP4
"""
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import time
import json
from typing import Dict, Any, Optional

from faceless_engine.config import OUTPUT_DIR
from faceless_engine.script_writer import generate_script_for_topic, generate_tall_tale_bank_script, ViralScript
from faceless_engine.voice_engine import generate_voiceover
from faceless_engine.subtitle_engine import (
    extract_word_timestamps,
    group_words_into_phrases,
    generate_viral_ass_subtitles
)
from faceless_engine.director_agent import DirectorAgent, VisualDirection
from faceless_engine.visual_engine import TallTaleRenderer
from faceless_engine.audio_mixer import synthesize_sfx, mix_master_audio
from faceless_engine.compositor import (
    concatenate_scene_videos,
    burn_subtitles_and_master,
    qa_verify_video
)

def create_faceless_short(
    prompt: str = "The man who bought an entire bank for $1",
    style: str = "Tall Tale 3D",
    voice: str = "am_adam",
    project_slug: str = "man_bought_bank_for_1_dollar"
) -> Dict[str, Any]:
    """
    Executes the 6-step Faceless Shorts Automation pipeline.
    Produces a 1080x1920 viral vertical video ready for Reels, Shorts, and TikTok.
    """
    t0 = time.time()
    work_dir = os.path.join(OUTPUT_DIR, project_slug)
    os.makedirs(work_dir, exist_ok=True)
    
    # 0. 🎯 AUTONOMOUS DIRECTOR AGENT
    direction: VisualDirection = DirectorAgent.direct_production(
        prompt=prompt,
        requested_style=style,
        requested_voice=voice
    )

    print("=" * 70)
    print("🎬 STARTING FACELESS SHORTS AUTOMATION PIPELINE")
    print(f"📌 Style: {direction.style}")
    print(f"📌 Director Voice: {direction.voice}")
    print(f"📌 Character Archetype: {direction.character_archetype}")
    print(f"📌 Project: {project_slug}")
    print(f"📌 Work Directory: {work_dir}")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. ✍️ SCRIPT GENERATION
    # -------------------------------------------------------------
    print("\n[Step 1/6] ✍️ Writing high-retention viral script...")
    script: ViralScript = generate_script_for_topic(title=prompt, style=direction.style)
    script_path = os.path.join(work_dir, "script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": script.title,
            "style": script.style,
            "target_duration": script.target_duration,
            "full_narration": script.full_narration,
            "loop_transition": script.loop_transition,
            "scenes": [s.__dict__ for s in script.scenes]
        }, f, indent=2)
    print(f"  ✓ Script ready: {len(script.scenes)} scenes, {len(script.full_narration.split())} words.")

    # -------------------------------------------------------------
    # 2. 🎙️ ULTRA-REALISTIC AI VOICEOVER
    # -------------------------------------------------------------
    print(f"\n[Step 2/6] 🎙️ Generating neural voiceover ({direction.voice})...")
    voice_wav_path = os.path.join(work_dir, "voice.wav")
    generate_voiceover(
        text=script.full_narration,
        output_path=voice_wav_path,
        voice_preference=direction.voice,
        speed=1.06
    )
    print(f"  ✓ Voiceover generated: {voice_wav_path}")

    # -------------------------------------------------------------
    # 3. ⏱️ WORD-BY-WORD SUBTITLE ALIGNMENT (WHISPER)
    # -------------------------------------------------------------
    print("\n[Step 3/6] ⏱️ Transcribing word-level timestamps with Whisper...")
    words = extract_word_timestamps(voice_wav_path)
    words_json_path = os.path.join(work_dir, "words.json")
    with open(words_json_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
        
    phrases = group_words_into_phrases(words, max_words=3)
    ass_subtitles_path = os.path.join(work_dir, "subtitles.ass")
    generate_viral_ass_subtitles(phrases, ass_subtitles_path)
    print(f"  ✓ Word alignment complete: {len(words)} words aligned, viral yellow ASS subtitles saved.")

    total_voice_duration = words[-1]["end"] if words else 35.0
    print(f"  ✓ Exact voice duration: {total_voice_duration:.2f} seconds")

    # -------------------------------------------------------------
    # 4. 🎨 ANIMATED 3D & CARTOON VISUAL RENDERING
    # -------------------------------------------------------------
    print(f"\n[Step 4/6] 🎨 Rendering {direction.style} dynamic visuals (1080x1920 @ 30fps)...")
    renderer = TallTaleRenderer(width=1080, height=1920)
    
    # Calculate per-scene duration proportional to script beat duration
    total_est = sum(s.est_duration_sec for s in script.scenes)
    scene_video_paths = []
    
    for s in script.scenes:
        scene_ratio = s.est_duration_sec / total_est
        actual_scene_duration = round(total_voice_duration * scene_ratio, 2)
        scene_mp4 = os.path.join(work_dir, f"scene_{s.scene_index}.mp4")
        
        print(f"  -> Rendering Scene {s.scene_index}: '{s.name}' ({actual_scene_duration:.2f}s)...")
        renderer.render_scene_video(
            scene_idx=s.scene_index,
            duration_sec=actual_scene_duration,
            output_mp4_path=scene_mp4,
            scene_beat=s,
            style=direction.style,
            title=prompt,
            fps=30
        )
        scene_video_paths.append(scene_mp4)

    # Concatenate all visual scene clips
    visual_full_path = os.path.join(work_dir, "visuals_full.mp4")
    concatenate_scene_videos(scene_video_paths, visual_full_path)
    print(f"  ✓ Visual scenes rendered & assembled: {visual_full_path}")

    # -------------------------------------------------------------
    # 5. 🔊 SOUND EFFECTS & DUCKED MUSIC
    # -------------------------------------------------------------
    print("\n[Step 5/6] 🔊 Adding comedy sound effects and ducked background music...")
    # Synthesize hero cash register ding
    sfx_ding_path = os.path.join(work_dir, "sfx_cash_ding.wav")
    synthesize_sfx("cash_register_ding", sfx_ding_path)
    
    master_audio_path = os.path.join(work_dir, "master_audio.aac")
    mix_master_audio(
        voice_path=voice_wav_path,
        output_master_path=master_audio_path,
        music_volume=0.20,
        ducking_db=-12.0
    )
    print(f"  ✓ Audio mix complete (-12dB sidechain ducking applied): {master_audio_path}")

    # -------------------------------------------------------------
    # 6. 🎬 COMPOSITING & FINAL QA
    # -------------------------------------------------------------
    print("\n[Step 6/6] 🎬 Burning subtitles & exporting master .MP4 video...")
    final_video_path = os.path.join(work_dir, f"{project_slug}_final.mp4")
    burn_subtitles_and_master(
        visual_video_path=visual_full_path,
        master_audio_path=master_audio_path,
        ass_subtitles_path=ass_subtitles_path,
        final_output_path=final_video_path
    )
    
    # Run QA
    qa_report = qa_verify_video(final_video_path)
    elapsed = round(time.time() - t0, 1)
    
    print("\n" + "=" * 70)
    print(f"✅ PIPELINE FINISHED IN {elapsed} SECONDS!")
    print(f"🎬 Master Video: {final_video_path}")
    print(f"📊 QA Status: {'PASSED' if qa_report.get('passed') else 'CHECK'}")
    print(f"📏 Resolution: {qa_report.get('width')}x{qa_report.get('height')}")
    print(f"⏱️ Duration: {qa_report.get('duration_sec')}s")
    print(f"📦 Size: {qa_report.get('file_size_mb')} MB")
    print("=" * 70)

    return {
        "status": "SUCCESS",
        "project_slug": project_slug,
        "style": style,
        "final_video_path": final_video_path,
        "script": script.__dict__,
        "qa_report": qa_report,
        "elapsed_seconds": elapsed,
        "work_dir": work_dir
    }
