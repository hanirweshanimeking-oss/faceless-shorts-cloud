"""
Faceless Shorts Master Vault & Scheduler
Manages 670 scheduled viral reels (10 reels/day across 10 peak viral timings)
from Nov 8, 2026 to Jan 14, 2027 for Instagram Reels & YouTube Shorts.
Stores all production files safely on Drive E: (364 GB free).
"""
import os
import sys
import json
import sqlite3
import datetime
from typing import List, Dict, Any, Optional

from faceless_engine.config import FFMPEG_BIN, FFMPEG_BIN
from faceless_engine.pipeline import create_faceless_short
from faceless_engine.script_writer import ViralScript, SceneBeat
from faceless_engine.voice_engine import generate_voiceover
from faceless_engine.subtitle_engine import extract_word_timestamps, group_words_into_phrases, generate_viral_ass_subtitles
from faceless_engine.visual_engine import TallTaleRenderer
from faceless_engine.audio_mixer import synthesize_sfx, mix_master_audio
from faceless_engine.compositor import concatenate_scene_videos, burn_subtitles_and_master, qa_verify_video

# Drive E: storage vault
VAULT_DIR = "E:\\faceless_shorts_vault"
if not os.path.exists("E:\\"):
    # Fallback to D: or workspace if E: not available
    VAULT_DIR = "D:\\faceless_shorts_vault" if os.path.exists("D:\\") else os.path.abspath("output/faceless_vault")

os.makedirs(VAULT_DIR, exist_ok=True)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dragon_studios", "database", "dragon_studios.db"))

# The 10 Daily Peak Viral Engagement Timings (IST)
DAILY_SLOTS = [
    {"slot": 1,  "time": "08:15", "pillar": "MINDSET_PSYCHOLOGY",   "style": "Tall Tale 3D",  "focus": "Morning mindset & crazy human behavior"},
    {"slot": 2,  "time": "09:45", "pillar": "INSIDE_OUT_SCIENCE",   "style": "Inside Out",    "focus": "How things actually work inside everyday objects"},
    {"slot": 3,  "time": "11:30", "pillar": "CRAZY_LOOPHOLES",      "style": "Tall Tale 3D",  "focus": "Financial loopholes, heists, and legal glitches"},
    {"slot": 4,  "time": "13:15", "pillar": "DEEP_DIVE_ANATOMY",    "style": "Deep Dive 3D",  "focus": "Zack D. style human body & medical explainers"},
    {"slot": 5,  "time": "15:00", "pillar": "SURVIVAL_DILEMMAS",    "style": "Stick Story",   "focus": "Hypothetical dilemmas, escape hacks, and riddles"},
    {"slot": 6,  "time": "16:45", "pillar": "HISTORIC_CONQUESTS",   "style": "Paper Atlas",   "focus": "Epic battles, empire collapses, and map journeys"},
    {"slot": 7,  "time": "18:30", "pillar": "BIZARRE_INVENTIONS",   "style": "Tall Tale 3D",  "focus": "Wild inventions that accidentally made millions"},
    {"slot": 8,  "time": "20:00", "pillar": "NIGHT_FILE_MYSTERIES", "style": "Night File 3D", "focus": "Atmospheric unsolved crimes and spooky history"},
    {"slot": 9,  "time": "21:30", "pillar": "GLOBAL_WEALTH_HACKS",  "style": "Tall Tale 3D",  "focus": "US/EU peak crossover - billionaires & wealth glitches"},
    {"slot": 10, "time": "23:00", "pillar": "DARK_PSYCHOLOGY",      "style": "Tall Tale 3D",  "focus": "Late-night psychological paradoxes & cognitive tricks"}
]

# Curated Topic Seeds for high retention
VIRAL_SEEDS = [
    # Loopholes & Heists
    ("The Man Who Bought an Entire Bank for $1", "In 1995, one man walked into Britain's oldest bank and bought the whole empire for one dollar."),
    ("The Grocery Store Millionaire", "In 1999, an engineer found a pudding coupon glitch that earned him 1.2 million frequent flyer miles for free."),
    ("The Red Paperclip Trade", "In 2005, one man started with a single red paperclip and traded it fourteen times until he owned a two-story house."),
    ("The Fake Cop Who Stole 100 Million", "In 1990, two men dressed as police officers walked into a Boston museum and pulled off the biggest art heist in history."),
    ("The Man Who Sued Pepsi for a Harrier Jet", "In 1996, a college student collected seven million Pepsi points to claim an actual military fighter jet."),
    ("The Bank Teller Who Stole Pennies", "How one accountant rounded down bank transaction fractions to zero and quietly pocketed millions without anyone noticing."),
    ("The Guy Who Sold the Eiffel Tower Twice", "Victor Lustig posed as a French government official and successfully sold the Eiffel Tower for scrap metal—two separate times."),
    ("The Lottery Professor Who Broke the Odds", "A retired math professor noticed an arithmetic flaw in the state lottery and won 26 million dollars completely legally."),
    ("The Airline Ticket Name Loophole", "How a student changed his legal name to save two hundred dollars on an airline ticket correction fee."),
    ("The Man Who Rented a Luxury Penthouse for $0", "A tenant discovered a 19th-century real estate law that granted him free rent for twenty-five years."),
    
    # Body & Medical (Zack D. style)
    ("What Actually Happens If You Swallow Chewing Gum?", "Contrary to school rumors, gum does not stay in your stomach for seven years—here is what your body actually does."),
    ("What Happens When a Bullet Ant Stings You?", "The bullet ant sting creates 24 hours of burning waves that feel like being struck by a hot bullet."),
    ("Why Your Brain Wakes Up Right Before You Die in a Dream", "Your brain cannot simulate the actual afterlife, so it triggers an emergency adrenaline shock to pull you awake."),
    ("What Happens If You Drink Liquid Nitrogen?", "Freezing your throat in milliseconds causes instant gas expansion that can explode internal tissues."),
    ("Why Cracking Your Knuckles Doesn't Cause Arthritis", "The pop is actually nitrogen gas bubbles collapsing inside synovial fluid, completely harmless to your joints."),
    ("What Happens If You Never Sleep for 11 Days?", "Hallucinations, paranoia, and organ shutdown: what happened to Randy Gardner during his extreme sleep experiment."),
    ("Why Salt Water Makes You Dehydrated Faster", "Your kidneys need more fresh water to flush out ocean salt than the ocean water actually provides."),
    ("What Happens Inside Your Ear When You Use a Q-Tip?", "Instead of cleaning wax, you are packing it tightly against your eardrum like a cannon plug."),
    ("Why Your Eyes Twitch Uncontrollably", "Myokymia happens when sleep deprivation and caffeine trigger misfiring facial nerve impulses."),
    ("How Mosquitoes Actually Find Your Blood", "They detect the carbon dioxide plumes you exhale from fifty yards away before tasting your heat signature."),

    # Science & Inside Out
    ("How Airplanes Dump Fuel in Mid-Air", "When emergency landings happen, pilots vent thousands of gallons of jet fuel that vaporize into clouds before hitting the ground."),
    ("Why Submarines Cannot Use Regular Windows", "At deep ocean depths, glass windows crack from water pressure equal to an elephant standing on your thumb."),
    ("How Escalator Handrails Move at a Different Speed", "The handrail uses a friction pulley that wears down faster than the metal step drive chains."),
    ("Why Mirror Glass Appears Green Around the Edges", "Standard float glass contains tiny traces of iron oxide that absorb red light, leaving an emerald rim."),
    ("How Noise-Canceling Headphones Kill Sound", "They listen to incoming sound waves and instantly blast the exact opposite sound wave to erase the noise in mid-air."),
    ("Why Highway Overpasses Have Bumpy Expansion Joints", "Concrete expands in the summer heat; without those steel teeth, the entire highway would buckle and crack."),
    ("How Bulletproof Glass Actually Stops Bullets", "A tough layer of polycarbonate absorbs the kinetic punch and flattens the lead mushroom before it breaks through."),
    ("Why Ship Hulls Have a Bulbous Nose Underwater", "That rounded bulb creates a cancelling wave that cuts water drag and saves millions in fuel every year."),
    ("How Traffic Jams Form for No Reason", "A phantom traffic jam occurs when one driver taps their brakes, creating a shockwave that stalls cars miles behind them."),
    ("Why Airbags Deploy with Explosive Rocket Fuel", "They use sodium azide pellets that ignite into harmless nitrogen gas in under thirty milliseconds flat."),

    # Dark Psychology & Paradoxes
    ("The Benjamin Franklin Effect", "If you want someone to like you, do not do them a favor—ask them to do a small favor for you instead."),
    ("The Doorway Effect: Why You Forget When Entering a Room", "Walking through a doorway signals your brain to clear working memory and create a fresh mental event boundary."),
    ("The Dark Mirror Technique in Negotiations", "Repeating the last three words of someone's sentence with a rising inflection forces them to involuntarily confess details."),
    ("The Spotlight Effect: Nobody Is Watching You", "We overestimate how much people notice our flaws by over four hundred percent due to ego-centric bias."),
    ("The Bystander Paradox", "The more people who witness an emergency, the less likely anyone is to help because responsibility is diffused across the crowd."),
    ("The Pygmalion Effect: How Expectations Shape Reality", "When someone believes you are capable of greatness, your brain subconscious aligns behavior to fulfill their prediction."),
    ("Why Liars Always Over-Explain Details", "Deceptive storytellers add unnecessary times, names, and routes because they rehearse a script rather than recalling a memory."),
    ("The Zeigarnik Effect: Why Cliffhangers Drive You Crazy", "Your brain cannot rest when a task is unfinished; it keeps firing cognitive alarms until resolution is reached."),
    ("The Contrast Principle of Influence", "Showing an overpriced 5,000 dollar item first makes the 500 dollar item feel like a total bargain."),
    ("The Silent Treatment Paradox", "Ignoring someone activates the anterior cingulate cortex—the exact same brain region that registers physical bodily pain.")
]

def init_scheduler_db():
    """Initializes the scheduled_reels table in dragon_studios.db."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_reels (
            id TEXT PRIMARY KEY,
            date_str TEXT NOT NULL,
            slot_number INTEGER NOT NULL,
            scheduled_time TEXT NOT NULL,
            pillar TEXT NOT NULL,
            style TEXT NOT NULL,
            title TEXT NOT NULL,
            hook_text TEXT NOT NULL,
            script_json TEXT NOT NULL,
            caption TEXT NOT NULL,
            hashtags TEXT NOT NULL,
            yt_title TEXT NOT NULL,
            yt_description TEXT NOT NULL,
            yt_tags TEXT NOT NULL,
            video_path TEXT,
            status TEXT NOT NULL CHECK(status IN ('SCHEDULED', 'RENDERING', 'READY', 'PUBLISHED', 'FAILED')),
            published_platforms TEXT DEFAULT 'INSTAGRAM,YOUTUBE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sched_date ON scheduled_reels(date_str, slot_number);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sched_status ON scheduled_reels(status);")
        conn.commit()

def generate_packaging(title: str, hook: str, pillar: str, style: str) -> Dict[str, Any]:
    """Generates high-converting captions, search terms, and hashtags for Instagram & YouTube."""
    # Instagram Caption with the "more" cut hook
    ig_caption = (
        f"{hook} 🤯\n\n"
        f"Did you know this actually happened? Watch till the end to see how this crazy loophole unfolded!\n\n"
        f"💬 Drop your thoughts below — would you have done the same thing?\n\n"
        f"👉 Follow @dragon.studios.india for daily mind-blowing true stories & animated breakdowns."
    )
    
    # Curated high-volume hashtags
    pillar_tags = {
        "CRAZY_LOOPHOLES": "#loopholes #truestory #crazyfacts #historyfacts #mindblown #billionairemindset #moneyglitch",
        "DEEP_DIVE_ANATOMY": "#bodyfacts #anatomy #sciencefacts #medicalmystery #zackdfilms #biology #didyouknow",
        "INSIDE_OUT_SCIENCE": "#howitworks #engineering #sciencefacts #curiosity #satisfying #techfacts #interestingfacts",
        "MINDSET_PSYCHOLOGY": "#psychology #darkpsychology #mindset #manipulation #humanbehavior #stoic #brainhacks",
        "SURVIVAL_DILEMMAS": "#survival #riddles #whatwouldyoudo #lifehacks #hypothetical #puzzles #dilemma",
        "HISTORIC_CONQUESTS": "#history #ancienthistory #epicbattles #warhistory #empires #worldhistory #maps",
        "NIGHT_FILE_MYSTERIES": "#mystery #unsolved #truecrime #spookyhistory #creepyfacts #paranormal #investigation",
        "GLOBAL_WEALTH_HACKS": "#wealth #moneyhacks #businessgrowth #entrepreneur #success #financialfreedom #millionaire",
        "DARK_PSYCHOLOGY": "#darkpsychology #psychologytricks #influence #behavior #mindcontrol #subconscious #philosophy",
        "BIZARRE_INVENTIONS": "#inventions #creativity #viralfacts #bizarre #entrepreneur #businessstories #trending"
    }
    
    hashtags = pillar_tags.get(pillar, "#viral #shorts #reels #facts #truestory #trending")
    
    # YouTube Short Title (< 60 chars)
    yt_title = (title[:48] + " #Shorts") if len(title) > 48 else f"{title} #Shorts"
    
    # YouTube Description with SEO keywords
    yt_description = (
        f"{hook}\n\n"
        f"In this animated Short, we explore the incredible true story of {title}.\n\n"
        f"Subscribe to Dragon Studios India for daily animated deep dives, true stories, and psychology breakdowns!\n\n"
        f"#Shorts #Animated #TrueStory #Viral #DidYouKnow"
    )
    
    yt_tags = "Shorts, Animation, True Story, Facts, Psychology, Loopholes, Science, Dragon Studios"
    
    return {
        "ig_caption": ig_caption,
        "hashtags": hashtags,
        "yt_title": yt_title,
        "yt_description": yt_description,
        "yt_tags": yt_tags
    }

def populate_master_calendar(start_date_str: str = "2026-11-08", end_date_str: str = "2027-01-14"):
    """
    Populates all 670 time slots (10 slots/day across 67 days) in the database.
    Nov 8, 2026 to Jan 14, 2027.
    """
    init_scheduler_db()
    start_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    
    total_days = (end_dt - start_dt).days + 1
    total_slots = total_days * 10
    
    print(f"[MasterCalendar] Populating {total_days} days ({total_slots} total reel slots) from {start_date_str} to {end_date_str}...")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        inserted = 0
        seed_idx = 0
        current_dt = start_dt
        
        while current_dt <= end_dt:
            date_str = current_dt.strftime("%Y-%m-%d")
            
            for s in DAILY_SLOTS:
                slot_num = s["slot"]
                slot_time = s["time"]
                scheduled_timestamp = f"{date_str} {slot_time}:00"
                reel_id = f"reel_{date_str}_{slot_num:02d}"
                
                # Check if already present
                exists = cursor.execute("SELECT 1 FROM scheduled_reels WHERE id = ?", (reel_id,)).fetchone()
                if not exists:
                    # Pick topic seed
                    title, hook = VIRAL_SEEDS[seed_idx % len(VIRAL_SEEDS)]
                    seed_idx += 1
                    
                    pkg = generate_packaging(title, hook, s["pillar"], s["style"])
                    
                    cursor.execute("""
                        INSERT INTO scheduled_reels (
                            id, date_str, slot_number, scheduled_time, pillar, style,
                            title, hook_text, script_json, caption, hashtags,
                            yt_title, yt_description, yt_tags, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SCHEDULED')
                    """, (
                        reel_id, date_str, slot_num, scheduled_timestamp, s["pillar"], s["style"],
                        title, hook, json.dumps({"title": title, "hook": hook}), pkg["ig_caption"], pkg["hashtags"],
                        pkg["yt_title"], pkg["yt_description"], pkg["yt_tags"]
                    ))
                    inserted += 1
                    
            current_dt += datetime.timedelta(days=1)
            
        conn.commit()
        
    print(f"[MasterCalendar] Successfully created/verified {total_slots} scheduled reel slots ({inserted} new entries added).")

def render_scheduled_reel(reel_id: str) -> Optional[str]:
    """
    Renders a specific scheduled reel into the Drive E: vault.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM scheduled_reels WHERE id = ?", (reel_id,)).fetchone()
        if not row:
            return None
            
        reel = dict(row)

    project_slug = reel["id"]
    output_video_path = os.path.join(VAULT_DIR, f"{project_slug}.mp4")
    
    if os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 1000000:
        # Already rendered
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE scheduled_reels SET status = 'READY', video_path = ? WHERE id = ?", (output_video_path, reel_id))
            conn.commit()
        return output_video_path

    # Mark as rendering
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE scheduled_reels SET status = 'RENDERING' WHERE id = ?", (reel_id,))
        conn.commit()

    print(f"\n[SchedulerVault] Rendering reel '{reel['title']}' ({reel['id']}) into {VAULT_DIR}...")
    try:
        res = create_faceless_short(
            prompt=reel["title"],
            style=reel["style"],
            voice="am_adam",
            project_slug=project_slug
        )
        final_mp4 = res.get("final_video_path")
        
        # Copy or move into VAULT_DIR if not already there
        vault_mp4 = os.path.join(VAULT_DIR, f"{project_slug}.mp4")
        if final_mp4 and os.path.exists(final_mp4) and final_mp4 != vault_mp4:
            import shutil
            shutil.copy2(final_mp4, vault_mp4)
            final_mp4 = vault_mp4
            
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE scheduled_reels SET status = 'READY', video_path = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (final_mp4, reel_id))
            conn.commit()
            
        print(f"[SchedulerVault] ✓ Reel {reel_id} rendered successfully -> {final_mp4}")
        return final_mp4
    except Exception as e:
        print(f"[SchedulerVault] ✗ Failed rendering {reel_id}: {e}")
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE scheduled_reels SET status = 'FAILED' WHERE id = ?", (reel_id,))
            conn.commit()
        return None

def render_batch_for_date(date_str: str, max_count: int = 10) -> List[str]:
    """Renders all reels scheduled for a specific date (e.g. today or tomorrow)."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id FROM scheduled_reels WHERE date_str = ? ORDER BY slot_number ASC LIMIT ?",
            (date_str, max_count)
        ).fetchall()
        reel_ids = [r["id"] for r in rows]

    rendered_paths = []
    for rid in reel_ids:
        path = render_scheduled_reel(rid)
        if path:
            rendered_paths.append(path)
            
    return rendered_paths

def get_schedule_summary(date_str: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves scheduled reels for display."""
    if date_str is None:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM scheduled_reels WHERE date_str = ? ORDER BY slot_number ASC",
            (date_str,)
        ).fetchall()
        return [dict(r) for r in rows]

if __name__ == "__main__":
    populate_master_calendar()
