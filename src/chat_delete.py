#!/usr/bin/env python3
"""Delete a chat session."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import session_manager


def main():
    session_id = os.environ.get("session_id", "").strip()
    if not session_id and len(sys.argv) > 1:
        session_id = sys.argv[1].strip()

    if session_id:
        session_manager.delete_session(session_id)


if __name__ == "__main__":
    main()
