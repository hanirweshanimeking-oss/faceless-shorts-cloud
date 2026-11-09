# Worked example — "The Remote" (15s)

Bible excerpt: Leo (`sheets/char-leo.png`, voice "lazy teenage boy, low, dry,
slightly nasal", sarcastic), his pug Baxter (`sheets/char-baxter.png`, no voice,
barks), living room `sheets/loc-livingroom-1.png` (wide, facing the sofa) and
`sheets/loc-livingroom-2.png` (close on the cushions), prop
`sheets/prop-timeremote.png` (chunky golden remote, one big red button).
Style: 3D animated feature look, soft warm lighting.

User request: *"Leo is lying on the couch looking for a mysterious remote hidden
between the cushions. When he finally finds it and presses the button, he gets
teleported to the age of dinosaurs. Baxter watches."*

```
SCENE: The Remote
DURATION: 15 seconds
STYLE: 3D animated feature look, soft warm lighting

[0:00–0:04] WIDE SHOT, eye level, static — composition: the sofa fills the frame, Baxter small on the rug in the foreground
Leo lies sprawled on the sofa in the living room, one arm buried to the shoulder between the cushions, digging with growing frustration, eyes on the ceiling. Baxter watches him, head tilted.
Leo (lazy teenage boy, low, dry, slightly nasal): "Where is that stupid remote?"

[0:04–0:08] CUT TO: CLOSE-UP on the cushions, slow push-in — composition: Leo's digging hand dominates the frame
Leo's hand yanks out the golden time remote. Off-screen, Baxter gives one sharp bark.
Leo (lazy teenage boy, low, dry, slightly nasal): "…This is not our remote."

[0:08–0:11] CONTINUOUS, pulling back to MEDIUM SHOT, eye level — composition: Leo centered, remote raised toward camera
Leo squints at the remote, shrugs, and presses the big red button. The remote flashes; white light floods the room.

[0:11–0:15] CUT TO: WIDE SHOT, low angle, static — composition: the sofa suddenly tiny, jungle towering, a dinosaur head filling the top of frame
The light fades: same sofa, same Leo — but the living room is gone, replaced by a prehistoric jungle. The huge dinosaur head rises slowly behind the sofa. Leo freezes mid-blink, eyes sliding up. Baxter barks frantically at the edge of frame.
Leo (lazy teenage boy, low, dry, slightly nasal): "Okay. Wrong button."

Characters, costumes, objects and lighting EXACTLY as in the reference images. Only Leo speaks; Baxter never talks. No on-screen text, no captions, no watermark.
```

| Setting | Value |
|---|---|
| Model | Gemini Omni (or any video model that accepts reference images and generates dialogue) |
| Reference images | attach `sheets/char-leo.png`, `sheets/char-baxter.png`, `sheets/loc-livingroom-1.png`, `sheets/prop-timeremote.png` |
| Aspect · Duration | 16:9 · 15s |
| Save as | `scenes/01-the-remote.mp4` |

Notice what the example does: the jungle gets no sheet because it is a one-off
payoff described inline; Baxter's barks live in the action text because he has
no voice; shot three carries no dialogue because the action is the line; the
CONTINUOUS pull-back binds the find to the button press as one gesture, while
hard cuts frame the setup and the payoff; and the location change is allowed
inside the scene because the teleport *is* the joke.
