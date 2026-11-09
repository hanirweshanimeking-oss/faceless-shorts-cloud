"""
Antigravity Autonomous Cloud Agent & Mobile Studio Director
Runs 24/7 on GitHub Actions Cloud Runner & Serverless Infrastructure.
Empowers Hanirwesh with the complete Antigravity agentic capabilities remotely via Telegram.
"""

import os
import sys
import json
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
You have FULL AUTONOMOUS ACCESS to this cloud workspace ({REPO_ROOT}).

You have tools to:
1. Run bash/shell commands (`run_command`)
2. Read files (`read_file`)
3. Write or edit files (`write_file`, `edit_file`)
4. List directory contents (`list_files`)
5. Produce Dragon Studios reels or 3D faceless shorts (`produce_video`)
6. Send updates to Telegram (`notify_telegram`)

Operating Directives:
{RULES_TEXT[:2000] if RULES_TEXT else "Follow high-velocity autonomous pair programming standards."}

When given a coding, debugging, or media production task:
- Break it down, inspect existing files first if needed.
- Write clean, robust code.
- Test your changes using run_command.
- Deliver a clear, concise report of what was executed.
"""

# Available Tools Definition
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a bash/shell command in the workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The exact shell command line string to execute."}
                },
                "required": ["command"]
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
                    "max_lines": {"type": "integer", "description": "Maximum lines to read (default 200)."}
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

# Tool Implementations
def tool_run_command(command: str) -> str:
    print(f"[TOOL] Running command: {command}")
    try:
        res = subprocess.run(command, shell=True, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120)
        out = (res.stdout or "") + (("\nSTDERR:\n" + res.stderr) if res.stderr else "")
        return f"Exit Code: {res.returncode}\n{out[:4000]}"
    except subprocess.TimeoutExpired:
        return "Command timed out after 120s."
    except Exception as e:
        return f"Execution error: {str(e)}"

def tool_read_file(path: str, max_lines: int = 200) -> str:
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
    for item in list(target.iterdir())[:60]:
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
        return json.dumps(res)
    except Exception as e:
        return f"Video production error: {str(e)}"

def tool_notify_telegram(message: str) -> str:
    ok = send_telegram(message)
    return "Notification delivered to Telegram." if ok else "Failed to deliver Telegram notification."

TOOL_MAPPING = {
    "run_command": tool_run_command,
    "read_file": tool_read_file,
    "write_file": tool_write_file,
    "list_files": tool_list_files,
    "produce_video": tool_produce_video,
    "notify_telegram": tool_notify_telegram
}

def call_groq_llm(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
        temperature=0.3,
        max_tokens=2048
    )
    return response.choices[0].message

def execute_autonomous_agent(task_instruction: str, max_iterations: int = 8) -> str:
    """
    Main autonomous agent loop executing tool-calling until the task is complete.
    """
    print(f"\n=======================================================")
    print(f"🚀 ANTIGRAVITY AUTONOMOUS CLOUD AGENT ACTIVATED")
    print(f"📋 Goal / Task: {task_instruction}")
    print(f"=======================================================\n")

    send_telegram(
        f"⚡ *ANTIGRAVITY AUTONOMOUS CLOUD AGENT ACTIVATED*\n\n"
        f"🎯 *Task:* `{task_instruction}`\n"
        f"☁️ *Host:* GitHub Actions Ubuntu Runner (Cloud Studio)\n"
        f"⏳ *Status:* Thinking and analyzing workspace..."
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
    parser = argparse.ArgumentParser(description="Antigravity Autonomous Cloud Agent")
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
