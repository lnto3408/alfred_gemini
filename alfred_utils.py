#!/usr/bin/env python3
"""Alfred JSON output helpers."""

import json
import sys


def output_items(items):
    """Output Alfred Script Filter JSON."""
    print(json.dumps({"items": items}))


def make_item(title, subtitle="", arg="", icon=None, variables=None, valid=True, mods=None):
    """Create a single Alfred item dict."""
    item = {
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": valid,
    }
    if icon:
        item["icon"] = {"path": icon}
    if variables:
        item["variables"] = variables
    if mods:
        item["mods"] = mods
    return item


def output_error(message):
    """Output an error as an Alfred item."""
    output_items([make_item("Error", subtitle=message, valid=False)])


def text_view_response(text, rerun=None, behaviour=None):
    """Output JSON for Alfred Text View with optional rerun."""
    result = {"response": text}
    if behaviour:
        result["behaviour"] = behaviour
    if rerun is not None:
        result["rerun"] = rerun
    print(json.dumps(result))


def stream_response(text, done=False):
    """Output streaming text view response with rerun."""
    obj = {
        "response": text,
        "behaviour": {
            "response": "replace",
            "scroll": "end",
        },
    }
    if not done:
        obj["rerun"] = 0.3
    # footer
    if not done:
        obj["response"] = text + "\n\n---\n*Generating...*"
    print(json.dumps(obj))
