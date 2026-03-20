#!/usr/bin/env python3
"""Chat Script Filter: gg keyword - shows input prompt or active session."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from alfred_utils import output_items, make_item


def main():
    query = "{query}" if len(sys.argv) < 2 else sys.argv[1]
    query = query.strip()

    if not query or query == "{query}":
        items = [
            make_item(
                "Chat with Gemini",
                subtitle="Type your message...",
                valid=False,
                icon="icon.png",
            )
        ]
    else:
        items = [
            make_item(
                query,
                subtitle="Press Enter to send to Gemini",
                arg=query,
                icon="icon.png",
                variables={"chat_message": query},
            )
        ]

    output_items(items)


if __name__ == "__main__":
    main()
