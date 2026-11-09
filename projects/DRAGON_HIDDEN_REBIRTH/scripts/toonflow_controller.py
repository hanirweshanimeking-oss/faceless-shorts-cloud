"""
Toonflow MCP Client & Project Controller
Provides high-level helpers to interact with Toonflow:
- Initialize session
- Open / create project workspaces
- Create & switch canvases
- Add storyboard nodes, character reference cards, and edge connections
- Arrange canvas & fit view
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class ToonflowMCPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:10588/mcp", token: str = "9226dcd9d945a8677ea8cae9be7b05009dcb1a307286e6e9debe9bd6c9749632"):
        self.base_url = base_url
        self.token = token
        self.session_id: Optional[str] = None
        self.connection_id: Optional[str] = None
        self.workspace_root: Optional[str] = None
        self.current_directory: Optional[str] = None
        self.current_canvas_id: Optional[str] = None
        self._msg_id = 1
        self.connect()

    def _send(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._msg_id += 1
        payload: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self._msg_id,
            "method": method
        }
        if params is not None:
            payload["params"] = params

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self.token}"
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers
        )

        with urllib.request.urlopen(req, timeout=10) as res:
            new_sid = res.headers.get("mcp-session-id")
            if new_sid:
                self.session_id = new_sid
            body = res.read().decode("utf-8")
            
            # Parse event-stream / json-rpc response
            for line in body.splitlines():
                if line.startswith("data:"):
                    return json.loads(line[5:])
            try:
                return json.loads(body)
            except Exception:
                return {"raw": body}

    def connect(self):
        # 1. Initialize
        init_res = self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Antigravity", "version": "1.0.0"}
        })
        # 2. Initialized Notification
        self._send("notifications/initialized", {})

        # 3. Get App State
        app_state = self.call_tool("getAppState")
        try:
            struct = app_state.get("result", {}).get("structuredContent", {})
            self.workspace_root = struct.get("workspaceRoot")
            conns = struct.get("connections", [])
            if conns:
                self.connection_id = conns[0].get("id")
                st = conns[0].get("state", {})
                self.current_directory = st.get("directory")
                self.current_canvas_id = st.get("canvasId")
        except Exception as e:
            print("[!] Could not parse app state:", e)

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None, target: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"name": tool_name}
        
        args = arguments or {}
        if target:
            params["arguments"] = {"target": target, "args": args}
        else:
            tgt = {}
            if self.connection_id:
                tgt["connectionId"] = self.connection_id
            if self.current_directory:
                tgt["directory"] = self.current_directory
            if self.current_canvas_id:
                tgt["canvasId"] = self.current_canvas_id
            
            if tgt:
                params["arguments"] = {"target": tgt, "args": args}
            else:
                params["arguments"] = args

        return self._send("tools/call", params)

    def list_tools(self) -> List[Dict[str, Any]]:
        res = self._send("tools/list", {})
        return res.get("result", {}).get("tools", [])

if __name__ == "__main__":
    client = ToonflowMCPClient()
    print("[+] Connected to Toonflow MCP!")
    print(f"    Session ID: {client.session_id}")
    print(f"    Connection ID: {client.connection_id}")
    print(f"    Workspace Root: {client.workspace_root}")

    # Inspect tool schemas
    tools = client.list_tools()
    print(f"[+] Total tools: {len(tools)}")
    for t in tools:
        if t["name"] in ["openProject", "addCanvas", "addNode", "getCanvas"]:
            print(f"\n--- TOOL: {t['name']} ---")
            print(json.dumps(t["inputSchema"], indent=2))
