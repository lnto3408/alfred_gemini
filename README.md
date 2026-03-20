# Gemini Workflow for Alfred

An Alfred workflow powered by the Google Gemini API. Provides translation, AI chat, and text manipulation features.

> **Note:** This workflow requires [Alfred Powerpack](https://www.alfredapp.com/powerpack/) (paid license). Workflows are a Powerpack-exclusive feature and will not work with the free version of Alfred.

## Download

Two versions available on the [Releases](https://github.com/lnto3408/alfred_gemini/releases) page:

| Version | Dependencies | Description |
|---------|-------------|-------------|
| **Gemini-Workflow-Bash.alfredworkflow** (Recommended) | None | Uses macOS built-in JXA + curl |
| Gemini-Workflow.alfredworkflow | Python 3.9+ | Uses google-genai SDK |

## Features

### Translation (`gt`)
- Type `gt {text}` or select text and use Universal Action "Translate"
- `gt` with no text auto-reads from clipboard
- Auto-detects language: Korean input → English, other languages → Korean
- Configurable target language (Korean, Japanese, Chinese, Spanish, French, German, Portuguese, Vietnamese)

### AI Chat (`gg`)
- `gg {message}` to start a conversation with Gemini
- Streaming response (real-time text output)
- Session persistence for follow-up messages

### Chat History (`gh`)
- Browse previous conversations
- Select to resume a conversation

### Text Actions (Universal Actions + Hotkeys)
Select text and run via Universal Action or a custom hotkey:

| Action | Description |
|--------|-------------|
| Explain | Explain the selected text with structured breakdown |
| Fix Spelling & Grammar | Correct errors while preserving tone and style |
| Make Shorter | Reduce text by 40-60% keeping key information |
| Make Longer | Expand text by 50-100% with meaningful details |
| Tone: Friendly | Rewrite in a warm, approachable tone |
| Tone: Professional | Rewrite in a formal, polished tone |
| Add Code Comments | Add inline comments and docstrings to code |
| Find Synonym | Find 3-5 synonyms per word with part of speech |
| Summarize | TL;DR + bullet point summary |

## Requirements

- macOS
- [Alfred 5](https://www.alfredapp.com/) with [Powerpack](https://www.alfredapp.com/powerpack/)
- Google Gemini API Key (free)

## Installation

### Step 1: Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the generated key

### Step 2: Download and Install

1. Go to the [Releases](https://github.com/lnto3408/alfred_gemini/releases) page
2. Download **Gemini-Workflow-Bash.alfredworkflow** (recommended)
3. Double-click the downloaded file — Alfred will open and prompt you to import

### Step 3: Configure

1. After importing, Alfred will show the workflow configuration screen
2. Paste your **Gemini API Key** into the API Key field
3. Adjust other settings if needed (model, language, etc.)
4. Click **Save**

## Usage Guide

### Translation

**Using keyword:**
1. Open Alfred (`⌘ + Space`)
2. Type `gt hello world` and press `Enter`
3. The translation result appears in a text view

**Using clipboard (no typing):**
1. Copy text you want to translate (`⌘ + C`)
2. Open Alfred and type `gt` (no text after it)
3. It shows the clipboard text — press `Enter` to translate

**Using hotkey (fastest):**
1. Select text anywhere on your Mac
2. Press your configured translation hotkey
3. Translation appears instantly

**Using Universal Action:**
1. Select text anywhere on your Mac
2. Open Alfred Universal Actions (your configured hotkey)
3. Choose **Translate (Gemini)**

### AI Chat

**Start a new conversation:**
1. Open Alfred and type `gg your question here`
2. Press `Enter`
3. The response streams in real-time in a text view
4. Type a follow-up message in the input field at the bottom

**Resume a previous conversation:**
1. Open Alfred and type `gh`
2. Select a conversation to continue
3. Type your follow-up message

**Start fresh:**
1. Type `gh` → select **Start New Chat**

### Text Actions

1. Select any text in any application
2. Trigger via Universal Action or your configured hotkey
3. The result appears in a text view

> **Tip:** If you don't have a Universal Action hotkey set up, go to Alfred Preferences → Features → Universal Actions to configure one.

## Configuration

### General Settings

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

### Model Priority

`custom_model` > feature-specific model (`translation_model`, `chat_model`) > `default_model`

## Customizing Prompts

Every action's system prompt can be customized in the workflow settings. This lets you change how each action behaves without editing any code.

### How to Edit Prompts

1. Open **Alfred Preferences** (click Alfred menu bar icon → Preferences, or press `⌘,`)
2. Click **Workflows** in the left sidebar
3. Select **Gemini Workflow (Bash)** from the workflow list
4. Click the **`[≡]`** icon (Configure Workflow) in the **top-right corner** of the workflow editor — this opens the settings panel
5. Scroll down past the general settings (API Key, Model, etc.) — the **prompt text areas** are at the bottom
6. Edit any prompt to your needs
7. Click **Save**

> **Where exactly?** The prompt settings are in the same place where you entered your API Key. Just scroll down — they are large text areas below the general settings like Model, Safety Filter, and Translation Language.

### Available Prompts

| Setting | What it controls |
|---------|-----------------|
| Translation Prompt | How translation works (language detection rules, formatting) |
| Chat System Prompt | AI chat personality and response style |
| Explain Prompt | How text explanations are structured |
| Fix Grammar Prompt | Grammar correction behavior |
| Make Shorter Prompt | Text shortening rules and target reduction |
| Make Longer Prompt | Text expansion style and target increase |
| Friendly Tone Prompt | Friendly tone rewriting rules |
| Professional Tone Prompt | Professional tone rewriting rules |
| Add Comments Prompt | Code commenting style and format |
| Find Synonym Prompt | Synonym output format and rules |
| Summarize Prompt | Summary structure and format |

### Prompt Writing Tips

- Be specific about what format you want the output in
- Use bullet points in your prompt — each point becomes a rule the AI follows
- Include "Output ONLY the result" if you don't want explanations
- Add "Respond in the same language as the input" for multilingual support
- Test with a short text first after changing a prompt

### Example: Custom Explain Prompt

Default:
```
You are an expert explainer. When given text, provide a clear and structured explanation.
- Identify the core concept or topic first.
- Break down complex ideas into digestible parts.
...
```

Custom (e.g., for a 5-year-old):
```
You are a friendly teacher explaining things to a young child.
- Use very simple words and short sentences.
- Give fun, relatable examples.
- Avoid jargon completely.
- Respond in the same language as the input text.
```

### Example: Custom Translation Prompt

Default behavior translates Korean → English and everything else → Korean. You can change this:

```
You are a professional translator.
1. Always translate to Japanese.
2. Output ONLY the translated text.
3. Preserve formatting.
```

## Customizing Keywords

1. Open **Alfred Preferences** → **Workflows** → **Gemini Workflow**
2. Double-click on the **Script Filter** node you want to change (the leftmost block in each row)
3. Edit the **Keyword** field to your preferred trigger
4. Click **Save**

| Keyword | Feature |
|---------|---------|
| `gt` | Translation |
| `gg` | AI Chat |
| `gh` | Chat History |

## Setting Up Hotkeys

Each text action has a hotkey trigger that you can configure:

1. Open **Alfred Preferences** → **Workflows** → **Gemini Workflow (Bash)**
2. Find the **Hotkey** nodes (blank blocks on the left side)
3. Double-click a Hotkey node
4. Press your desired key combination (e.g., `⌘⇧T` for Translate)
5. Make sure **Argument** is set to **Selection in macOS**
6. Click **Save**

After setup: select text anywhere → press hotkey → result appears instantly.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No response from Gemini | Check your API key is correct in workflow settings |
| "Error: API key not valid" | Regenerate your API key at [Google AI Studio](https://aistudio.google.com/apikey) |
| Universal Actions not showing | Configure a Universal Action hotkey in Alfred Preferences → Features → Universal Actions |
| Text View shows raw JSON | Make sure you're using the Bash version (v1.1.0+) |
| Hotkey not working | Double-click the Hotkey node and verify **Argument** is set to **Selection in macOS** |

## License

[MIT](LICENSE)
