import os
import sys

sys.path.insert(0, os.path.abspath("."))
from dragon_studios.integrations.ayanokoji_voice import generate_html_player

def main():
    tracks = [
        {
            "name": "Kiyotaka Ayanokoji - Modern English Casual Slang",
            "badge": "ENGLISH NATURAL SLANG (RVC v2)",
            "description": "Natural conversational cadence & everyday slang: 'Look... to be honest? Most people think they're special. Truth is, everyone is just a tool to be used. I don't give a damn what needs to get sacrificed along the way. At the end of the day, winning is the only thing that actually matters.'",
            "file_path": "output/ayanokoji_slang_english.mp3"
        },
        {
            "name": "Kiyotaka Ayanokoji - Modern Hinglish Street Slang",
            "badge": "HINGLISH CASUAL SLANG (RVC v2)",
            "description": "Realistic conversational flow the way modern youth & creators actually speak: 'Sach bolu toh... log sochte hain wo bohot khaas hain. Par mere liye na, sab bas ek zariya hain, ek mohra. Mujhe ghanta farak nahi padta kisko qurban karna pade. End mein bas ek hi cheez matter karti hai... meri jeet.'",
            "file_path": "output/ayanokoji_slang_hinglish.mp3"
        },
        {
            "name": "Kiyotaka Ayanokoji - Conversational Hindi Slang",
            "badge": "HINDI NATURAL SLANG (RVC v2)",
            "description": "Natural everyday spoken Hindi flow: 'सच कहूं तो... लोग सोचते हैं कि वो बहुत खास हैं। पर सच ये है, कि मेरे लिए सब सिर्फ एक मोहरा हैं। मुझे कोई फर्क नहीं पड़ता कि रास्ते में किसकी बलि चढ़ानी पड़े। आखिरकार, सिर्फ जीत ही मायने रखती है।'",
            "file_path": "output/ayanokoji_slang_hindi_natural.mp3"
        },
        {
            "name": "Kiyotaka Ayanokoji - Classic Formal English Monologue",
            "badge": "FORMAL ANIME THEATER",
            "description": "Justin Briner cold monologue: 'All people are nothing but tools. It does not matter what needs to be sacrificed. In this world, winning is everything...'",
            "file_path": "output/ayanokoji_english_dub.mp3"
        },
        {
            "name": "Original Anime Reference: English Dub Studio Monologue",
            "badge": "ANIME REFERENCE STEM (EN)",
            "description": "Official English voice of Kiyotaka Ayanokoji (Justin Briner) from Season 1 finale.",
            "file_path": "models/ayanokoji_reference/ayanokoji_monologue_tools_en.wav"
        }
    ]

    out_path = "output/ayanokoji_player.html"
    generate_html_player(tracks, out_path)
    print(f"Generated clean player: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    main()
