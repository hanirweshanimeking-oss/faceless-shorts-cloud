# Show bible — template

The bible is the single source of truth for the show. It lives at
`projects/<slug>/bible.md`. Every scene prompt is written from it, never from
memory. Asset file names in the bible must match the files in `sheets/` exactly.

```
SHOW BIBLE — [Series title]

SERIES
- Logline: [one sentence — who, what world, what kind of show]
- Visual style: [3–6 keywords, e.g. "3D animated feature look, soft warm lighting, pastel palette"]
- Aspect ratio: [16:9 or 9:16]
- Default scene length: 15 seconds
- Style key: sheets/style-key.png

CHARACTERS (one block per character)
- [Name]
  - Sheet: sheets/char-[name].png
  - Visual lock: [hair, clothes, accessories, eye color — what must never change]
  - Voice: [one line the video model can act, e.g. "lazy teenage boy, low, dry, slightly nasal"]  (or "no voice — [sounds they make]")
  - Personality & speech style: [how they act and talk]

LOCATIONS (one block per recurring location)
- [Name]
  - Views: sheets/loc-[name]-1.png ([what this angle shows]), sheets/loc-[name]-2.png ([...])
  - Mood & lighting: [...]

PROPS
- [Name]: sheets/prop-[name].png — [one-line description]

EPISODE NOTES (optional)
- [Current episode outline, running gags, canon facts]
```

## Asset sheet spec

Every sheet prompt starts with the show's visual style line, byte-identical,
and attaches `sheets/style-key.png` as reference (except the style key itself).

- **Style key** — one representative scene of the show in the target aspect.
  The look anchor for everything else.
- **Characters** — full body, neutral standing pose, front three-quarter view,
  clean plain backdrop, `2:3`. Every visual-lock detail spelled out. One sheet
  per character.
- **Locations** — two views per recurring location, target aspect, dressed,
  **no characters**: view 1 the master wide (the angle most scenes use), view 2
  the counter-angle or detail the story needs. Every location prompt carries:
  `EMPTY LOCATION PLATE, take only the render style and palette from the
  reference image, NOT its subject. ABSOLUTELY NO characters, NO people, NO
  animals.`
- **Props** — isolated on a plain backdrop, `1:1`, no hands, no scene. Only
  props that recur or carry a story beat.

A one-off place or object (the dinosaur jungle in the worked example) gets no
sheet; it is described inline in the scene prompt.
