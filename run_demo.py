"""
run_demo.py – Command-line demo: runs a single ticket through the crew
without requiring the Streamlit UI.

Usage:
  python run_demo.py
  python run_demo.py --ticket "I can't log in to my account"
  python run_demo.py --cheap
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from crew import run_triage


DEMO_TICKETS = [
    "I was charged twice this month. Please refund the duplicate payment.",
    "My webhooks stopped delivering after I updated our server. The logs show 500 errors.",
    "I forgot my password and the reset email isn't arriving.",
    "Is the service currently having an outage? I can't reach the dashboard.",
]


def print_result(result: dict) -> None:
    print("\n" + "=" * 65)
    print(f"  TICKET: {result['ticket_text'][:70]}")
    print("=" * 65)
    print(f"  Category  : {result['category'].upper()}")
    print(f"  Priority  : {result['priority'].upper()}")
    print(f"  Confidence: {result['confidence']:.0%}")
    print(f"  Escalated : {result['escalated']}")

    if result["escalated"]:
        print(f"\n  ⚠  {result['escalation_reason']}")
    else:
        print(f"\n  Sources   : {', '.join(result['sources'])}")
        print(f"  QA Verdict: {result['qa_verdict']} (score={result.get('qa_score', 0):.0%})")
        print(f"\n  FINAL REPLY:\n  {result['final_reply']}")

    print(f"\n  Latency: {result['latency_seconds']}s | Model: {result['model_used']}")
    print("-" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a ticket through the triage crew")
    parser.add_argument("--ticket", type=str, default=None, help="Custom ticket text")
    parser.add_argument("--cheap", action="store_true", help="Use cheaper model")
    parser.add_argument("--all", action="store_true", help="Run all demo tickets")
    args = parser.parse_args()

    if args.all:
        for t in DEMO_TICKETS:
            result = run_triage(t, use_cheap_model=args.cheap)
            print_result(result)
    else:
        ticket = args.ticket or DEMO_TICKETS[0]
        result = run_triage(ticket, use_cheap_model=args.cheap)
        print_result(result)
