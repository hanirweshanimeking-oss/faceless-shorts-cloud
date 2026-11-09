"""
Dragon Studios India - Database Management Module
Handles SQLite schema migrations, CRUD operations, state updates,
and analytics persistence for autonomous video production.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "dragon_studios.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Returns a connection to the SQLite database with row factory enabled."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: str = DB_PATH, schema_path: str = SCHEMA_PATH) -> None:
    """Initializes the database schema if tables do not exist."""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with get_connection(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()

# --- Project Operations ---

def create_project(
    project_id: str,
    title: str,
    pillar: str,
    concept: str,
    aspect_ratio: str = "9:16",
    target_duration: float = 30.0,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """Creates a new video production project."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO projects (id, title, pillar, concept, status, aspect_ratio, target_duration)
            VALUES (?, ?, ?, ?, 'DRAFT', ?, ?)
            """,
            (project_id, title, pillar, concept, aspect_ratio, target_duration)
        )
        conn.commit()
    return get_project(project_id, db_path)

def get_project(project_id: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves a project record by ID."""
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        return dict(row) if row else None

def update_project_status(project_id: str, status: str, db_path: str = DB_PATH) -> None:
    """Updates the lifecycle status of a project."""
    with get_connection(db_path) as conn:
        conn.execute(
            "UPDATE projects SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, project_id)
        )
        conn.commit()

def list_projects(limit: int = 20, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Lists recent projects ordered by creation time."""
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM projects ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

# --- Scene & Storyboard Operations ---

def add_scenes(scenes: List[Dict[str, Any]], db_path: str = DB_PATH) -> None:
    """Bulk inserts scenes for a project."""
    with get_connection(db_path) as conn:
        for s in scenes:
            conn.execute(
                """
                INSERT OR REPLACE INTO scenes (
                    id, project_id, scene_order, duration_seconds, dialogue_text,
                    visual_prompt, camera_movement, video_asset_path, audio_asset_path,
                    subtitle_text, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    s["id"], s["project_id"], s["scene_order"], s["duration_seconds"],
                    s.get("dialogue_text"), s["visual_prompt"], s.get("camera_movement"),
                    s.get("video_asset_path"), s.get("audio_asset_path"),
                    s.get("subtitle_text"), s.get("status", "PENDING")
                )
            )
        conn.commit()

def get_project_scenes(project_id: str, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Gets all scenes for a project ordered by scene_order."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM scenes WHERE project_id = ? ORDER BY scene_order ASC",
            (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

def update_scene_asset(scene_id: str, video_path: Optional[str] = None, audio_path: Optional[str] = None, status: str = "COMPLETED", db_path: str = DB_PATH) -> None:
    """Updates generated video or audio asset paths for a scene."""
    with get_connection(db_path) as conn:
        if video_path and audio_path:
            conn.execute(
                "UPDATE scenes SET video_asset_path = ?, audio_asset_path = ?, status = ? WHERE id = ?",
                (video_path, audio_path, status, scene_id)
            )
        elif video_path:
            conn.execute(
                "UPDATE scenes SET video_asset_path = ?, status = ? WHERE id = ?",
                (video_path, status, scene_id)
            )
        elif audio_path:
            conn.execute(
                "UPDATE scenes SET audio_asset_path = ? WHERE id = ?",
                (audio_path, scene_id)
            )
        conn.commit()

# --- Character Consistency Vault ---

def save_character(
    char_id: str,
    name: str,
    visual_description: str,
    universe: str = "Chitran",
    master_seed: Optional[int] = None,
    reference_image_path: Optional[str] = None,
    negative_prompt: Optional[str] = None,
    db_path: str = DB_PATH
) -> None:
    """Saves or updates a character reference profile."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO characters (
                id, name, universe, visual_description, master_seed, reference_image_path, negative_prompt
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (char_id, name, universe, visual_description, master_seed, reference_image_path, negative_prompt)
        )
        conn.commit()

def get_character(name: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves a character profile by name."""
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM characters WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None

# --- Publishing & Approval Gate Operations ---

def create_publishing_record(
    record_id: str,
    project_id: str,
    platform: str,
    caption: str,
    hashtags: str,
    thumbnail_path: Optional[str] = None,
    scheduled_time: Optional[datetime] = None,
    db_path: str = DB_PATH
) -> None:
    """Creates a draft publishing record waiting for human approval."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO publishing_records (
                id, project_id, platform, status, caption, hashtags, thumbnail_path, scheduled_time
            ) VALUES (?, ?, ?, 'DRAFT', ?, ?, ?, ?)
            """,
            (record_id, project_id, platform, caption, hashtags, thumbnail_path, scheduled_time)
        )
        conn.commit()

def record_approval(record_id: str, approved_by: str = "USER", db_path: str = DB_PATH) -> None:
    """Records formal human approval before executing publication."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE publishing_records
            SET status = 'SCHEDULED', approved_by = ?, approval_timestamp = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (approved_by, record_id)
        )
        conn.commit()

def record_published(record_id: str, platform_media_id: str, post_url: str, db_path: str = DB_PATH) -> None:
    """Marks a post as successfully published with live platform IDs."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE publishing_records
            SET status = 'PUBLISHED', platform_media_id = ?, post_url = ?, published_time = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (platform_media_id, post_url, record_id)
        )
        conn.commit()

def record_publishing_failure(record_id: str, error_message: str, db_path: str = DB_PATH) -> None:
    """Logs a publishing error."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE publishing_records
            SET status = 'FAILED', error_log = ?
            WHERE id = ?
            """,
            (error_message, record_id)
        )
        conn.commit()

# --- Analytics & Intelligence Operations ---

def log_analytics(
    snapshot_id: str,
    publishing_id: str,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    saves: int = 0,
    watch_time_seconds: float = 0.0,
    retention_rate: float = 0.0,
    ctr: float = 0.0,
    db_path: str = DB_PATH
) -> None:
    """Logs a performance metrics snapshot."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO analytics_snapshots (
                id, publishing_id, views, likes, comments, shares, saves,
                watch_time_seconds, retention_rate, click_through_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (snapshot_id, publishing_id, views, likes, comments, shares, saves, watch_time_seconds, retention_rate, ctr)
        )
        conn.commit()

def save_growth_insight(
    insight_id: str,
    insight_key: str,
    category: str,
    finding: str,
    confidence_score: float,
    recommended_action: str,
    db_path: str = DB_PATH
) -> None:
    """Stores strategic findings derived from content analytics."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO growth_insights (
                id, insight_key, category, finding, confidence_score, recommended_action
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (insight_id, insight_key, category, finding, confidence_score, recommended_action)
        )
        conn.commit()
