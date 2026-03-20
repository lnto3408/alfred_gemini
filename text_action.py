#!/usr/bin/env python3
"""Text manipulation dispatcher for Universal Actions."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gemini_client


ACTIONS = {
    "explain": {
        "system": "You are a helpful explainer. Explain the given text clearly and concisely. Use the same language as the input text when possible.",
        "prompt": "Explain the following text:\n\n{text}",
    },
    "fix_grammar": {
        "system": "You are a grammar and spelling expert. Fix all grammar and spelling errors. Output ONLY the corrected text, nothing else.",
        "prompt": "{text}",
    },
    "make_shorter": {
        "system": "You are a concise writer. Shorten the given text while preserving its core meaning. Output ONLY the shortened text.",
        "prompt": "{text}",
    },
    "make_longer": {
        "system": "You are an expressive writer. Expand the given text with more detail and nuance. Output ONLY the expanded text.",
        "prompt": "{text}",
    },
    "tone_friendly": {
        "system": "You are a tone editor. Rewrite the text in a warm, friendly, approachable tone. Output ONLY the rewritten text.",
        "prompt": "{text}",
    },
    "tone_professional": {
        "system": "You are a tone editor. Rewrite the text in a professional, formal tone. Output ONLY the rewritten text.",
        "prompt": "{text}",
    },
    "add_comments": {
        "system": "You are a code documentation expert. Add clear, helpful comments to the code. Output ONLY the commented code.",
        "prompt": "{text}",
    },
    "find_synonym": {
        "system": "You are a thesaurus. For each significant word in the text, provide synonyms. Format: word → synonym1, synonym2, synonym3",
        "prompt": "{text}",
    },
    "ask_about": {
        "system": "You are a helpful AI assistant. Answer the user's question about the provided text. Respond in the same language as the question.",
        "prompt": "Text:\n{text}\n\nQuestion: {question}",
    },
    "summarize": {
        "system": "You are a summarizer. Provide a clear, concise summary of the given text. Use the same language as the input text.",
        "prompt": "Summarize the following text:\n\n{text}",
    },
}


def run_action(action_name, text, question=None):
    action = ACTIONS.get(action_name)
    if not action:
        return f"Unknown action: {action_name}"

    prompt_vars = {"text": text}
    if question:
        prompt_vars["question"] = question

    prompt = action["prompt"].format(**prompt_vars)
    system = action["system"]

    return gemini_client.generate(
        prompt=prompt,
        system_instruction=system,
    )


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"response": "Usage: text_action.py <action> [question]"}))
        return

    action_name = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else None

    # Read text from stdin (Universal Action passes text via stdin)
    text = sys.stdin.read().strip() if not sys.stdin.isatty() else ""

    # Fallback: read from environment variable
    if not text:
        text = os.environ.get("action_text", "").strip()

    if not text:
        print(json.dumps({"response": "No text provided."}))
        return

    try:
        result = run_action(action_name, text, question)
        print(json.dumps({"response": result}))
    except Exception as e:
        print(json.dumps({"response": f"Error: {e}"}))


if __name__ == "__main__":
    main()
