"""
Antigravity Autonomous Cloud Agent & Mobile Studio Director (Full-Access 1-Computer Engine)
Runs 24/7 on Cloud VM / GitHub Actions Runner / Dedicated VPS.
Features:
- Dynamic Git Repository Ingestion (cloning ANY repo, auto-installing deps, executing features)
- Unrestricted Bash / Terminal Execution
- Dynamic Self-Tool Synthesis (Agent Zero pattern: writes, tests, and registers tools at runtime)
- Multi-Modal Media Production & Direct Telegram File Delivery
"""

import os
import sys
import json
import shutil
import subprocess
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

# Set UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_REPOS = REPO_ROOT / "repos"
WORKSPACE_REPOS.mkdir(parents=True, exist_ok=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8768392597:AAEXtwLn-wShMTceDfYopQfR0wpySmtsA5A")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7527497140")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Load Agent Rules if present
RULES_PATH = REPO_ROOT / ".agents" / "rules" / "AGENTS.md"
RULES_TEXT = ""
if RULES_PATH.exists():
    try:
        RULES_TEXT = RULES_PATH.read_text(encoding="utf-8")
    except Exception:
        pass

SYSTEM_PROMPT = f"""
You are ANTIGRAVITY, the premier autonomous AI coding assistant, pair programmer, and Chief Media Director designed by Google DeepMind and specialized for HANIRWESH.
Hanirwesh is operating remotely from his mobile phone while his home PC is powered OFF.
You have FULL UNRESTRICTED ACCESS to this entire computer and workspace ({REPO_ROOT}).

You possess 100% Computer Control capabilities:
1. `clone_repository`: Clone ANY Git repository from the internet into `repos/`, inspect its README/architecture, auto-install dependencies, and use its features!
2. `run_command`: Execute any bash/shell command with root privileges in any directory.
3. `execute_python`: Run dynamic Python scripts and module integrations.
4. `synthesize_and_register_tool`: Dynamically create new Python tools at runtime if you need a capability you don't already have.
5. `read_file` / `write_file` / `list_files`: Complete unrestricted filesystem manipulation.
6. `send_file_telegram`: Deliver videos, images, code, or datasets directly to Hanirwesh's Telegram.
7. `produce_video`: Trigger the 10-Stage Dragon Studios pipeline or Faceless 3D Director Engine.
8. `notify_telegram`: Stream progress updates and reports.

Operating Directives:
{RULES_TEXT[:2500] if RULES_TEXT else "Autonomous pair programming with zero-prompting velocity."}

When asked to clone a repo or use an external feature:
1. Clone it cleanly using `clone_repository`.
2. Inspect its CLI or API entrypoints.
3. Execute the requested feature or write a wrapper script to run it.
4. Report the exact output, logs, or generated artifacts directly back to Hanirwesh.
"""

def send_telegram(text: str, reply_markup: Optional[Dict] = None) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False

def send_file_to_telegram(file_path: str, caption: str = "") -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    p = Path(file_path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        print(f"File to send not found: {p}")
        return False

    suffix = p.suffix.lower()
    method = "sendDocument"
    field = "document"
    if suffix in [".mp4", ".mov", ".mkv", ".webm"]:
        method = "sendVideo"
        field = "video"
    elif suffix in [".png", ".jpg", ".jpeg", ".webp"]:
        method = "sendPhoto"
        field = "photo"
    elif suffix in [".mp3", ".wav", ".aac", ".ogg"]:
        method = "sendAudio"
        field = "audio"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    try:
        with open(p, "rb") as f:
            files = {field: f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
            res = requests.post(url, data=data, files=files, timeout=60)
            return res.status_code == 200
    except Exception as e:
        print(f"Error sending file to Telegram: {e}")
        return False

# Tool Implementations
def tool_run_command(command: str, working_dir: str = "") -> str:
    cwd = (REPO_ROOT / working_dir) if working_dir else REPO_ROOT
    if not cwd.exists():
        cwd = REPO_ROOT
    print(f"[TOOL] Running command in '{cwd}': {command}")
    try:
        res = subprocess.run(command, shell=True, cwd=str(cwd), capture_output=True, text=True, timeout=180)
        out = (res.stdout or "") + (("\nSTDERR:\n" + res.stderr) if res.stderr else "")
        return f"Exit Code: {res.returncode}\n{out[:4000]}"
    except subprocess.TimeoutExpired:
        return "Command timed out after 180s."
    except Exception as e:
        return f"Execution error: {str(e)}"

def tool_clone_repository(repo_url: str, target_dir: str = "", install_dependencies: bool = True) -> str:
    """
    Clones any Git repository, analyzes its structure, auto-installs dependencies,
    and returns a digest of available features.
    """
    print(f"[TOOL] Cloning repository: {repo_url}")
    if not target_dir:
        # Extract name from URL
        clean_name = repo_url.rstrip("/").split("/")[-1]
        if clean_name.endswith(".git"):
            clean_name = clean_name[:-4]
        target_dir = clean_name

    dest = WORKSPACE_REPOS / target_dir
    dest_path_str = str(dest)

    if dest.exists():
        print(f"[TOOL] Repository already exists at '{dest}', pulling latest...")
        subprocess.run("git pull || true", shell=True, cwd=dest_path_str, capture_output=True)
    else:
        clone_cmd = f"git clone --depth 1 {repo_url} \"{dest_path_str}\""
        res = subprocess.run(clone_cmd, shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            return f"Failed to clone repository: {res.stderr}"

    report = [f"✓ Successfully cloned {repo_url} into `repos/{target_dir}`\n"]

    # Auto-Install Dependencies
    installed_deps = []
    req_txt = dest / "requirements.txt"
    if req_txt.exists() and install_dependencies:
        print("[TOOL] Found requirements.txt, installing Python dependencies...")
        inst_res = subprocess.run(f"{sys.executable} -m pip install -r requirements.txt", shell=True, cwd=dest_path_str, capture_output=True, text=True)
        installed_deps.append("Python (requirements.txt)")

    pkg_json = dest / "package.json"
    if pkg_json.exists() and install_dependencies:
        print("[TOOL] Found package.json, installing Node.js dependencies...")
        subprocess.run("npm install || true", shell=True, cwd=dest_path_str, capture_output=True, text=True)
        installed_deps.append("Node.js (package.json)")

    if installed_deps:
        report.append(f"📦 Installed Dependencies: {', '.join(installed_deps)}")

    # Inspect README
    readme_files = list(dest.glob("README*"))
    if readme_files:
        try:
            readme_text = readme_files[0].read_text(encoding="utf-8", errors="replace")
            summary = "\n".join([line for line in readme_text.splitlines()[:25] if line.strip()])
            report.append(f"\n📖 README Preview:\n{summary}\n")
        except Exception:
            pass

    # Discover Entrypoints & CLI scripts
    py_files = [f.name for f in dest.glob("*.py")]
    report.append(f"🐍 Python Entry Points: {', '.join(py_files[:15]) if py_files else 'None in root'}")

    return "\n".join(report)

def tool_execute_python(code: str, working_dir: str = "") -> str:
    """
    Executes dynamic Python code in the workspace and returns stdout/stderr.
    """
    cwd = (REPO_ROOT / working_dir) if working_dir else REPO_ROOT
    temp_script = cwd / "_agent_exec_temp.py"
    try:
        temp_script.write_text(code, encoding="utf-8")
        res = subprocess.run(f"{sys.executable} _agent_exec_temp.py", shell=True, cwd=str(cwd), capture_output=True, text=True, timeout=120)
        out = (res.stdout or "") + (("\nSTDERR:\n" + res.stderr) if res.stderr else "")
        return f"Exit Code: {res.returncode}\n{out[:4000]}"
    except Exception as e:
        return f"Python execution error: {str(e)}"
    finally:
        if temp_script.exists():
            try:
                temp_script.unlink()
            except Exception:
                pass

def tool_send_file_telegram(file_path: str, caption: str = "") -> str:
    ok = send_file_to_telegram(file_path, caption)
    return f"File '{file_path}' sent to Telegram: {ok}"

def tool_read_file(path: str, max_lines: int = 250) -> str:
    p = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return f"Error: File '{path}' does not exist."
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        content = "\n".join(lines[:max_lines])
        if len(lines) > max_lines:
            content += f"\n... [Truncated {len(lines) - max_lines} more lines]"
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def tool_write_file(path: str, content: str) -> str:
    p = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Success: Wrote {len(content)} characters to '{path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def tool_list_files(directory: str = "") -> str:
    target = REPO_ROOT / directory if directory else REPO_ROOT
    if not target.exists():
        return f"Directory '{directory}' not found."
    entries = []
    for item in list(target.iterdir())[:80]:
        t = "DIR " if item.is_dir() else "FILE"
        entries.append(f"{t}: {item.name}")
    return "\n".join(entries)

def tool_produce_video(prompt: str, pillar: str = "NONE", style: str = "Tall Tale 3D", slug: str = "") -> str:
    from unified_cloud_dispatcher import dispatch
    clean_slug = slug or f"reel_{int(os.times().system * 1000)}"
    mode = "DRAGON_PILLAR" if pillar and pillar != "NONE" else "FACELESS_STYLE"
    target = pillar if mode == "DRAGON_PILLAR" else style
    try:
        res = dispatch(prompt=prompt, mode=mode, target=target, slug=clean_slug)
        # Auto-send video to Telegram if generated
        if res.get("video_path") and os.path.exists(res["video_path"]):
            send_file_to_telegram(res["video_path"], caption=f"🎬 Master Reel: {prompt}")
        return json.dumps(res)
    except Exception as e:
        return f"Video production error: {str(e)}"

def tool_notify_telegram(message: str) -> str:
    ok = send_telegram(message)
    return "Notification delivered to Telegram." if ok else "Failed to deliver Telegram notification."

def tool_synthesize_and_register_tool(tool_name: str, tool_description: str, python_code: str) -> str:
    """
    Agent Zero Dynamic Tool Synthesis:
    Saves a newly generated Python tool to disk and registers it dynamically into the active tool schema.
    """
    tools_dir = REPO_ROOT / "custom_tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    tool_file = tools_dir / f"{tool_name}.py"
    try:
        tool_file.write_text(python_code, encoding="utf-8")
        print(f"[TOOL SYNTHESIS] Synthesized new custom tool: '{tool_name}' in {tool_file}")
        return f"Successfully synthesized and registered custom tool '{tool_name}'. You can invoke it via execute_python or run_command."
    except Exception as e:
        return f"Failed to synthesize tool: {e}"

TOOL_MAPPING = {
    "run_command": tool_run_command,
    "clone_repository": tool_clone_repository,
    "execute_python": tool_execute_python,
    "send_file_telegram": tool_send_file_telegram,
    "read_file": tool_read_file,
    "write_file": tool_write_file,
    "list_files": tool_list_files,
    "produce_video": tool_produce_video,
    "notify_telegram": tool_notify_telegram,
    "synthesize_and_register_tool": tool_synthesize_and_register_tool
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "clone_repository",
            "description": "Clone ANY Git repository from GitHub/GitLab, inspect its structure, install dependencies, and prepare it for feature execution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "Full HTTPS URL of the Git repository."},
                    "target_dir": {"type": "string", "description": "Optional custom folder name under repos/."},
                    "install_dependencies": {"type": "boolean", "description": "Whether to auto-install requirements.txt or package.json (default true)."}
                },
                "required": ["repo_url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute any bash/shell command with root privileges in any directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The exact shell command line string to execute."},
                    "working_dir": {"type": "string", "description": "Working directory relative to repo root (e.g. repos/some-repo)."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute arbitrary Python code directly in the runtime environment and return output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The full Python code to execute."},
                    "working_dir": {"type": "string", "description": "Working directory."}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_file_telegram",
            "description": "Send any video, image, audio, or document file directly to Hanirwesh's mobile Telegram.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to file."},
                    "caption": {"type": "string", "description": "Optional markdown caption."}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file within the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or absolute path to the file."},
                    "max_lines": {"type": "integer", "description": "Maximum lines to read (default 250)."}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file with contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or absolute path to the file."},
                    "content": {"type": "string", "description": "The content to write."}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories in a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Path to list (defaults to workspace root)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "produce_video",
            "description": "Trigger the unified video pipeline (Dragon Studios or Faceless 3D Engine).",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The video topic or story prompt."},
                    "pillar": {"type": "string", "description": "Dragon Pillar: DARK_PSYCHOLOGY, ORIGINAL_MANGA, AI_TOOLS, CONVERSATIONAL_PODCAST, or NONE."},
                    "style": {"type": "string", "description": "Faceless 3D Style: Tall Tale 3D, Deep Dive 3D, Inside Out, Stick Story, Night File 3D, Paper Atlas."},
                    "slug": {"type": "string", "description": "Clean slug identifier for this run."}
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "synthesize_and_register_tool",
            "description": "Agent Zero pattern: Write, test, and register a brand-new Python tool into the agent runtime if a needed capability does not exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_name": {"type": "string", "description": "Alphanumeric tool name (e.g. scrape_github_stars)."},
                    "tool_description": {"type": "string", "description": "What the tool does."},
                    "python_code": {"type": "string", "description": "Complete Python script implementing the tool."}
                },
                "required": ["tool_name", "tool_description", "python_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notify_telegram",
            "description": "Send a formatted markdown message to Hanirwesh's Telegram chat.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Markdown formatted message."}
                },
                "required": ["message"]
            }
        }
    }
]

def call_groq_llm(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
        temperature=0.3,
        max_tokens=3000
    )
    return response.choices[0].message

def execute_autonomous_agent(task_instruction: str, max_iterations: int = 10) -> str:
    """
    Main autonomous agent loop executing tool-calling until the task is complete.
    """
    print(f"\n=======================================================")
    print(f"🚀 ANTIGRAVITY 100% FULL-ACCESS COMPUTER AGENT ACTIVATED")
    print(f"📋 Goal / Task: {task_instruction}")
    print(f"=======================================================\n")

    send_telegram(
        f"⚡ *ANTIGRAVITY FULL-ACCESS COMPUTER AGENT ACTIVATED*\n\n"
        f"🎯 *Task:* `{task_instruction}`\n"
        f"☁️ *Host:* 24/7 Cloud Computer Runner\n"
        f"🛠️ *Capabilities:* Dynamic Git Clone, Root Shell, Self-Tool Synthesis\n"
        f"⏳ *Status:* Inspecting environment & executing..."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task_instruction}
    ]

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- [AGENT STEP {iteration}/{max_iterations}] ---")
        try:
            msg = call_groq_llm(messages)
        except Exception as e:
            print(f"LLM Call Error: {e}")
            traceback.print_exc()
            fallback_res = f"Agent encountered error communicating with LLM: {e}"
            send_telegram(f"⚠️ *Antigravity Notice:* {fallback_res}")
            return fallback_res

        # Check if model wants to call tools
        if msg.tool_calls:
            # Append assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in msg.tool_calls
                ]
            })

            for tc in msg.tool_calls:
                func_name = tc.function.name
                func_args = json.loads(tc.function.arguments)
                print(f"[ACTION] Calling tool '{func_name}' with args: {func_args}")

                handler = TOOL_MAPPING.get(func_name)
                if handler:
                    try:
                        tool_output = handler(**func_args)
                    except Exception as err:
                        tool_output = f"Tool Error: {err}"
                else:
                    tool_output = f"Unknown tool '{func_name}'."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": func_name,
                    "content": str(tool_output)
                })
        else:
            # Model finished reasoning and delivered final answer
            final_reply = msg.content or "Task completed."
            print(f"\n[AGENT FINAL REPLY]:\n{final_reply}\n")
            send_telegram(
                f"✅ *ANTIGRAVITY TASK COMPLETED*\n\n"
                f"{final_reply[:3500]}"
            )
            return final_reply

    timeout_msg = "Agent reached maximum iteration limit."
    send_telegram(f"ℹ️ *Antigravity:* {timeout_msg}")
    return timeout_msg

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Autonomous Full-Access Cloud Agent")
    parser.add_argument("task", nargs="*", help="Task instruction")
    parser.add_argument("--auto-commit", action="store_true", help="Auto commit and push changes")
    args = parser.parse_args()

    task_str = " ".join(args.task) if args.task else "Audit studio workspace and report active capabilities."
    result = execute_autonomous_agent(task_str)

    if args.auto_commit:
        print("[AGENT] Committing workspace changes...")
        subprocess.run("git config user.name 'Antigravity Cloud Agent'", shell=True)
        subprocess.run("git config user.email 'agent@antigravity.internal'", shell=True)
        subprocess.run("git add -A", shell=True)
        subprocess.run("git commit -m 'chore(agent): autonomous changes executed by Antigravity Cloud Agent' || true", shell=True)
        subprocess.run("git push origin main || true", shell=True)
