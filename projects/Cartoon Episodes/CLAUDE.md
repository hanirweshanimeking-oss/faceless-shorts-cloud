# Cartoon Episodes — studio project

This folder is a self-contained studio for making animated cartoon episodes
with a consistent cast, driven entirely by the `cartoon-episodes` skill in
`.claude/skills/`.

When the user greets you, asks to start, or says anything about a cartoon, a
scene, an episode or their characters — invoke the `cartoon-episodes` skill
and follow its staged flow exactly: welcome → show bible → cast and world →
scenes → episode. One stage per message; wait between stages.

Presentation matters as much as function: follow the skill's Global UI rules
in every message (tables, dividers, no internal chatter, clean pasteable
blocks).

State lives on disk: each show is a folder under `projects/` (bible.md,
sheets/, scenes/, episode.mp4). `EXPLAINER.md` is the one-page intro the
user received with this folder.

This studio writes prompts and runs the local episode cut only. Never submit
paid generations to any platform from here — the user runs every image and
video prompt in their own generator and brings the files back.
