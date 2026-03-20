#!/usr/bin/env python3
"""Translation feature: tr keyword and Universal Action."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gemini_client


SYSTEM_INSTRUCTION = """You are a professional translator. Follow these rules strictly:
1. If the input text is Korean, translate it to English.
2. If the input text is in any other language, translate it to {target_lang_name}.
3. Output ONLY the translated text. No explanations, no notes, no quotes.
4. Preserve the original formatting (line breaks, paragraphs, lists).
5. For technical terms, keep the original term in parentheses if the translation might be ambiguous."""

LANG_NAMES = {
    "ko": "Korean",
    "ja": "Japanese",
    "zh": "Chinese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "vi": "Vietnamese",
    "th": "Thai",
    "id": "Indonesian",
}


def translate(text):
    target_lang = os.environ.get("translation_default_lang", "ko").strip() or "ko"
    target_lang_name = LANG_NAMES.get(target_lang, "Korean")

    system = SYSTEM_INSTRUCTION.format(target_lang_name=target_lang_name)
    result = gemini_client.generate(
        prompt=text,
        system_instruction=system,
        feature_model_key="translation_model",
    )
    return result.strip()


def main():
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not query:
        # Read from stdin (Universal Action)
        query = sys.stdin.read().strip()
    if not query:
        result = {"response": "No text provided for translation."}
        print(json.dumps(result))
        return

    try:
        translated = translate(query)
        result = {"response": translated}
        print(json.dumps(result))
    except Exception as e:
        result = {"response": f"Translation error: {e}"}
        print(json.dumps(result))


if __name__ == "__main__":
    main()
