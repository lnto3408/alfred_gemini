#!/usr/bin/env python3
"""Chat history: ggh keyword - list previous conversations."""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from alfred_utils import output_items, make_item
import session_manager


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    # Clean up old sessions first
    session_manager.cleanup_old_sessions()

    sessions = session_manager.list_sessions()

    if not sessions:
        output_items([make_item(
            "No chat history",
            subtitle="Start a new conversation with 'gg'",
            valid=False,
        )])
        return

    items = []
    for session in sessions:
        title = session.get("title", "Untitled")
        updated = session.get("updated", "")
        turn_count = len(session.get("history", []))
        model = session.get("model", "")

        # Filter by query
        if query and query.lower() not in title.lower():
            continue

        try:
            dt = datetime.fromisoformat(updated)
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            time_str = updated

        subtitle = f"{time_str} · {turn_count} messages"
        if model:
            subtitle += f" · {model}"

        items.append(make_item(
            title,
            subtitle=subtitle,
            arg=session["id"],
            variables={"session_id": session["id"]},
            mods={
                "cmd": {
                    "subtitle": "Delete this conversation",
                    "arg": session["id"],
                    "variables": {"action": "delete_session"},
                }
            },
        ))

    if not items:
        output_items([make_item(
            f"No results for '{query}'",
            subtitle="Try a different search term",
            valid=False,
        )])
    else:
        output_items(items)


if __name__ == "__main__":
    main()
