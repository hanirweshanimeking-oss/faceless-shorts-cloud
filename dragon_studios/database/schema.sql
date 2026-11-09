-- Dragon Studios India: SQLite Database Schema
-- Location: dragon_studios/database/schema.sql

PRAGMA foreign_keys = ON;

-- 1. Projects Master Table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    pillar TEXT NOT NULL CHECK(pillar IN ('ORIGINAL_MANGA', 'DARK_PSYCHOLOGY', 'CINEMATIC_EDIT', 'AI_TOOLS', 'TECH_HACKS', 'CONVERSATIONAL_PODCAST', 'RAJ_SHAMANI')),
    concept TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'GENERATING', 'EDITING', 'PENDING_APPROVAL', 'APPROVED', 'PUBLISHED', 'FAILED')),
    aspect_ratio TEXT DEFAULT '9:16',
    target_duration REAL DEFAULT 30.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Scene Breakdown & Production Timeline
CREATE TABLE IF NOT EXISTS scenes (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    scene_order INTEGER NOT NULL,
    duration_seconds REAL NOT NULL,
    dialogue_text TEXT,
    visual_prompt TEXT NOT NULL,
    camera_movement TEXT,
    video_asset_path TEXT,
    audio_asset_path TEXT,
    subtitle_text TEXT,
    status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'GENERATING', 'COMPLETED', 'FAILED')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 3. Character Consistency Vault
CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    universe TEXT DEFAULT 'Chitran',
    visual_description TEXT NOT NULL,
    master_seed INTEGER,
    reference_image_path TEXT,
    negative_prompt TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Audio & Sound FX Asset Library
CREATE TABLE IF NOT EXISTS audio_assets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('MUSIC', 'SFX', 'VOICEOVER', 'AMBIENCE')),
    mood TEXT,
    file_path TEXT NOT NULL,
    duration_seconds REAL,
    license_type TEXT DEFAULT 'ROYALTY_FREE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Publishing Records (Multi-Platform)
CREATE TABLE IF NOT EXISTS publishing_records (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    platform TEXT NOT NULL CHECK(platform IN ('INSTAGRAM', 'YOUTUBE')),
    platform_media_id TEXT,
    post_url TEXT,
    caption TEXT NOT NULL,
    hashtags TEXT,
    thumbnail_path TEXT,
    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'SCHEDULED', 'PUBLISHING', 'PUBLISHED', 'FAILED')),
    scheduled_time DATETIME,
    published_time DATETIME,
    approved_by TEXT,
    approval_timestamp DATETIME,
    error_log TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 6. Analytics Snapshots
CREATE TABLE IF NOT EXISTS analytics_snapshots (
    id TEXT PRIMARY KEY,
    publishing_id TEXT NOT NULL,
    snapshot_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    watch_time_seconds REAL DEFAULT 0,
    retention_rate REAL DEFAULT 0,
    click_through_rate REAL DEFAULT 0,
    FOREIGN KEY(publishing_id) REFERENCES publishing_records(id) ON DELETE CASCADE
);

-- 7. Growth & Intelligence Feedback Memory
CREATE TABLE IF NOT EXISTS growth_insights (
    id TEXT PRIMARY KEY,
    insight_key TEXT NOT NULL,
    category TEXT NOT NULL, -- 'HOOK', 'PACING', 'TOPIC', 'THUMBNAIL', 'HASHTAG'
    finding TEXT NOT NULL,
    confidence_score REAL DEFAULT 0.5,
    recommended_action TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for rapid query performance
CREATE INDEX IF NOT EXISTS idx_scenes_project ON scenes(project_id);
CREATE INDEX IF NOT EXISTS idx_publishing_project ON publishing_records(project_id);
CREATE INDEX IF NOT EXISTS idx_analytics_publishing ON analytics_snapshots(publishing_id);
