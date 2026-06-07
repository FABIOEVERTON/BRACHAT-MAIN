# Design & Creative
## 19 skills
---

## audio-transcriber
*Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration*

Tags: [audio, transcription, whisper, meeting-minutes, speech-to-text]
Risk: safe

## Purpose

This skill automates audio-to-text transcription with professional Markdown output, extracting rich technical metadata (speakers, timestamps, language, file size, duration) and generating structured meeting minutes and executive summaries. It uses Faster-Whisper or Whisper with zero configuration, working universally across projects without hardcoded paths or API keys.

Inspired by tools like Plaud, this skill transforms raw audio recordings into actionable documentation, making it ideal for meetings, interviews, lectures, and content analysis.

## When to Use
Invoke this skill when:

- User needs to transcribe audio/video files to text
- User wants meeting minutes automatically generated from recordings
- User requires speaker identification (diarization) in conversations
- User needs subtitles/captions (SRT, VTT formats)
- User wants executive summaries of long audio content
- User asks variations of "transcribe this audio", "convert audio to text", "generate meeting notes from recording"
- User has audio files in common formats (MP3, WAV, M4A, OGG, FLAC, WEBM)

## Workflow

### Step 0: Discovery (Auto-detect Transcription Tools)

**Objective:** Identify available transcription engines without user configuration.

**Actions:**

Run detection commands to find installed tools:

```bash
# Check for Faster-Whisper (preferred - 4-5x faster)
if python3 -c "import faster_whisper" 2>/dev/null; then
    TRANSCRIBER="faster-whisper"
    echo "✅ Faster-Whisper detected (optimized)"
# Fallback to original Whisper
elif python3 -c "import whisper" 2>/dev/null; then
    TRANSCRIBER="whisper"
    echo "✅ OpenAI Whisper detected"
else
    TRANSCRIBER="none"
    echo "⚠️  No transcription tool found"
fi

# Check for ffmpeg (audio format conversion)
if command -v ffmpeg &>/dev/null; then
    echo "✅ ffmpeg available (format conversion enabled)"
else
    echo "ℹ️  ffmpeg not found (limited format support)"
fi
```

**If no transcriber found:**

Offer automatic installation using the provided script:

```bash
echo "⚠️  No transcription tool found"
echo ""
echo "🔧 Auto-install dependencies? (Recommended)"
read -p "Run installation script? [Y/n]: " AUTO_INSTALL

if [[ ! "$AUTO_INSTALL" =~ ^[Nn] ]]; then
    # Get skill directory (works for both repo and symlinked installations)
    SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Run installation script
    if [[ -f "$SKILL_DIR/scripts/install-requirements.sh" ]]; then
        bash "$SKILL_DIR/scripts/install-requirements.sh"
    else
        echo "❌ Installation script not found"
        echo ""
        echo "📦 Manual installation:"
        echo "  pip install faster-whisper  # Recommended"
        echo "  pip install openai-whisper  # Alternative"
        echo "  brew install ffmpeg         # Optional (macOS)"
        exit 1
    fi
    
    # Verify installation succeeded
    if python3 -c "import faster_whisper" 2>/dev/null || python3 -c "import whisper" 2>/dev/null; then
        echo "✅ Installation successful! Proceeding with transcription..."
    else
        echo "❌ Installation failed. Please install manually."
        exit 1
    fi
else
    echo ""
    echo "📦 Manual installation required:"
    echo ""
    echo "Recommended (fastest):"
    echo "  pip install faster-whisper"
    echo ""
    echo "Alternative (original):"
    echo "  pip install openai-whisper"
    echo ""
    echo "Optional (format conversion):"
    echo "  brew install ffmpeg  # macOS"
    echo "  apt install ffmpeg   # Linux"
    echo ""
    exit 1
fi
```

This ensures users can install dependencies with one confirmation, or opt for manual installation if preferred.

**If transcriber found:**

Proceed to Step 0b (CLI Detection).


### Step 1: Validate Audio File

**Objective:** Verify file exists, check format, and extract metadata.

**Actions:**

1. **Accept file path or URL** from user:
   - Local file: `meeting.mp3`
   - URL: `https://example.com/audio.mp3` (download to temp directory)

2. **Verify file exists:**

```bash
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "❌ File not found: $AUDIO_FILE"
    exit 1
fi
```

3. **Extract metadata** using ffprobe or file utilities:

```bash
# Get file size
FILE_SIZE=$(du -h "$AUDIO_FILE" | cut -f1)

# Get duration and format using ffprobe
DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)
FORMAT=$(ffprobe -v error -select_streams a:0 -show_entries \
    stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)

# Convert duration to HH:MM:SS
DURATION_HMS=$(date -u -r "$DURATION" +%H:%M:%S 2>/dev/null || echo "Unknown")
```

4. **Check file size** (warn if large for cloud APIs):

```bash
SIZE_MB=$(du -m "$AUDIO_FILE" | cut -f1)
if [[ $SIZE_MB -gt 25 ]]; then
    echo "⚠️  Large file ($FILE_SIZE) - processing may take several minutes"
fi
```

5. **Validate format** (supported: MP3, WAV, M4A, OGG, FLAC, WEBM):

```bash
EXTENSION="${AUDIO_FILE##*.}"
SUPPORTED_FORMATS=("mp3" "wav" "m4a" "ogg" "flac" "webm" "mp4")

if [[ ! " ${SUPPORTED_FORMATS[@]} " =~ " ${EXTENSION,,} " ]]; then
    echo "⚠️  Unsupported format: $EXTENSION"
    if command -v ffmpeg &>/dev/null; then
        echo "🔄 Converting to WAV..."
        ffmpeg -i "$AUDIO_FILE" -ar 16000 "${AUDIO_FILE%.*}.wav" -y
        AUDIO_FILE="${AUDIO_FILE%.*}.wav"
    else
        echo "❌ Install ffmpeg to convert formats: brew install ffmpeg"
        exit 1
    fi
fi
```


### Step 3: Generate Markdown Output

**Objective:** Create structured Markdown with metadata, transcription, meeting minutes, and summary.

**Output Template:**

```markdown
# Audio Transcription Report

## 📊 Metadata

| Field | Value |
|-------|-------|
| **File Name** | {filename} |
| **File Size** | {file_size} |
| **Duration** | {duration_hms} |
| **Language** | {language} ({language_code}) |
| **Processed Date** | {process_date} |
| **Speakers Identified** | {num_speakers} |
| **Transcription Engine** | {engine} (model: {model}) |


## 📋 Meeting Minutes

### Participants
- {speaker_1}
- {speaker_2}
- ...

### Topics Discussed
1. **{topic_1}** ({timestamp})
   - {key_point_1}
   - {key_point_2}

2. **{topic_2}** ({timestamp})
   - {key_point_1}

### Decisions Made
- ✅ {decision_1}
- ✅ {decision_2}

### Action Items
- [ ] **{action_1}** - Assigned to: {speaker} - Due: {date_if_mentioned}
- [ ] **{action_2}** - Assigned to: {speaker}


*Generated by audio-transcriber skill v1.0.0*  
*Transcription engine: {engine} | Processing time: {elapsed_time}s*
```

**Implementation:**

Use Python or bash with AI model (Claude/GPT) for intelligent summarization:

```python
def generate_meeting_minutes(segments):
    """Extract topics, decisions, action items from transcription."""
    
    # Group segments by topic (simple clustering by timestamps)
    topics = cluster_by_topic(segments)
    
    # Identify action items (keywords: "should", "will", "need to", "action")
    action_items = extract_action_items(segments)
    
    # Identify decisions (keywords: "decided", "agreed", "approved")
    decisions = extract_decisions(segments)
    
    return {
        "topics": topics,
        "decisions": decisions,
        "action_items": action_items
    }

def generate_summary(segments, max_paragraphs=5):
    """Create executive summary using AI (Claude/GPT via API or local model)."""
    
    full_text = " ".join([s["text"] for s in segments])
    
    # Use Chain of Density approach (from prompt-engineer frameworks)
    summary_prompt = f"""
    Summarize the following transcription in {max_paragraphs} concise paragraphs.
    Focus on key topics, decisions, and action items.
    
    Transcription:
    {full_text}
    """
    
    # Call AI model (placeholder - user can integrate Claude API or use local model)
    summary = call_ai_model(summary_prompt)
    
    return summary
```

**Output file naming:**

```bash
# v1.1.0: Use timestamp para evitar sobrescrever
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TRANSCRIPT_FILE="transcript-${TIMESTAMP}.md"
ATA_FILE="ata-${TIMESTAMP}.md"

echo "$TRANSCRIPT_CONTENT" > "$TRANSCRIPT_FILE"
echo "✅ Transcript salvo: $TRANSCRIPT_FILE"

if [[ -n "$ATA_CONTENT" ]]; then
    echo "$ATA_CONTENT" > "$ATA_FILE"
    echo "✅ Ata salva: $ATA_FILE"
fi
```


#### **SCENARIO A: User Provided Custom Prompt**

**Workflow:**

1. **Display user's prompt:**
   ```
   📝 Prompt fornecido pelo usuário:
   ┌──────────────────────────────────┐
   │ [User's prompt preview]          │
   └──────────────────────────────────┘
   ```

2. **Automatically improve with prompt-engineer (if available):**
   ```bash
   🔧 Melhorando prompt com prompt-engineer...
   [Invokes: gh copilot -p "melhore este prompt: {user_prompt}"]
   ```

3. **Show both versions:**
   ```
   ✨ Versão melhorada:
   ┌──────────────────────────────────┐
   │ Role: Você é um documentador...  │
   │ Instructions: Transforme...      │
   │ Steps: 1) ... 2) ...             │
   │ End Goal: ...                    │
   └──────────────────────────────────┘

   📝 Versão original:
   ┌──────────────────────────────────┐
   │ [User's original prompt]         │
   └──────────────────────────────────┘
   ```

4. **Ask which to use:**
   ```bash
   💡 Usar versão melhorada? [s/n] (default: s):
   ```

5. **Process with selected prompt:**
   - If "s": use improved
   - If "n": use original


#### **LLM Processing (Both Scenarios)**

Once prompt is finalized:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

def process_with_llm(transcript, prompt, cli_tool='claude'):
    full_prompt = f"{prompt}\n\n---\n\nTranscrição:\n\n{transcript}"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(
            description=f"🤖 Processando com {cli_tool}...",
            total=None
        )
        
        if cli_tool == 'claude':
            result = subprocess.run(
                ['claude', '-'],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
        elif cli_tool == 'gh-copilot':
            result = subprocess.run(
                ['gh', 'copilot', 'suggest', '-t', 'shell', full_prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None
```

**Progress output:**
```
🤖 Processando com claude... ⠋
[After completion:]
✅ Ata gerada com sucesso!
```


#### **Final Output**

**Success (both files):**
```bash
💾 Salvando arquivos...

✅ Arquivos criados:
  - transcript-20260203-023045.md  (transcript puro)
  - ata-20260203-023045.md         (processado com LLM)

🧹 Removidos arquivos temporários: metadata.json, transcription.json

✅ Concluído! Tempo total: 3m 45s
```

**Transcript only (user declined LLM):**
```bash
💾 Salvando arquivos...

✅ Arquivo criado:
  - transcript-20260203-023045.md

ℹ️  Ata não gerada (processamento LLM recusado pelo usuário)

🧹 Removidos arquivos temporários: metadata.json, transcription.json

✅ Concluído!
```


### Step 5: Display Results Summary

**Objective:** Show completion status and next steps.

**Output:**

```bash
echo ""
echo "✅ Transcription Complete!"
echo ""
echo "📊 Results:"
echo "  File: $OUTPUT_FILE"
echo "  Language: $LANGUAGE"
echo "  Duration: $DURATION_HMS"
echo "  Speakers: $NUM_SPEAKERS"
echo "  Words: $WORD_COUNT"
echo "  Processing time: ${ELAPSED_TIME}s"
echo ""
echo "📝 Generated:"
echo "  - $OUTPUT_FILE (Markdown report)"
[if alternative formats:]
echo "  - ${OUTPUT_FILE%.*}.srt (Subtitles)"
echo "  - ${OUTPUT_FILE%.*}.json (Structured data)"
echo ""
echo "🎯 Next steps:"
echo "  1. Review meeting minutes and action items"
echo "  2. Share report with participants"
echo "  3. Track action items to completion"
```


## Example Usage

### **Example 1: Basic Transcription**

**User Input:**
```bash
copilot> transcribe audio to markdown: meeting-2026-02-02.mp3
```

**Skill Output:**

```bash
✅ Faster-Whisper detected (optimized)
✅ ffmpeg available (format conversion enabled)

📂 File: meeting-2026-02-02.mp3
📊 Size: 12.3 MB
⏱️  Duration: 00:45:32

🎙️  Processing...
[████████████████████] 100%

✅ Language detected: Portuguese (pt-BR)
👥 Speakers identified: 4
📝 Generating Markdown output...

✅ Transcription Complete!

📊 Results:
  File: meeting-2026-02-02.md
  Language: pt-BR
  Duration: 00:45:32
  Speakers: 4
  Words: 6,842
  Processing time: 127s

📝 Generated:
  - meeting-2026-02-02.md (Markdown report)

🎯 Next steps:
  1. Review meeting minutes and action items
  2. Share report with participants
  3. Track action items to completion
```


### **Example 3: Batch Processing**

**User Input:**
```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**Skill Output:**

```bash
📦 Batch mode: 5 files found
  1. team-standup.mp3
  2. client-call.mp3
  3. brainstorm-session.mp3
  4. product-demo.mp3
  5. retrospective.mp3

🎙️  Processing batch...

[1/5] team-standup.mp3 ✅ (2m 34s)
[2/5] client-call.mp3 ✅ (15m 12s)
[3/5] brainstorm-session.mp3 ✅ (8m 47s)
[4/5] product-demo.mp3 ✅ (22m 03s)
[5/5] retrospective.mp3 ✅ (11m 28s)

✅ Batch Complete!
📝 Generated 5 Markdown reports
⏱️  Total processing time: 6m 15s
```


### **Example 5: Large File Warning**

**User Input:**
```bash
copilot> transcribe audio to markdown: conference-keynote.mp3
```

**Skill Output:**

```bash
✅ Faster-Whisper detected (optimized)

📂 File: conference-keynote.mp3
📊 Size: 87.2 MB
⏱️  Duration: 02:15:47
⚠️  Large file (87.2 MB) - processing may take several minutes

Continue? [Y/n]:
```

**User:** `Y`

```bash
🎙️  Processing... (this may take 10-15 minutes)
[████░░░░░░░░░░░░░░░░] 20% - Estimated time remaining: 12m
```


This skill is **platform-agnostic** and works in any terminal context where GitHub Copilot CLI is available. It does not depend on specific project configurations or external APIs, following the zero-configuration philosophy.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## bulletmind
*Convert input into clean, structured, hierarchical bullet points for summarization, note-taking, and structured thinking.*

Risk: safe

# Bulletmind

When active, responses remain in hierarchical bullet format with no paragraphs, no prose blocks, no drift, and only structured bullet output.

---

## When to Use This Skill

Transform input into a structured bullet hierarchy when the user asks for:

- Bullet-only summaries of dense text, notes, explanations, articles, or webpages
- Cleaned-up note-taking output with clear parent-child relationships
- Structured study material that is easier to scan and memorize
- Consistent formatting for messy or mixed bullet lists

Use this skill to enforce:

- No paragraphs or long prose
- Only bullets with clean indentation

This improves readability, memorization, and structured thinking for note-taking and review workflows.

---

## Mode

Default mode: **full**. Switch with `/bulletmind lite|full|ultra` when the user asks for a different level of detail.

---

## Intensity

| Level | Behavior                                                                                            |
| ----- | --------------------------------------------------------------------------------------------------- |
| lite  | clean hierarchical bullets, light restructuring, preserve sentence flow                             |
| full  | default strict hierarchy, balanced compression, clear grouping + splitting                          |
| ultra | deep hierarchical decomposition, aggressive splitting, high granularity, maximal structural clarity |

---

## Bullet Structure

Use consistent indentation:
- Top-level idea
  - Sub-point
    - Detail
  - Sub-point
- Next top-level idea
  - Sub-point

---

## Rules

- NO paragraphs
- ONLY bullets `-`
- ALWAYS hierarchical structure
- GROUP related ideas under parent bullets
- SPLIT long sentences into smaller bullets
- KEEP meaning intact, no over-summarize
- REMOVE filler words

---

## Formatting

- Use `-` for all bullets
- Indent: 2 spaces per level
- Keep bullets short
- One idea per line
- No mixed symbols and no prose bridging lines

---

## Transformation Logic

- Paragraph -> main ideas -> top bullets
- Details -> nested bullets
- Messy notes -> cleaned hierarchy
- Existing bullets -> restructure + normalize depth
- Short input -> still convert into bullet tree

---

## Compression Strategy

- Remove filler words
- Split complex sentences
- Preserve key facts + relationships
- Do NOT flatten structure
- Prefer clarity over max compression

---

## When Not to Use This Skill

- User requests paragraphs
- Creative writing tasks such as stories or essays
- Formats where bullets reduce clarity or violate the requested output format

---

## Output Rule

When the skill is active, output:

- Structured bullet hierarchy
- No commentary or explanation

## Limitations

- Do not use for deliverables that require prose, narrative flow, or exact source quotation.
- Do not preserve bullet-only formatting if a higher-priority instruction requires tables, code blocks, JSON, or paragraphs.
- Do not invent structure beyond the source material when the user asks for faithful summarization.

### Examples

- Refer to `EXAMPLES.md` for output templates.

---

## Important Notes

- Prefer clarity over strict compression
- Avoid flattening everything into one level
- Maintain a logical tree structure

---

## humanize-chinese
*Detect and rewrite AI-like Chinese text with a practical workflow for scoring, humanization, academic AIGC reduction, and style conversion. Use when the user asks to 去AI味, 降AIGC, 去除AI痕迹, 论文降重, 知网检测, 维普检测, humanize chinese, detect AI text, or make Chinese text sound more natural.*

Risk: safe

# Humanize Chinese

Use this skill when you need to detect AI-like Chinese writing, rewrite it to feel less synthetic, reduce AIGC signals in academic prose, or convert the text into a more specific Chinese writing style.

## When to Use
- Use when the user says `去AI味`, `降AIGC`, `去除AI痕迹`, `让文字更自然`, `改成人话`, or `降低AI率`
- Use when the user wants a Chinese text checked for AI-writing patterns or suspicious phrasing
- Use when the user wants academic-paper-specific AIGC reduction for CNKI, VIP, or Wanfang-style checks
- Use when the user wants Chinese text rewritten into a different style such as `zhihu`, `xiaohongshu`, `wechat`, `weibo`, `literary`, or `academic`

## Core Workflow

### 1. Detect Before Rewriting

Start by identifying the most obvious AI markers instead of rewriting blindly:

- rigid `first/second/finally` structures
- mechanical connectors such as `综上所述`, `值得注意的是`, `由此可见`
- abstract grandiose wording with low information density
- repeated sentence rhythm and paragraph length
- academic prose that sounds too complete, too certain, or too template-driven

If the user provides a short sample, call out the suspicious phrases directly before rewriting.

### 2. Rewrite in the Smallest Useful Pass

Prefer targeted rewrites over total regeneration:

- remove formulaic connectors rather than paraphrasing every sentence
- vary sentence length and paragraph rhythm
- replace repeated verbs and noun phrases
- swap abstract summaries for concrete observations where possible
- keep the original claims, facts, citations, and terminology intact

### 3. Validate the Result

After rewriting, verify that the text:

- still says the same thing
- sounds less templated
- uses more natural rhythm
- does not introduce factual drift
- stays in the correct register for the target audience

For academic text, preserve a scholarly tone. Do not over-casualize.

## Optional CLI Flow

If the user has a local clone of the source toolkit, these examples are useful:

```bash
python3 scripts/detect_cn.py text.txt -v
python3 scripts/compare_cn.py text.txt -a -o clean.txt
python3 scripts/academic_cn.py paper.txt -o clean.txt --compare
python3 scripts/style_cn.py text.txt --style xiaohongshu -o out.txt
```

Use this CLI sequence when available:

1. detect and inspect suspicious sentences
2. rewrite or compare
3. rerun detection on the cleaned file
4. optionally convert into a target style

## Manual Rewrite Playbook

If the scripts are unavailable, use this manual process.

### Common AI Markers

- numbered or mirrored structures that feel too symmetrical
- filler transitions that add no meaning
- repeated stock phrases
- overly even sentence length
- conclusions that sound final, polished, and risk-free

### Rewrite Moves

- delete weak transitions first
- collapse repetitive phrases into one stronger sentence
- split sentences at natural turns instead of forcing long balanced structures
- merge choppy sentences when they feel robotic
- replace generic abstractions with concrete wording
- introduce light variation in cadence so the prose does not march at a constant tempo

## Academic AIGC Reduction

For papers, reports, or theses:

- keep discipline-specific terminology unchanged
- replace AI-academic stock phrases with more grounded scholarly phrasing
- reduce absolute certainty with measured hedging where appropriate
- vary paragraph structure so each section does not read like the same template
- add limitations or uncertainty if the conclusion feels unnaturally complete

Examples of safer direction changes:

- `本文旨在` -> `本文尝试` or `本研究关注`
- `具有重要意义` -> `值得关注` or `有一定参考价值`
- `研究表明` -> `前人研究发现` or `已有文献显示`

Do not invent citations, evidence, or data.

## Style Conversion

Use style conversion only after the base text is readable and natural.

Supported style directions from the source workflow:

- `casual`
- `zhihu`
- `xiaohongshu`
- `wechat`
- `academic`
- `literary`
- `weibo`

When switching style, keep the user's meaning stable and change only tone, structure, and surface wording.

## Output Rules

- Show the main AI-like patterns you found
- Explain the rewrite strategy in 1-3 short bullets
- Return the rewritten Chinese text
- If helpful, include a short note on remaining weak spots

## Source

Adapted from the `voidborne-d/humanize-chinese` project and its CLI/script workflow for Chinese AI-text detection and rewriting.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## rayden-use
*Build and maintain Rayden UI components and screens in Figma via Figma MCP with full design token enforcement*

Tags: figma, design-system, ui, components, mcp, rayden, rayna-ui
Tools: mcp__claude_ai_Figma__use_figma, mcp__claude_ai_Figma__get_screenshot, mcp__claude_ai_Figma__whoami, Read
Risk: safe

# Rayden UI Design Skill

## Overview

Build and maintain Rayden UI components and screens directly in Figma using the Figma MCP. The skill enforces the Rayna UI design system — resolved design tokens, craft rules, anti-pattern detection, and visual validation — so every output is mechanically correct and visually premium. Supports three style modes (conservative, balanced, expressive) and includes a dedicated subagent for full-page screen composition.

## When to Use This Skill

- You need to build a new Rayden UI component with all its variants in Figma
- You're composing a full screen (dashboard, landing page, auth form, settings, data table) from Rayden patterns
- You want to audit an existing Figma file for design system compliance
- You need to add new variants to an existing Figma component
- You're syncing React component updates back to Figma

## How It Works

1. **Verifies environment** — Checks Figma MCP connection and write access via `whoami`
2. **Loads component data** — Reads Rayden component specs, anatomy, and tokens from the `@raydenui/ai` MCP server or installed package
3. **Loads craft rules** — Reads supporting files: resolved token values, craft rules, anti-patterns, and screen layout patterns
4. **Identifies task type** — Determines if building a single component, composing a screen, auditing, or adding variants
5. **Applies style mode** — Adjusts spacing, shadow, typography, and visual weight based on conservative/balanced/expressive mode
6. **Builds with helpers** — Generates Figma Plugin API code using mandatory helper functions (hexToRgb, loadFonts, applyShadow, applyBorder) with auto layout on every frame
7. **Visual validation** — Takes screenshots after each build stage and validates against 8 acceptance criteria (alignment, spacing, color accuracy, hierarchy, radius, shadow, primary action count)

## Examples

### Build a component with all variants

```
/rayden-use Button https://figma.com/file/abc123
```

**Use case:** You're starting a new design system file and need the Button component with all variants (primary, secondary, grey, destructive) in solid and outlined appearances across SM and LG sizes.

### Design a SaaS dashboard

```
/rayden-use dashboard-screen balanced https://figma.com/file/abc123
```

**Use case:** You're designing an analytics dashboard and need a sidebar layout with KPI cards, a data table, and an activity feed — all using consistent Rayden tokens and spacing.

### Build a marketing landing page

```
/rayden-compose landing expressive https://figma.com/file/abc123
```

**Use case:** You need a high-impact landing page with bolder typography, stronger shadows, and asymmetric layouts that avoid the generic "AI-generated" look.

### Audit an existing design for compliance

```
/rayden-use audit https://figma.com/file/abc123
```

**Use case:** You have an existing Figma file and want to check that all colors match Rayden tokens, spacing is on the 4px grid, and radius is concentric.

### Add variants to an existing component

```
/rayden-use add-variants Input https://figma.com/file/abc123
```

**Use case:** The Input component exists in your Figma file but is missing error and success states — the skill reads the existing structure and extends it.

## Best Practices

- Always provide a Figma file URL as the last argument
- Use `balanced` mode (default) for most use cases; `conservative` for dense admin UIs, `expressive` for marketing pages
- Let the skill take screenshots between build stages — this is how it validates output quality
- Install `@raydenui/ai` as an MCP server for the richest component data access
- Review the generated output in Figma after completion — the skill validates mechanically but human judgment on aesthetics is still valuable

## Security & Safety Notes

- This skill only reads local supporting files and calls the Figma MCP — no external network requests beyond Figma's API
- Requires Figma Dev or Full seat with write access to the target file
- Does not modify files outside of the target Figma document
- All design tokens are bundled in the skill's supporting files — no secrets or credentials involved

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| "Font not found" error | The skill falls back to Roboto if Inter is unavailable — ensure Inter is loaded in your Figma file for best results |
| Components don't combine as variants | All components must share the same parent frame before calling `combineAsVariants` |
| Colors look wrong | Verify you're using resolved token hex values from tokens.md, not approximations |
| Figma permission denied | Check that your Figma seat is Dev or Full (not Viewer) and the file isn't view-only |

## Related Skills

- `rayden-code` — Generate React code with Rayden UI components (included in the same package)
- `rayden-compose` — Dedicated subagent for composing full-page Figma screens (included in this skill package)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-a11y
*Audit a StyleSeed-based component or page for WCAG 2.2 AA issues and apply practical accessibility fixes where the code makes them safe.*

Tags: [ui, accessibility, wcag, audit, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Accessibility Audit

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill audits components and pages for accessibility issues with an emphasis on the Toss seed's mobile UI patterns. It combines WCAG 2.2 AA checks with practical code fixes for touch targets, focus states, contrast, labels, and reduced motion.

## When to Use
- Use when reviewing a page or component for accessibility regressions
- Use when a StyleSeed UI looks polished but has uncertain keyboard or contrast behavior
- Use when adding new interactive controls to a mobile-first screen
- Use when you want a prioritized list of issues and fixable items

## Audit Areas

### Perceivable

- text contrast
- non-text contrast for controls and graphics
- alt text for images
- labels for meaningful icons
- no information conveyed by color alone

### Operable

- touch targets at least 44x44px
- keyboard reachability for all interactive controls
- logical tab order
- visible focus indicators
- reduced-motion support for nonessential animation

### Understandable

- visible labels or `aria-label` on inputs
- error text associated with the correct field
- clear wording for errors and validation
- document language set appropriately

### Robust

- semantic HTML where possible
- correct use of ARIA when semantics alone are insufficient
- no faux buttons or links without the right roles and behavior

## Output

Return:
1. Issues found, grouped by severity
2. Safe autofixes that can be applied directly
3. Items that need manual review or product judgment
4. A short summary of the accessibility risk level

## Best Practices

- Fix semantics before layering on ARIA
- Use the design system tokens only if they still meet contrast requirements
- Treat touch target failures as real usability defects, not polish issues
- Prefer partial, verified fixes over speculative accessibility changes

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-a11y/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-component
*Generate a new UI component that follows StyleSeed Toss conventions for structure, tokens, accessibility, and component ergonomics.*

Tags: [ui, components, design-system, frontend, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Component

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill generates components that respect the Toss seed's design language instead of improvising ad hoc markup and styling. It emphasizes semantic tokens, predictable typing, reusable variants, and mobile-friendly accessibility defaults.

## When to Use
- Use when you need a new UI primitive or composed component inside a StyleSeed-based project
- Use when you want a component to match the existing Toss seed conventions
- Use when a component should be reusable, typed, and design-token driven
- Use when the AI might otherwise invent spacing, colors, or interaction patterns

## How It Works

### Step 1: Read the Local Design Context

Before generating code, inspect the seed's source of truth:
- `CLAUDE.md` for conventions
- `css/theme.css` for semantic tokens
- at least one representative component from `components/ui/`

If the user already has a better local example, follow the local codebase over a generic template.

### Step 2: Choose the Correct Home

Place the output where it belongs:
- `src/components/ui/` for primitives and low-level building blocks
- `src/components/patterns/` for composed sections or multi-part patterns

Do not create a new primitive if an existing one can be extended safely.

### Step 3: Follow the Structural Rules

Use these defaults unless the host project strongly disagrees:
- function declaration instead of a `const` component
- `React.ComponentProps<>` or equivalent native prop typing
- `className` passthrough support
- `cn()` or the project's standard class merger
- `data-slot` for component identification
- CVA or equivalent only when variants are genuinely needed

### Step 4: Use Semantic Tokens Only

Do not hardcode visual values if the design system has a token for them.

Preferred examples:
- `bg-card`
- `text-foreground`
- `text-muted-foreground`
- `border-border`
- `shadow-[var(--shadow-card)]`

### Step 5: Preserve StyleSeed Typography and Spacing

- Use the scale already defined by the seed
- Prefer multiples of 6px
- Use logical spacing utilities where supported
- Keep display and heading text tight, body text readable, captions restrained

### Step 6: Bake in Accessibility

- Touch targets should be at least 44x44px for interactive elements
- Keyboard focus must be visible
- Pass through `aria-*` attributes where appropriate
- Respect reduced-motion preferences for nonessential motion

## Output

Provide:
1. The generated component
2. The target path
3. Any required imports or dependencies
4. Notes on variants, tokens, or follow-up integration work

## Best Practices

- Compose from existing primitives before inventing new ones
- Keep the component API small and predictable
- Prefer semantic layout classes over arbitrary values
- Export named components unless the host project uses another standard consistently

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-component/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-page
*Scaffold a new mobile-first page using StyleSeed Toss layout patterns, section rhythm, and existing shell components.*

Tags: [ui, page-design, mobile, layout, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Page

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill scaffolds a complete page or screen using the Toss seed's mobile-first composition rules. It keeps page structure consistent by building on the existing shell, top bar, bottom navigation, and card rhythm instead of producing disconnected sections.

## When to Use
- Use when you need a new page in a Toss-seed app
- Use when you want a consistent page shell, spacing, and navigation structure
- Use when you are adding a new product flow and need a solid starting layout
- Use when you want to stay mobile-first even if the project later expands to larger breakpoints

## How It Works

### Step 1: Inspect the Existing Shell

Read the current page scaffolding patterns first, especially:
- page shell
- top bar
- bottom navigation
- representative pages using the same route family

### Step 2: Define the Page Purpose

Clarify:
- the page name
- the primary user question the screen answers
- the top one or two actions the user should take

Every screen should have one dominant purpose.

### Step 3: Use the Information Pyramid

Lay out the page from highest importance to lowest:
1. Hero or top summary
2. KPI or key actions
3. detail cards or supporting modules
4. lists, history, or secondary content

Avoid repeating the same section type mechanically from top to bottom.

### Step 4: Apply the Toss Layout Rules

Default layout choices:
- mobile viewport width around `max-w-[430px]`
- page background on `bg-background`
- horizontal padding around `px-6`
- section rhythm with `space-y-6`
- generous bottom padding if a bottom nav is present
- cards using semantic surface tokens, rounded corners, and light shadows

### Step 5: Compose Instead of Rebuilding

Use existing `ui/` and `patterns/` components wherever possible. New pages should primarily orchestrate existing building blocks, not recreate them.

### Step 6: Account for Real Device Constraints

- handle safe-area insets
- avoid horizontal overflow
- keep interactive clusters thumb-friendly
- ensure long content scrolls cleanly without clipping the bottom navigation

## Output

Return:
1. The page scaffold
2. The chosen section structure
3. Reused components and any newly required components
4. Empty, loading, and error states that the page will need next

## Best Practices

- Keep the first version structurally correct before adding decoration
- Use one strong hero instead of multiple competing highlights
- Preserve navigation consistency across sibling screens
- Prefer reusable section components when the page will likely repeat

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-page/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-pattern
*Generate reusable UI patterns such as card sections, grids, lists, forms, and chart wrappers using StyleSeed Toss primitives.*

Tags: [ui, patterns, design-system, reuse, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Pattern

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill builds reusable composed patterns from the seed's primitives. It is intended for sections like card lists, grids, form blocks, ranking lists, and chart wrappers that appear across multiple pages and need to look deliberate rather than ad hoc.

## When to Use
- Use when you need a reusable layout pattern rather than a one-off page section
- Use when a page repeats the same arrangement of cards, rows, filters, or data blocks
- Use when you want to build from existing StyleSeed primitives instead of copying markup
- Use when you want a pattern component with props for dynamic content

## How It Works

### Step 1: Identify the Pattern Type

Common pattern families include:
- card section
- two-column grid
- horizontal scroller
- list section
- form section
- stat grid
- data table
- detail card
- chart card
- filter bar
- action sheet

### Step 2: Read the Available Building Blocks

Inspect both:
- `components/ui/` for primitives
- `components/patterns/` for neighboring patterns that can be extended

The goal is composition, not duplication.

### Step 3: Apply StyleSeed Layout Rules

Keep the Toss seed defaults intact:
- card surfaces on semantic tokens
- rounded corners from the system scale
- shadow tokens instead of improvised shadow values
- consistent internal padding
- section wrappers that align with the page margin system

### Step 4: Make the Pattern Dynamic

Expose data through props instead of hardcoding content. If a pattern has multiple variants, keep the API explicit and small.

### Step 5: Keep the Pattern Reusable Across Pages

Avoid page-specific assumptions unless the user explicitly wants a one-off section. If the markup only works on one route, it probably belongs in a page component, not a shared pattern.

## Output

Provide:
1. The generated pattern component
2. The target location
3. Expected props and usage example
4. Notes on which existing primitives were reused

## Best Practices

- Start from the smallest existing building block that solves the problem
- Keep container, section, and item responsibilities separate
- Use tokens and spacing rules consistently
- Prefer extending a pattern over adding a near-duplicate sibling

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-pattern/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-review
*Review UI code for StyleSeed design-system compliance, accessibility, mobile ergonomics, spacing discipline, and implementation quality.*

Tags: [ui, review, design-system, accessibility, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Review

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill audits UI code against the Toss seed's conventions instead of reviewing it as generic frontend work. It focuses on design-token discipline, component ergonomics, accessibility, mobile readiness, typography, and spacing consistency.

## When to Use
- Use when a component or page should follow the StyleSeed Toss design language
- Use when reviewing a UI-heavy PR for consistency and design-system violations
- Use when the output looks "mostly fine" but feels off in subtle ways
- Use when you need a structured review with concrete fixes

## Review Checklist

### Design Tokens

- no hardcoded hex colors when semantic tokens exist
- no improvised shadow values when tokenized shadows exist
- no arbitrary radius choices outside the system scale
- no random spacing values that break the seed rhythm

### Component Conventions

- uses the project's class merge helper
- supports `className` extension when appropriate
- uses the agreed typing pattern
- avoids wrapper components that only forward one class string
- reuses existing primitives before inventing new ones

### Accessibility

- touch targets large enough for mobile
- visible keyboard focus states
- labels and `aria-*` attributes where needed
- adequate color contrast
- reduced-motion respect for animation

### Mobile UX

- no horizontal overflow
- safe-area handling where relevant
- readable text sizes
- thumb-friendly interaction spacing
- bottom nav or sticky actions do not obscure content

### Typography and Spacing

- uses the system type hierarchy
- display and headings are not overly loose
- body text remains readable
- spacing follows the seed grid instead of arbitrary values

## Output Format

Return:
1. A verdict: Pass, Needs Improvement, or Fail
2. A prioritized list of issues with file and line references when available
3. Concrete fixes for each issue
4. Any open questions where the design intent is ambiguous

## Best Practices

- Review against the seed, not against personal taste
- Separate stylistic drift from real usability or accessibility bugs
- Prefer actionable diffs over abstract criticism
- Call out duplication when an existing component already solves the problem

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-review/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-setup
*Interactive StyleSeed setup wizard for choosing app type, brand color, visual style, typography, and the first screen scaffold.*

Tags: [ui, design-system, setup, frontend, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Setup

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this setup wizard turns a raw project into a design-system-guided workspace. It collects the minimum brand and product context needed to configure tokens, pick a visual direction, and generate an initial page without drifting into generic UI.

## When to Use
- Use when you are starting a new app with the StyleSeed Toss seed
- Use when you copied the seed into an existing project and need to personalize it
- Use when you want the AI to ask one design decision at a time instead of guessing
- Use when you need a first page scaffold after selecting colors, font, and app type

## How It Works

### Step 1: Ask One Question at a Time

Do not front-load the full questionnaire. Ask a single question, wait for the answer, store it, then continue.

### Step 2: Capture the App Type

Identify the product shape before touching tokens or layout recipes.

Suggested buckets:
- SaaS dashboard
- E-commerce
- Fintech
- Social or content
- Productivity or internal tool
- Other with a short freeform description

Use the answer to choose the page composition pattern and the type of first screen to scaffold.

### Step 3: Choose the Brand Color

Offer a few safe defaults plus a custom hex option. Once selected:
- update the light theme brand token
- update the dark theme brand token with a lighter accessible variant
- keep all other colors semantic rather than hardcoding the brand everywhere

If the project uses the StyleSeed Toss seed, the main target is `css/theme.css`.

### Step 4: Offer an Optional Visual Reference

Ask whether the user wants to borrow the feel of an established brand or design language. Good examples include Stripe, Linear, Vercel, Notion, Spotify, Supabase, and Airbnb.

Use the reference to influence density, tone, and composition, not to clone assets or trademarks.

### Step 5: Pick Typography

Confirm the font direction:
- keep the default stack
- swap to a preferred font if already installed or available
- preserve hierarchy rules for display, heading, body, and caption text

If the seed is present, update the font-related files rather than scattering overrides across components.

### Step 6: Generate the First Screen

Ask for:
- app name
- first page or screen name
- a one-sentence purpose for that page

Then scaffold the page using the seed's page shell, top bar, navigation, spacing scale, and card structure.

## Output

Return:
1. The captured setup decisions
2. The files or tokens updated
3. The first page or scaffold created
4. Any follow-up recommendations for components, patterns, accessibility, or copy

## Best Practices

- Keep the interaction conversational, but deterministic
- Make brand color changes through tokens, not component-by-component edits
- Use an inspiration brand as a reference, not as a permission slip to copy
- Prefer semantic tokens and reusable patterns over page-specific CSS

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [StyleSeed Toss seed](https://github.com/bitjaru/styleseed/tree/main/seeds/toss)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-setup/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ui-tokens
*List, add, and update StyleSeed design tokens while keeping JSON sources, CSS variables, and dark-mode values in sync.*

Tags: [ui, tokens, design-system, theming, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UI Tokens

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill manages design tokens without letting the source-of-truth files drift apart. It is meant for teams using the Toss seed's JSON token files and CSS implementation together.

## When to Use
- Use when you need to inspect the current token set
- Use when you want to add a new color, shadow, radius, spacing, or typography token
- Use when you need to update a token and propagate the change safely
- Use when the project has both JSON token files and CSS variables that must stay aligned

## How It Works

### Supported Actions

- `list`: show the current tokens in a human-readable form
- `add`: introduce a new token and wire it through the implementation
- `update`: change an existing token value and audit the downstream usage

### Typical Source-of-Truth Split

For the Toss seed:
- JSON under `tokens/`
- CSS variables and theme wiring under `css/theme.css`
- typography support in the font and base CSS files

### Rules

- keep JSON and CSS in sync
- prefer semantic names over descriptive names
- provide dark-mode support where relevant
- update the token implementation, not just the source manifest
- check for direct component usage that might now be stale

## Output

Return:
1. The requested token inventory or change summary
2. Every file touched
3. Any affected components or utilities that should be reviewed
4. Follow-up actions if the new token requires broader adoption

## Best Practices

- Add semantic intent, not one-off brand shades
- Avoid token sprawl by extending existing scales first
- Keep naming consistent with the rest of the system
- Review contrast and accessibility when introducing new colors

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-tokens/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## unslop
*Post-process AI-generated text through the unslop CLI to strip AI writing patterns before publishing*

Tags: [writing, content-quality, ai-writing, text-processing, cli, publishing]
Tools: [claude-code, cursor, gemini-cli, codex-cli, antigravity]
Risk: safe

# unslop — Strip AI Writing Patterns via CLI

## Overview

unslop is a CLI tool that post-processes text to remove AI writing patterns programmatically. Unlike skills that ask the agent to avoid AI-isms, unslop runs as a deterministic pipeline step: pipe text in, get clean text out. Use it as a final pass before committing docs, publishing posts, or sending any AI-generated content to production.

The `--deterministic` flag makes output reproducible — same input always produces same output. The `--stdin` flag reads from stdin, enabling shell pipeline composition.

## When to Use This Skill

- When you have AI-generated text ready to publish and want a final cleanup pass
- When working in a shell pipeline where text quality needs to be enforced automatically
- When writing commit hooks or CI steps that validate content before it ships
- When you need reproducible text normalization across multiple runs

## Setup

Install once:

```bash
pipx install unslop
# or
uv tool install unslop
```

Verify:

```bash
unslop --version
```

## How It Works

### Step 1: Pipe Text Through unslop

Standard cleanup (may vary slightly between runs):

```bash
echo "This leverages cutting-edge AI to deliver robust solutions." | unslop --stdin
```

Deterministic cleanup (same input → same output every run):

```bash
echo "This leverages cutting-edge AI to deliver robust solutions." | unslop --stdin --deterministic
```

### Step 2: Use in Shell Pipelines

Pipe the output of any command through unslop:

```bash
cat draft.md | unslop --stdin --deterministic > clean.md
```

Or chain with other tools:

```bash
cat draft.md | unslop --stdin --deterministic | pbcopy   # macOS: copy clean text to clipboard
```

### Step 3: Integrate into Commit Hooks or CI

Add to a pre-commit hook or CI step to enforce quality gates on any generated content before it ships:

```bash
# In .git/hooks/pre-commit or a CI script
CONTENT=$(cat docs/changelog.md)
CLEANED=$(echo "$CONTENT" | unslop --stdin --deterministic)
if [ "$CONTENT" != "$CLEANED" ]; then
  echo "Changelog contains AI writing patterns. Run: cat docs/changelog.md | unslop --stdin --deterministic > docs/changelog.md"
  exit 1
fi
```

## Examples

### Example 1: Clean a Draft Document

```bash
cat blog-post-draft.md | unslop --stdin --deterministic > blog-post-final.md
```

### Example 2: Inline Cleanup During Writing

```bash
# Write content, pipe through unslop, write result back
cat README.md | unslop --stdin > README.clean.md && mv README.clean.md README.md
```

### Example 3: Validate Before Submitting a PR

```bash
# Check if any generated docs need cleanup
for f in docs/*.md; do
  ORIGINAL=$(cat "$f")
  CLEANED=$(echo "$ORIGINAL" | unslop --stdin --deterministic)
  [ "$ORIGINAL" != "$CLEANED" ] && echo "Needs cleanup: $f"
done
```

## Best Practices

- ✅ Use `--deterministic` in CI and automation to ensure reproducible output
- ✅ Run on the final draft, not intermediate iterations
- ✅ Combine with the `avoid-ai-writing` skill for both generation-time guidance and post-processing
- ❌ Don't run on code files — unslop targets prose, not source code
- ❌ Don't skip review after unslop: automated cleanup can occasionally change meaning; read the output

## Limitations

- Processes prose only — not code, JSON, or structured data
- Does not catch factual errors or substantive writing issues
- Some replacements may not fit every context; review the output before publishing
- Requires Python tooling such as `pipx` or `uv` for standalone CLI installation

## Security & Safety Notes

- unslop reads from stdin and writes to stdout — no file system side effects by default
- `--deterministic` mode is local and does not make LLM API calls
- Default LLM mode may use `ANTHROPIC_API_KEY` or the Claude CLI; use `--deterministic` for sensitive local files and CI gates
- Safe to run in CI pipelines and commit hooks when pinned to deterministic mode

---

## ux-audit
*Audit screens against Nielsen's heuristics and mobile UX best practices using the StyleSeed Toss design language as the implementation context.*

Tags: [ux, audit, usability, mobile, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UX Audit

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill audits usability rather than just visuals. It uses Nielsen's 10 heuristics plus modern mobile UX expectations to find issues in navigation, feedback, recovery, hierarchy, and cognitive load.

## When to Use
- Use when a screen feels awkward even though the code and styling seem correct
- Use when evaluating a flow before or after implementation
- Use when reviewing a mobile-first product for usability regressions
- Use when you want findings framed as user experience problems with remediation

## Audit Framework

Review the target against:
- visibility of system status
- match between system and real-world language
- user control and freedom
- consistency and standards
- error prevention
- recognition rather than recall
- flexibility and efficiency
- aesthetic and minimalist design
- recovery from errors
- help, onboarding, and empty-state guidance

Add mobile-specific checks for reachability, touch ergonomics, input burden, and thumb-friendly action placement.

## Output

Return:
1. A prioritized issue list
2. The heuristic violated by each issue
3. Why the issue matters to real users
4. Specific remediation suggestions for the page, component, or flow

## Best Practices

- Judge the experience from the user's point of view, not the implementer's
- Separate high-severity flow blockers from minor polish issues
- Include recovery and state-management guidance, not only layout comments
- Tie recommendations back to concrete UI changes

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-audit/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ux-copy
*Generate UX microcopy in StyleSeed's Toss-inspired voice for buttons, empty states, errors, toasts, confirmations, and form guidance.*

Tags: [ux, copywriting, microcopy, frontend, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UX Copy

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill generates concise product copy for common UI states. It follows the Toss-inspired tone: casual but polite, direct, active, and specific enough to help the user recover or proceed.

## When to Use
- Use when you need button labels, helper text, toasts, empty states, or error messages
- Use when a feature has functional UI but weak or robotic wording
- Use when you want consistent product voice across a flow
- Use when confirmation dialogs or state feedback need better phrasing

## Tone Rules

- casual but polite
- active voice over passive voice
- positive framing where it stays honest
- plain language instead of internal jargon
- concise wording where every word earns its place

## Common Patterns

### Buttons

Use a short action verb plus object when needed.

### Empty States

Start with a friendly observation, then suggest the next action.

### Errors

Explain what happened in user-facing language and what to do next. Do not surface raw internal error strings.

### Toasts

Confirm the result quickly. Add an undo action for reversible destructive behavior.

### Forms

Use clear labels, useful placeholders, specific helper text, and corrective error messages.

### Confirmation Dialogs

State the action in plain language and explain the consequence if the decision is risky or irreversible.

## Output

Return:
1. The requested microcopy grouped by UI surface
2. Notes on tone or localization considerations if relevant
3. Any places where the UX likely needs a structural fix in addition to better copy

## Best Practices

- Make the next action obvious
- Avoid generic labels like "Submit" or "OK" when the action can be named precisely
- Blame the system, not the user, when something fails
- Keep error and empty states useful even without visual context

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-copy/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ux-feedback
*Add loading, empty, error, and success feedback states to StyleSeed components and pages with practical mobile-first rules.*

Tags: [ux, states, loading, error-handling, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UX Feedback

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill ensures data-dependent UI does not stop at the happy path. It adds the four core feedback states every serious product needs: loading, empty, error, and success.

## When to Use
- Use when a component or page fetches, mutates, or depends on async data
- Use when a flow currently renders only the success path
- Use when a card, list, or page needs better state communication
- Use when the product needs clear recovery and confirmation behavior

## The Four Required States

### Loading

Use skeletons that match the final layout. Avoid spinners inside cards unless the pattern genuinely requires them. Delay skeletons slightly to avoid flashes on fast responses.

### Empty

Provide a friendly explanation and a next action. Zero values should still render meaningfully instead of disappearing.

### Error

Use plain-language failure messages and always offer recovery where possible. Localize failures to the affected card or section if the rest of the page can still work.

### Success

Use toasts or equivalent lightweight confirmation for completed actions. Add undo for reversible destructive changes.

## Output

Return:
1. The data-dependent areas identified
2. The loading, empty, error, and success states added for each one
3. Any reusable empty-state or toast patterns created
4. Follow-up work needed for analytics, retries, or accessibility

## Best Practices

- Match loading placeholders to the real layout
- Keep partial failure isolated whenever possible
- Make recovery obvious, not hidden in logs or developer tools
- Use success feedback sparingly but clearly

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-feedback/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ux-flow
*Design user flows and screen structure using StyleSeed UX patterns such as progressive disclosure, hub-and-spoke navigation, and information pyramids.*

Tags: [ux, flows, navigation, product-design, styleseed]
Tools: [claude, cursor, codex, gemini]
Risk: safe

# UX Flow

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill designs flows before screens. It uses proven UX patterns to define entry points, exits, screen inventory, and navigation structure so the implementation has a coherent user journey instead of a pile of disconnected pages.

## When to Use
- Use when planning onboarding, checkout, account management, dashboards, or drill-down flows
- Use when a new feature spans multiple screens or modal states
- Use when users need a clear path through a task instead of a single isolated page
- Use when the UI needs navigation logic before components are built

## How It Works

### Information Architecture Principles

- progressive disclosure: reveal complexity only when needed
- Miller's Law: chunk content into manageable groups
- Hick's Law: minimize decision overload on each screen

### Common Navigation Models

- hub and spoke for dashboards and detail views
- linear flow for onboarding, forms, and checkout
- tab navigation for 3 to 5 top-level areas

### Flow Rules

- every flow has a clear entry point
- every flow has a clear exit or success condition
- key features should usually be reachable within three taps from home
- non-root screens need back navigation
- loading, empty, and error states need explicit recovery paths

## Output

Provide:
1. An ASCII flow diagram
2. A screen inventory with each screen's purpose
3. Edge cases for loading, empty, and error states
4. Recommended page scaffolds and reusable patterns to implement next

## Best Practices

- Optimize for clarity before density
- Let one screen answer one primary question
- Keep escape hatches visible for risky or destructive steps
- Define state transitions before drawing detailed layouts

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-flow/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## uxui-principles
*Evaluate interfaces against 168 research-backed UX/UI principles, detect antipatterns, and inject UX context into AI coding sessions.*

Tags: [ux, ui, design, evaluation, principles, antipatterns, accessibility]
Tools: [claude, cursor, windsurf]
Risk: safe

# UX/UI Principles

A collection of 5 agent skills for evaluating interfaces against 168 research-backed UX/UI principles, detecting antipatterns, and injecting UX context into AI-assisted design and coding sessions.

**Source:** https://github.com/uxuiprinciples/agent-skills

## Skills

| Skill | Purpose |
|-------|---------|
| `uxui-evaluator` | Evaluate interface descriptions against 168 research-backed principles |
| `interface-auditor` | Detect UX antipatterns using the uxuiprinciples smell taxonomy |
| `ai-interface-reviewer` | Audit AI-powered interfaces against 44 AI-era UX principles |
| `flow-checker` | Check user flows against decision, error, and feedback principles |
| `vibe-coding-advisor` | Inject UX context into vibe coding sessions before implementation |

## When to Use
- Auditing an existing interface for UX issues
- Checking if a UI follows research-backed best practices
- Detecting antipatterns and UX smells in designs
- Reviewing AI-powered interfaces for trust, transparency, and safety
- Getting UX guidance before or during implementation

## How It Works

1. Install any skill from the collection
2. Describe the interface, screen, or flow you want to evaluate
3. The skill evaluates against the relevant principles and returns structured findings with severity levels and remediation steps
4. Optionally connect to the uxuiprinciples.com API for enriched output with full citations

## Install

```
npx skills add uxuiprinciples/agent-skills
```

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## wordpress-centric-high-seo-optimized-blogwriting-skill
*Create long-form, high-quality, SEO-optimized blog posts ready for WordPress with truth boxes and FAQ schema.*

Tags: [writing, blog, seo, content, wordpress]
Tools: [claude, cursor, gemini]
Risk: safe

# WordPress Centric High SEO Optimized Blog Writing Skill

## Overview

This skill is designed for Senior Content Strategists and Expert Copywriters to create high-quality, long-form blog posts that are ready for direct publication in WordPress. It emphasizes professional structure, factual accuracy (Truth Boxes), and comprehensive SEO optimization (Yoast elements and Schema markup).

## When to Use This Skill

- Use when you need to write a professional blog post or article.
- Use when creating SEO-optimized content for a WordPress site.
- Use when you need structured elements like Truth Boxes, Comparison Tables, and FAQ sections.
- Use when the user requires Yoast SEO metadata and JSON-LD schema.

## How It Works

### Step 1: Gather Inputs
The skill requires a Title, Primary Keyword, Intent, and Niche/Industry. It also prompts for Yoast SEO preference and image count if not provided.

### Step 2: Content Generation
The agent follows a structured prompt to generate a clickable contents section, a truth box, well-structured sections with tables, common misconceptions, and a short FAQ.

### Step 3: SEO & Schema (Optional)
If requested, the agent provides Yoast SEO metadata (Social titles, meta descriptions) and JSON-LD Schema (BlogPosting, FAQPage).

## Prompt Template

FINAL MASTER PROMPT (Refined & Generalized Version)

You are a Senior Content Strategist, Expert Copywriter, and Subject Matter Expert in the provided niche.

Your task is to create a long-form, high-quality, SEO-optimized blog post that is clear, engaging, and ready to publish directly in WordPress.

INPUT

Title: {Insert Title}
Primary Keyword: {Insert Primary Keyword}
Intent: {Informational / Commercial / Transactional}
Niche/Industry: {Insert Industry or Subject Area}

USER PREFERENCES (ASK IF MISSING)
Yoast SEO: {Are Yoast SEO elements like meta descriptions and focus keyphrases needed?}
Image Count: {How many images should be included in the SEO plan?}

Optional Context
Brand: {Insert Brand Name}
Target Audience: {Insert Target Audience}
Key Themes/Context: {Insert any specific context, locations, products, or pain points to highlight}

RESEARCH REQUIREMENT

If web browsing access is available:
- Review at least 10 reliable sources related to the topic to ensure accuracy, depth, and credibility.

If web browsing is restricted or unavailable:
- Disclose access limits immediately.
- Forbid claiming a specific source count.
- Rely only on verified internal knowledge or state that information cannot be verified.


WRITING RULES
Use simple, natural, human language
Avoid robotic or AI-like tone
Keep sentences short and clear
Keep paragraphs concise
Avoid long dashes
Avoid unnecessary symbols
Minimize use of brackets
Do not number headings
Maintain clean and consistent formatting
Make content easy to scan and copy

FACT AND ACCURACY RULES

Do not guess or fabricate data.
- Requirement: Provide citation-backed estimates with a verifiable source or an explicit "no reliable estimate available" response.
- Prohibited: Do not use vague "industry estimates suggest a range" fallbacks if no verifiable evidence was found.

Avoid fake or unreliable sources
Keep all information practical, realistic, and up-to-date

CONTENTS SECTION

Create a clickable contents section with:

Contents

Introduction
[Core Topic Section 1 - e.g., Overview/Key Concepts]
[Core Topic Section 2 - e.g., Deep Dive/Analysis]
[Core Topic Section 3 - e.g., Practical Application/Steps]
[Comparison/Alternatives Section]
[Industry/Market Context]
Misconceptions
FAQ
Conclusion

Do not use hyphen bullets

MAIN BLOG STRUCTURE

Main Title

Introduction

Truth Box


[Core Topic Section 1]

[Relevant Output Table 1 - e.g., Key Features, Pros/Cons, Pricing, or Summary]

[Core Topic Section 2]

[Relevant Output Table 2 - e.g., Data, Comparison, or Checklist]

[Core Topic Section 3]

[Comparison/Alternatives Section]

Common Misconceptions

FAQ

Conclusion

TRUTH BOX

Create a table with 5 strong insights relevant to the topic.

Example columns:
Key Point | Insight

TABLE USAGE

Use clean tables where helpful, such as:

Features or Pricing comparison
Pros & Cons
Industry or category comparisons
Step-by-step summaries

WRITING STYLE
Clear and direct
Professional yet simple
No fluff
Logical flow
Break long sections into small readable parts

COMMON MISCONCEPTIONS

Include 3 common myths with simple corrections

FAQ SECTION
Add 5 real user questions relevant to the intent and target keywords.
Keep answers short and clear

IMAGE SEO SECTION

Include {User Requested Count} images

For each image, provide:

Alt Text
Title
Caption
Description
Placement

Requirements:

Include one Feature Image
At least one alt text must contain the primary keyword

FINAL CHECKLIST
Remove unnecessary symbols
Ensure no numbered headings
Ensure no long dashes
Ensure readability
Ensure WordPress-ready formatting
Ensure clean and consistent structure

OUTPUT REQUIREMENT

The final output must be generated in this order:
1. The full blog post (from Main Title to Conclusion)
2. SEO Section (if requested)
3. Schema Markup (if requested)

The content must be:

Clean and well-structured
SEO optimized
Human-sounding
Professional quality
Ready to copy and paste into WordPress

SEO SECTION (YOAST)
*Only provide this section if the user requested Yoast SEO elements.*

Provide the following:

Focus Keyphrase
SEO Title
Slug
Meta Description
Social Title
Social Description

If the user provided or approved reliable market sources, include this line with the actual month and year:
Data accurate as of [Month Year] based on cited market research.

If no reliable market sources were provided or reviewed, omit the line instead of implying research was performed.

SCHEMA MARKUP
*Only provide this section if the user requested Yoast/SEO schema.*

Add clean JSON-LD for:

BlogPosting
FAQPage

Use placeholder URLs if needed

## Examples

### Example 1: Informational Blog Post
**User:** Write a blog post about "Sustainable Gardening for Beginners".
**Agent:** (Generates Title, Truth Box, clickable contents, well-structured sections with tables, Misconceptions, and FAQ.)

## Best Practices

- ✅ Use short, punchy sentences.
- ✅ Ensure tables are clean and use `|` markdown syntax.
- ✅ Maintain the Truth Box at the very beginning of the post for high engagement.
- ❌ Avoid using numbered headings; stick to standard markdown `#`, `##`, `###`.
- ❌ Do not use hyphen bullets in the contents section.

## Limitations

- This skill does not replace environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, or safety boundaries are missing.
- Use this skill only when the task clearly matches the scope described above.

## Security & Safety Notes

- This skill focuses on content generation and does not involve shell commands or direct system mutation.
- Ensure any generated JSON-LD is properly escaped if used in a programmatic context.

## Common Pitfalls

- **Problem:** Missing Primary Keyword in Alt Text.
  **Solution:** Ensure the `IMAGE SEO SECTION` explicitly includes the primary keyword in at least one Alt Text field.
- **Problem:** AI-sounding or repetitive tone.
  **Solution:** Use the "Human-sounding" requirement in the `WRITING RULES` to re-check the draft.

## Related Skills

- `@seo-plan` - Use for high-level SEO strategy before writing.
- `@seo-content` - For broader SEO content optimization across different platforms.
- `@copywriting` - General professional writing and marketing copy.

---

## youtube-summarizer
*Extract transcripts from YouTube videos and generate comprehensive, detailed summaries using intelligent analysis frameworks*

Tags: [video, summarization, transcription, youtube, content-analysis]
Risk: safe

# youtube-summarizer

## Purpose

This skill extracts transcripts from YouTube videos and generates comprehensive, verbose summaries using the STAR + R-I-S-E framework. It validates video availability, extracts transcripts using the `youtube-transcript-api` Python library, and produces detailed documentation capturing all insights, arguments, and key points.

The skill is designed for users who need thorough content analysis and reference documentation from educational videos, lectures, tutorials, or informational content.

## When to Use This Skill

This skill should be used when:

- User provides a YouTube video URL and wants a detailed summary
- User needs to document video content for reference without rewatching
- User wants to extract insights, key points, and arguments from educational content
- User needs transcripts from YouTube videos for analysis
- User asks to "summarize", "resume", or "extract content" from YouTube videos
- User wants comprehensive documentation prioritizing completeness over brevity

## Step 0: Discovery & Setup

Before processing videos, validate the environment and dependencies:

```bash
# Check if youtube-transcript-api is installed
python3 -c "import youtube_transcript_api" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  youtube-transcript-api not found"
    # Offer to install
fi

# Check Python availability
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi
```

**Ask the user if dependency is missing:**

```
youtube-transcript-api is required but not installed.

Would you like to install it now?
- [ ] Yes - Install with pip (pip install youtube-transcript-api)
- [ ] No - I'll install it manually
```

**If user selects "Yes":**

```bash
pip install youtube-transcript-api
```

**Verify installation:**

```bash
python3 -c "import youtube_transcript_api; print('✅ youtube-transcript-api installed successfully')"
```

## Main Workflow

### Progress Tracking Guidelines

Throughout the workflow, display a visual progress gauge before each step to keep the user informed. The gauge format is:

```bash
echo "[████░░░░░░░░░░░░░░░░] 20% - Step 1/5: Validating URL"
```

**Format specifications:**
- 20 characters wide (use █ for filled, ░ for empty)
- Percentage increments: Step 1=20%, Step 2=40%, Step 3=60%, Step 4=80%, Step 5=100%
- Step counter showing current/total (e.g., "Step 3/5")
- Brief description of current phase

**Display the initial status box before Step 1:**

```
╔══════════════════════════════════════════════════════════════╗
║     📹  YOUTUBE SUMMARIZER - Processing Video                ║
╠══════════════════════════════════════════════════════════════╣
║ → Step 1: Validating URL                 [IN PROGRESS]       ║
║ ○ Step 2: Checking Availability                              ║
║ ○ Step 3: Extracting Transcript                              ║
║ ○ Step 4: Generating Summary                                 ║
║ ○ Step 5: Formatting Output                                  ║
╠══════════════════════════════════════════════════════════════╣
║ Progress: ██████░░░░░░░░░░░░░░░░░░░░░░░░  20%               ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 1: Validate YouTube URL

**Objective:** Extract video ID and validate URL format.

**Supported URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

**Actions:**

```bash
# Extract video ID using regex or URL parsing
URL="$USER_PROVIDED_URL"

# Pattern 1: youtube.com/watch?v=VIDEO_ID
if echo "$URL" | grep -qE 'youtube\.com/watch\?v='; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*[?&]v=([^&]+).*/\1/')
# Pattern 2: youtu.be/VIDEO_ID  
elif echo "$URL" | grep -qE 'youtu\.be/'; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*youtu\.be\/([^?]+).*/\1/')
else
    echo "❌ Invalid YouTube URL format"
    exit 1
fi

echo "📹 Video ID extracted: $VIDEO_ID"
```

**If URL is invalid:**

```
❌ Invalid YouTube URL

Please provide a valid YouTube URL in one of these formats:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Step 2: Check Video & Transcript Availability

**Progress:**
```bash
echo "[████████░░░░░░░░░░░░] 40% - Step 2/5: Checking Availability"
```

**Objective:** Verify video exists and transcript is accessible.

**Actions:**

```python
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import sys

video_id = sys.argv[1]

try:
    # Get list of available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print(f"✅ Video accessible: {video_id}")
    print("📝 Available transcripts:")
    
    for transcript in transcript_list:
        print(f"  - {transcript.language} ({transcript.language_code})")
        if transcript.is_generated:
            print("    [Auto-generated]")
    
except TranscriptsDisabled:
    print(f"❌ Transcripts are disabled for video {video_id}")
    sys.exit(1)
    
except NoTranscriptFound:
    print(f"❌ No transcript found for video {video_id}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error accessing video: {e}")
    sys.exit(1)
```

**Error Handling:**

| Error | Message | Action |
|-------|---------|--------|
| Video not found | "❌ Video does not exist or is private" | Ask user to verify URL |
| Transcripts disabled | "❌ Transcripts are disabled for this video" | Cannot proceed |
| No transcript available | "❌ No transcript found (not auto-generated or manually added)" | Cannot proceed |
| Private/restricted video | "❌ Video is private or restricted" | Ask for public video |

### Step 3: Extract Transcript

**Progress:**
```bash
echo "[████████████░░░░░░░░] 60% - Step 3/5: Extracting Transcript"
```

**Objective:** Retrieve transcript in preferred language.

**Actions:**

```python
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "VIDEO_ID"

try:
    # Try to get transcript in user's preferred language first
    # Fall back to English if not available
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, 
        languages=['pt', 'en']  # Prefer Portuguese, fallback to English
    )
    
    # Combine transcript segments into full text
    full_text = " ".join([entry['text'] for entry in transcript])
    
    # Get video metadata
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("✅ Transcript extracted successfully")
    print(f"📊 Transcript length: {len(full_text)} characters")
    
    # Save to temporary file for processing
    with open(f"/tmp/transcript_{video_id}.txt", "w") as f:
        f.write(full_text)
    
except Exception as e:
    print(f"❌ Error extracting transcript: {e}")
    exit(1)
```

**Transcript Processing:**

- Combine all transcript segments into coherent text
- Preserve punctuation and formatting where available
- Remove duplicate or overlapping segments (if auto-generated artifacts)
- Store in temporary file for analysis

### Step 4: Generate Comprehensive Summary

**Progress:**
```bash
echo "[████████████████░░░░] 80% - Step 4/5: Generating Summary"
```

**Objective:** Apply enhanced STAR + R-I-S-E prompt to create detailed summary.

**Prompt Applied:**

Use the enhanced prompt from Phase 2 (STAR + R-I-S-E framework) with the extracted transcript as input.

**Actions:**

1. Load the full transcript text
2. Apply the comprehensive summarization prompt
3. Use AI model (Claude/GPT) to generate structured summary
4. Ensure output follows the defined structure:
   - Header with video metadata
   - Executive synthesis
   - Detailed section-by-section breakdown
   - Key insights and conclusions
   - Concepts and terminology
   - Resources and references

**Implementation:**

```bash
# Use the transcript file as input to the AI prompt
TRANSCRIPT_FILE="/tmp/transcript_${VIDEO_ID}.txt"

# The AI agent will:
# 1. Read the transcript
# 2. Apply the STAR + R-I-S-E summarization framework
# 3. Generate comprehensive Markdown output
# 4. Structure with headers, lists, and highlights

Read "$TRANSCRIPT_FILE"  # Read transcript into context
```

Then apply the full summarization prompt (from enhanced version in Phase 2).

### Step 5: Format and Present Output

**Progress:**
```bash
echo "[████████████████████] 100% - Step 5/5: Formatting Output"
```

**Objective:** Deliver the summary in clean, well-structured Markdown.

**Output Structure:**

```markdown
# [Video Title]

**Canal:** [Channel Name]  
**Duração:** [Duration]  
**URL:** [https://youtube.com/watch?v=VIDEO_ID]  
**Data de Publicação:** [Date if available]


## 📝 Detailed Summary

### [Topic 1]

[Comprehensive explanation with examples, data, quotes...]

#### [Subtopic 1.1]

[Detailed breakdown...]

### [Topic 2]

[Continued detailed analysis...]


## 📚 Concepts and Terminology

- **[Term 1]:** [Definition and context]
- **[Term 2]:** [Definition and context]


## 📌 Conclusion

[Final synthesis and takeaways]
```


### **Example 2: Missing Dependency**

**User Input:**
```
claude> summarize this youtube video https://youtu.be/abc123
```

**Skill Response:**

```
⚠️  youtube-transcript-api not installed

This skill requires the Python library 'youtube-transcript-api'.

Would you like me to install it now?
- [ ] Yes - Install with pip
- [ ] No - I'll install manually
```

**User selects "Yes":**

```bash
$ pip install youtube-transcript-api
Successfully installed youtube-transcript-api-0.6.1

✅ Installation complete! Proceeding with video summary...
```


### **Example 4: Invalid URL**

**User Input:**
```
claude> summarize youtube video www.youtube.com/some-video
```

**Skill Response:**

```
❌ Invalid YouTube URL format

Expected format examples:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Please provide a valid YouTube video URL.
```


## 📊 Executive Summary

This video provides a comprehensive introduction to the fundamental concepts of Artificial Intelligence (AI), designed for beginners and professionals who want to understand the technical foundations and practical applications of modern AI. The instructor covers everything from basic definitions to machine learning algorithms, using practical examples and visualizations to facilitate understanding.

[... continued detailed summary ...]
```

**Save Options:**

```
What would you like to save?
→ Summary + raw transcript

✅ File saved: resumo-exemplo123-2026-02-01.md (includes raw transcript)
[████████████████████] 100% - ✓ Processing complete!
```


Welcome to this comprehensive tutorial on machine learning fundamentals. In today's video, we'll explore the core concepts that power modern AI systems...
```


**Version:** 1.2.0
**Last Updated:** 2026-02-02
**Maintained By:** Eric Andrade

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---
