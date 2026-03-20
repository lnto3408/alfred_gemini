#!/usr/bin/env python3
"""Chat session persistence manager."""

import json
import os
import time
import uuid
from datetime import datetime, timedelta


def get_sessions_dir():
    data_dir = os.environ.get("alfred_workflow_data", "")
    if not data_dir:
        data_dir = os.path.join(os.path.expanduser("~"), ".alfred_gemini_workflow")
    sessions_dir = os.path.join(data_dir, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    return sessions_dir


def get_stream_cache_path():
    data_dir = os.environ.get("alfred_workflow_data", "")
    if not data_dir:
        data_dir = os.path.join(os.path.expanduser("~"), ".alfred_gemini_workflow")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "active_stream.json")


def create_session(first_message, model=None):
    """Create a new chat session, return session dict."""
    session_id = str(uuid.uuid4())
    title = first_message[:60] + ("..." if len(first_message) > 60 else "")
    session = {
        "id": session_id,
        "title": title,
        "model": model or "",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "history": [],
    }
    save_session(session)
    return session


def save_session(session):
    """Save session to disk."""
    sessions_dir = get_sessions_dir()
    path = os.path.join(sessions_dir, f"{session['id']}.json")
    session["updated"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)


def load_session(session_id):
    """Load a session by ID."""
    sessions_dir = get_sessions_dir()
    path = os.path.join(sessions_dir, f"{session_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_sessions():
    """List all sessions, sorted by most recent first."""
    sessions_dir = get_sessions_dir()
    sessions = []
    if not os.path.exists(sessions_dir):
        return sessions
    for fname in os.listdir(sessions_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(sessions_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                session = json.load(f)
                sessions.append(session)
        except (json.JSONDecodeError, IOError):
            continue
    sessions.sort(key=lambda s: s.get("updated", ""), reverse=True)
    return sessions


def delete_session(session_id):
    """Delete a session by ID."""
    sessions_dir = get_sessions_dir()
    path = os.path.join(sessions_dir, f"{session_id}.json")
    if os.path.exists(path):
        os.remove(path)


def add_turn(session, role, text):
    """Add a turn to session history and enforce max turns."""
    max_turns = int(os.environ.get("max_history_turns", "20"))
    session["history"].append({
        "role": role,
        "parts": [{"text": text}],
    })
    # Trim oldest turns (keep pairs) if exceeding max
    while len(session["history"]) > max_turns * 2:
        session["history"] = session["history"][2:]
    save_session(session)


def cleanup_old_sessions():
    """Remove sessions older than session_ttl_days."""
    ttl_days = int(os.environ.get("session_ttl_days", "7"))
    cutoff = datetime.now() - timedelta(days=ttl_days)
    sessions_dir = get_sessions_dir()
    if not os.path.exists(sessions_dir):
        return 0
    removed = 0
    for fname in os.listdir(sessions_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(sessions_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                session = json.load(f)
            updated = datetime.fromisoformat(session.get("updated", "2000-01-01"))
            if updated < cutoff:
                os.remove(path)
                removed += 1
        except (json.JSONDecodeError, IOError, ValueError):
            continue
    return removed


def save_stream_cache(data):
    """Save streaming state to cache file."""
    path = get_stream_cache_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_stream_cache():
    """Load streaming state from cache file."""
    path = get_stream_cache_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def clear_stream_cache():
    """Remove the stream cache file."""
    path = get_stream_cache_path()
    if os.path.exists(path):
        os.remove(path)
