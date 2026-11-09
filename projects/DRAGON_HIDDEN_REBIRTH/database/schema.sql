-- SSS+ Manga Production Database Schema
-- Project: DRAGON: HIDDEN REBIRTH
-- Engine: SQLite 3

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS story_bible (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL, -- 'PREMISE', 'LORE', 'MAGIC_SYSTEM', 'CHRONOLOGY'
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    version TEXT DEFAULT '1.0.0',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    alias TEXT,
    age TEXT,
    gender TEXT,
    height_cm INTEGER,
    build TEXT,
    facial_features TEXT,
    hair_details TEXT,
    eye_details TEXT,
    clothing_details TEXT,
    weapons TEXT,
    personality_traits TEXT,
    visual_prompt_base TEXT NOT NULL,
    negative_prompt TEXT,
    master_seed INTEGER DEFAULT 42,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_references (
    id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL,
    view_type TEXT NOT NULL, -- 'FRONT', 'SIDE', 'BACK', 'CLOSEUP', 'ACTION'
    expression_type TEXT DEFAULT 'NEUTRAL', -- 'NEUTRAL', 'COLD_GLARE', 'AWAKENED', 'SMUG'
    outfit_variant TEXT DEFAULT 'DEFAULT',
    image_path TEXT,
    is_approved BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(character_id) REFERENCES characters(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS world_locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    description TEXT NOT NULL,
    visual_prompt TEXT NOT NULL,
    reference_image_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapters (
    id TEXT PRIMARY KEY,
    chapter_number INTEGER NOT NULL UNIQUE,
    title TEXT NOT NULL,
    logline TEXT NOT NULL,
    target_pages INTEGER DEFAULT 20,
    status TEXT DEFAULT 'DRAFT' CHECK(status IN ('DRAFT', 'STORYBOARDING', 'GENERATING', 'COMPOSING', 'QA_REVIEW', 'APPROVED', 'EXPORTED')),
    reading_direction TEXT DEFAULT 'RTL' CHECK(reading_direction IN ('RTL', 'LTR', 'VERTICAL_WEBTOON')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pages (
    id TEXT PRIMARY KEY,
    chapter_id TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    layout_type TEXT DEFAULT 'DYNAMIC_ACTION', -- 'DYNAMIC_ACTION', 'DOUBLE_SPREAD', 'CONVERSATIONAL', 'VERTICAL_STRIP'
    width_px INTEGER DEFAULT 2480,  -- Standard B5 Manga 300 DPI (2480 x 3508)
    height_px INTEGER DEFAULT 3508,
    dpi INTEGER DEFAULT 300,
    reading_direction TEXT DEFAULT 'RTL',
    master_image_path TEXT,
    status TEXT DEFAULT 'PLANNED' CHECK(status IN ('PLANNED', 'STORYBOARDED', 'GENERATING_PANELS', 'COMPOSITED', 'QA_PASSED', 'FAILED')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
    UNIQUE(chapter_id, page_number)
);

CREATE TABLE IF NOT EXISTS panels (
    id TEXT PRIMARY KEY,
    page_id TEXT NOT NULL,
    panel_index INTEGER NOT NULL,
    bbox_x INTEGER NOT NULL,
    bbox_y INTEGER NOT NULL,
    bbox_w INTEGER NOT NULL,
    bbox_h INTEGER NOT NULL,
    shot_type TEXT DEFAULT 'MEDIUM', -- 'EXTREME_WIDE', 'WIDE', 'MEDIUM', 'CLOSE_UP', 'DUTCH_ANGLE'
    character_ids TEXT, -- JSON array of character ids
    visual_prompt TEXT NOT NULL,
    dialogue_text TEXT,
    speaker_name TEXT,
    thought_text TEXT,
    sfx_text TEXT,
    sfx_style TEXT, -- 'EXPLOSION', 'SLASH', 'CRACKLE', 'HEAVY_IMPACT'
    balloon_position TEXT, -- 'TOP_RIGHT', 'TOP_LEFT', 'CENTER', 'BOTTOM'
    screentone_style TEXT DEFAULT 'STANDARD_DOTS',
    raw_panel_path TEXT,
    final_panel_path TEXT,
    status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'GENERATED', 'INKED', 'COMPOSITED', 'DEFECTIVE')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(page_id) REFERENCES pages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS qa_reports (
    id TEXT PRIMARY KEY,
    page_id TEXT NOT NULL,
    overall_verdict TEXT CHECK(overall_verdict IN ('PASS', 'REVISE', 'FAIL')),
    score_composition REAL DEFAULT 0.0,
    score_contrast REAL DEFAULT 0.0,
    score_character_consistency REAL DEFAULT 0.0,
    score_readability REAL DEFAULT 0.0,
    defect_notes TEXT,
    inspector TEXT DEFAULT 'Automated_QA_Agent',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(page_id) REFERENCES pages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS production_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    context_json TEXT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
