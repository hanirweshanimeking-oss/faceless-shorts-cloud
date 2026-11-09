"""
Build Toonflow Canvas for CHITRAN: THE MANGA (DRAGON: HIDDEN REBIRTH)
Chapter 2 - Sanctuary Visual Workspace
"""

import json
from pathlib import Path

def create_canvas():
    workspace_dir = Path(r"C:\Users\DESKTOP\Downloads\money\stable\data\workspaces\Chitran_Manga")
    workspace_dir.mkdir(parents=True, exist_ok=True)
    canvas_path = workspace_dir / "Chapter_002_Sanctuary.json"

    bible_text = """# DRAGON: HIDDEN REBIRTH
## CHITRAN: THE MANGA — Chapter 2: The Dragon Awakens

### Canonical Cast:
- **Aarav**: 16-year-old warrior youth, messy black hair, copper-bronze skin, awakened golden solar left eye, red-orange Vedic dhoti with gold embroidery.
- **Neel**: Sovereign of Night, 17-year-old dark anime prince, jet-black hair with violet tips, obsidian angavastram, wielding the celestial glowing Void Trishul.
- **Ananya**: 15-year-old temple maiden priestess, saffron-white sari, silver bindi, braided dark hair.
- **Void Stalker**: Monolithic obsidian shadow beast with glowing violet hollow eyes and serrated fangs.

### Canonical Layout Formula:
- 1024x1536 Master Resolution
- 8 Panels per Page (Multi-tier dynamic grid)
- Official Brush Logo: CHITRAN with flame icon
- Official Ending Slogan: *"STORIES WILL LIVE... OR THE WORLD WILL DIE."*

### Chapter 3 Setup:
Neel extends his hand toward Aarav as the celestial constellation of the dragon burns across the roofless night sky.
"""

    canvas_data = {
        "toonflowCanvas": True,
        "viewport": {
            "x": 50.0,
            "y": 50.0,
            "zoom": 0.75
        },
        "nodes": [
            # --- Tier 1: Character Reference Models ---
            {
                "id": "char-aarav",
                "type": "imageNode",
                "position": {"x": 50, "y": 50},
                "data": {
                    "label": "Character: Aarav (Awakened Solar Hero)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Aarav_Hero_Ref.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },
            {
                "id": "char-neel",
                "type": "imageNode",
                "position": {"x": 480, "y": 50},
                "data": {
                    "label": "Character: Neel (Sovereign of Night)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Neel_Sovereign_Ref.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },
            {
                "id": "char-ananya",
                "type": "imageNode",
                "position": {"x": 910, "y": 50},
                "data": {
                    "label": "Character: Ananya (Temple Priestess Maiden)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Ananya_Maiden_Ref.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },
            {
                "id": "char-void-stalker",
                "type": "imageNode",
                "position": {"x": 1340, "y": 50},
                "data": {
                    "label": "Enemy: Void Stalker (Shadow Chimera)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Void_Stalker_Ref.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },

            # --- Tier 2: Master Storyboard Pages ---
            {
                "id": "page-001",
                "type": "imageNode",
                "position": {"x": 50, "y": 550},
                "data": {
                    "label": "Chapter 2 - Page 1: Subterranean Sanctum (8 Panels)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Chitran_Ch2_Page1.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },
            {
                "id": "page-002",
                "type": "imageNode",
                "position": {"x": 700, "y": 550},
                "data": {
                    "label": "Chapter 2 - Page 2: Shadow Eruption & Fire Shield (8 Panels)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Chitran_Ch2_Page2.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },
            {
                "id": "page-003",
                "type": "imageNode",
                "position": {"x": 1350, "y": 550},
                "data": {
                    "label": "Chapter 2 - Page 3: Sovereign Arrival & Cliffhanger (8 Panels)",
                    "outputs": {
                        "image": {
                            "dataType": "IMAGE",
                            "value": {
                                "url": "assets/Chitran_Ch2_Page3.png",
                                "mimeType": "image/png"
                            }
                        }
                    }
                }
            },

            # --- Tier 3: Motion Comic Video Generation Nodes ---
            {
                "id": "motion-shot-1",
                "type": "videoGenerationNode",
                "position": {"x": 50, "y": 1280},
                "data": {
                    "label": "Motion Shot 1: Sanctum Camera Descent (9:16)",
                    "prompt": "Cinematic vertical anime motion comic camera slow tilt-down inside ancient subterranean Vedic stone temple with glowing blue-gold glyphs on pillars, dust particles, mystery atmosphere, 9:16 vertical framing",
                    "ratio": "9:16",
                    "duration": 3,
                    "mode": "text-to-video",
                    "generateAudio": True
                }
            },
            {
                "id": "motion-shot-2",
                "type": "videoGenerationNode",
                "position": {"x": 700, "y": 1280},
                "data": {
                    "label": "Motion Shot 2: Solar Flame Shield Climax Burst (9:16)",
                    "prompt": "Dynamic anime action vertical 9:16 shot of Indian warrior youth Aarav with blazing golden solar eyes summoning an immense Vedic fire mandala shield, blocking shadowy tendrils with fiery shockwaves and flying embers",
                    "ratio": "9:16",
                    "duration": 3,
                    "mode": "image-to-video",
                    "generateAudio": True
                }
            },
            {
                "id": "motion-shot-3",
                "type": "videoGenerationNode",
                "position": {"x": 1350, "y": 1280},
                "data": {
                    "label": "Motion Shot 3: Neel Sovereign Trishul Descent (9:16)",
                    "prompt": "Epic dark anime vertical 9:16 reel of dark prince Neel floating in dark skies with glowing mystical trident trishul, swirling violet-blue cosmic galaxy vortex dispersing shadow monsters into starlight bursts",
                    "ratio": "9:16",
                    "duration": 3,
                    "mode": "text-to-video",
                    "generateAudio": True
                }
            },

            # --- Master Motion Comic Video Player Node ---
            {
                "id": "node-motion-comic-player",
                "type": "videoNode",
                "position": {"x": 1950, "y": 600},
                "data": {
                    "label": "Master 9:16 Motion Comic Reel (15.5s HD)",
                    "outputs": {
                        "video": {
                            "dataType": "VIDEO",
                            "value": {
                                "url": "assets/Chitran_Ch2_Motion_Comic_Reel.mp4",
                                "mimeType": "video/mp4"
                            }
                        }
                    }
                }
            },

            # --- Production Bible & Script Note ---
            {
                "id": "bible-script-note",
                "type": "textNode",
                "position": {"x": 1950, "y": 50},
                "data": {
                    "label": "Production Bible: Chapter 2 - The Dragon Awakens",
                    "outputs": {
                        "text": {
                            "dataType": "STRING",
                            "value": bible_text
                        }
                    }
                }
            }
        ],
        "edges": [
            # Link Characters to Page 1
            {"id": "e-char-aarav-p1", "source": "char-aarav", "sourceHandle": "image", "target": "page-001", "targetHandle": "in"},
            {"id": "e-char-ananya-p1", "source": "char-ananya", "sourceHandle": "image", "target": "page-001", "targetHandle": "in"},

            # Link Characters to Page 2
            {"id": "e-char-void-p2", "source": "char-void-stalker", "sourceHandle": "image", "target": "page-002", "targetHandle": "in"},
            {"id": "e-char-aarav-p2", "source": "char-aarav", "sourceHandle": "image", "target": "page-002", "targetHandle": "in"},

            # Link Characters to Page 3
            {"id": "e-char-neel-p3", "source": "char-neel", "sourceHandle": "image", "target": "page-003", "targetHandle": "in"},

            # Link Storyboard Pages to Motion Comic Shot Nodes
            {"id": "e-p1-to-shot1", "source": "page-001", "sourceHandle": "image", "target": "motion-shot-1", "targetHandle": "in"},
            {"id": "e-p2-to-shot2", "source": "page-002", "sourceHandle": "image", "target": "motion-shot-2", "targetHandle": "in"},
            {"id": "e-p3-to-shot3", "source": "page-003", "sourceHandle": "image", "target": "motion-shot-3", "targetHandle": "in"},
            {"id": "e-shot2-to-player", "source": "motion-shot-2", "sourceHandle": "video", "target": "node-motion-comic-player", "targetHandle": "in"}
        ]
    }

    with open(canvas_path, "w", encoding="utf-8") as f:
        json.dump(canvas_data, f, indent=2, ensure_ascii=False)

    print(f"[+] Created Toonflow canvas at: {canvas_path}")
    print(f"    Total Nodes: {len(canvas_data['nodes'])}")
    print(f"    Total Edges: {len(canvas_data['edges'])}")

if __name__ == "__main__":
    create_canvas()
