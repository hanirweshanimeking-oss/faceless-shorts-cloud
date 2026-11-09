# 🎬 Cartoon Episodes — make an animated series with Claude

**What this is.** A studio-in-a-folder. Animation studios don't start with
episodes, they build a production pipeline first: the characters, the
locations, the props, the voices, the visual language. Then every episode is
just another story on top of the same assets. That's what this builds, and
it runs on one rule: whatever you don't define, the AI invents. So everything
is defined once and reused forever.

**How it works:**

| Step | What happens | Who does it |
|---|---|---|
| 1 | You describe the show. Claude writes the show bible: cast, world, style, a voice for every character. | Claude |
| 2 | **Cast and world** — one image prompt per character, location view and prop. Run them in your image generator, save them as `sheets/<name>.png`. | You (~6–10 generations, once per show) |
| 3 | **Scenes** — describe what happens in one sentence. Claude hands you the full production prompt: shots, timestamps, camera, blocking, dialogue, and which sheets to attach. Run it in your video generator, save it as `scenes/01-<name>.mp4`. | You (1 generation per scene) |
| 4 | **The episode** — Claude cuts your scene clips into one episode. | Claude |

**What you need:**
- Claude Code, with this folder opened as a project
- An image model and a video model that accept reference images and
  generate dialogue (Seedream and Gemini Omni are the proven pair)
- ffmpeg, one small free tool for the episode cut — Claude checks for it

**To start:** open this folder in Claude Code and say **"let's make a
cartoon."** Every show you make is kept in `projects/<name>/`.
