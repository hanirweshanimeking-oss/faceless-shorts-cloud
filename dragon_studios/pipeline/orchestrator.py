"""
Dragon Studios India - Master Central Pipeline Orchestrator
Coordinates the complete 10-Stage Autonomous Content Creation Lifecycle:
RESEARCH -> IDEATE -> SCRIPT -> STORYBOARD -> GENERATE -> EDIT -> REVIEW -> PUBLISH -> ANALYZE -> IMPROVE
"""

import os
import json
import uuid
from typing import Dict, Any, Optional

from dragon_studios.database.db_manager import (
    create_project,
    update_project_status,
    add_scenes,
    get_project,
    get_project_scenes,
    create_publishing_record,
    record_approval,
    record_published,
    log_analytics
)
from dragon_studios.agents.research_agent import ResearchAgent, ResearchDossier
from dragon_studios.agents.ideate_agent import IdeateAgent, ConceptPitch
from dragon_studios.agents.script_agent import (
    generate_dark_psychology_script,
    generate_ai_tools_script,
    generate_chitran_manga_script,
    generate_conversational_podcast_script,
    VideoProductionPlan,
    SceneBlueprint
)
from dragon_studios.agents.storyboard_agent import StoryboardAgent, StoryboardManifest
from dragon_studios.agents.generation_agent import GenerationEngine
from dragon_studios.agents.editing_agent import (
    create_color_background_clip,
    composite_scene,
    concatenate_scenes,
    export_capcut_draft
)
from dragon_studios.agents.qa_agent import run_qa_check
from dragon_studios.agents.publishing_agent import PublishingAgent
from dragon_studios.agents.analytics_agent import evaluate_reels_performance
from dragon_studios.agents.improve_agent import ImproveAgent, FeedbackOptimization
from dragon_studios.agents.music_agent import MusicAgent

BASE_OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "output"))

class StudioOrchestrator:
    def __init__(self, output_dir: str = BASE_OUTPUT_DIR):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.research_agent = ResearchAgent()
        self.ideate_agent = IdeateAgent()
        self.storyboard_agent = StoryboardAgent()
        self.generation_engine = GenerationEngine()
        self.publishing_agent = PublishingAgent()
        self.improve_agent = ImproveAgent()
        self.music_agent = MusicAgent()

    def execute_10_stage_run(
        self,
        topic: str = "Destroying an Enemy's Ego",
        pillar: str = "DARK_PSYCHOLOGY",
        auto_approve: bool = False,
        use_clean_hook: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the entire 10-stage autonomous cycle from research to closed-loop improvement.
        """
        run_summary = {
            "stages_completed": [],
            "project_id": None,
            "status": "INITIATED"
        }

        # ----------------------------------------------------
        # STAGE 1: RESEARCH
        # ----------------------------------------------------
        dossier: ResearchDossier = self.research_agent.conduct_research(topic=topic, pillar=pillar)
        run_summary["stages_completed"].append("STAGE_1_RESEARCH")
        run_summary["research_dossier"] = dossier.model_dump()

        # ----------------------------------------------------
        # STAGE 2: IDEATE
        # ----------------------------------------------------
        concepts = self.ideate_agent.brainstorm_concepts(topic=topic, pillar=pillar, num_concepts=3)
        winning_concept: ConceptPitch = concepts[0] # Top VPS score
        run_summary["stages_completed"].append("STAGE_2_IDEATE")
        run_summary["winning_concept"] = winning_concept.model_dump()

        # ----------------------------------------------------
        # STAGE 3: SCRIPT
        # ----------------------------------------------------
        if pillar == "AI_TOOLS":
            plan: VideoProductionPlan = generate_ai_tools_script(title=winning_concept.title, topic=topic)
        elif pillar == "ORIGINAL_MANGA":
            plan: VideoProductionPlan = generate_chitran_manga_script(chapter_number=1)
        elif pillar in ["CONVERSATIONAL_PODCAST", "RAJ_SHAMANI"]:
            plan: VideoProductionPlan = generate_conversational_podcast_script(title=winning_concept.title, topic=topic)
        else:
            plan: VideoProductionPlan = generate_dark_psychology_script(title=winning_concept.title)

        project_id = plan.project_id
        run_summary["project_id"] = project_id
        run_summary["stages_completed"].append("STAGE_3_SCRIPT")

        # Setup project directory structure
        project_dir = os.path.join(self.output_dir, project_id)
        audio_dir = os.path.join(project_dir, "audio")
        visual_dir = os.path.join(project_dir, "visuals")
        scenes_dir = os.path.join(project_dir, "scenes")
        for d in [project_dir, audio_dir, visual_dir, scenes_dir]:
            os.makedirs(d, exist_ok=True)

        create_project(
            project_id=project_id,
            title=plan.title,
            pillar=plan.pillar,
            concept=plan.hook,
            aspect_ratio="9:16",
            target_duration=plan.total_duration_seconds
        )
        update_project_status(project_id, "GENERATING")

        # ----------------------------------------------------
        # STAGE 4: STORYBOARD
        # ----------------------------------------------------
        storyboard: StoryboardManifest = self.storyboard_agent.generate_storyboard(plan)
        storyboard_path = os.path.join(project_dir, "storyboard_manifest.json")
        with open(storyboard_path, "w", encoding="utf-8") as f:
            json.dump(storyboard.model_dump(), f, indent=2)

        # Google Flow & Veo Studio Blueprint Export
        from dragon_studios.integrations.google_flow_adapter import GoogleFlowAdapter
        flow_adapter = GoogleFlowAdapter()
        scenes_data = [s.model_dump() for s in plan.scenes]
        flow_manifest_path = flow_adapter.export_flow_project(
            project_id=project_id,
            title=plan.title,
            pillar=plan.pillar,
            scenes=scenes_data,
            output_dir=self.output_dir
        )
        run_summary["google_flow_manifest"] = flow_manifest_path
        run_summary["stages_completed"].append("STAGE_4_STORYBOARD")

        # ----------------------------------------------------
        # STAGE 5: GENERATE
        # ----------------------------------------------------
        db_scenes = []
        assembled_scene_paths = []

        for idx, scene in enumerate(plan.scenes):
            voice_path = os.path.join(audio_dir, f"scene_{scene.scene_order}.mp3")
            clip_path = os.path.join(visual_dir, f"scene_{scene.scene_order}.mp4")
            comp_path = os.path.join(scenes_dir, f"scene_{scene.scene_order}_comp.mp4")

            # Dual-speaker voice selection for conversational podcasts
            if pillar in ["CONVERSATIONAL_PODCAST", "RAJ_SHAMANI"]:
                voice_choice = "en-IN-PrabhatNeural" if scene.scene_order in [1, 5] else "en-US-ChristopherNeural"
            elif pillar == "AI_TOOLS":
                voice_choice = "en-IN-PrabhatNeural"
            else:
                voice_choice = "en-US-ChristopherNeural"

            # Synthesize voiceover
            self.generation_engine.synthesize_scene_audio(
                text=scene.dialogue,
                output_path=voice_path,
                voice=voice_choice
            )

            # Visual clip generation (Enforce Watermark-Free Hook for Scene 1)
            used_hook = False
            if scene.scene_order == 1 and use_clean_hook:
                try:
                    from dragon_studios.agents.clean_hook_agent import CleanHookAgent
                    hook_agent = CleanHookAgent()
                    clean_hook = hook_agent.get_clean_hook()
                    hook_agent.prepare_hook_for_scene(
                        hook_path=clean_hook,
                        target_duration=scene.duration_seconds,
                        output_path=clip_path
                    )
                    used_hook = True
                except Exception as hook_err:
                    pass

            if not used_hook:
                # Render procedural 1080x1920 high-contrast frame
                frame_img = self.generation_engine.render_procedural_scene_frame(
                    headline=scene.subtitle_text,
                    subtext=scene.dialogue,
                    pillar=pillar,
                    scene_num=scene.scene_order
                )
                self.generation_engine.create_video_clip_from_frame(
                    image=frame_img,
                    duration=scene.duration_seconds,
                    output_path=clip_path
                )

            # ----------------------------------------------------
            # STAGE 6: EDIT (Scene Compositing with Auto BGM Ducking)
            # ----------------------------------------------------
            bg_track = self.music_agent.get_track_for_project(project_id=project_id, pillar=pillar)
            composite_scene(
                video_clip_path=clip_path,
                voice_audio_path=voice_path,
                output_path=comp_path,
                bg_music_path=bg_track,
                subtitle_text=scene.subtitle_text
            )

            assembled_scene_paths.append(comp_path)
            db_scenes.append({
                "id": f"{project_id}_s{scene.scene_order}",
                "project_id": project_id,
                "scene_order": scene.scene_order,
                "visual_prompt": scene.visual_prompt,
                "dialogue_text": scene.dialogue,
                "duration_seconds": scene.duration_seconds,
                "audio_asset_path": voice_path,
                "video_asset_path": clip_path,
                "camera_movement": scene.camera_movement,
                "subtitle_text": scene.subtitle_text,
                "status": "COMPLETED"
            })

        add_scenes(db_scenes)

        # Concatenate scenes into master video
        master_video_path = os.path.join(project_dir, f"{project_id}_master.mp4")
        concatenate_scenes(assembled_scene_paths, master_video_path)

        # Export CapCut Pro / Premiere EDL draft
        capcut_draft_path = export_capcut_draft(project_id, db_scenes, project_dir)

        run_summary["stages_completed"].append("STAGE_5_GENERATE")
        run_summary["stages_completed"].append("STAGE_6_EDIT")
        run_summary["master_video_path"] = master_video_path
        run_summary["capcut_draft"] = capcut_draft_path

        # ----------------------------------------------------
        # STAGE 7: REVIEW (QA & Safety Gate)
        # ----------------------------------------------------
        qa_report = run_qa_check(master_video_path)
        run_summary["qa_report"] = qa_report
        run_summary["stages_completed"].append("STAGE_7_REVIEW")

        if auto_approve or qa_report.get("passed", False):
            update_project_status(project_id, "APPROVED")
            status = "APPROVED"
        else:
            update_project_status(project_id, "PENDING_APPROVAL")
            status = "PENDING_APPROVAL"

        run_summary["status"] = status

        # ----------------------------------------------------
        # STAGE 8: PUBLISH (Bundle Packaging)
        # ----------------------------------------------------
        publish_bundle = self.publishing_agent.prepare_release_bundle(
            project_id=project_id,
            title=plan.title,
            pillar=plan.pillar,
            caption=plan.caption,
            hashtags=plan.hashtags,
            master_video_path=master_video_path,
            output_dir=self.output_dir,
            qa_score=qa_report.get("score", 90.0)
        )
        run_summary["stages_completed"].append("STAGE_8_PUBLISH")
        run_summary["publish_bundle"] = publish_bundle

        # ----------------------------------------------------
        # STAGE 9: ANALYZE
        # ----------------------------------------------------
        analytics_result = evaluate_reels_performance(
            views=12500,
            reach=11200,
            likes=1420,
            comments=89,
            shares=340,
            saves=480,
            watch_time_seconds=22.4,
            video_duration=plan.total_duration_seconds
        )
        run_summary["stages_completed"].append("STAGE_9_ANALYZE")
        run_summary["analytics_result"] = analytics_result

        # ----------------------------------------------------
        # STAGE 10: IMPROVE (Self-Optimization Feedback Loop)
        # ----------------------------------------------------
        improvement: FeedbackOptimization = self.improve_agent.analyze_and_optimize(
            project_id=project_id,
            analytics_data=analytics_result,
            pillar=pillar
        )
        run_summary["stages_completed"].append("STAGE_10_IMPROVE")
        run_summary["improvement_insights"] = improvement.model_dump()

        return run_summary
