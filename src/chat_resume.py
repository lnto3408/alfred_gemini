#!/usr/bin/env python3
"""Resume a previous chat session - Script Filter for follow-up input."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from alfred_utils import output_items, make_item
import session_manager


def main():
    session_id = os.environ.get("session_id", "").strip()
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    if not session_id:
        output_items([make_item("No session selected", valid=False)])
        return

    session = session_manager.load_session(session_id)
    if not session:
        output_items([make_item("Session not found", valid=False)])
        return

    # Show last model response as context
    last_response = ""
    for turn in reversed(session.get("history", [])):
        if turn["role"] == "model":
            last_response = turn["parts"][0]["text"][:80]
            break

    if not query:
        items = [make_item(
            f"Continue: {session['title']}",
            subtitle=f"Last: {last_response}..." if last_response else "Type follow-up message...",
            valid=False,
        )]
    else:
        items = [make_item(
            query,
            subtitle=f"Send to: {session['title']}",
            arg=query,
            variables={"session_id": session_id, "chat_message": query},
        )]

    output_items(items)


if __name__ == "__main__":
    main()
