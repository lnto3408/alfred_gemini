# Gemini Workflow for Alfred

An Alfred workflow powered by the Google Gemini API. Provides translation, AI chat, and text manipulation features.

## Features

### Translation (`gt`)
- Type `gt {text}` or select text and use Universal Action "Translate"
- Auto-detects language: Korean input → English, other languages → Korean
- Configurable target language (Korean, Japanese, Chinese, English, German, French, Spanish, Portuguese, Vietnamese, Thai)

### AI Chat (`gg`)
- `gg {message}` to start a conversation with Gemini
- Streaming response (real-time text output)
- Session persistence for follow-up messages

### Chat History (`gh`)
- Browse previous conversations
- Select to resume a conversation
- `⌘ + Enter` to delete a conversation

### Text Actions (Universal Actions)
Select text and run via Universal Action:

| Action | Description |
|--------|-------------|
| Explain | Explain the selected text |
| Fix Spelling & Grammar | Correct spelling and grammar |
| Make Shorter | Condense the text |
| Make Longer | Expand the text |
| Tone: Friendly | Rewrite in a friendly tone |
| Tone: Professional | Rewrite in a professional tone |
| Add Code Comments | Add comments to code |
| Find Synonym | Find synonyms |
| Summarize | Summarize the text |

## Installation

### Requirements
- Alfred 5 (Powerpack)
- Python 3.9+
- Google Gemini API Key (get one from [Google AI Studio](https://aistudio.google.com/apikey))

### Setup
1. Download the `.alfredworkflow` file from [Releases](https://github.com/lnto3408/alfred_gemini/releases)
2. Double-click to install in Alfred
3. Enter your **Gemini API Key** in the workflow settings

> The `google-genai` SDK is automatically installed on first run (takes a few seconds).

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `api_key` | (required) | Gemini API Key |
| `default_model` | `gemini-2.5-flash` | Default model |
| `custom_model` | - | Custom model ID (overrides default model) |
| `translation_model` | - | Model for translation only |
| `chat_model` | - | Model for chat only |
| `safety_threshold` | `BLOCK_MEDIUM_AND_ABOVE` | Safety filter level |
| `translation_default_lang` | `ko` | Default target language for translation |
| `max_history_turns` | `20` | Max conversation turns per session |
| `session_ttl_days` | `7` | Auto-delete sessions older than this |

## Model Priority

`custom_model` > feature-specific model (`translation_model`, `chat_model`) > `default_model`

## Customizing Keywords

You can change the trigger keywords to your preference:

1. Open **Alfred Preferences** → **Workflows** → **Gemini Workflow**
2. Double-click on the **Script Filter** node you want to change (the leftmost block in each row)
3. Edit the **Keyword** field to your preferred trigger
4. Click **Save**

Default keywords:

| Keyword | Feature |
|---------|---------|
| `gt` | Translation |
| `gg` | AI Chat |
| `gh` | Chat History |

## License

[MIT](LICENSE)
