"""
Faceless Shorts Subtitle Engine
Word-by-word timestamps from local Whisper with viral highlight generation.
Outputs structured JSON and styled ASS/SRT for dynamic animated subtitles.
"""
import os
import json
from typing import List, Dict, Any, Optional

_whisper_instance = None

def get_whisper_model(model_size: str = "tiny"):
    global _whisper_instance
    if _whisper_instance is None:
        from faster_whisper import WhisperModel
        # CPU int8 execution for fast low-memory inference
        _whisper_instance = WhisperModel(model_size, device="cpu", compute_type="int8")
    return _whisper_instance

def extract_word_timestamps(audio_path: str) -> List[Dict[str, Any]]:
    """
    Transcribes audio and extracts precise word-level start/end timestamps.
    Returns: List of dicts with keys: 'word', 'start', 'end', 'probability'
    """
    model = get_whisper_model()
    segments, _ = model.transcribe(
        audio_path,
        word_timestamps=True,
        language="en"
    )
    
    words_data = []
    for segment in segments:
        for w in segment.words:
            clean_word = w.word.strip()
            if clean_word:
                words_data.append({
                    "word": clean_word,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })
                
    return words_data

def group_words_into_phrases(words: List[Dict[str, Any]], max_words: int = 3) -> List[Dict[str, Any]]:
    """
    Groups words into short, high-impact screen phrases (1 to 3 words)
    suitable for fast-paced vertical Reels / Shorts.
    """
    phrases = []
    i = 0
    n = len(words)
    
    while i < n:
        chunk = words[i : min(i + max_words, n)]
        start_time = chunk[0]["start"]
        end_time = chunk[-1]["end"]
        phrase_text = " ".join(w["word"] for w in chunk)
        
        phrases.append({
            "text": phrase_text,
            "start": start_time,
            "end": end_time,
            "words": chunk
        })
        i += len(chunk)
        
    return phrases

def format_ass_time(seconds: float) -> str:
    """Formats float seconds into ASS time format: H:MM:SS.cs"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

def generate_viral_ass_subtitles(
    phrases: List[Dict[str, Any]],
    output_ass_path: str,
    font_name: str = "Arial Black",
    font_size: int = 68,
    primary_color: str = "&H00FFFFFF",      # White in BGR
    highlight_color: str = "&H0000E6FF",    # Viral Yellow in BGR (#FFE600 -> &H0000E6FF)
    border_color: str = "&H00000000",       # Black border
    border_width: int = 8,
    shadow_width: int = 4
) -> str:
    """
    Generates an Advanced SubStation Alpha (.ass) file with word-by-word yellow highlight animation.
    """
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralYellow,{font_name},{font_size},{primary_color},&H000000FF,{border_color},&H80000000,-1,0,0,0,100,100,1,0,1,{border_width},{shadow_width},2,60,60,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for ph in phrases:
        p_words = ph["words"]
        for active_idx, w in enumerate(p_words):
            w_start = format_ass_time(w["start"])
            w_end = format_ass_time(w["end"])
            
            # Build phrase with the active word colored yellow and scaled slightly
            colored_parts = []
            for j, other_w in enumerate(p_words):
                if j == active_idx:
                    colored_parts.append(f"{{\\c{highlight_color}\\fscx112\\fscy112}}{other_w['word']}{{\\r}}")
                else:
                    colored_parts.append(f"{{\\c{primary_color}}}{other_w['word']}{{\\r}}")
                    
            event_text = " ".join(colored_parts)
            lines.append(f"Dialogue: 0,{w_start},{w_end},ViralYellow,,0,0,0,,{event_text}")
            
    os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")
        
    return output_ass_path
