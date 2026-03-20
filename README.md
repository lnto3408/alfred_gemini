# Gemini Workflow for Alfred

An Alfred workflow powered by the Google Gemini API. Provides translation, AI chat, and text manipulation features.

> **Note:** This workflow requires [Alfred Powerpack](https://www.alfredapp.com/powerpack/) (paid license). Workflows are a Powerpack-exclusive feature and will not work with the free version of Alfred.

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

## Requirements

- macOS
- [Alfred 5](https://www.alfredapp.com/) with [Powerpack](https://www.alfredapp.com/powerpack/)
- Python 3.9+ (pre-installed on macOS)
- Google Gemini API Key (free)

## Installation

### Step 1: Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the generated key

### Step 2: Download and Install

**Option A: From Releases (Recommended)**
1. Go to the [Releases](https://github.com/lnto3408/alfred_gemini/releases) page
2. Download the latest `.alfredworkflow` file
3. Double-click the downloaded file — Alfred will open and prompt you to import

**Option B: From Source**
1. Clone or download this repository
2. Open Alfred Preferences → Workflows
3. Drag the entire project folder into the workflow list

### Step 3: Configure

1. After importing, Alfred will show the workflow configuration screen
2. Paste your **Gemini API Key** into the API Key field
3. Adjust other settings if needed (model, language, etc.)
4. Click **Save**

> On the first run, the workflow will automatically install the required Python package (`google-genai`). This takes a few seconds and only happens once.

## Usage Guide

### Translation

**Using keyword:**
1. Open Alfred (`⌘ + Space`)
2. Type `gt hello world` and press `Enter`
3. The translation result appears in a text view
4. Press `⌘ + C` to copy the result

**Using Universal Action:**
1. Select text anywhere on your Mac
2. Open Alfred Universal Actions (`⌘ + C` then `⌘ + Space`, or your configured hotkey)
3. Choose **Translate (Gemini)**
4. The translation result appears in a text view

### AI Chat

**Start a new conversation:**
1. Open Alfred and type `gg your question here`
2. Press `Enter`
3. The response streams in real-time in a text view
4. Type a follow-up message in the input field at the bottom to continue the conversation

**Resume a previous conversation:**
1. Open Alfred and type `gh`
2. Browse your conversation history
3. Select a conversation to continue
4. Type your follow-up message and press `Enter`

**Delete a conversation:**
1. Type `gh` to open chat history
2. Highlight the conversation you want to delete
3. Press `⌘ + Enter` to delete

### Text Actions

1. Select any text in any application
2. Trigger Alfred Universal Actions (default: select text → press your Universal Action hotkey)
3. Scroll down to find the Gemini actions (they all end with "(Gemini)")
4. Select an action (e.g., "Explain (Gemini)", "Summarize (Gemini)")
5. The result appears in a text view

> **Tip:** If you don't have a Universal Action hotkey set up, go to Alfred Preferences → Features → Universal Actions to configure one.

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

### Model Priority

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

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Dependency installation failed" | Ensure Python 3 is installed: run `python3 --version` in Terminal |
| No response from Gemini | Check your API key is correct in workflow settings |
| First run is slow | Normal — the SDK is being installed. Subsequent runs will be fast |
| Universal Actions not showing | Make sure you have a Universal Action hotkey configured in Alfred Preferences |

## License

[MIT](LICENSE)
