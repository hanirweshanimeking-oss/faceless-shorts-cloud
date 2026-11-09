"""Pocket Creator Director (Pocket CD) - FastAPI Server.

Full REST API and Static File Server for AI Media Engine.
"""

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# Force utf-8 encoding for Windows console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Ensure pocket-cd directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from engine.compositor import compositor
from engine.director_agent import director_agent
from engine.dna_extractor import dna_extractor
from engine.exporters import exporters
from engine.storyteller import storyteller

DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
RENDERS_DIR = BASE_DIR / "renders"
EXPORTS_DIR = BASE_DIR / "exports"
TEMPLATES_DIR = BASE_DIR / "templates"

SIGNATURES_FILE = DATA_DIR / "signatures.json"
LIBRARY_FILE = DATA_DIR / "library.json"
SCRIPTS_FILE = DATA_DIR / "scripts.json"
BOARDS_FILE = DATA_DIR / "boards.json"

app = FastAPI(
    title="Pocket Creator Director (Pocket CD) API",
    description="Autonomous Media Engine: 11-Ingredient Style DNA, Director Agent, Storyteller & Gyan FFmpeg Compositor",
    version="1.0.0"
)

# Enable CORS for all local development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static and renders directories
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if RENDERS_DIR.exists():
    app.mount("/renders", StaticFiles(directory=str(RENDERS_DIR)), name="renders")


# Helper File I/O
def read_json_file(file_path: Path, default_val: Any = None) -> Any:
    if not file_path.exists():
        return default_val if default_val is not None else []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_val if default_val is not None else []


def write_json_file(file_path: Path, data: Any) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# Pydantic Request Models
class RuleUpdateRequest(BaseModel):
    rules: Dict[str, Any]


class SignatureCreateRequest(BaseModel):
    title: str
    category: Optional[str] = "Commercial"
    description: Optional[str] = ""
    rules: Optional[Dict[str, Any]] = None


class LibraryItemRequest(BaseModel):
    title: str
    category: str
    type: str
    status: Optional[str] = "Done"
    thumbnail: Optional[str] = "/static/assets/frame_0001.jpg"
    badge: Optional[str] = "General"
    starred: Optional[bool] = False
    description: Optional[str] = ""


class ScriptGenerateRequest(BaseModel):
    topic: str
    style: Optional[str] = "carl_voice"
    duration_sec: Optional[int] = 22


class VoiceSynthesizeRequest(BaseModel):
    text: str
    voice: Optional[str] = "carl"
    filename: Optional[str] = None


class CardCreateRequest(BaseModel):
    title: str
    type: str  # 'video', 'image', 'notes'
    url: Optional[str] = None
    content: Optional[str] = None
    x: Optional[int] = 50
    y: Optional[int] = 50
    width: Optional[int] = 300


class DNAExtractRequest(BaseModel):
    video_path: Optional[str] = None
    prompt: Optional[str] = None
    title: Optional[str] = None


class DirectorCommandRequest(BaseModel):
    command: str
    signature_id: Optional[str] = "ackman-edit-dna"
    project_state: Optional[Dict[str, Any]] = None


class RenderRequest(BaseModel):
    signature_id: Optional[str] = "ackman-edit-dna"
    title_text: Optional[str] = "BILL ACKMAN"
    subtitle_text: Optional[str] = "PERSHING SQUARE CAPITAL"
    counter_label: Optional[str] = "AUM"
    target_value: Optional[int] = 18000000000
    source_video: Optional[str] = None
    narration_audio: Optional[str] = None
    duration_sec: Optional[float] = 8.0
    resolution: Optional[str] = "720x1280"
    fps: Optional[int] = 30
    rules: Optional[Dict[str, Any]] = None


# -------------------------------------------------------------
# Root Web Dashboard
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    index_path = TEMPLATES_DIR / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Pocket Creator Director</h1><p>API Running. Index template pending.</p>")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "engine": "Pocket Creator Director",
        "version": "1.0.0",
        "ffmpeg": "Gyan FFmpeg 9.0.2",
        "system": sys.platform
    }


# -------------------------------------------------------------
# Signatures REST API
# -------------------------------------------------------------
@app.get("/api/signatures")
async def list_signatures():
    sigs = read_json_file(SIGNATURES_FILE, [])
    return JSONResponse(content=sigs)


@app.get("/api/signatures/{sig_id}")
async def get_signature(sig_id: str):
    sigs = read_json_file(SIGNATURES_FILE, [])
    item = next((s for s in sigs if s.get("id") == sig_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Signature '{sig_id}' not found")
    return JSONResponse(content=item)


@app.post("/api/signatures")
async def create_signature(req: SignatureCreateRequest):
    new_sig = dna_extractor.extract_from_prompt(
        prompt=req.description or req.title,
        title=req.title
    )
    if req.category:
        new_sig["category"] = req.category
    if req.rules:
        new_sig.setdefault("rules", {}).update(req.rules)
    dna_extractor.save_signature(new_sig)
    return JSONResponse(content=new_sig, status_code=201)


@app.post("/api/signatures/{sig_id}/rules")
async def update_signature_rules(sig_id: str, req: RuleUpdateRequest):
    sigs = read_json_file(SIGNATURES_FILE, [])
    target = next((s for s in sigs if s.get("id") == sig_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Signature '{sig_id}' not found")

    target.setdefault("rules", {}).update(req.rules)
    write_json_file(SIGNATURES_FILE, sigs)
    return JSONResponse(content={"success": True, "signature_id": sig_id, "rules": target["rules"]})


# -------------------------------------------------------------
# Library REST API
# -------------------------------------------------------------
@app.get("/api/library")
async def list_library():
    lib = read_json_file(LIBRARY_FILE, [])
    return JSONResponse(content=lib)


@app.post("/api/library")
async def add_library_item(req: LibraryItemRequest):
    lib = read_json_file(LIBRARY_FILE, [])
    item_id = f"lib_{uuid.uuid4().hex[:6]}"
    item = {
        "id": item_id,
        "title": req.title,
        "category": req.category,
        "type": req.type,
        "status": req.status,
        "thumbnail": req.thumbnail,
        "badge": req.badge,
        "starred": req.starred,
        "description": req.description
    }
    lib.insert(0, item)
    write_json_file(LIBRARY_FILE, lib)
    return JSONResponse(content=item, status_code=201)


# -------------------------------------------------------------
# Scripts & Voice REST API
# -------------------------------------------------------------
@app.get("/api/scripts")
async def list_scripts():
    scripts = storyteller.load_scripts()
    return JSONResponse(content=scripts)


@app.post("/api/scripts/generate")
async def generate_script(req: ScriptGenerateRequest):
    script_obj = storyteller.generate_vsl_script(
        topic=req.topic,
        style=req.style or "carl_voice",
        target_duration_sec=req.duration_sec or 22
    )
    return JSONResponse(content=script_obj, status_code=201)


@app.post("/api/voice/synthesize")
async def synthesize_voice(req: VoiceSynthesizeRequest):
    try:
        res = await storyteller.synthesize_speech_async(
            text=req.text,
            voice_key=req.voice or "carl",
            output_filename=req.filename
        )
        return JSONResponse(content=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------------------
# Boards REST API
# -------------------------------------------------------------
@app.get("/api/boards")
async def list_boards():
    boards = read_json_file(BOARDS_FILE, [])
    return JSONResponse(content=boards)


@app.post("/api/boards/{board_id}/cards")
async def add_board_card(board_id: str, req: CardCreateRequest):
    boards = read_json_file(BOARDS_FILE, [])
    target = next((b for b in boards if b.get("id") == board_id), None)
    if not target:
        # Create board if not found
        target = {"id": board_id, "title": "Production Moodboard", "updated_at": "2026-11-09", "cards": []}
        boards.append(target)

    card_id = f"card_{uuid.uuid4().hex[:6]}"
    card = {
        "id": card_id,
        "title": req.title,
        "type": req.type,
        "url": req.url,
        "content": req.content,
        "x": req.x,
        "y": req.y,
        "width": req.width
    }
    target.setdefault("cards", []).append(card)
    write_json_file(BOARDS_FILE, boards)
    return JSONResponse(content=card, status_code=201)


# -------------------------------------------------------------
# DNA Extractor & Director Agent Endpoints
# -------------------------------------------------------------
@app.post("/api/dna/extract")
async def extract_dna(req: DNAExtractRequest):
    try:
        sig = dna_extractor.decompile(
            video_path=req.video_path,
            prompt=req.prompt,
            title=req.title
        )
        return JSONResponse(content=sig)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/api/director/command")
async def director_command(req: DirectorCommandRequest):
    try:
        res = director_agent.execute_command(
            command=req.command,
            signature_id=req.signature_id,
            project_state=req.project_state
        )
        return JSONResponse(content=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Director command failed: {str(e)}")


# -------------------------------------------------------------
# FFmpeg Compositor Endpoint
# -------------------------------------------------------------
@app.post("/api/render")
async def render_reel(req: RenderRequest):
    try:
        # If rules were not supplied, pull from signature
        rules = req.rules
        if not rules and req.signature_id:
            sigs = read_json_file(SIGNATURES_FILE, [])
            match = next((s for s in sigs if s.get("id") == req.signature_id), None)
            if match:
                rules = match.get("rules", {})

        result = compositor.render_vertical_reel(
            signature_id=req.signature_id,
            title_text=req.title_text or "BILL ACKMAN",
            subtitle_text=req.subtitle_text or "PERSHING SQUARE CAPITAL",
            counter_label=req.counter_label or "AUM",
            target_value=req.target_value or 18000000000,
            source_video=req.source_video,
            narration_audio=req.narration_audio,
            duration_sec=req.duration_sec or 8.0,
            resolution=req.resolution or "720x1280",
            fps=req.fps or 30,
            rules=rules
        )
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Render failed"))
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------------------
# Multi-Engine Exporters Endpoint
# -------------------------------------------------------------
@app.get("/api/export/{fmt}/{signature_id}")
async def export_script(fmt: str, signature_id: str):
    sigs = read_json_file(SIGNATURES_FILE, [])
    target = next((s for s in sigs if s.get("id") == signature_id), None)
    if not target:
        if sigs:
            target = sigs[0]
        else:
            raise HTTPException(status_code=404, detail="No signatures found")

    fmt_lower = fmt.lower()
    if fmt_lower in ["jsx", "ae", "aftereffects", "after-effects"]:
        file_path = exporters.generate_after_effects_jsx(target)
        media_type = "application/javascript"
        filename = f"{target.get('id')}_after_effects.jsx"
    elif fmt_lower in ["py", "resolve", "davinci", "davinci-resolve"]:
        file_path = exporters.generate_davinci_resolve_py(target)
        media_type = "text/x-python"
        filename = f"{target.get('id')}_davinci_resolve.py"
    elif fmt_lower in ["lua", "reaper", "reaper-lua"]:
        file_path = exporters.generate_reaper_lua(target)
        media_type = "text/x-lua"
        filename = f"{target.get('id')}_reaper.lua"
    elif fmt_lower in ["json", "dna", "manifest"]:
        file_path = exporters.generate_style_dna_manifest_json(target)
        media_type = "application/json"
        filename = f"{target.get('id')}_manifest.json"
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported export format '{fmt}'. Use jsx, py, lua, or json.")

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
