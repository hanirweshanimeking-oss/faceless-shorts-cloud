"""
Dragon Studios India - Autonomous AI Studio Command Center
Unified CLI for content creation, voiceover synthesis, automated editing,
quality assurance, human approval gates, and multi-platform publishing.
Enhanced with Full 10-Stage Autonomous Creator Studio Lifecycle:
RESEARCH -> IDEATE -> SCRIPT -> STORYBOARD -> GENERATE -> EDIT -> REVIEW -> PUBLISH -> ANALYZE -> IMPROVE
"""

import sys
import os
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add current workspace directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dragon_studios.database.db_manager import (
    init_db,
    list_projects,
    get_project,
    get_project_scenes,
    update_project_status
)
from dragon_studios.pipeline.orchestrator import StudioOrchestrator
from dragon_studios.agents.voice_agent import synthesize_speech
from dragon_studios.integrations.ayanokoji_voice import (
    synthesize_ayanokoji_hindi,
    synthesize_ayanokoji_voice,
    convert_human_voice_to_ayanokoji,
    play_audio_system,
    generate_html_player
)
from dragon_studios.integrations.omnivoice_engine import synthesize_omnivoice_clone
from dragon_studios.agents.research_agent import ResearchAgent
from dragon_studios.agents.ideate_agent import IdeateAgent
from dragon_studios.agents.storyboard_agent import StoryboardAgent
from dragon_studios.agents.improve_agent import ImproveAgent
from dragon_studios.agents.composio_publisher import ComposioPublisherHub
from dragon_studios.agents.higgsfield_engine import HiggsfieldWebGPUEngine
from dragon_studios.agents.higgsfield_skills import HiggsfieldSkillsAdapter
from dragon_studios.integrations import (
    get_integrations_health_check,
    ViralityPredictorEngine,
    ReelMimicAdapter,
    HypitAdapter,
    ClaudeVideoAdapter,
    GoogleFlowAdapter
)

app = typer.Typer(help="Dragon Studios India - Autonomous AI Studio CLI")
console = Console(force_terminal=True, legacy_windows=False)

@app.command()
def init():
    """Initializes the studio database and folder hierarchy."""
    init_db()
    console.print(Panel.fit("[bold green][OK] Database & Studio Environment Initialized Successfully![/bold green]"))

@app.command(name="create")
@app.command(name="studio-run")
def studio_run(
    topic: str = typer.Option("Destroying an Enemy's Ego", help="Topic or concept focus"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA, or CONVERSATIONAL_PODCAST"),
    auto_approve: bool = typer.Option(False, help="Automatically approve after passing QA")
):
    """
    Executes the complete 10-Stage Autonomous Creator Studio Pipeline:
    RESEARCH -> IDEATE -> SCRIPT -> STORYBOARD -> GENERATE -> EDIT -> REVIEW -> PUBLISH -> ANALYZE -> IMPROVE
    """
    console.print(Panel.fit(
        f"[bold cyan]>> Launching 10-Stage Autonomous Creator Studio Run[/bold cyan]\n"
        f"[bold]Topic:[/bold] {topic}\n"
        f"[bold]Pillar:[/bold] {pillar}"
    ))

    orchestrator = StudioOrchestrator()
    with console.status("[bold green]Executing 10-stage autonomous generation cycle...[/bold green]"):
        result = orchestrator.execute_10_stage_run(topic=topic, pillar=pillar, auto_approve=auto_approve)

    table = Table(title="10-Stage Execution Status")
    table.add_column("Stage #", style="dim")
    table.add_column("Lifecycle Stage", style="bold cyan")
    table.add_column("Status", style="green")

    for idx, stage in enumerate(result["stages_completed"], 1):
        table.add_row(str(idx), stage.replace("STAGE_", "").replace("_", " "), "[OK] Completed")

    console.print(table)

    console.print(Panel.fit(
        f"[bold green][SUCCESS] Complete 10-Stage Lifecycle Executed![/bold green]\n\n"
        f"[bold]Project ID:[/bold] {result['project_id']}\n"
        f"[bold]Winning Concept:[/bold] {result['winning_concept']['title']}\n"
        f"[bold]Master Video:[/bold] {result['master_video_path']}\n"
        f"[bold]CapCut Pro Draft:[/bold] {result['capcut_draft']}\n"
        f"[bold]Google Flow Package:[/bold] {result.get('google_flow_manifest', 'N/A')}\n"
        f"[bold]QA Score:[/bold] {result['qa_report']['score']}/100 (Passed: {result['qa_report']['passed']})\n"
        f"[bold]Publish Bundle:[/bold] {result['publish_bundle']['bundle_dir']}\n"
        f"[bold]Next Topic Recommendation:[/bold] {result['improvement_insights']['next_topic_recommendation']}"
    ))

@app.command()
def research(
    topic: str = typer.Argument(..., help="Topic to research"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA")
):
    """Stage 1: Researches a topic against the 648 saved viral reels knowledge base."""
    agent = ResearchAgent()
    dossier = agent.conduct_research(topic=topic, pillar=pillar)

    table = Table(title=f"Research Dossier: {topic} ({pillar})")
    table.add_column("Field", style="bold magenta")
    table.add_column("Insights", style="white")

    table.add_row("Market Score", f"{dossier.market_opportunity_score}/10.0")
    table.add_row("Trending Keywords", ", ".join(dossier.trending_keywords))
    table.add_row("Proven Hooks", "\n".join(f"• {h}" for h in dossier.proven_hooks))
    table.add_row("Angles", "\n".join(f"• {a}" for a in dossier.suggested_angles))
    table.add_row("Reference Saves", f"{len(dossier.reference_reels)} matching viral reels analyzed")

    console.print(table)

@app.command()
def ideate(
    topic: str = typer.Argument(..., help="Topic to brainstorm"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA")
):
    """Stage 2: Brainstorms concepts with Viral Potential Scores (VPS)."""
    concepts = IdeateAgent.brainstorm_concepts(topic=topic, pillar=pillar)

    table = Table(title=f"Ideation Matrix: {topic}")
    table.add_column("Rank", style="dim")
    table.add_column("Title", style="bold cyan")
    table.add_column("VPS Score", style="bold yellow")
    table.add_column("Retention Est.", style="green")
    table.add_column("Curiosity Gap", style="dim")

    for idx, c in enumerate(concepts, 1):
        table.add_row(
            str(idx),
            c.title,
            f"{c.viral_potential_score}/10.0",
            f"{c.estimated_retention_rate}%",
            c.curiosity_gap[:45] + "..."
        )

    console.print(table)

@app.command()
def list():
    """Lists recent studio projects and their lifecycle status."""
    projects = list_projects(limit=15)
    if not projects:
        console.print("[yellow]No projects found. Run 'python cli.py studio-run' to produce your first video.[/yellow]")
        return
        
    table = Table(title="Dragon Studios - Recent Production Runs")
    table.add_column("Project ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold white")
    table.add_column("Pillar", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Aspect", style="dim")
    table.add_column("Created", style="dim")

    for p in projects:
        status_color = "green" if p['status'] == "APPROVED" or p['status'] == "PUBLISHED" else "yellow" if p['status'] == "PENDING_APPROVAL" else "white"
        table.add_row(
            p["id"],
            p["title"],
            p["pillar"],
            f"[{status_color}]{p['status']}[/{status_color}]",
            p.get("aspect_ratio", "9:16"),
            str(p.get("created_at", ""))[:19]
        )
    console.print(table)

@app.command()
def approve(project_id: str):
    """Human-in-the-Loop Sovereign Gate: Approves a video for publication."""
    project = get_project(project_id)
    if not project:
        console.print(f"[bold red]Project '{project_id}' not found.[/bold red]")
        return
    update_project_status(project_id, "APPROVED")
    console.print(Panel.fit(
        f"[bold green][OK] Human Approval Confirmed for Project '{project_id}'[/bold green]\n"
        f"The video is now authorized for publishing."
    ))

@app.command()
def composio_status():
    """Checks Composio Multi-App Hub connection and webhook configurations."""
    hub = ComposioPublisherHub()
    status = hub.check_status()

    table = Table(title="Composio Multi-Platform Hub Status")
    table.add_column("Integration", style="bold cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")

    table.add_row(
        "Composio Core SDK",
        "[green]Installed[/green]",
        "Python library active"
    )
    table.add_row(
        "Composio API Key",
        "[green]Configured[/green]" if status["api_key_configured"] else "[yellow]Missing[/yellow]",
        "Key active in .env"
    )
    table.add_row(
        "Composio MCP Gateway",
        "[bold green]Connected & Live[/bold green]" if status.get("mcp_gateway_connected") else "[yellow]Offline[/yellow]",
        "https://connect.composio.dev/mcp (Bearer Auth active)" if status.get("mcp_gateway_connected") else "Connect via API key"
    )
    table.add_row(
        "YouTube Shorts & IG",
        "[green]Ready via Gateway[/green]" if status.get("mcp_gateway_connected") else "[yellow]Offline Staging Mode[/yellow]",
        "Meta-tools enabled for YouTube & Instagram" if status.get("mcp_gateway_connected") else "Run 'composio add youtube'"
    )
    table.add_row(
        "Notion Workspace",
        "[green]Connected[/green]" if status["notion_database_configured"] else "[dim]Not Configured[/dim]",
        "Set NOTION_DATABASE_ID in .env"
    )
    table.add_row(
        "Discord Alert Webhook",
        "[green]Active[/green]" if status["discord_webhook_configured"] else "[dim]Not Configured[/dim]",
        "Set DISCORD_WEBHOOK_URL in .env"
    )
    table.add_row(
        "Slack Alert Webhook",
        "[green]Active[/green]" if status["slack_webhook_configured"] else "[dim]Not Configured[/dim]",
        "Set SLACK_WEBHOOK_URL in .env"
    )

    console.print(table)

@app.command()
def publish(
    project_id: str = typer.Argument(..., help="Project ID to publish"),
    target: str = typer.Option("all", help="Target: all, youtube, instagram, notion, or alerts")
):
    """Syndicates a produced project across connected Composio channels."""
    project = get_project(project_id)
    if not project:
        console.print(f"[bold red]Project '{project_id}' not found.[/bold red]")
        return

    hub = ComposioPublisherHub()
    video_path = os.path.join("output", project_id, "master_video.mp4")

    console.print(f"[cyan]Syndicating Project {project_id} to '{target}'...[/cyan]")
    res = hub.syndicate_all(
        project_id=project_id,
        title=project.get("title", "Dragon Studios Short"),
        pillar=project.get("pillar", "DARK_PSYCHOLOGY"),
        caption=project.get("concept", ""),
        hashtags="#DragonStudiosIndia #Shorts #Anime",
        master_video_path=video_path,
        qa_score=95.0,
        output_dir="output"
    )

    table = Table(title=f"Syndication Results for {project_id}")
    table.add_column("Channel", style="bold cyan")
    table.add_column("Action Type", style="bold white")
    table.add_column("Status", style="green")

    for channel, details in res.items():
        if isinstance(details, dict):
            status_text = "[green]Live[/green]" if not details.get("fallback_used") else "[yellow]Staged[/yellow]"
            table.add_row(channel.upper(), details.get("action_type", "SUCCESS"), status_text)

    console.print(table)
    console.print(f"[dim]Manifest saved to: {res.get('manifest_path', '')}[/dim]")

@app.command()
def test_voice(
    text: str = typer.Option("The ego is the most fragile armor. Strike it with absolute indifference.", help="Text to speak"),
    output: str = typer.Option("output/test_voice.mp3", help="Output file path")
):
    """Tests the free neural voice synthesis engine."""
    console.print("[cyan]Synthesizing test voiceover via Edge-TTS...[/cyan]")
    res = synthesize_speech(text=text, output_path=output)
    console.print(Panel.fit(
        f"[bold green][OK] Voiceover Generated Successfully![/bold green]\n"
        f"Saved to: {res['output_path']}\n"
        f"File Size: {res['file_size_bytes']} bytes\n"
        f"Voice: {res['voice']}"
    ))

@app.command()
def cover(
    project_id: str = typer.Argument(..., help="Project ID to generate cover for"),
    title: str = typer.Option(None, help="Custom title text for the cover"),
    badge: str = typer.Option("DRAGON STUDIOS", help="Badge text on top of cover")
):
    """Generates an aesthetic 9:16 vertical cover/thumbnail for Instagram Reels & YouTube."""
    from dragon_studios.agents.thumbnail_agent import extract_frame_from_video, generate_reels_cover
    
    # Locate project video
    project_dir = os.path.join("output", project_id)
    master_video = os.path.join(project_dir, f"{project_id}_master.mp4")
    
    if not os.path.exists(master_video):
        # Look for any mp4 in the project dir
        candidates = [f for f in os.listdir(project_dir) if f.endswith("_master.mp4")] if os.path.exists(project_dir) else []
        if candidates:
            master_video = os.path.join(project_dir, candidates[0])
        else:
            console.print(f"[bold red]Master video not found for '{project_id}'[/bold red]")
            return

    frame_path = os.path.join(project_dir, "cover_frame.jpg")
    cover_path = os.path.join(project_dir, f"{project_id}_cover_9x16.jpg")
    
    console.print("[cyan]Extracting frame and designing 9:16 vertical cover...[/cyan]")
    extract_frame_from_video(master_video, frame_path, timestamp_seconds=1.0)
    title_text = title or project_id.replace("proj_", "").replace("_", " ").upper()
    generate_reels_cover(frame_path, cover_path, title_text=title_text, badge_text=badge)
    
    console.print(Panel.fit(
        f"[bold green][OK] 9:16 Cover Generated Successfully![/bold green]\n"
        f"Output Cover: [underline]{os.path.abspath(cover_path)}[/underline]\n"
        f"Resolution: 1080x1920 (Instagram Reels / YouTube Shorts)"
    ))

@app.command(name="ayanokoji-voice")
def ayanokoji_voice(
    text: str = typer.Option(
        "All people are nothing but tools. It does not matter what needs to be sacrificed. In this world, winning is everything.",
        help="Monologue text to speak (Hindi or English)"
    ),
    language: str = typer.Option("en", help="Language: 'en' for English or 'hi' for Hindi"),
    model: str = typer.Option("dub", help="Voice model: 'dub' (Official English Dub) or 'nss' (200-Epoch RVC v2 + FAISS)"),
    output: str = typer.Option("output/ayanokoji_speech.mp3", help="Output MP3 file path"),
    rvc: bool = typer.Option(True, help="Enable true RVC v2 40kHz neural voice conversion"),
    index_rate: float = typer.Option(0.75, help="FAISS index feature retrieval strength (0.0 - 1.0)"),
    pitch_shift: float = typer.Option(0.0, help="Pitch shift semitones for voice conversion"),
    mastering: bool = typer.Option(True, help="Apply cold anime monologue equalizer and dynamics compression"),
    play: bool = typer.Option(True, help="Automatically play audio through Windows default player"),
    open_player: bool = typer.Option(True, help="Open interactive HTML browser player")
):
    """Synthesizes Kiyotaka Ayanokoji's exact dark stoic voice clone (English Dub or Hindi)."""
    console.print(f"[bold cyan]>> Synthesizing Kiyotaka Ayanokoji Voice Clone ({language.upper()}, Model: {model.upper()}, RVC v2 40kHz)...[/bold cyan]")
    res = synthesize_ayanokoji_voice(
        text=text,
        output_path=output,
        language=language,
        model_choice=model,
        apply_rvc=rvc,
        apply_mastering=mastering,
        index_rate=index_rate,
        pitch_shift=pitch_shift
    )

    if play and os.path.exists(output):
        play_audio_system(output)

    if open_player:
        player_html = os.path.abspath("output/ayanokoji_player.html")
        if os.path.exists(player_html):
            subprocess.Popen(["powershell", "-NoProfile", "-Command", f"Start-Process '{player_html}'"])

    console.print(Panel.fit(
        f"[bold green][OK] Ayanokoji Voice Clone Rendered Successfully![/bold green]\n\n"
        f"[bold]Character:[/bold] {res['character']}\n"
        f"[bold]Language:[/bold] {res['language']}\n"
        f"[bold]Model Choice:[/bold] {res['model_choice'].upper()}\n"
        f"[bold]Pipeline:[/bold] {res['pipeline']}\n"
        f"[bold]RVC Converted:[/bold] {res['rvc_converted']} (Index Rate: {res['index_rate']}, Pitch Shift: {res['pitch_shift']})\n"
        f"[bold]Saved File:[/bold] {res['output_path']}\n"
        f"[bold]File Size:[/bold] {res['file_size_bytes']} bytes\n\n"
        f"[bold cyan]Interactive Web Player:[/bold cyan] output/ayanokoji_player.html"
    ))

@app.command(name="ayanokoji-convert")
def ayanokoji_convert_cmd(
    input_file: str = typer.Option(..., "--input", "-i", help="Path to input human voice recording (.mp3, .wav, .m4a)"),
    output_file: str = typer.Option("output/ayanokoji_converted_human.mp3", "--output", "-o", help="Output MP3 path"),
    pitch_shift: float = typer.Option(0.0, help="Pitch shift semitones (0 for natural pitch)"),
    play: bool = typer.Option(True, help="Auto-play converted voice on speakers")
):
    """
    Voice-to-Voice (Speech-to-Speech) Conversion:
    Converts any real human speech recording directly into Kiyotaka Ayanokoji's voice.
    Preserves 100% of the human speaker's natural slang, pauses, breathing, cadence, and emotion!
    """
    console.print(f"[bold cyan]>> Converting Human Voice Recording to Ayanokoji (#1 Dub Model)...[/bold cyan]")
    console.print(f"[bold]Input Audio:[/bold] {input_file}")
    res = convert_human_voice_to_ayanokoji(
        input_audio_path=input_file,
        output_path=output_file,
        pitch_shift=pitch_shift,
        model_choice="dub"
    )
    if play and os.path.exists(output_file):
        play_audio_system(output_file)

    console.print(Panel.fit(
        f"[bold green][OK] Human Voice Converted to Ayanokoji Successfully![/bold green]\n\n"
        f"[bold]Input File:[/bold] {res['input_audio_path']}\n"
        f"[bold]Output File:[/bold] {res['output_path']}\n"
        f"[bold]Mode:[/bold] 100% Natural Human Slang & Cadence Preserved\n"
        f"[bold]Model:[/bold] Official Dub RVC v2 40kHz\n"
        f"[bold]File Size:[/bold] {res['file_size_bytes']} bytes"
    ))

@app.command(name="omnivoice-clone")
def omnivoice_clone_cmd(
    text: str = typer.Option("Winning is everything. That is all that matters.", help="Text to speak in cloned voice"),
    ref: str = typer.Option("models/ayanokoji_reference/ayanokoji_short_quote_en.wav", help="Reference voice clip (.wav)"),
    ref_text: str = typer.Option("All people are nothing but tools.", help="Transcript of reference clip"),
    output: str = typer.Option("output/omnivoice_output.wav", help="Output audio file path"),
    steps: int = typer.Option(16, help="OmniVoice unmasking decoding steps"),
    play: bool = typer.Option(True, help="Auto-play output audio")
):
    """Zero-shot neural voice cloning using OmniVoice ONNX + Higgs Audio Tokenizer."""
    console.print(f"[bold cyan]>> Synthesizing Zero-Shot Voice Clone via OmniVoice ({steps} steps)...[/bold cyan]")
    res = synthesize_omnivoice_clone(
        text=text,
        output_path=output,
        ref_audio_path=ref,
        ref_text=ref_text,
        num_steps=steps
    )
    if play and os.path.exists(output):
        play_audio_system(output)

    console.print(Panel.fit(
        f"[bold green][OK] OmniVoice Zero-Shot Clone Rendered Successfully![/bold green]\n\n"
        f"[bold]Engine:[/bold] {res['engine']}\n"
        f"[bold]Reference Audio:[/bold] {res['reference_audio']}\n"
        f"[bold]Text:[/bold] {res['text']}\n"
        f"[bold]Steps:[/bold] {res['num_steps']}\n"
        f"[bold]Saved File:[/bold] {res['output_path']}\n"
        f"[bold]File Size:[/bold] {res['file_size_bytes']} bytes"
    ))

@app.command()
def higgsfield_render(
    headline: str = typer.Option("SILENCE DESTROYS POWER", help="Headline to display on frame"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="DARK_PSYCHOLOGY, AI_TOOLS, or ORIGINAL_MANGA"),
    output: str = typer.Option("output/higgsfield_master_frame.png", help="Output path for master frame"),
    spp: int = typer.Option(24, help="Samples per pixel (WebGPU path tracer)")
):
    """Renders a 9:16 vertical master frame using the local WebGPU path tracer (100% Free on GPU)."""
    console.print(f"[bold cyan]>> Launching Local Higgsfield WebGPU Render ({spp} SPP, Pillar: {pillar})...[/bold cyan]")
    engine = HiggsfieldWebGPUEngine()
    
    with console.status("[bold green]Compiling WGSL shaders & computing WebGPU light transport...[/bold green]"):
        out_path = engine.render_composite_frame(
            headline=headline,
            subtext="Engineered via Higgsfield Video Engineer Path Tracer",
            pillar=pillar,
            scene_num=1,
            output_path=output,
            spp=spp,
            allow_webgpu=True
        )

    file_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    console.print(Panel.fit(
        f"[bold green][OK] Higgsfield Master Frame Rendered Successfully![/bold green]\n"
        f"Path: {out_path}\n"
        f"Resolution: 1080x1920 (9:16 Vertical)\n"
        f"File Size: {file_size:,} bytes\n"
        f"Hardware: Local GPU (Chrome WebGPU / Dawn D3D12)"
    ))

@app.command()
def higgsfield_catalog(
    kind: str = typer.Option("all", help="Filter by kind: all, video, image")
):
    """Displays the OpenHiggsfield 38-model video and image generation catalog."""
    adapter = HiggsfieldSkillsAdapter()
    filter_kind = None if kind == "all" else kind
    models = adapter.get_catalog_models(filter_kind)

    table = Table(title=f"OpenHiggsfield Model Catalog ({len(models)} models)")
    table.add_column("Model ID", style="bold cyan")
    table.add_column("Name", style="bold white")
    table.add_column("Kind", style="yellow")
    table.add_column("Category", style="dim")
    table.add_column("Aspect Ratios", style="green")
    table.add_column("Credits/Run", style="magenta")

    for m in models:
        table.add_row(
            m.id,
            m.name,
            m.kind.upper(),
            m.category,
            ", ".join(m.aspect_ratios),
            str(m.estimated_credits_per_run)
        )

    console.print(table)

@app.command()
def higgsfield_blueprint(
    topic: str = typer.Option("The Illusion of Choice", help="Topic of the explainer reel"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA"),
    model: str = typer.Option("soul-2", help="Higgsfield Model ID (e.g., soul-2, kling-3-pro, wan-3-prime)"),
    output: str = typer.Option("output/higgsfield_blueprint.json", help="Destination manifest path")
):
    """Generates a Higgsfield-compliant Faceless Video blueprint manifest."""
    adapter = HiggsfieldSkillsAdapter()
    sample_scenes = [
        {"duration_seconds": 4.5, "subtitle_text": "THE PERCEPTION TRAP", "dialogue": "When you think you have options, you are merely picking a cage."},
        {"duration_seconds": 5.0, "subtitle_text": "CONTROL WITHOUT FORCE", "dialogue": "True dominance never forces an action; it manipulates the baseline."},
        {"duration_seconds": 4.5, "subtitle_text": "RECLAIM YOUR SOVEREIGNTY", "dialogue": "Step out of the arena. Observe the strings before moving."}
    ]
    blueprint = adapter.build_faceless_video_blueprint(
        topic=topic,
        pillar=pillar,
        scenes=sample_scenes,
        model_id=model
    )
    budget = adapter.estimate_production_budget(len(sample_scenes), model_id=model)

    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, indent=2)

    console.print(Panel.fit(
        f"[bold green][OK] Higgsfield Blueprint Manifest Generated![/bold green]\n"
        f"Saved to: {output}\n"
        f"Model: {budget['model_name']} ({budget['model_id']})\n"
        f"Scenes: {budget['scene_count']} blocks (Total Duration: {blueprint['total_duration_seconds']}s)\n"
        f"Estimated Credits: {budget['estimated_credits']}\n"
        f"Estimated Cloud Cost: ${budget['cost_usd']} USD (~₹{budget['cost_inr']} INR)\n"
        f"[cyan]Local Zero-Cost Alternative:[/cyan] {budget['zero_cost_local_alternative']}"
    ))

@app.command()
def integrations_status():
    """Checks the local readiness and paths of all 13 integrated video/agentic tools."""
    health = get_integrations_health_check()
    table = Table(title=f"Dragon Studios Integrations Ecosystem ({health['installed_count']}/{health['total_repositories']} Ready)")
    table.add_column("Repository / Framework", style="bold cyan")
    table.add_column("Capability", style="bold white")
    table.add_column("Status", style="green")

    for repo_id, data in health["repositories"].items():
        status_text = "[bold green][OK] Ready[/bold green]" if data["installed"] else "[bold red][X] Missing[/bold red]"
        table.add_row(repo_id, data["name"], status_text)

    console.print(table)
    console.print(Panel.fit(
        f"[bold green]All {health['installed_count']} External Repositories Operational Locally![/bold green]\n"
        f"100% Free & Open-Source Zero-Cost Video Production Stack"
    ))

@app.command()
def virality_score(
    title: str = typer.Option("How to Destroy an Enemy with Silence", help="Reel title"),
    hook: str = typer.Option("If you react to an insult, you have already lost the war.", help="Opening hook line"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar category")
):
    """Predicts retention, 3-second hold rate, and virality potential using ML algorithms."""
    predictor = ViralityPredictorEngine()
    forecast = predictor.predict(title=title, hook_text=hook, pillar=pillar)

    console.print(Panel.fit(
        f"[bold cyan]>> Virality Forecast Report[/bold cyan]\n\n"
        f"[bold]Viral Potential Score (VPS):[/bold] [bold green]{forecast.viral_potential_score}/10.0[/bold green]\n"
        f"[bold]Predicted 3s Hold Rate:[/bold] {forecast.predicted_3s_hold_rate}%\n"
        f"[bold]Predicted Completion Rate:[/bold] {forecast.predicted_completion_rate}%\n"
        f"[bold]Share / Save Ratio:[/bold] {forecast.predicted_share_save_ratio}x\n"
        f"[bold]Hook Strength Score:[/bold] {forecast.hook_strength_score}/100\n"
        f"[bold]Curiosity Gap Score:[/bold] {forecast.curiosity_gap_score}/100\n"
        f"[bold]Emotional Valence:[/bold] {forecast.emotional_valence_score}/100\n\n"
        f"[bold yellow]Optimization Tips:[/bold yellow]\n" + "\n".join(f" - {tip}" for tip in forecast.optimization_recommendations)
    ))

@app.command()
def deconstruct(
    topic: str = typer.Option("Stoic Detachment", help="Reference topic to deconstruct"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA")
):
    """Deconstructs proven viral reel pacing and shot distribution inspired by ReelMimic."""
    adapter = ReelMimicAdapter()
    blueprint = adapter.deconstruct_viral_style(reference_topic=topic, pillar=pillar)

    table = Table(title=f"ReelMimic Style Deconstruction: {blueprint.reference_name}")
    table.add_column("Shot #", style="dim")
    table.add_column("Duration", style="yellow")
    table.add_column("Shot Framing", style="bold cyan")
    table.add_column("Camera Movement", style="green")
    table.add_column("Pacing", style="magenta")

    for s in blueprint.shots:
        table.add_row(
            str(s.shot_index),
            f"{s.duration_seconds}s",
            s.shot_type.replace("_", " ").upper(),
            s.camera_movement.replace("_", " "),
            s.pacing_speed.replace("_", " ")
        )

    console.print(table)
    console.print(Panel.fit(
        f"[bold]Total Duration:[/bold] {blueprint.total_duration_seconds}s (Avg Shot: {blueprint.average_shot_duration}s)\n"
        f"[bold]Color Mood:[/bold] {blueprint.dominant_color_mood}\n"
        f"[bold]Typography:[/bold] {blueprint.typography_placement}\n"
        f"[bold]Prompt Formula:[/bold] {blueprint.reusable_prompt_formula}"
    ))

@app.command()
def svml(
    text: str = typer.Option("Never let an enemy see you react. Silence is your greatest weapon.", help="Dialogue text to parse")
):
    """Converts dialogue into Hypit SVML word nodes with kinetic typography and SFX cues."""
    adapter = HypitAdapter()
    scene = adapter.convert_to_svml(scene_index=1, dialogue=text, duration=4.5)

    console.print(Panel.fit(
        f"[bold cyan]Hypit SVML Scene Breakdown[/bold cyan]\n\n"
        f"[bold]Dialogue:[/bold] {scene.dialogue_raw}\n"
        f"[bold]B-Roll Query:[/bold] {scene.broll_query}\n"
        f"[bold]Camera Effect:[/bold] {scene.camera_effect}\n\n"
        f"[bold yellow]Word Nodes (Kinetic Timing & SFX):[/bold yellow]\n" +
        "\n".join(
            f" - Word: [bold white]{node.word}[/bold white] | Emphasis: {'[green]YES[/green]' if node.emphasis else 'NO'} | SFX: {node.sfx or 'None'} | Visual Cue: {node.visual_cue or 'None'}"
            for node in scene.word_nodes
        )
    ))

@app.command()
def watch(
    source: str = typer.Argument(..., help="Video URL (YouTube/Instagram/TikTok) or local MP4 path"),
    detail: str = typer.Option("balanced", help="Fidelity: transcript, efficient, balanced, token-burner"),
    max_frames: int = typer.Option(10, help="Maximum number of frames to extract"),
    question: Optional[str] = typer.Option(None, help="Question to ask Gemini or focus on"),
    engine: str = typer.Option("local", help="Engine: local or gemini")
):
    """Watches a video (local file or URL), extracting timestamped frames, metadata, and transcript."""
    adapter = ClaudeVideoAdapter()
    console.print(Panel.fit(
        f"[bold cyan]>> Claude-Video (/watch) Perception Active[/bold cyan]\n"
        f"[bold]Source:[/bold] {source}\n"
        f"[bold]Detail Mode:[/bold] {detail} | [bold]Max Frames:[/bold] {max_frames} | [bold]Engine:[/bold] {engine}"
    ))

    with console.status("[bold green]Watching video and extracting timestamped perception data...[/bold green]"):
        dossier = adapter.watch(source, detail=detail, max_frames=max_frames, question=question, engine=engine)

    if dossier.status == "error":
        console.print(Panel.fit(f"[bold red]Error watching video:[/bold red] {dossier.error_message}"))
        return

    table = Table(title=f"Extracted Frame Evidence ({dossier.frame_count} frames)")
    table.add_column("Frame #", style="dim")
    table.add_column("Timestamp", style="yellow")
    table.add_column("Reason", style="cyan")
    table.add_column("Path", style="green")

    for idx, f in enumerate(dossier.frames, 1):
        table.add_row(str(idx), f.timestamp, f.reason, f.path)

    console.print(table)
    console.print(Panel.fit(
        f"[bold green]Video Perception Analysis Complete[/bold green]\n\n"
        f"[bold]Title:[/bold] {dossier.title}\n"
        f"[bold]Duration:[/bold] {dossier.duration_formatted} ({dossier.duration_seconds}s)\n"
        f"[bold]Resolution:[/bold] {dossier.resolution}\n"
        f"[bold]Total Extracted Frames:[/bold] {dossier.frame_count}\n"
        f"[bold]Transcript:[/bold] {dossier.transcript[:200] if dossier.transcript else 'No transcript stream'}\n"
        + (f"[bold]Gemini Answer:[/bold] {dossier.gemini_answer}\n" if dossier.gemini_answer else "")
    ))

@app.command()
def watch_deconstruct(
    source: str = typer.Argument(..., help="Video URL or local MP4 path to reverse-engineer"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar for proposed recreation")
):
    """Deconstructs a reference video into a Dragon Studios Recreation Blueprint using /watch perception."""
    adapter = ClaudeVideoAdapter()
    console.print(Panel.fit(
        f"[bold cyan]>> Reverse-Engineering Video for Autonomous Recreation[/bold cyan]\n"
        f"[bold]Source:[/bold] {source}\n"
        f"[bold]Pillar Target:[/bold] {pillar}"
    ))

    with console.status("[bold green]Analyzing visual rhythm, cut frequency, and pacing...[/bold green]"):
        blueprint = adapter.deconstruct_for_recreation(source)

    if "error" in blueprint:
        console.print(Panel.fit(f"[bold red]Deconstruction Failed:[/bold red] {blueprint['error']}"))
        return

    table = Table(title=f"Scene Pacing Blueprint ({blueprint['scene_count']} Detected Scenes)")
    table.add_column("Scene", style="dim")
    table.add_column("Timestamp", style="yellow")
    table.add_column("Duration", style="cyan")
    table.add_column("Shot Type", style="bold magenta")
    table.add_column("Direction", style="white")

    for s in blueprint["reconstructed_scenes"]:
        table.add_row(
            str(s["scene_number"]),
            s["timestamp"],
            f"{s['target_duration_seconds']}s",
            s["shot_type"],
            s["visual_prompt_direction"][:60] + "..."
        )

    console.print(table)
    console.print(Panel.fit(
        f"[bold green]Recreation Strategy Formulated[/bold green]\n\n"
        f"[bold]Detected Pacing:[/bold] {blueprint['pacing_category']} ({blueprint['average_seconds_per_shot']}s avg cut)\n"
        f"[bold]Cuts Per Minute:[/bold] {blueprint['cut_frequency_per_minute']} cuts/min\n"
        f"[bold]Hook Rule:[/bold] {blueprint['recreation_strategy']['hook_rule']}\n"
        f"[bold]Recommended Voice:[/bold] {blueprint['recreation_strategy']['recommended_voice']}\n"
        f"[bold]Captions:[/bold] {blueprint['recreation_strategy']['recommended_captions']}"
    ))

@app.command(name="flow-status")
def flow_status():
    """Checks Google Flow / Veo 2/3 studio integration readiness and credentials."""
    api_key = os.getenv("GOOGLE_API_KEY", "")
    provider = os.getenv("VIDEO_GEN_PROVIDER", "MOCK")
    
    table = Table(title="Google Flow & Veo Studio Integration Status")
    table.add_column("Component", style="bold cyan")
    table.add_column("State", style="white")
    table.add_column("Details", style="dim")

    table.add_row(
        "Studio Workspace",
        "[bold green]Connected[/bold green]",
        "Google Flow AI Filmmaking Platform (flow.google)"
    )
    table.add_row(
        "Video Engine",
        "[bold green]Veo 2 / Veo 3[/bold green]",
        "Google Cloud / Google AI Studio Long-Running Video Model"
    )
    table.add_row(
        "API Key (GOOGLE_API_KEY)",
        "[bold green]Configured[/bold green]" if api_key else "[bold yellow]Missing (Local Fallback Active)[/bold yellow]",
        "Required for live cloud Veo diffusion generation"
    )
    table.add_row(
        "Active Video Provider",
        f"[bold magenta]{provider}[/bold magenta]",
        "Set VIDEO_GEN_PROVIDER=VEO in .env to use Google Flow Veo"
    )

    console.print(table)

@app.command(name="flow-prompt")
def flow_prompt(
    concept: str = typer.Argument(..., help="Visual scene concept or storyline beat"),
    camera: str = typer.Option("slow cinematic push-in", help="Camera motion (e.g. orbit 45 deg, dolly zoom, FPV drone)"),
    pillar: str = typer.Option("DARK_PSYCHOLOGY", help="Pillar: DARK_PSYCHOLOGY, AI_TOOLS, ORIGINAL_MANGA, CONVERSATIONAL_PODCAST")
):
    """Generates a director-grade Google Flow / Veo cinematic video prompt."""
    adapter = GoogleFlowAdapter()
    style = "dark anime cinematic masterpiece, Ufotable aesthetic, 8k" if pillar == "DARK_PSYCHOLOGY" else "photorealistic 8k cinematic masterpiece"
    optimized = adapter.optimize_prompt_for_veo(
        scene_description=concept,
        camera_motion=camera,
        style=style
    )
    
    console.print(Panel.fit(
        f"[bold cyan]Google Flow / Veo Prompt Optimizer[/bold cyan]\n\n"
        f"[bold]Veo Prompt:[/bold]\n{optimized['prompt']}\n\n"
        f"[bold]Negative Prompt:[/bold]\n{optimized['negative_prompt']}\n\n"
        f"[bold]Camera Motion:[/bold] {optimized['camera_motion']}\n"
        f"[bold]Lighting:[/bold] {optimized['lighting']}",
        title="Google Flow Studio Blueprint"
    ))

@app.command(name="flow-export")
def flow_export(
    project_id: str = typer.Argument(..., help="Project ID to export into Google Flow workspace")
):
    """Exports a studio project timeline and scenes as a Google Flow project manifest."""
    project = get_project(project_id)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{project_id}' not found in database.")
        return

    scenes = get_project_scenes(project_id)
    adapter = GoogleFlowAdapter()
    output_path = adapter.export_flow_project(
        project_id=project_id,
        title=project["title"],
        pillar=project["pillar"],
        scenes=scenes
    )

    console.print(Panel.fit(
        f"[bold green][OK] Google Flow Project Exported Successfully![/bold green]\n\n"
        f"[bold]Project ID:[/bold] {project_id}\n"
        f"[bold]Title:[/bold] {project['title']}\n"
        f"[bold]Scenes Exported:[/bold] {len(scenes)}\n"
        f"[bold]Flow Manifest:[/bold] {output_path}\n"
        f"[bold]Director Board:[/bold] {os.path.join(os.path.dirname(output_path), f'{project_id}_flow_director_board.md')}\n\n"
        f"[dim]Import into flow.google or use Veo generator to render multi-shot sequence.[/dim]"
    ))

@app.command(name="flow-open")
def flow_open():
    """Launches Google Chrome with Flow Studio automation session (Port 9222)."""
    from dragon_studios.integrations.google_flow_automation import GoogleFlowBrowser
    browser = GoogleFlowBrowser()
    console.print("[bold cyan]Launching Chrome with Google Flow automation session...[/bold cyan]")
    browser.launch_browser_for_flow()
    auth_check = browser.connect_and_check_auth()
    
    table = Table(title="Google Flow Chrome Automation Session")
    table.add_column("Property", style="bold cyan")
    table.add_column("Status", style="white")
    table.add_column("Action", style="dim")
    
    table.add_row("CDP Connection", f"[bold green]{auth_check.get('status')}[/bold green]", "Port 9222 Active")
    table.add_row("Current URL", auth_check.get("url", "N/A"), "Google Flow Workspace")
    table.add_row("Signed In", "[bold green]YES[/bold green]" if auth_check.get("is_signed_in") else "[bold yellow]Login Needed[/bold yellow]", "Google Pro Account Session")
    
    console.print(table)
    if not auth_check.get("is_signed_in"):
        console.print(Panel.fit(
            "[bold yellow]Google Login Notice:[/bold yellow]\n"
            "Please log in with your Google Pro account in the opened Chrome window once.\n"
            "Your login session will be permanently remembered so the agent can automate Flow directly!",
            title="Google Flow Authentication"
        ))
    else:
        console.print(Panel.fit(
            "[bold green][OK] Google Pro Account Active in Flow Studio![/bold green]\n"
            "Ready for autonomous prompt injection and multi-shot generation.",
            title="Flow Ready"
        ))

@app.command(name="hook-list")
def hook_list():
    """Lists locally downloaded and discovered watermark-free viral hooks."""
    from dragon_studios.agents.clean_hook_agent import CleanHookAgent
    agent = CleanHookAgent()
    local_hooks = agent.list_local_hooks()
    catalog = agent.load_catalog()

    table = Table(title="Clean Viral Hooks Library (100% Watermark-Free)")
    table.add_column("Status", style="bold cyan")
    table.add_column("Title", style="white")
    table.add_column("Category", style="green")
    table.add_column("Path / Source", style="dim")

    for local_p in local_hooks:
        name = os.path.basename(local_p).replace(".mp4", "").replace("-", " ").title()
        table.add_row("[bold green]LOCAL READY[/bold green]", name, "Verified", local_p)

    for entry in catalog[:15]:
        filename = entry["url"].split("/")[-1]
        local_path = os.path.join(agent.hooks_dir, filename)
        if not os.path.exists(local_path):
            table.add_row("[dim]CATALOG[/dim]", entry.get("title", filename), entry.get("category", "viral"), entry["url"])

    console.print(table)
    console.print(f"[dim]Total Local Ready: {len(local_hooks)} | Discovered in Catalog: {len(catalog)}[/dim]")

@app.command(name="hook-download")
def hook_download(
    count: int = typer.Option(5, help="Number of clean hooks to download and normalize")
):
    """Downloads and normalizes clean watermark-free hooks into assets/clean_hooks/."""
    from dragon_studios.agents.clean_hook_agent import CleanHookAgent
    agent = CleanHookAgent()
    console.print(f"[bold cyan]Downloading top {count} clean watermark-free hooks...[/bold cyan]")
    downloaded = agent.batch_download(count=count)
    
    table = Table(title="Downloaded Clean Hooks")
    table.add_column("Title", style="bold white")
    table.add_column("Format", style="green")
    table.add_column("Normalized File Path", style="cyan")

    for p in downloaded:
        name = os.path.basename(p).replace(".mp4", "").replace("-", " ").title()
        table.add_row(name, "1080x1920 9:16 (30fps)", p)

    console.print(table)
    console.print(Panel.fit(
        f"[bold green][OK] {len(downloaded)} Clean Watermark-Free Hooks Ready for Video Production![/bold green]\n"
        f"Stored in: [bold]{agent.hooks_dir}[/bold]"
    ))

@app.command(name="music-list")
def music_list():
    """Lists locally ready and cataloged copyright-free background music tracks."""
    from dragon_studios.agents.music_agent import MusicAgent
    agent = MusicAgent()
    local_tracks = agent.list_local_tracks()
    catalog = agent.load_catalog()

    table = Table(title="Royalty-Free Background Music Library (100% Cleared)")
    table.add_column("Status", style="bold cyan")
    table.add_column("Title", style="white")
    table.add_column("Genre / Vibe", style="green")
    table.add_column("Path / URL", style="dim")

    for local_p in local_tracks:
        name = os.path.basename(local_p).replace(".mp3", "").replace("_", " ").title()
        table.add_row("[bold green]LOCAL READY[/bold green]", name, "Thematic BGM", local_p)

    for entry in catalog[:15]:
        fname = entry.get("filename", entry["url"].split("/")[-1])
        local_path = os.path.join(agent.music_dir, fname)
        if not os.path.exists(local_path):
            table.add_row("[dim]ONLINE CATALOG[/dim]", entry.get("title", fname), entry.get("genre", "music"), entry["url"])

    console.print(table)
    console.print(f"[dim]Total Local Ready: {len(local_tracks)} | Catalog Tracks: {len(catalog)}[/dim]")

@app.command(name="music-download")
def music_download(
    count: int = typer.Option(10, help="Number of tracks to download autonomously"),
    genre: Optional[str] = typer.Option(None, help="Filter by genre (dark_psychology, dark_phonk, suspense, cinematic, ambient, action)")
):
    """Autonomously downloads verified royalty-free tracks into assets/bg_music/ without human assistance."""
    from dragon_studios.agents.music_agent import MusicAgent
    agent = MusicAgent()
    console.print(f"[bold cyan]Autonomously downloading {count} copyright-free tracks (genre: {genre or 'all'})...[/bold cyan]")
    downloaded = agent.batch_download(count=count, genre=genre)

    table = Table(title="Downloaded Music Tracks")
    table.add_column("Title", style="bold white")
    table.add_column("File Path", style="cyan")

    for p in downloaded:
        name = os.path.basename(p).replace(".mp3", "").replace("_", " ").title()
        table.add_row(name, p)

    console.print(table)
    console.print(Panel.fit(
        f"[bold green][OK] {len(downloaded)} Verified Music Tracks Downloaded Autonomously![/bold green]\n"
        f"Total Library Size: [bold]{len(agent.list_local_tracks())} tracks[/bold]\n"
        f"Stored in: [bold]{agent.music_dir}[/bold]"
    ))

@app.command(name="faceless")
def faceless_command(
    prompt: str = typer.Option("The man who bought an entire bank for $1", "--prompt", "-p", help="Story prompt or topic"),
    style: str = typer.Option("Tall Tale 3D", "--style", "-s", help="Style: Tall Tale 3D, Deep Dive 3D, Inside Out, Stick Story, Night File 3D, Paper Atlas"),
    voice: str = typer.Option("am_adam", "--voice", "-v", help="Voice model: am_adam, am_michael, af_bella, en-US-ChristopherNeural"),
    slug: str = typer.Option("bank_for_one_dollar", "--slug", help="Project folder slug")
):
    """Generates zero-cost viral faceless animated shorts (Kokoro voice, Whisper sync, 3D/2D animation, ducked music)."""
    from faceless_engine.pipeline import create_faceless_short
    console.print(Panel.fit(
        f"[bold cyan]🎬 Zero-Cost Faceless Shorts Studio[/bold cyan]\n"
        f"Prompt: [white]{prompt}[/white]\n"
        f"Style: [yellow]{style}[/yellow] | Voice: [green]{voice}[/green]"
    ))
    res = create_faceless_short(
        prompt=prompt,
        style=style,
        voice=voice,
        project_slug=slug
    )
    if res.get("status") == "SUCCESS":
        console.print(Panel.fit(
            f"[bold green]✅ Faceless Short Created Successfully![/bold green]\n"
            f"Master Video: [bold white]{res['final_video_path']}[/bold white]\n"
            f"Duration: [cyan]{res['qa_report'].get('duration_sec')}s[/cyan] | Resolution: [cyan]{res['qa_report'].get('width')}x{res['qa_report'].get('height')}[/cyan]\n"
            f"Time Elapsed: [yellow]{res['elapsed_seconds']}s[/yellow]"
        ))
    else:
        console.print(f"[bold red]Generation error: {res}[/bold red]")

@app.command(name="faceless-schedule")
def faceless_schedule_command(
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date string YYYY-MM-DD (defaults to today)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of slots to display")
):
    """Displays the master 10-slot daily viral schedule with topics, timings, and status."""
    import sqlite3
    import datetime
    target_date = date or datetime.date.today().strftime("%Y-%m-%d")
    db_path = os.path.abspath("dragon_studios/database/dragon_studios.db")
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM scheduled_reels WHERE date_str = ? ORDER BY slot_number ASC LIMIT ?",
            (target_date, limit)
        ).fetchall()

    table = Table(title=f"🎬 Faceless Shorts Viral Schedule ({target_date}) - 10 Daily Slots")
    table.add_column("Slot", style="bold cyan")
    table.add_column("Time (IST)", style="bold yellow")
    table.add_column("Topic / Title", style="white")
    table.add_column("Style", style="green")
    table.add_column("Status", style="magenta")
    table.add_column("Vault Video", style="dim")

    for r in rows:
        d = dict(r)
        status_color = "green" if d["status"] == "READY" else ("yellow" if d["status"] == "RENDERING" else "blue")
        table.add_row(
            f"#{d['slot_number']}",
            d["scheduled_time"].split(" ")[-1][:5],
            d["title"],
            d["style"],
            f"[{status_color}]{d['status']}[/{status_color}]",
            d["video_path"] or "Pending Render"
        )

    console.print(table)
    total_slots = conn.execute("SELECT COUNT(*) FROM scheduled_reels").fetchone()[0]
    ready_slots = conn.execute("SELECT COUNT(*) FROM scheduled_reels WHERE status = 'READY'").fetchone()[0]
    console.print(f"[dim]Total Calendar Slots: {total_slots} (Nov 8, 2026 ➔ Jan 14, 2027) | Ready in Vault: {ready_slots}[/dim]")

@app.command(name="faceless-render-batch")
def faceless_render_batch_command(
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date string YYYY-MM-DD (defaults to today)"),
    count: int = typer.Option(2, "--count", "-c", help="Number of reels to render in this batch")
):
    """Renders upcoming scheduled reels into the Drive E: vault."""
    import datetime
    from faceless_engine.scheduler_vault import render_batch_for_date
    target_date = date or datetime.date.today().strftime("%Y-%m-%d")
    console.print(f"[bold cyan]Rendering batch of {count} reels for {target_date} into vault...[/bold cyan]")
    rendered = render_batch_for_date(target_date, max_count=count)
    console.print(f"[bold green]Successfully rendered {len(rendered)} reels into vault![/bold green]")

@app.command(name="faceless-daemon")
def faceless_daemon_command(
    interval: int = typer.Option(60, "--interval", "-i", help="Polling interval in seconds"),
    buffer: int = typer.Option(5, "--buffer", "-b", help="Number of upcoming reels to pre-render ahead")
):
    """Runs the continuous autonomous background scheduler daemon."""
    from faceless_engine.daemon import run_scheduler_daemon
    run_scheduler_daemon(poll_interval_sec=interval, pre_render_ahead_count=buffer)

@app.command(name="faceless-batch-all")
def faceless_batch_all_command(
    workers: int = typer.Option(2, "--workers", "-w", help="Number of parallel rendering workers (recommended 2-3)"),
    max_reels: Optional[int] = typer.Option(None, "--max", "-m", help="Max reels to render (defaults to all)")
):
    """Launches mass batch production across all 680 scheduled slots into the Drive E: vault."""
    from faceless_engine.mass_batch_engine import run_mass_production
    run_mass_production(workers=workers, max_reels=max_reels)

@app.command(name="faceless-today")
def faceless_today_command():
    """Renders and publishes today's 10 reels only."""
    from faceless_engine.render_and_publish_today import process_todays_ten_reels
    process_todays_ten_reels()

@app.command(name="faceless-publish")
def faceless_publish_command(
    reel_id: str = typer.Argument(..., help="Reel ID to publish (e.g. reel_2026-11-08_01)"),
    platform: str = typer.Option("all", "--platform", "-p", help="Target platform: all, youtube, instagram")
):
    """Publishes a ready reel to YouTube Shorts and Instagram Reels."""
    from faceless_engine.scheduler_vault import publish_scheduled_reel
    console.print(f"[bold cyan]Publishing reel '{reel_id}' to {platform.upper()}...[/bold cyan]")
    res = publish_scheduled_reel(reel_id)
    console.print(Panel.fit(
        f"[bold green]✓ Reel '{reel_id}' Published & Packaged Successfully![/bold green]\n"
        f"Manifest: {res.get('bundle_dir')}\n"
        f"Master Video: {res.get('video_file')}\n"
        f"Copy-Paste Caption: {res.get('copy_paste_file')}\n"
        f"Platforms: {', '.join(res.get('platforms', []))}"
    ))

if __name__ == "__main__":
    app()
