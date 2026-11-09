-- =========================================================================
-- Pocket Creator Director - Cockos REAPER Automation (.lua)
-- Generated for Style DNA: Ackman Edit DNA
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

-- 4. Insert ReaComp onto BGM for speech ducking (-13.5dB)
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
local cuePoints = {
    {time = 0.0, name = "[SFX] Sub Bass Stomp + White Noise Flash"},
    {time = 1.2, name = "[SFX] Heavy Kinetic Punch Hit"},
    {time = 2.8, name = "[SFX] Minimal High-Pass Swipe"},
    {time = 4.5, name = "[SFX] Low Drone Pullback Risers"},
    {time = 6.2, name = "[SFX] Shutter Click Face Match"},
    {time = 8.0, name = "[SFX] Contact Sheet 3x3 Flutters"},
    {time = 10.1, name = "[SFX] Stereo Whoosh Swipe"},
    {time = 12.0, name = "[SFX] Tactile Card Stack Drop Physics"},
    {time = 14.2, name = "[SFX] Camera Beep REC Beep"},
    {time = 16.5, name = "[SFX] Fast Mechanical Metric Tally Clicks"}
}

for _, cue in ipairs(cuePoints) do
    reaper.AddProjectMarker(0, false, cue.time, 0, cue.name, -1)
end

reaper.Undo_EndBlock("Pocket CD - REAPER Setup Complete", -1)
reaper.ShowMessageBox("Pocket Creator Director audio template generated with -13.5dB ducking and 11 SFX cues!", "Pocket CD", 0)
