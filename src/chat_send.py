#!/usr/bin/env python3
"""Send chat message with streaming via rerun mechanism."""

import json
import os
import sys
import subprocess
import time

sys.path.insert(0, os.path.dirname(__file__))

import gemini_client
import session_manager
from alfred_utils import stream_response


def start_background_stream(session_id, message):
    """Launch background process to stream response and write to cache."""
    script = os.path.join(os.path.dirname(__file__), "chat_stream_worker.py")
    subprocess.Popen(
        [sys.executable, script, session_id, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=os.environ.copy(),
    )


def main():
    message = os.environ.get("chat_message", "").strip()
    session_id = os.environ.get("session_id", "").strip()

    if not message:
        message = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""

    if not message:
        print(json.dumps({"response": "No message provided."}))
        return

    # Check if we're reading from an active stream
    cache = session_manager.load_stream_cache()

    if cache and cache.get("session_id") and cache.get("in_progress"):
        # Ongoing stream - read and display
        text = cache.get("text", "")
        if cache.get("done"):
            cache["in_progress"] = False
            session_manager.save_stream_cache(cache)
            # Final output
            sid = cache.get("session_id", "")
            result = {
                "response": text,
                "behaviour": {"response": "replace", "scroll": "end"},
                "variables": {"session_id": sid, "chat_message": ""},
                "footer": "Type follow-up message below",
            }
            print(json.dumps(result))
        else:
            stream_response(text, done=False)
        return

    # Start new stream
    if not session_id:
        session = session_manager.create_session(message, gemini_client.resolve_model("chat_model"))
        session_id = session["id"]
    else:
        session = session_manager.load_session(session_id)
        if not session:
            session = session_manager.create_session(message, gemini_client.resolve_model("chat_model"))
            session_id = session["id"]

    # Initialize stream cache
    session_manager.save_stream_cache({
        "session_id": session_id,
        "message": message,
        "text": "",
        "done": False,
        "in_progress": True,
        "started": time.time(),
    })

    # Start background worker
    start_background_stream(session_id, message)

    # Initial response with rerun
    stream_response("", done=False)


if __name__ == "__main__":
    main()
