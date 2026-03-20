#!/usr/bin/env python3
"""Translate Script Filter: tr keyword - shows input prompt."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from alfred_utils import output_items, make_item


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    if not query:
        items = [make_item(
            "Translate",
            subtitle="Type text to translate (Korean↔English auto-detect)",
            valid=False,
            icon="icon.png",
        )]
    else:
        lang = os.environ.get("translation_default_lang", "ko").strip() or "ko"
        items = [make_item(
            query,
            subtitle=f"Press Enter to translate (target: {lang})",
            arg=query,
            icon="icon.png",
        )]

    output_items(items)


if __name__ == "__main__":
    main()
