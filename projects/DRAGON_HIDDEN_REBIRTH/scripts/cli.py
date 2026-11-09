"""
DRAGON: HIDDEN REBIRTH - Studio Master CLI
The unified command-line entrypoint for the SSS+ Autonomous Manga Production Studio.
"""

import argparse
import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add root directory to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.production_manager import ProductionManager

def main():
    parser = argparse.ArgumentParser(description="DRAGON: HIDDEN REBIRTH - Manga Production Studio CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Produce Page
    produce_parser = subparsers.add_parser("produce-page", help="Execute end-to-end production pipeline for a manga page")
    produce_parser.add_argument("--page-id", type=str, default="page_001_01", help="Target Page ID (default: page_001_01)")
    produce_parser.add_argument("--cloud", action="store_true", help="Attempt Tier 2 cloud generation before local fallback")

    # 2. Studio Status
    subparsers.add_parser("status", help="Display executive studio production dashboard")

    # 3. Inspect Character
    char_parser = subparsers.add_parser("character", help="Inspect character profile and canonical prompts")
    char_parser.add_argument("character_id", type=str, help="Character ID (e.g. char_chitran)")

    args = parser.parse_args()
    manager = ProductionManager(ROOT_DIR)

    if args.command == "produce-page":
        res = manager.produce_page(args.page_id, prefer_cloud=args.cloud)
        print("\n=======================================================")
        print(f"[+] PAGE PRODUCTION COMPLETE: {res['page_id']}")
        print(f"[+] Master Page: {res['master_page_path']}")
        print(f"[+] Elapsed Time: {res['elapsed_seconds']}s")
        print(f"[+] Budget Spent: ₹{res['budget_spent_inr']}")
        print(f"[+] QA Verdict: {res['qa_result']['verdict']} (Score: {res['qa_result']['overall_score']:.2f}/10)")
        print(f"[+] QA Report: {res['qa_result']['report_path']}")
        print("=======================================================")

    elif args.command == "status":
        stats = manager.get_studio_status()
        print("\n" + "=" * 55)
        print(f"      {stats['studio_title']}")
        print("=" * 55)
        for k, v in stats.items():
            print(f"  {k:.<30} : {v}")
        print("=" * 55)

    elif args.command == "character":
        char = manager.character_agent.get_character(args.character_id)
        if not char:
            print(f"[-] Character {args.character_id} not found.")
            sys.exit(1)
        print("\n" + "=" * 55)
        print(f"  CHARACTER PROFILE: {char['name']} ({char.get('alias', '')})")
        print("=" * 55)
        print(f"  Age        : {char.get('age')}")
        print(f"  Build      : {char.get('build')}")
        print(f"  Facial     : {char.get('facial_features')}")
        print(f"  Base Prompt: {char.get('visual_prompt_base')}")
        print("=" * 55)

if __name__ == "__main__":
    main()
