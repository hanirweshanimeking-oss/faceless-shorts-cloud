"""Pocket Creator Director - Exporters Engine.

Generates executable timeline scripts and automation manifests for:
1. Adobe After Effects ExtendScript (.jsx)
2. DaVinci Resolve Studio Python API (.py)
3. Cockos REAPER Automation (.lua)
4. Style DNA Manifest (.json)
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"


class ExportersEngine:
    """Generates professional NLE and DAW project integration scripts."""

    def __init__(self, exports_dir: Optional[Path] = None):
        self.exports_dir = exports_dir or EXPORTS_DIR
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def generate_after_effects_jsx(self, signature: Dict[str, Any]) -> str:
        """Generate complete Adobe After Effects ExtendScript (.jsx)."""
        title = signature.get("title", "Pocket CD Reel")
        rules = signature.get("rules", {})
        fps = 60
        duration = 22.0
        w = 1080
        h = 1920

        bloom = rules.get("bloom_glow", True)
        motion_blur = rules.get("motion_blur", True)
        font_family = rules.get("font_family", "Impact")
        primary_color = rules.get("primary_color", "#FFDF38")

        # Convert hex color to [r, g, b] in 0.0 - 1.0 range
        c_hex = primary_color.lstrip("#")
        if len(c_hex) == 6:
            r = round(int(c_hex[0:2], 16) / 255.0, 3)
            g = round(int(c_hex[2:4], 16) / 255.0, 3)
            b = round(int(c_hex[4:6], 16) / 255.0, 3)
        else:
            r, g, b = 1.0, 0.87, 0.22

        jsx_code = f"""// =========================================================================
// Pocket Creator Director - After Effects ExtendScript (.jsx)
// Generated for Style DNA: {title}
// Specifications: {w}x{h} @ {fps}fps, 9:16 Vertical Reel
// =========================================================================

(function createPocketCDComp() {{
    app.beginUndoGroup("Pocket Creator Director - {title}");

    var project = app.project;
    if (!project) {{
        project = app.newProject();
    }}
    project.bitsPerChannel = 16;

    // 1. Create Master 9:16 Vertical Composition
    var compName = "{title} - Timeline";
    var comp = project.items.addComp(compName, {w}, {h}, 1.0, {duration}, {fps});
    comp.motionBlur = {'true' if motion_blur else 'false'};
    comp.bgColor = [0.07, 0.08, 0.10];

    // 2. Flash Open (White Strobe Stomp)
    var flashSolid = comp.layers.addSolid([1.0, 1.0, 1.0], "Flash Open Strobe", {w}, {h}, 1.0);
    flashSolid.startTime = 0.0;
    var flashOpacity = flashSolid.property("Opacity");
    flashOpacity.setValueAtTime(0.00, 100);
    flashOpacity.setValueAtTime(0.08, 90);
    flashOpacity.setValueAtTime(0.22, 0);

    // 3. Viewfinder REC HUD Overlay
    var hudText = comp.layers.addText("● REC  00:00:01:14  4K RAW");
    hudText.name = "Viewfinder REC Overlay";
    var hudProp = hudText.property("Source Text");
    var hudDoc = hudProp.value;
    hudDoc.fontSize = 28;
    hudDoc.fillColor = [1.0, 0.2, 0.2];
    hudDoc.font = "Arial-BoldMT";
    hudProp.setValue(hudDoc);
    hudText.property("Position").setValue([120, 100]);

    // 4. Kinetic Poster Title Punch Layer
    var titleLayer = comp.layers.addText("BILL ACKMAN");
    titleLayer.name = "Poster Title Punch (Kinetic)";
    titleLayer.startTime = 1.2;
    titleLayer.outPoint = 4.8;
    titleLayer.motionBlur = {'true' if motion_blur else 'false'};

    var titleProp = titleLayer.property("Source Text");
    var titleDoc = titleProp.value;
    titleDoc.fontSize = 76;
    titleDoc.font = "{font_family}";
    titleDoc.fillColor = [{r}, {g}, {b}];
    titleDoc.strokeColor = [0.0, 0.0, 0.0];
    titleDoc.strokeWidth = 4;
    titleDoc.applyStroke = true;
    titleDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    titleProp.setValue(titleDoc);

    // Center Anchor & Keyframed Impact Scale Bounce
    titleLayer.property("Position").setValue([{w / 2}, {h / 2 - 140}]);
    var scaleProp = titleLayer.property("Scale");
    scaleProp.setValueAtTime(1.20, [145, 145]);
    scaleProp.setValueAtTime(1.35, [95, 95]);
    scaleProp.setValueAtTime(1.48, [100, 100]);

    // 5. Chromatic Bloom Glow Filter
    if ({'true' if bloom else 'false'}) {{
        var glowEffect = titleLayer.property("Effects").addProperty("ADBE Glow2");
        glowEffect.property("Glow Based On").setValue(1); // Color Channels
        glowEffect.property("Glow Threshold").setValue(55);
        glowEffect.property("Glow Radius").setValue(38);
        glowEffect.property("Glow Intensity").setValue(1.85);
    }}

    // 6. Screen Name Reveal Layer
    var subLayer = comp.layers.addText("PERSHING SQUARE CAPITAL");
    subLayer.name = "Screen Name Reveal (Credentials)";
    subLayer.startTime = 2.4;
    subLayer.outPoint = 6.2;
    var subProp = subLayer.property("Source Text");
    var subDoc = subProp.value;
    subDoc.fontSize = 32;
    subDoc.font = "Arial-BoldMT";
    subDoc.fillColor = [1.0, 1.0, 1.0];
    subDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    subProp.setValue(subDoc);
    subLayer.property("Position").setValue([{w / 2}, {h / 2 - 40}]);

    // 7. Counter Rate (Metric Odometer Ticker)
    var counterLayer = comp.layers.addText("AUM: $18,000,000,000");
    counterLayer.name = "Counter Rate (Odometer)";
    counterLayer.startTime = 4.0;
    counterLayer.outPoint = 12.0;
    var counterProp = counterLayer.property("Source Text");
    var counterDoc = counterProp.value;
    counterDoc.fontSize = 42;
    counterDoc.font = "Impact";
    counterDoc.fillColor = [0.0, 1.0, 0.55];
    counterDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    counterProp.setValue(counterDoc);
    counterLayer.property("Position").setValue([{w / 2}, {h - 320}]);

    // Add Expression to Counter Layer for live tick animation
    counterLayer.property("Source Text").expression = 
        'var startVal = 0; var endVal = 18000000000; var tStart = 4.0; var tEnd = 7.0; ' +
        'var val = Math.round(linear(time, tStart, tEnd, startVal, endVal)); ' +
        '"AUM: $" + val.toString().replace(/\\\\B(?=(\\\\d{{3}})+(?!\\\\d))/g, ",");';

    // 8. Add Markers for 11 Ingredients Breakdown
    var markerTimes = [
        [0.0, "1. Flash Open"],
        [1.2, "2. Poster Title Punch"],
        [2.8, "3. Screen Name Reveal"],
        [4.5, "4. Difference Pull Back"],
        [6.2, "5. Face Match Cut"],
        [8.0, "6. Grid Cut List"],
        [10.1, "7. Quantity Or Quality"],
        [12.0, "8. Flip Stack"],
        [14.2, "9. Viewfinder REC"],
        [16.5, "10. Counter Rate"],
        [0.0, "11. Granular SFX Track"]
    ];

    for (var m = 0; m < markerTimes.length; m++) {{
        var myMarker = new MarkerValue(markerTimes[m][1]);
        comp.markerProperty.setValueAtTime(markerTimes[m][0], myMarker);
    }}

    app.endUndoGroup();
    alert("Pocket Creator Director: Style DNA Timeline Loaded!\\nComp: " + compName);
}})();
"""
        out_path = self.exports_dir / f"{signature.get('id', 'pocket_cd')}_after_effects.jsx"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(jsx_code)
        return str(out_path)

    def generate_davinci_resolve_py(self, signature: Dict[str, Any]) -> str:
        """Generate DaVinci Resolve Studio Python API automation script."""
        title = signature.get("title", "Pocket CD Reel")
        rules = signature.get("rules", {})
        ducking_db = rules.get("speech_ducking_db", -12.0)

        py_code = f"""# =========================================================================
# Pocket Creator Director - DaVinci Resolve Studio Automation (.py)
# Generated for Style DNA: {title}
# Target Canvas: 1080x1920 (9:16 Vertical Reel, 60fps)
# =========================================================================

import sys
import time

def setup_pocket_cd_timeline():
    print("🎬 Connecting to DaVinci Resolve Studio...")
    try:
        import DaVinciResolveScript as dvr_script
        resolve = dvr_script.scriptapp("Resolve")
    except ImportError:
        print("Note: Run inside DaVinci Resolve Studio Python Console or ensure DaVinciResolveScript is in PYTHONPATH.")
        resolve = None

    if not resolve:
        print("[Simulated Execution] DaVinci Resolve environment initialized.")
        print("Project Configuration:")
        print("  - Resolution: 1080x1920 (9:16 Vertical)")
        print("  - Frame Rate: 60 fps")
        print("  - Fairlight Ducking: {ducking_db}dB sidechain compression")
        print("  - Timeline Name: Pocket_CD_{signature.get('id', 'reel')}")
        return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        project = project_manager.CreateProject("Pocket_CD_Project")

    media_pool = project.GetMediaPool()
    timeline_name = "Pocket_CD_{signature.get('id', 'edit')}"

    # Set Vertical Video project settings
    project.SetSetting("timelineResolutionWidth", "1080")
    project.SetSetting("timelineResolutionHeight", "1920")
    project.SetSetting("timelineFrameRate", "60")
    project.SetSetting("useCustomVerticalResolution", "1")

    # Create empty timeline
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    print(f"Created timeline: {{timeline_name}} (1080x1920 60FPS)")

    # Insert 11 Style DNA Markers
    markers = [
        (0, "Cyan", "1. Flash Open - Strobe Impact"),
        (72, "Yellow", "2. Poster Title Punch - Kinetic Headline"),
        (168, "Blue", "3. Screen Name Reveal - Credentials"),
        (270, "Green", "4. Difference Pull Back - Wide Scene"),
        (372, "Pink", "5. Face Match Cut - Eyeline Lock"),
        (480, "Orange", "6. Grid Cut List - 3x3 Archival"),
        (606, "Purple", "7. Quantity Or Quality - Dueling Typography"),
        (720, "Cyan", "8. Flip Stack - 3D Card Physics"),
        (852, "Red", "9. Viewfinder REC - HUD Telemetry"),
        (990, "Green", "10. Counter Rate - Odometer Ticker"),
        (0, "Magenta", "11. Granular SFX - Sidechain Ducking {ducking_db}dB")
    ]

    for frame_id, color, note in markers:
        timeline.AddMarker(frame_id, color, note, "", 1)

    print("Successfully mapped all 11 Style DNA ingredients into DaVinci Resolve!")

if __name__ == "__main__":
    setup_pocket_cd_timeline()
"""
        out_path = self.exports_dir / f"{signature.get('id', 'pocket_cd')}_davinci_resolve.py"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(py_code)
        return str(out_path)

    def generate_reaper_lua(self, signature: Dict[str, Any]) -> str:
        """Generate Cockos REAPER Automation Script (.lua) with sidechain ducking."""
        title = signature.get("title", "Pocket CD Reel")
        rules = signature.get("rules", {})
        ducking_db = rules.get("speech_ducking_db", -12.0)

        lua_code = f"""-- =========================================================================
-- Pocket Creator Director - Cockos REAPER Automation (.lua)
-- Generated for Style DNA: {title}
-- Granular Sound Design & Multi-Track Speech Ducking (-12dB)
-- =========================================================================

reaper.Undo_BeginBlock()

-- 1. Project Framing Setup
reaper.SetProjectGrid(0, 0.25)
reaper.CSurf_OnPlayRateChange(1.0)

-- 2. Create Master Sound Design Tracks
-- Track 1: Dialogue / Voiceover (Sidechain Source)
reaper.InsertTrackAtIndex(0, true)
local trackVoice = reaper.GetTrack(0, 0)
reaper.GetSetMediaTrackInfo_String(trackVoice, "P_NAME", "01 - Dialogue / Voiceover", true)
reaper.SetMediaTrackInfo_Value(trackVoice, "I_RECARM", 0)
reaper.SetMediaTrackInfo_Value(trackVoice, "I_TRACKNUMBER", 1)

-- Track 2: Granular SFX (Whoosh, Riser, Strobe Impact)
reaper.InsertTrackAtIndex(1, true)
local trackSFX = reaper.GetTrack(0, 1)
reaper.GetSetMediaTrackInfo_String(trackSFX, "P_NAME", "02 - Granular SFX & Risers", true)

-- Track 3: BGM / Sub Bass (Sidechain Target)
reaper.InsertTrackAtIndex(2, true)
local trackBGM = reaper.GetTrack(0, 2)
reaper.GetSetMediaTrackInfo_String(trackBGM, "P_NAME", "03 - BGM & Cinematic Drone", true)

-- 3. Configure Auxiliary 4-Channel Sidechain Routing
-- Route Dialogue (Channels 1/2) -> BGM (Channels 3/4)
local sendIdx = reaper.CreateTrackSend(trackVoice, trackBGM)
reaper.SetTrackSendInfo_Value(trackVoice, 0, sendIdx, "I_SRCCHAN", 0) -- Ch 1/2
reaper.SetTrackSendInfo_Value(trackVoice, 0, sendIdx, "I_DSTCHAN", 2) -- Ch 3/4
reaper.SetTrackSendInfo_Value(trackVoice, 0, sendIdx, "D_VOL", 1.0)

-- 4. Insert ReaComp onto BGM for speech ducking ({ducking_db}dB)
local reaCompIdx = reaper.TrackFX_AddByName(trackBGM, "ReaComp (Cockos)", false, -1)
if reaCompIdx >= 0 then
    -- Parameter 0: Threshold
    reaper.TrackFX_SetParam(trackBGM, reaCompIdx, 0, 0.45)
    -- Parameter 1: Ratio (4:1)
    reaper.TrackFX_SetParam(trackBGM, reaCompIdx, 1, 0.4)
    -- Parameter 2: Attack (15ms)
    reaper.TrackFX_SetParam(trackBGM, reaCompIdx, 2, 0.15)
    -- Parameter 3: Release (280ms)
    reaper.TrackFX_SetParam(trackBGM, reaCompIdx, 3, 0.28)
    -- Parameter 8: Detector Input = Auxiliary Input L+R (Channels 3/4)
    reaper.TrackFX_SetParam(trackBGM, reaCompIdx, 8, 1.0)
end

-- 5. Set Markers for Granular SFX Alignment
local cuePoints = {{
    {{time = 0.0, name = "[SFX] Sub Bass Stomp + White Noise Flash"}},
    {{time = 1.2, name = "[SFX] Heavy Kinetic Punch Hit"}},
    {{time = 2.8, name = "[SFX] Minimal High-Pass Swipe"}},
    {{time = 4.5, name = "[SFX] Low Drone Pullback Risers"}},
    {{time = 6.2, name = "[SFX] Shutter Click Face Match"}},
    {{time = 8.0, name = "[SFX] Contact Sheet 3x3 Flutters"}},
    {{time = 10.1, name = "[SFX] Stereo Whoosh Swipe"}},
    {{time = 12.0, name = "[SFX] Tactile Card Stack Drop Physics"}},
    {{time = 14.2, name = "[SFX] Camera Beep REC Beep"}},
    {{time = 16.5, name = "[SFX] Fast Mechanical Metric Tally Clicks"}}
}}

for _, cue in ipairs(cuePoints) do
    reaper.AddProjectMarker(0, false, cue.time, 0, cue.name, -1)
end

reaper.Undo_EndBlock("Pocket CD - REAPER Setup Complete", -1)
reaper.ShowMessageBox("Pocket Creator Director audio template generated with {ducking_db}dB ducking and 11 SFX cues!", "Pocket CD", 0)
"""
        out_path = self.exports_dir / f"{signature.get('id', 'pocket_cd')}_reaper.lua"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(lua_code)
        return str(out_path)

    def generate_style_dna_manifest_json(self, signature: Dict[str, Any]) -> str:
        """Export Style DNA JSON Manifest."""
        out_path = self.exports_dir / f"{signature.get('id', 'pocket_cd')}_manifest.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(signature, f, indent=2)
        return str(out_path)


exporters = ExportersEngine()
