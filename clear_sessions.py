#!/usr/bin/env python3
"""Clear old chat sessions."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import session_manager


def main():
    removed = session_manager.cleanup_old_sessions()
    print(f"Removed {removed} old session(s).")


if __name__ == "__main__":
    main()
