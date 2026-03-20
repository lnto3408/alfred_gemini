#!/usr/bin/env python3
"""Background worker: streams Gemini response and writes chunks to cache file."""

import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))

import gemini_client
import session_manager


CHAT_SYSTEM = "You are a helpful AI assistant. Respond in the same language the user uses. Use Markdown formatting for readability."


def main():
    if len(sys.argv) < 3:
        return

    session_id = sys.argv[1]
    message = sys.argv[2]

    session = session_manager.load_session(session_id)
    if not session:
        session_manager.save_stream_cache({
            "session_id": session_id,
            "text": "Error: Session not found.",
            "done": True,
            "in_progress": True,
        })
        return

    # Add user message to history
    session_manager.add_turn(session, "user", message)

    try:
        full_text = ""
        for chunk in gemini_client.chat_generate_stream(
            history=session["history"][:-1],  # exclude the message we just added
            message=message,
            system_instruction=CHAT_SYSTEM,
            feature_model_key="chat_model",
        ):
            full_text += chunk
            session_manager.save_stream_cache({
                "session_id": session_id,
                "text": full_text,
                "done": False,
                "in_progress": True,
            })

        # Save model response to session
        session_manager.add_turn(session, "model", full_text)

        # Mark stream as done
        session_manager.save_stream_cache({
            "session_id": session_id,
            "text": full_text,
            "done": True,
            "in_progress": True,
        })

    except Exception as e:
        error_msg = f"Error: {e}\n\n```\n{traceback.format_exc()}\n```"
        session_manager.save_stream_cache({
            "session_id": session_id,
            "text": error_msg,
            "done": True,
            "in_progress": True,
        })


if __name__ == "__main__":
    main()
