---
name: google-flow
description: AI Filmmaking, multi-scene storyboard orchestration, character consistency management, and video generation powered by Google Flow and Google Veo (Veo 2 / Veo 3). Use when the user asks to create or direct cinematic videos with Google Flow, storyboard multi-scene films, generate Veo video prompts, manage scene-by-scene character consistency, or export/sync projects to Google Flow (flow.google).
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins: ["python"]
      env: ["GOOGLE_API_KEY"]
---

# Google Flow & Veo AI Filmmaking Studio Skill

This skill integrates **Google Flow** (Google Labs' generative filmmaking workspace at `flow.google`) and the **Google Veo** video generation foundation models (Veo 2 & Veo 3) into Antigravity.

---

## 1. Capabilities & Workflow Architecture

Google Flow moves AI video from single isolated prompts into structured, multi-shot cinematic productions:

1. **Conversational Storyboarding (Gemini Co-Director):** Scripting narrative arcs, beat sheets, and shot lists with precise timing.
2. **Character & Aesthetic Consistency:** Locking character appearance, clothing, and artistic style across multiple scenes.
3. **Directorial Camera Controls:** Granular prompt keywords controlling camera movements (`pan`, `tilt`, `dolly`, `orbit`, `zoom`, `FPV`, `crane`).
4. **Cloud Video Generation (Google Veo):** High-definition 9:16 or 16:9 video synthesis with realistic physics and native audio synchronization.
5. **Compositing & Post-Production:** Seamlessly combining Flow/Veo video with Dragon Studios' neural voiceover, ducking, and auto-subtitling.

---

## 2. Google Flow Prompting Grammar & Directorial Syntax

When generating prompts for Google Flow / Veo, structure each shot using this exact director syntax:

```text
[Aesthetic/Style Preset]. [Subject & Action]. [Environment & Atmosphere]. Camera: [Camera Movement & Lens]. Lighting: [Lighting Setup].
```

### Camera Motion Vocabulary
* **Slow Push-In / Dolly In:** Builds intensity, intimacy, or reveals an epiphany.
* **Dramatic Low-Angle Orbit:** Conveys dominance, authority, or dramatic intimidation.
* **High-Angle Static Wide:** Establishes vulnerability, isolation, or monumental scale.
* **Tracking Side Profile:** Follows character movement smoothly with cinematic motion blur.
* **Dutch Angle Whip Pan:** High-energy transitions and abrupt narrative shifts.

### Standard Negative Prompt
```text
blurry, low quality, distorted anatomy, text artifacts, watermark, jittery frames, mutated hands, flickering
```

---

## 3. Command-Line Studio Tools

Use the verified studio Python environment to execute Google Flow commands:

```powershell
# 1. Check Google Flow & Veo integration readiness
& "C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe" cli.py flow-status

# 2. Generate a director-grade Google Flow / Veo cinematic prompt
& "C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe" cli.py flow-prompt "<scene concept>" --camera "<camera motion>" --pillar DARK_PSYCHOLOGY

# 3. Export an existing project as a Google Flow workspace manifest (.flow.json + Markdown Director Board)
& "C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe" cli.py flow-export <project_id>
```

---

## 4. End-to-End Production Process

When the user asks to direct or produce a video using Google Flow:

1. **Ideate & Script:** Break the idea down into 3–6 distinct shots (each 3–6 seconds).
2. **Assign Visual Directions:** Formulate Veo-optimized prompts with camera and lighting rules for every shot.
3. **Export Google Flow Manifest:** Run `cli.py flow-export <project_id>` so the project timeline can be opened directly on `flow.google`.
4. **Audio & Subtitle Synthesis:** Synthesize neural dialogue via Edge-TTS / Paradee and composite using FFmpeg.
5. **Deliver:** Present the generated video, shot manifest, and directorial script to the user.
