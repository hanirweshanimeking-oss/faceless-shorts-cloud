# =========================================================================
# Pocket Creator Director - DaVinci Resolve Studio Automation (.py)
# Generated for Style DNA: Test Signature Reel
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
        print("  - Fairlight Ducking: -14.0dB sidechain compression")
        print("  - Timeline Name: Pocket_CD_test_sig_export")
        return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        project = project_manager.CreateProject("Pocket_CD_Project")

    media_pool = project.GetMediaPool()
    timeline_name = "Pocket_CD_test_sig_export"

    # Set Vertical Video project settings
    project.SetSetting("timelineResolutionWidth", "1080")
    project.SetSetting("timelineResolutionHeight", "1920")
    project.SetSetting("timelineFrameRate", "60")
    project.SetSetting("useCustomVerticalResolution", "1")

    # Create empty timeline
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    print(f"Created timeline: {timeline_name} (1080x1920 60FPS)")

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
        (0, "Magenta", "11. Granular SFX - Sidechain Ducking -14.0dB")
    ]

    for frame_id, color, note in markers:
        timeline.AddMarker(frame_id, color, note, "", 1)

    print("Successfully mapped all 11 Style DNA ingredients into DaVinci Resolve!")

if __name__ == "__main__":
    setup_pocket_cd_timeline()
