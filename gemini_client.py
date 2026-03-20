#!/usr/bin/env python3
"""Gemini API client shared across all workflow features."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import bootstrap  # noqa: F401 — ensures deps are installed

from google import genai
from google.genai import types


def get_env(key, default=""):
    return os.environ.get(key, default).strip()


def resolve_model(feature_model_key=None):
    """Resolve model: custom_model > feature-specific > default_model."""
    custom = get_env("custom_model")
    if custom:
        return custom
    if feature_model_key:
        feat = get_env(feature_model_key)
        if feat:
            return feat
    return get_env("default_model", "gemini-2.5-flash")


def get_safety_settings():
    threshold = get_env("safety_threshold", "BLOCK_MEDIUM_AND_ABOVE")
    categories = [
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
    ]
    return [
        types.SafetySetting(category=cat, threshold=threshold)
        for cat in categories
    ]


def get_client():
    api_key = get_env("api_key")
    if not api_key:
        print("Error: Gemini API key not configured.", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)


def generate(prompt, system_instruction=None, feature_model_key=None):
    """Single-shot generation, returns full text."""
    client = get_client()
    model = resolve_model(feature_model_key)
    config = types.GenerateContentConfig(
        safety_settings=get_safety_settings(),
    )
    if system_instruction:
        config.system_instruction = system_instruction
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""


def generate_stream(prompt, system_instruction=None, feature_model_key=None):
    """Streaming single-shot generation, yields text chunks."""
    client = get_client()
    model = resolve_model(feature_model_key)
    config = types.GenerateContentConfig(
        safety_settings=get_safety_settings(),
    )
    if system_instruction:
        config.system_instruction = system_instruction
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    ):
        if chunk.text:
            yield chunk.text


def chat_generate_stream(history, message, system_instruction=None, feature_model_key=None):
    """Chat generation with history, yields text chunks.

    history: list of {"role": "user"/"model", "parts": [{"text": "..."}]}
    """
    client = get_client()
    model = resolve_model(feature_model_key)
    config = types.GenerateContentConfig(
        safety_settings=get_safety_settings(),
    )
    if system_instruction:
        config.system_instruction = system_instruction

    contents = []
    for turn in history:
        contents.append(
            types.Content(
                role=turn["role"],
                parts=[types.Part(text=p["text"]) for p in turn["parts"]],
            )
        )
    contents.append(
        types.Content(role="user", parts=[types.Part(text=message)])
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if chunk.text:
            yield chunk.text
