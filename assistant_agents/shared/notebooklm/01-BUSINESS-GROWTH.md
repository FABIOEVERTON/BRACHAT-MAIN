# Business & Growth
## 13 skills
---

## blueprint
*Turn a one-line objective into a step-by-step construction plan any coding agent can execute cold. Each step has a self-contained context brief — a fresh agent in a new session can pick up any step without reading prior steps.*

Risk: safe

# Blueprint — Construction Plan Generator

Turn a one-line objective into a step-by-step plan any coding agent can execute cold.

## Overview

Blueprint is for multi-session, multi-agent engineering projects where each step must be independently executable by a fresh agent that has never seen the conversation history. Install it once, invoke it with `/blueprint <project> <objective>`.

## When to Use This Skill

- Use when the task requires multiple PRs or sessions
- Use when multiple agents or team members need to share execution
- Use when you want adversarial review of the plan before execution
- Use when parallel step detection and dependency graphs matter

## How It Works

1. **Research** — Scans the codebase, reads project memory, runs pre-flight checks
2. **Design** — Breaks the objective into one-PR-sized steps, identifies parallelism, assigns model tiers
3. **Draft** — Generates the plan from a structured template with branch workflow rules, CI policy, and rollback strategies inline
4. **Review** — Delegates adversarial review to a strongest-model sub-agent (falls back to default model if unavailable)
5. **Register** — Saves the plan and updates project memory

## Examples

### Example 1: Database migration
```
/blueprint myapp "migrate database to PostgreSQL"
```

### Example 2: Plugin extraction
```
/blueprint antbot "extract providers into plugins"
```

## Best Practices

- ✅ Use for tasks requiring 3+ PRs or multiple sessions
- ✅ Let Blueprint auto-detect git/gh availability — it degrades gracefully
- ❌ Don't invoke for tasks completable in a single PR
- ❌ Don't invoke when the user says "just do it"

## Key Differentiators

- **Cold-start execution**: Every step has a self-contained context brief
- **Adversarial review gate**: Strongest-model review before execution
- **Zero runtime risk**: Pure markdown — no hooks, no scripts, no executable code
- **Plan mutation protocol**: Steps can be split, inserted, skipped with audit trail

## Installation

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/antbotlab/blueprint.git ~/.claude/skills/blueprint
```

## Additional Resources

- [GitHub Repository](https://github.com/antbotlab/blueprint)
- [Examples: small plan](https://github.com/antbotlab/blueprint/blob/main/examples/small-plan.md)
- [Examples: large plan](https://github.com/antbotlab/blueprint/blob/main/examples/large-plan.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## content-creator
*Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.*

Risk: unknown

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

## When to Use
Use this skill when writing blog posts, creating social media content, establishing brand voice, optimizing content for SEO, or planning content calendars.

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy

## Quick Start

### For Brand Voice Development
1. Run `scripts/brand_voice_analyzer.py` on existing content to establish baseline
2. Review `references/brand_guidelines.md` to select voice attributes
3. Apply chosen voice consistently across all content

### For Blog Content Creation
1. Choose template from `references/content_frameworks.md`
2. Research keywords for topic
3. Write content following template structure
4. Run `scripts/seo_optimizer.py [file] [primary-keyword]` to optimize
5. Apply recommendations before publishing

### For Social Media Content
1. Review platform best practices in `references/social_media_optimization.md`
2. Use appropriate template from `references/content_frameworks.md`
3. Optimize based on platform-specific guidelines
4. Schedule using `assets/content_calendar_template.md`

## Core Workflows

### Establishing Brand Voice (First Time Setup)

When creating content for a new brand or client:

1. **Analyze Existing Content** (if available)
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```
   
2. **Define Voice Attributes**
   - Review brand personality archetypes in `references/brand_guidelines.md`
   - Select primary and secondary archetypes
   - Choose 3-5 tone attributes
   - Document in brand guidelines

3. **Create Voice Sample**
   - Write 3 sample pieces in chosen voice
   - Test consistency using analyzer
   - Refine based on results

### Creating SEO-Optimized Blog Posts

1. **Keyword Research**
   - Identify primary keyword (search volume 500-5000/month)
   - Find 3-5 secondary keywords
   - List 10-15 LSI keywords

2. **Content Structure**
   - Use blog template from `references/content_frameworks.md`
   - Include keyword in title, first paragraph, and 2-3 H2s
   - Aim for 1,500-2,500 words for comprehensive coverage

3. **Optimization Check**
   ```bash
   python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
   ```

4. **Apply SEO Recommendations**
   - Adjust keyword density to 1-3%
   - Ensure proper heading structure
   - Add internal and external links
   - Optimize meta description

### Social Media Content Creation

1. **Platform Selection**
   - Identify primary platforms based on audience
   - Review platform-specific guidelines in `references/social_media_optimization.md`

2. **Content Adaptation**
   - Start with blog post or core message
   - Use repurposing matrix from `references/content_frameworks.md`
   - Adapt for each platform following templates

3. **Optimization Checklist**
   - Platform-appropriate length
   - Optimal posting time
   - Correct image dimensions
   - Platform-specific hashtags
   - Engagement elements (polls, questions)

### Content Calendar Planning

1. **Monthly Planning**
   - Copy `assets/content_calendar_template.md`
   - Set monthly goals and KPIs
   - Identify key campaigns/themes

2. **Weekly Distribution**
   - Follow 40/25/25/10 content pillar ratio
   - Balance platforms throughout week
   - Align with optimal posting times

3. **Batch Creation**
   - Create all weekly content in one session
   - Maintain consistent voice across pieces
   - Prepare all visual assets together

## Key Scripts

### brand_voice_analyzer.py
Analyzes text content for voice characteristics, readability, and consistency.

**Usage**: `python scripts/brand_voice_analyzer.py <file> [json|text]`

**Returns**:
- Voice profile (formality, tone, perspective)
- Readability score
- Sentence structure analysis
- Improvement recommendations

### seo_optimizer.py
Analyzes content for SEO optimization and provides actionable recommendations.

**Usage**: `python scripts/seo_optimizer.py <file> [primary_keyword] [secondary_keywords]`

**Returns**:
- SEO score (0-100)
- Keyword density analysis
- Structure assessment
- Meta tag suggestions
- Specific optimization recommendations

## Reference Guides

### When to Use Each Reference

**references/brand_guidelines.md**
- Setting up new brand voice
- Ensuring consistency across content
- Training new team members
- Resolving voice/tone questions

**references/content_frameworks.md**
- Starting any new content piece
- Structuring different content types
- Creating content templates
- Planning content repurposing

**references/social_media_optimization.md**
- Platform-specific optimization
- Hashtag strategy development
- Understanding algorithm factors
- Setting up analytics tracking

## Best Practices

### Content Creation Process
1. Always start with audience need/pain point
2. Research before writing
3. Create outline using templates
4. Write first draft without editing
5. Optimize for SEO
6. Edit for brand voice
7. Proofread and fact-check
8. Optimize for platform
9. Schedule strategically

### Quality Indicators
- SEO score above 75/100
- Readability appropriate for audience
- Consistent brand voice throughout
- Clear value proposition
- Actionable takeaways
- Proper visual formatting
- Platform-optimized

### Common Pitfalls to Avoid
- Writing before researching keywords
- Ignoring platform-specific requirements
- Inconsistent brand voice
- Over-optimizing for SEO (keyword stuffing)
- Missing clear CTAs
- Publishing without proofreading
- Ignoring analytics feedback

## Performance Metrics

Track these KPIs for content success:

### Content Metrics
- Organic traffic growth
- Average time on page
- Bounce rate
- Social shares
- Backlinks earned

### Engagement Metrics
- Comments and discussions
- Email click-through rates
- Social media engagement rate
- Content downloads
- Form submissions

### Business Metrics
- Leads generated
- Conversion rate
- Customer acquisition cost
- Revenue attribution
- ROI per content piece

## Integration Points

This skill works best with:
- Analytics platforms (Google Analytics, social media insights)
- SEO tools (for keyword research)
- Design tools (for visual content)
- Scheduling platforms (for content distribution)
- Email marketing systems (for newsletter content)

## Quick Commands

```bash
# Analyze brand voice
python scripts/brand_voice_analyzer.py content.txt

# Optimize for SEO
python scripts/seo_optimizer.py article.md "main keyword"

# Check content against brand guidelines
grep -f references/brand_guidelines.md content.txt

# Create monthly calendar
cp assets/content_calendar_template.md this_month_calendar.md
```

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## daily-gift
*Relationship-aware daily gift engine with five-stage creative pipeline — editorial judgment, synthesis, concept generation, visual strategy, and rendering in H5, image, or video*

Tags: [creative, gift, personalization, h5, image-generation, video-generation, relationship]
Tools: [openclaw]
Risk: unknown

# Daily Gift

## Overview

A relationship-aware gift engine that decides *whether* a gift should exist before deciding *what* it should be. Uses a five-stage creative pipeline to generate personalized daily gifts in H5 (interactive web pages), AI-generated images, or AI-generated videos. The core design principle is "idea before medium" — the creative concept is locked before the output format is chosen.

Published on ClawHub: https://clawhub.ai/jiawei248/daily-gift

## When to Use This Skill

- Use when the agent should autonomously decide whether today deserves a personalized gift
- Use when a milestone, anniversary, or emotionally meaningful moment should be marked with a creative artifact
- Use when the user manually requests a visual gift from a quote, poem, or creative brief
- Use when you want a daily cron-triggered creative output that avoids repetition and template fatigue

## How It Works

### Stage 1: Editorial Judgment

Decide whether a gift should exist today, how heavy it should be (skip / nudge / light / standard / heavy), and what content direction to take (reflect, extension, compass, mirror, play, curation, utility, etc.). Format is NOT chosen here.

### Stage 2: Synthesis + Gift Thesis

Extract six content slots from conversation context (today_theme, emotion_peaks, historical_echo, open_loop, lobster_judgment, preference_hint). Form a gift thesis = anchor (which moment deserves the center) + return (what new perspective the agent gives back). If the thesis has no return, it's not a gift — it's a decorated log entry.

### Stage 2.5: Creative Concept

Generate 5+ concept candidates using seven thinking angles (metaphor flip, format mashup, impossible action, scale shift, role reversal, time distortion, cultural remix). Cross-pollinate with a library of 73 creative seeds across 8 categories. Run three quality checks: concept quality, concept diversity (8 families), and visual/theme collision detection.

### Format Selection

Only after the concept is locked does the system choose the output format (H5, image, or video) based on what best serves the concept.

### Stage 3: Visual Strategy

Choose visual approach, plan assets (pure code, generated background, hybrid), select visual style, and run pre-visualization checks against recent gifts for anti-repetition.

### Stage 4: Rendering

Produce the final artifact. H5 gifts use p5.js/canvas with a quality floor set by built-in templates (300-400 lines of tuned code). Image and video gifts use AI generation APIs. All formats have fallback chains.

## Key Features

- **Five-stage creative pipeline** with explicit quality gates between stages
- **Multi-layer anti-repetition**: concept family, visual elements, theme, style, content direction — each tracked across sliding windows of recent gifts
- **Three-layer user taste profile**: Layer 1 (identity — stable), Layer 2 (context — updates every 5-7 gifts), Layer 3 (signals — auto-appended after every gift)
- **Three runtime modes**: onboarding setup, daily cron, and manual trigger
- **11 content directions**: reflect, extension, compass, mirror, gift-from-elsewhere, play, real-world-nudge, curation, delayed-payoff, openclaw-inner-life, utility
- **8 concept families**: borrowed-media, interactive-object, transformation, narrative, data-viz, game-puzzle, real-world, poetic-literary

## Best Practices

- ✅ Let the editorial judgment decide — not every day needs a gift
- ✅ Generate 5+ concept candidates before selecting one
- ✅ Check recent gifts for visual and thematic collision before rendering
- ✅ Use the taste profile to personalize over time
- ❌ Don't skip straight from thesis to rendering without a real creative concept
- ❌ Don't default to "reflect on today" every time — vary content direction
- ❌ Don't choose the format before locking the concept

## Limitations

- Requires API keys for image/video generation (optional — H5 works without them)
- Cron mode runs in the agent's main session for full conversation context access
- Shell scripts make external API calls for rendering and asset fetching
- The skill creates and manages local workspace files for state, history, and taste profiling

## Security & Safety Notes

- The skill creates a recurring cron job for daily gift delivery. Review and approve the cron setup step.
- Shell scripts in `scripts/` call external APIs (image generation, video generation, asset hosting). Supply API keys only after reviewing which scripts use them.
- User taste data and gift history are stored locally in `workspace/daily-gift/`. No data is sent to external services beyond the configured rendering APIs.
- The skill reads conversation context and memory files to inform editorial judgment — this is core to personalization but means it has broad read access within the agent's workspace.

## Related Skills

- Image generation skills — for standalone image creation without the gift pipeline
- Cron/scheduling skills — for understanding the daily trigger mechanism

---

## decision-navigator
*Guide stuck or overwhelmed users through targeted branching questions until they reach concrete next steps.*

Risk: safe

# Decision Navigator

Help users who feel stuck or overwhelmed by guiding them through a structured branching exploration
of their situation — one clear question at a time — until they arrive at concrete, actionable steps.

## Core Philosophy

Most people go blank not because they're incapable, but because the problem space feels infinite.
Your job is to collapse that space progressively: ask one clarifying question, offer 3–5 distinct
paths, let them choose, and repeat — getting more specific each level — until you reach a leaf
where concrete steps make sense.

Never overwhelm with a wall of options or advice upfront. Navigate, don't lecture.

---

## When to Use This Skill

Use this skill whenever a user feels stuck, overwhelmed, or does not know where to start.
Trigger on phrases like "I don't know what to do", "I want to X but don't know how",
"I'm not sure where to begin", "help me figure out...", "I feel lost about...", or broad
open-ended goals like "I want to start a business", "I want to change careers", "I want to
learn something new", or "I need to make a decision about X".

Do not wait for the user to ask a precise question. If they seem stuck or overwhelmed, use
this skill.

## The Process

### Step 1 — Acknowledge and orient (1–2 sentences)

Reflect the situation back briefly so the user feels heard. Don't give advice yet.

> "Changing careers is a big one — lots of directions it could go. Let me help you narrow it down."

### Step 2 — Ask one clarifying question

Ask the single most useful question to understand *what kind* of problem this actually is.
Frame it as a choice between 3–5 concrete options, not open-ended.

**Option labels must be short** — 2 to 6 words max. No explanations inside the bullet.
The question itself carries the context; the options are just the choices.

**Good question format:**
> "What's driving this for you right now?
> - Unhappy in my current role
> - Want to earn more
> - Want more flexibility
> - Found a new interest
> - Not sure yet"

**Bad question format:**
> "Tell me more about your situation." ← too open, doesn't reduce the space

> "- Simplicity: I want the easiest setup with zero server management." ← option labels should never have colons or sub-explanations

### Step 2b — Extract before you ask

If the user's message already contains useful information (they described constraints, named
platforms, listed requirements), pull that out first. Don't make them re-answer what they
already told you.

> "Ok so you've got: Docker container ready, needs auth + multi-tenant DB, websockets, and
> the client wants AWS or GCP. That's a lot. What's the scariest part right now?
> - Choosing between AWS and GCP
> - Understanding how all the pieces connect
> - Actually deploying the container
> - Not sure where to even begin"

### Step 3 — Branch based on their answer

After they choose, go one level deeper. Each level should feel more specific.

Typical depth: 3–4 levels before reaching actionable steps.

**Level 1** — What kind of problem is this? (motivation, constraint, knowledge gap, fear, resources...)
**Level 2** — What's the most important factor for them? (urgency, risk tolerance, resources available...)
**Level 3** — What's their current situation / starting point?
**Level 4** (leaf) — Give concrete steps

### Step 4 — Deliver concrete steps at the leaf

When you've narrowed things down enough (usually 3–4 questions in), stop branching and give
3–6 specific, ordered action steps. These should be immediately doable, not vague advice.

**Good leaf output:**
> Based on what you've shared — you're unhappy in your current role, want to stay in tech, and
> have about 3 months before you need to move — here's where to start:
>
> 1. Spend one hour this week writing down what specifically drains you vs. energizes you at work.
> 2. Look at 3 job postings in roles that seem interesting — note what skills overlap with yours.
> 3. Reach out to 1–2 people doing those roles on LinkedIn for a 20-min conversation.
> 4. Set a decision deadline: commit to applying somewhere within 6 weeks.
> 5. Tell one trusted person about your plan so you have accountability.

**Bad leaf output:**
> "You should network more and update your resume." ← too vague

---

## Branching Guidelines

### How to design your questions

- **Short option labels** — 2 to 6 words. Never a colon + explanation inside a bullet.
  The question sets the context; options are just the fork in the road.
- **Mutually exclusive options** — each choice should lead down a genuinely different path
- **Concrete labels** — "Earn more money" not "financial reasons"
- **Cover the realistic space** — include the uncomfortable options (e.g. "Scared of failing")
- **Always offer an escape** — include "Not sure yet" so no one feels forced
- **Extract first** — if the user already gave you info, acknowledge it before asking the next question.
  Summarize what you know in 1–2 lines, then ask only what's still missing.

### When to branch vs. when to go straight to steps

Go straight to concrete steps when:
- The user's situation is already specific enough (they've answered 3+ questions)
- The remaining branches would all lead to the same advice
- The user says something like "just tell me what to do"

Keep branching when:
- The advice would be meaningfully different depending on their answer
- You'd be guessing at key constraints (budget, timeline, risk tolerance, etc.)
- The problem space still feels large

### How many options per question

- **3 options** — when the distinctions are clear-cut
- **4–5 options** — when the space is genuinely varied
- **Never more than 5** — more than that is overwhelming (the whole problem we're solving)

---

## Tone and Style

- Warm but efficient — not therapist-soft, not consultant-cold
- Short sentences. No jargon.
- Reflect their words back to them (if they said "burned out", use "burned out" not "fatigued")
- Never judge the path they choose
- If they seem emotionally distressed (not just confused), acknowledge that before navigating

---

## Format

Present choices as a short list, not prose:

```
[Question]

- Option A
- Option B
- Option C
- Something else / not sure
```

At the leaf, use a numbered list for steps. Start with the number ("1.") not a bullet.

Keep the whole interaction feeling like a conversation, not a form.

---

## Example Flow

**User:** I want to start a business but I have no idea where to start.

**Claude (Level 1):**
Starting a business means different things to different people. What's the main thing drawing you to it?

- I have a specific idea I want to build
- I want freedom / to be my own boss
- I want to make more money than my job pays
- I'm not sure yet — I just know I want something different

**User:** I have a specific idea I want to build.

**Claude (Level 2):**
Got it. Where are you in terms of the idea itself?

- It's clear in my head but I haven't done anything yet
- I've talked to some people about it but haven't built anything
- I've started building / have a prototype
- I've tried before and it didn't work out

**User:** It's clear in my head but I haven't done anything yet.

**Claude (Level 3):**
One more thing — what feels like the biggest blocker right now?

- I don't know if the idea is actually good
- I don't know how to build it / lack technical skills
- I'm worried about the financial risk
- I don't know the first practical step to take

**User:** I don't know if the idea is actually good.

**Claude (Leaf):**
That's the right thing to worry about first — most ideas fail on this, not execution.
Here's how to find out quickly:

1. Write one sentence describing who your customer is and what problem you solve for them.
2. Find 5 people who match that description. Not friends — people who'd actually pay.
3. Ask them: "Do you have this problem? How do you currently deal with it?"
4. Do NOT pitch your solution yet. Just listen. If they describe your problem unprompted, that's signal.
5. After 5 conversations, you'll know if this is real. If 3+ people have the problem badly, keep going.

---

## Edge Cases

**User gives a very vague situation** ("I don't know what to do with my life")
→ Start even broader: ask what *area* of life feels most stuck (work, relationships, health, purpose, finances)

**User picks "something else"**
→ Ask them to describe it briefly, then fit their answer into the next level of branching

**User wants to explore multiple paths**
→ Finish one path to the leaf, then offer: "Want to explore what the [other option] path looks like too?"

**User is clearly in distress**
→ Pause the navigation. Acknowledge first. Ask if they want to talk through how they're feeling or
  if they'd find it helpful to focus on practical next steps.

## Limitations

- This skill helps structure uncertainty; it does not replace professional legal, medical, financial, or mental-health advice.
- It should not force branching when the user has already requested a specific action or direct answer.
- It depends on the user's stated preferences and constraints, so recommendations should stay tentative when important facts are missing.

---

## faf-wizard
*Done-for-you .faf generator. One-click AI context for any project - new, legacy, or famous. Auto-detects stack, scores readiness, works everywhere.*

Tags: [faf, automation, project-setup, ai-context, productivity]
Tools: [claude, cursor, gemini, windsurf, any-ai]
Risk: safe

# FAF Wizard - One-Click AI Intelligence

**The pit crew for your projects.** Point it at any codebase and get scored, AI-ready context in 60 seconds.

Transform any project - new, legacy, famous OSS, or forgotten side projects - into an AI-intelligent workspace with persistent context that works across all AI tools.

## The Problem It Solves

**Even React.js scores 0% AI-readiness.** Famous repositories have no AI context.

| What Exists | What It Tells AI |
|-------------|------------------|
| README.md | "What this does" (for humans) |
| docs/ | "How to use it" (for humans) |
| **project.faf** | "How to help build this" (for AI) |

Documentation tells humans how to use your code. AI context tells AI how to help you build it. **They're completely different things.**

## Works on ANY Project

| Project Type | What FAF Wizard Does |
|-------------|----------------------|
| **Brand new** | Perfect AI context from line one |
| **Legacy nightmare** | AI finally understands the archaeology |
| **Famous OSS** | Even React doesn't have this |
| **Side projects** | Stop re-explaining every session |
| **Client handoffs** | Portable context for any AI tool |
| **Team projects** | Shared context that everyone can use |

## Real Success Stories

### Before/After: Legacy E-commerce Platform
```
Before: "This 50k-line PHP codebase from 2015..."
AI: "I don't understand this architecture"

After: 60 seconds with FAF Wizard
AI: "I see this is a Laravel-based e-commerce system with 
payment processing, inventory management, and multi-tenant 
architecture. Here's how I can help..."
```

### Before/After: Modern React App
```
Before: Every AI session starts with context explanation
Time lost: 5-10 minutes per session

After: project.faf exists
AI: Instant understanding, productive from message one
Time saved: 2+ hours per day
```

## The 60-Second Workflow

### Step 1: Detection (10 seconds)
```bash
faf auto
# Scans manifest files, directory structure, dependencies
# Detects: React + TypeScript + Tailwind + Vercel
```

### Step 2: Generation (30 seconds)  
```yaml
# Auto-generated project.faf
project:
  name: my-saas-dashboard  
  goal: Customer analytics platform

stack:
  frontend: react-18
  css: tailwind
  deployment: vercel
  
human_context:
  who: Solo founder
  what: SaaS analytics dashboard
  why: Customer insights for small businesses
```

### Step 3: Scoring & Report (20 seconds)
```
✅ Generated: project.faf
🏆 AI-Readiness: 87% Bronze - Production ready

Filled: 9/11 active slots
Ignored: 22 slots (not applicable)

To reach Silver (95%):
  + Add API documentation (+5%)  
  + Define deployment details (+3%)
```

## Performance Data (Real Numbers)

**Analyzed 8,400+ Projects:**
- ✅ **99.2% detection accuracy** across 153+ formats
- ✅ **Average generation time**: 12.3 seconds
- ✅ **Bronze tier or higher**: 94% of projects
- ✅ **Zero manual configuration**: Works out of the box

### Format Support
Automatically detects and configures:
- **JavaScript**: React, Vue, Angular, Svelte, Next.js, Nuxt
- **Python**: Django, Flask, FastAPI, Jupyter, Poetry
- **TypeScript**: All JS frameworks + native TS projects  
- **Rust**: Cargo projects, CLI tools, web servers
- **Go**: Modules, Docker, microservices
- **Java**: Maven, Gradle, Spring Boot
- **+147 more formats**

## Universal Compatibility

### Works With Every AI Tool
- ✅ **Claude Code** - Reads .faf natively
- ✅ **Cursor** - Auto-syncs to .cursorrules  
- ✅ **Gemini CLI** - Converts to GEMINI.md
- ✅ **Windsurf** - Syncs to .windsurfrules
- ✅ **ChatGPT** - Readable YAML format
- ✅ **Any AI** - Universal format support

### Migration Support
Already have AI context files?
```bash
# Migrates existing context
faf migrate --from .cursorrules
faf migrate --from CLAUDE.md  
faf migrate --from README.md

# One format, works everywhere
faf sync --target all
```

## Installation Options

### Option 1: CLI (Recommended)
```bash
npm install -g faf-cli
cd your-project
faf auto
```

### Option 2: MCP Server (Claude Code)
```json
{
  "mcpServers": {
    "faf": {
      "command": "npx", 
      "args": ["-y", "claude-faf-mcp@latest"]
    }
  }
}
```

### Option 3: Browser Extension
Install from Chrome Web Store - works on any Git repository.

## Three-Phase Intelligence

### Phase 1: Stack Detection
- Scans `package.json`, `Cargo.toml`, `pyproject.toml`, etc.
- Analyzes directory structure and file patterns
- Identifies frameworks, deployment targets, testing setup

### Phase 2: Context Mining  
- Extracts project description from README
- Identifies architecture patterns from code structure
- Pulls dependency information for AI context

### Phase 3: Optimization
- Generates focused 33-slot IANA format
- Validates against format specification
- Scores AI-readiness with improvement suggestions

## Success Metrics by Project Type

| Project Type | Avg Score | Time to Bronze | Detection Rate |
|-------------|-----------|----------------|----------------|
| **React/Vue** | 89% | Instant | 99.8% |
| **Python Django** | 91% | Instant | 99.5% |  
| **Rust CLI** | 85% | Instant | 99.1% |
| **Legacy PHP** | 76% | 30 seconds | 94.2% |
| **Monorepo** | 82% | 45 seconds | 91.8% |

## When to Use faf-expert Instead

Use `faf-wizard` for:
- ✅ Quick project onboarding
- ✅ Automatic everything
- ✅ "Just make it work"
- ✅ Time-constrained scenarios

Use `faf-expert` for:
- 🎯 Fine-tuned championship scoring (95%+)
- 🎯 Complex MCP server configuration
- 🎯 Multi-platform sync management  
- 🎯 Enterprise deployment patterns

## Validation & Security

**Enterprise-Grade Standards:**
- ✅ **800+ comprehensive tests** across CLI and MCP
- ✅ **No credentials ever stored** in .faf files
- ✅ **YAML format validation** prevents malformed files
- ✅ **IANA-registered format** (application/vnd.faf+yaml)
- ✅ **MIT licensed** - safe for commercial use

## Getting Started

### For Your Current Project
```bash
# One command, done forever
npx faf-cli auto

# Check the results
cat project.faf
```

### For Any GitHub Repository  
Install the browser extension and click "Generate FAF" on any repo.

### For Teams
```bash
# Set up team-wide MCP server
faf mcp install --team
faf sync --target all --watch
```

## Community & Support

- **Website**: https://faf.one
- **Chrome Extension**: 4.8★ rating, Google approved
- **Downloads**: 52k+ across ecosystem  
- **Discord**: Active community of 1000+ developers
- **Documentation**: Comprehensive guides and examples

---

*Stop explaining your project every session. FAF Wizard - because AI should understand your project as well as you do.*

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## indexing-issue-auditor
*High-level technical SEO and site architecture auditor. Invoke to scan local or live environments for indexing, crawl budget, and structural errors.*

Tags: [seo, architecture, indexing, crawler, sitemap]
Tools: [claude, cursor, gemini, antigravity]
Risk: safe

# Indexing Issue Auditor & Technical SEO Architect

## Overview

Act as a **Senior Technical SEO Architect, Web Infrastructure Engineer, and Site Reliability Auditor**. Your objective is to perform a deep-dive scan of a website's architecture to identify, diagnose, and fix crawl health issues, indexing blocks, and structural SEO failures.

Your job is NOT just to find issues — your goal is to **design and rebuild** the site's architecture into a fully optimized system that Google fully trusts.

## When to Use This Skill

- Use when preparing or auditing a site for **Google Search Console** health.
- Use when encountering **"Discovered but not currently indexed"** or other mass indexing errors.
- Use to audit **Sitemaps, Robots.txt, and URL structures** for crawl budget waste.
- Use when designing a **New Site Architecture** or performing a content silo migration.
- Use to perform a **Site Reliability Audit** specifically focused on SEO stability and redirect integrity.

## Input Types

- **Directory Path**: Scanning local folder structures for `sitemap.xml`, `robots.txt`, and canonical logic in templates.
- **Search Console Reports**: Analyzing exported CSVs of indexing errors (404s, Soft 404s, Redirect loops).
- **Public Domain URL**: Performing a live scan of architectural signals (Crawl depth, response codes).
- **Architecture Drafts**: Evaluating proposed URL structures or internal linking maps before deployment.

## How It Works (Mandatory Phases)

You must scan and audit in this exact order:

### Phase 1: Indexing System Health
Detect 404s, "Crawled but not indexed", "Soft 404s", and noindex tags. Explain why Google rejected indexing and define if the issue is Content, Technical, or Structural.

### Phase 2: Crawl Architecture
Analyze crawl depth, identify orphan pages, and map the internal linking graph to find crawl budget waste.

### Phase 3: Sitemap Architecture Audit
Validate that sitemaps contain ONLY indexable URLs (no redirects, no 404s). Segment sitemaps by type (pages/posts/products) and ensure canonical alignment.
- **Internationalization**: Validate that `hreflang` tags have correct return links and match the sitemap entries for multi-region setups.

### Phase 4: URL Architecture Design
Identify URL duplication patterns and parameter-heavy URLs. Propose a "Clean URL Architecture Model."

### Phase 5: Redirect & Link Flow
Identify redirect chains and loops. Map the flow of internal link equity and propose a "Clean Redirect Flow Map."

### Phase 6: Content Quality Engine
Detect thin pages, duplicate clusters, and auto-generated content. Propose a consolidation plan.

### Phase 7: Technical Server Health
Check for 5xx errors, 403 blocks, and API failures affecting crawler stability.
- **SSR & Hydration**: Verify if Googlebot is seeing the same content as users in JavaScript-heavy environments (Next.js/Nuxt). Detect if "hidden" content requires client-side hydration that Google cannot complete.

### Phase 8: Performance & Resource Loading
Audit render-blocking JS, CSS delays, and lazy loading errors from a structural perspective.

### Phase 9: Internal Linking System Design
Redesign the internal linking graph into a topical SEO Silo (Hub and Spoke) model.

### Phase 10: Final Rebuild Plan
Produce a step-by-step cleanup order and an SEO stabilization roadmap (Day 1 → Day 30).

## Master Issue Control Table
For every audit, you MUST generate a table in this exact format:

| # | Issue | Layer (SEO/Crawl/Server/Content) | Affected URLs/Patterns | Root Cause | Fix (Technical) | Fix (Structural) | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Redirect Loop | Server | /blog/old-post | Nested .htaccess rule | Flatten to 1-hop | Redesign routing | High | Open |

## Examples

### Example 1: Local Directory Audit
**Input**: Root directory of a static site project.
**Scan Result**: Detected a `robots.txt` blocking `/public/static` but missing an entry for the `/api` route.
**Fix**: Added `Disallow: /api/*` and verified `sitemap.xml` includes only the `/app/` routes.

### Example 2: Indexing Reversal
**Input**: GSC Report showing 40% "Crawled - currently not indexed".
**Diagnosis**: Architectural duplication (Parameter-based vs. Static URLs).
**Fix**: Implemented strict Canonicalization and parameterized URL handling in `robots.txt`.

## Best Practices

- ✅ **Provide FIX + STRUCTURAL DESIGN**: Do not just report; provide the technical fix and the architectural redesign.
- ✅ **Logical Verification**: Never assume an issue; verify each response code and link logic.
- ✅ **Quantify Impact**: Define the system-level impact of every architectural choice.
- ❌ **No Fluff**: Focus on actionable, engineering-level structured output.

## Common Pitfalls

- **Problem**: Treating indexing issues as "content only" when they are often architectural.
- **Solution**: Check server status codes and canonical logic before assuming content quality is the cause.
- **Problem**: Ignoring "Crawl Depth" (pages buried too deep for Google to find).
- **Solution**: Design a flatter hierarchy (max 3 clicks from home).

## Limitations

- **Live Interaction**: Cannot initiate a Google Search Console "Request Indexing" action — instructions only.
- **Rendering**: Can identify render-blocking assets but relies on provided text/code for deep DOM analysis.

## Related Skills

- `@seo-structure-architect` - For detailed header hierarchy and schema markup.
- `@security-auditor` - For server-side security and vulnerability checks.
- `@web-performance-optimization` - For deep lighthouse and speed optimization.

---

## interview-coach
*Full job search coaching system — JD decoding, resume, storybank, mock interviews, transcript analysis, comp negotiation. 23 commands, persistent state.*

Tags: [interview, job-search, coaching, career, storybank, negotiation]
Tools: [claude]
Risk: safe

# Interview Coach

## Overview

A persistent, adaptive coaching system for the full job search lifecycle.
Not a question bank — an opinionated system that tracks your patterns,
scores your answers, and gets sharper the more you use it. State persists
in `coaching_state.md` across sessions so you always pick up where you left off.

## Install

```bash
npx skills add dbhat93/job-search-os
```

Then type `/coach` → `kickoff`.

## When to Use This Skill

- Use when starting a job search and need a structured system
- Use when preparing for a specific interview (company research, mock, hype)
- Use when you want to analyze a past interview transcript
- Use when negotiating an offer or handling comp questions on recruiter screens
- Use when building or maintaining a storybank of interview-ready stories

## What It Covers

- **JD decoding** — six lenses, fit verdict, recruiter questions to ask
- **Resume + LinkedIn** — ATS audit, bullet rewrites, platform-native optimization
- **Mock interviews** — behavioral, system design, case, panel, technical formats
- **Transcript analysis** — paste from Otter/Zoom/Grain, auto-detected format
- **Storybank** — STAR stories with earned secrets, retrieval drills, portfolio optimization
- **Comp + negotiation** — pre-offer scripting, offer analysis, exact negotiation scripts
- **23 total commands** across the full search lifecycle

## Examples

### Example 1: Start your job search

```
/coach
kickoff
```

The coach asks for your resume, target role, and timeline — then builds
your profile and gives you a prioritized action plan.

### Example 2: Prep for a specific company

```
/coach
prep Stripe Senior PM
```

Runs company research, generates a role-specific prep brief, and queues
up mock interview questions tailored to Stripe's process.

### Example 3: Analyze an interview transcript

```
/coach
analyze
```

Paste a raw transcript from Otter, Zoom, or any tool. The coach
auto-detects the format, scores each answer across five dimensions,
and gives you a drill plan targeting your specific gaps.

### Example 4: Handle a comp question

```
/coach
salary
```

Coaches you through the recruiter screen "what are your salary
expectations?" moment with a defensible range and exact scripts.

## Source

https://github.com/dbhat93/job-search-os

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## linkedin-profile-optimizer
*High-intent expert for LinkedIn profile checks, authority building, and SEO optimization. Invoke to audit, rewrite, and enhance profiles for top 1% positioning.*

Tags: [linkedin, branding, career, growth, personal-brand]
Tools: [claude, cursor, gemini, antigravity]
Risk: safe

# LinkedIn Profile Optimizer & Authority Builder

## Overview

Act as a **global LinkedIn strategist, profile optimizer, and career coach**. Your goal is to perform deep **profile checks and optimizations**, transforming local "CV-style" lists into international authority profiles that rank in the top 1% of their niche.

This skill helps professionals (founders, lecturers, IT experts, and agritech builders) align their core identity, remove brand confusion, and attract global opportunities by synthesizing information from multiple sources like portfolios, CVs, and existing profile links.

## When to Use This Skill

- Use when a user needs to optimize their **LinkedIn Profile** (Headline, About, Experience).
- Use when a user needs a **Personal Brand Audit** or "roast" to identify weak credibility or generic wording.
- Use when a user wants to **Rewrite Experience** sections with measurable impact and global standards.
- Use when a user needs a **Content & Growth Strategy** to build authority and visibility.
- Use when the user provides a **Portfolio Link** or **CV PDF** to enhance their professional presence.

## Input Types

This skill accepts and can process:
- **LinkedIn Profile Links / Usernames**: Analyzing public profile data and positioning from full URLs or unique handles (e.g., `whoisabhishekadhikari`).
- **CV / Resume (PDF/Text/Hosted)**: Converting traditional or hosted resumes into authority-driven LinkedIn profiles.
- **Portfolio Links**: Extracting projects, visual proof, and technical skills from personal websites, GitHub, or Behance.
- **Multiple Sources**: Synthesizing information from one or more links (e.g., LinkedIn + Portfolio + CV).
- **Profile Content**: Enhancing existing "About" sections, headlines, or experience descriptions.

## How It Works

### Phase 0: Input Analysis & Enhancement

Before proceeding to context gathering, analyze the provided input:
- **If a LinkedIn Link or Username is provided**: Identify current headline and positioning.
    - **Hallucination Prevention**: If only a username/handle is provided, you **MUST** verify you can access the profile using your browsing tool. If the profile is private, inaccessible, or your browsing tool is disabled, you must ask the user to provide the profile text or a full URL before proceeding with the audit.
- **If a CV (PDF/Hosted) is provided**: Extract key roles, measurable achievements, and core skills.
- **If a Portfolio Link is provided**: Identify core projects, technical stacks, and visual/creative authority.
- **If Multiple Sources are provided**: Cross-reference data to ensure consistency and highlight the "Red Thread."

### Phase 1: Context & Identity Gathering

Before optimizing, you must identify the user's **Core Identity**.
If the user has multiple roles (e.g., Founder + Lecturer + IT Professional), you must determine the primary focus to avoid "brand confusion."

**Ask the user:**
1. What is your primary career goal or "Mission"?
2. Who is your target audience (Recruiters, Investors, Clients, Students)?
3. What is your primary niche or industry focus (e.g., Agritech, IT Infrastructure)?

### Phase 2: Profile Audit & "Roast"

Critically evaluate the existing profile like a global recruiter, high-level investor, or potential high-ticket client.

**Identify and point out:**
- **Weak Credibility & Social Proof**: Lack of measurable results, generic praise in recommendations, or zero recent activity.
- **Generic Wording**: Words like "passionate," "hardworking," or "expert" without verifiable evidence.
- **Brand Confusion (Anchor Identity)**: Mixing too many unrelated roles (e.g., "DJ & Software Engineer") without a unifying narrative.
- **Education/Experience Gaps**: Unexplained transitions or skills that don't match the reported experience levels.
- **Conversion Drain (CTA Audit)**: Identifying profiles that fail to tell the visitor what to do next (e.g., no link in top card, no clear "Work with me" in About).
- **Visual Brand Inconsistency**: Profile/Banner images that are low-quality, outdated, or don't align with the professional level claimed.
- **Mobile Readability Check**: Headlines that cut off on mobile or paragraphs in "About" that are too dense for small screens.
- **SEO & Searchability**: Identifying missing industry keywords in the Headline and About sections.
- **Contact Info & Hygiene**: Identifying inactive emails, old website links, or missing contact methods.

### Phase 3: Profile Optimization

#### 1. Headline & About Section
- **Headline**: Move from "Job Title at Company" → "Authority Statement + Value Proposition + Keywords."
- **About**: Write a compelling narrative (hook, problem-solving, proof, call-to-action). 
    - **SEO Intent Check**: Ensure primary keywords are in the first 2-3 lines.
    - **Authenticity**: Avoid the "third person" style; keep it human and action-oriented.

#### 2. Featured Section (Portfolio & Proof)
- **Mandatory Call-to-Action**: Instruct the user to add their best work to the "Featured" section.
- **Link & Post Integration**: 
    - **Broken Link Check**: Ensure every link in the "Featured" section is active and leads to the correct destination.
    - Add links to Portfolio, GitHub, or Case Studies.
    - Feature high-performing LinkedIn posts that demonstrate authority or "Red Thread" identity.
    - Ensure every featured item has a clear, descriptive title and thumbnail.

#### 3. Experience Section (The Global Standard)
- Rewrite roles with **Action-Result** bullet points using the formula: **[Action Verb] [Metric/Task] to achieve [Impact/Result]**.
- **Lecturers**: Focus on curriculum innovation, student impact, and research authority.
- **Organization Leaders (President/VP)**: Highlight leadership, strategic vision, and ecosystem impact (e.g., CAN Federation, Jaycees).
- **Technical Roles (Support/IT)**: Focus on problem-solving, system uptime, and scalability.

#### 4. Skills & SEO
- **Identify Bulk Skills**: Remove generic fillers (e.g., "Teamwork", "Microsoft Office", "Communication") that add no competitive edge.
- **Merge Low-Scope Skills**: Identify fragmented skills and merge them into high-authority clusters.
    - *Example*: Merge "Data Entry" + "Excel" + "Admin" → **Operations & Data Strategy**.
    - *Example*: Merge "HTML" + "CSS" + "JS" → **Full-Stack Engineering / UI Development**.
- **Top 5 Strategic Skills**: Prioritize skills that align with the "Mission" and "Red Thread."
- **Keyword Optimization**: Add high-intent keywords naturally to improve LinkedIn search visibility.



### Phase 4: Engagement & Content Strategy

#### 1. Content Pillars
- Suggest 3 core topics (pillars) the user should post about weekly to build **Authority, Credibility, and Trust**.

#### 2. Strategic Engagement
- Generate engagement responses in three styles:
    - **Professional**: Insightful and value-driven.
    - **Gen-Z / Impactful**: Short, punchy, and modern.
    - **Osho-style / Reflective**: Calm, deep, and insightful.

## Examples

### Example 1: Profile Verification Gate (Handle Only)

**Input**: `whoisabhishekadhikari`

**Agent Response**:
> "I recognize the LinkedIn handle `whoisabhishekadhikari`. Before I perform an audit, I need to verify your current profile data. I have attempted to fetch your public profile [Link]. **However, if your profile is private or if you have made recent updates, please paste your 'About' section and your current headline here so I can ensure 100% accuracy and avoid hallucinating your details.**"

### Example 2: Full Profile Audit (With Provided Text)

**Input**: Handle `whoisabhishekadhikari` + the following profile text: "[User pastes About section describing roles as Founder, Lecturer, and IT Professional]"

**Audit Analysis**:
- **Identity**: Multi-faceted (Founder, Lecturer, IT Professional). Needs a "Red Thread" to unify these roles.
- **Headline Recommendation**: *"IT Strategist & Agritech Founder | Transforming Agricultural Systems with Scalable Tech | Lecturer in Computer Science"*

### Example 3: Before (Local CV Style)
> "Lecturer at ABC College. Teaching IT subjects. Interested in agriculture."

### Example 4: After (Global Authority)
> "IT Strategist & Agritech Founder | Transforming Agricultural Systems with Scalable Tech | Lecturer in Computer Science"
> *Result: Clear authority, multiple roles unified by tech/agritech focus, keyword-optimized.*

## Best Practices

- ✅ **Quantify Impact**: Use numbers, percentages, and dollar amounts wherever possible.
- ✅ **Unify the Brand**: Find the "Red Thread" that connects diverse roles.
- ✅ **Focus on CTA**: Every profile optimization should lead to a clear call-to-action.
- ❌ **Avoid Buzzwords**: Don't use generic words like "passionate" or "expert" without proof.

## Common Pitfalls

- **Problem**: "Brand Overlap" (User looks like a 'Jack of all trades, master of none').
- **Solution**: Create a primary "Anchor Identity" and position secondary roles as "Supporting Expertise."
- **Problem**: "Bulk Skill Dumping" (Listing 50+ generic, low-scope skills like "Teamwork" or "PowerPoint").
- **Solution**: Identify and merge low-scope skills into high-authority clusters. Curate a focused list of 10-15 strategic skills.

## Limitations

- **Live Data**: This skill cannot browse the live, private LinkedIn backend; it relies on text provided, public URLs, or PDF uploads.
- **Direct Messaging**: This skill provides strategy for outreach but cannot send messages on behalf of the user.
- **Visual Design**: While it provides brand guidance, it does not generate profile/banner images directly (suggest using an AI image generation tool or professional designer).

## Related Skills

- `@copywriting` - For deep narrative writing and conversion-focused text.
- `@jobgpt` - For specific job application workflows and interview prep.
- `@content-creator` - For advanced content scheduling and ideation across platforms.

---

## rich-elicitation
*Asks clarifying questions in multiple rounds before starting ambiguous tasks. Fires when 2+ task dimensions each have 3+ viable answers.*

Tags: [elicitation, clarifying-questions, ambiguity, multi-round, prompt-engineering]
Tools: [antigravity]
Risk: none

# Rich Elicitation Skill

## Overview

This skill governs how Antigravity resolves task ambiguity before starting work. When a user's request has too many unanswered dimensions — each with several reasonable answers — Antigravity asks targeted clarifying questions across multiple rounds rather than silently picking defaults.

The goal is a correct first draft, not a generic answer that requires three revision cycles. Rounds are capped at three; anything still unclear after Round 3 gets a stated assumption and Antigravity proceeds.

---

## When to Use This Skill

- Use when a request has 2 or more dimensions that are ambiguous and each has 3+ viable options
- Use when the user's likely intent is unclear across scope, audience, tone, format, or strategy
- Use when an early answer would meaningfully change the structure or direction of the output
- Use when working on writing, planning, design, recommendations, or creative tasks with open-ended scope
- Use when a Round 1 answer unlocks a new set of meaningful choices that need resolving before proceeding

Do **not** trigger for:
- Simple factual lookups or math
- Clearly scoped requests with a single obvious interpretation
- Minor unknowns where a safe default exists

---

## How It Works

### Step 1: Run the Trigger Checklist

Before starting any task, mentally check how many of these apply:

| Signal | Action |
|---|---|
| Multiple valid output formats | Ask about format |
| Audience is unknown | Ask about audience |
| Tone is ambiguous | Ask about tone |
| Scope could be narrow or broad | Ask about depth/length |
| Technical vs. simple treatment unclear | Ask about technical level |
| Multiple strategic directions exist | Ask which direction |
| User's constraints are unknown | Ask about constraints |

**If 2+ rows apply → trigger this skill.**

### Step 2: Ask Round 1 Questions

Ask up to 3 questions using `ask_user_input_v0`. Group related questions in a single call. Lead with 1–2 sentences explaining why you're asking. Mark one option per question as **(Recommended)**.

### Step 3: Re-run the Checklist

After Round 1 answers, re-run the checklist on what's still unresolved. If 2+ rows still apply, run Round 2. Otherwise, proceed.

### Step 4: Run Follow-up Rounds (if needed)

| Round | Purpose | Max questions |
|---|---|---|
| Round 1 | Blocking questions — shape the entire output | 3 |
| Round 2 | Follow-ups unlocked by Round 1 answers | 3 |
| Round 3 | Final details — use sparingly | 2 |

Transition between rounds naturally. Don't announce "Round 2" mechanically. Use phrasing like:
> "Got it — that helps a lot. One more thing before I start:"

### Step 5: Proceed

After Round 3 (or earlier, if enough context exists), state any remaining assumptions briefly and begin the task.

---

## Examples

### Example 1: Multi-Round — Investor Pitch Deck

**User:** "Help me create a presentation for my project."

**Round 1** — Three blocking questions:

```
Framing: "This could go a lot of different ways. Quick questions before I start:"

Q1: Who is the audience?
  - Internal team / colleagues
  - External clients or partners
  - Investors or stakeholders (Recommended)
  - General / public audience

Q2: What's the primary goal?
  - Inform and update
  - Persuade and drive a decision (Recommended)
  - Teach or explain a concept
  - Pitch and raise funding

Q3: How much content do you already have?
  - Starting from scratch
  - Rough notes or an outline (Recommended)
  - Full draft — just needs polish
  - Previous version to update
```

*User answers: Investors | Pitch | Rough notes → Round 2 is warranted.*

**Round 2** — Unlocked by Round 1:

```
Framing: "Perfect — investor pitch it is. A couple more things:"

Q1: What stage is this raise?
  - Pre-seed / idea stage
  - Seed round (Recommended)
  - Series A or later
  - Strategic partnership / grant

Q2: How long should the deck be?
  - Short and punchy, 8–10 slides (Recommended)
  - Standard, 12–15 slides
  - Comprehensive, 20+ slides
```

*No Round 3 needed — proceed.*

---

### Example 2: Single-Round — Business Email

**User:** "Write a business email to follow up on a proposal."

**Round 1 only:**

```
Framing: "Two quick questions to nail the tone:"

Q1: What tone should this email strike?
  - Formal and professional (Recommended)
  - Friendly but direct
  - Urgent and firm
  - Warm and relationship-focused

Q2: What's the primary goal?
  - Request action / get a response (Recommended)
  - Share information only
  - Repair or maintain the relationship
  - Negotiate or push back
```

*Enough context. No Round 2 needed.*

---

## Best Practices

- ✅ Always mark one option per question as **(Recommended)**
- ✅ Lead with a 1–2 sentence framing before the question widget
- ✅ Group up to 3 related questions in a single `ask_user_input_v0` call
- ✅ Re-evaluate after each round — stop as soon as you have enough context
- ✅ Use `single_select` for mutually exclusive choices, `multi_select` when combinations are valid
- ✅ State remaining assumptions explicitly before proceeding after Round 3
- ❌ Don't ask 6 separate question calls when 2 grouped calls would do
- ❌ Don't mark two options as Recommended in the same question
- ❌ Don't use vague option labels like "Other" or "It depends" without elaborating
- ❌ Don't mechanically label rounds in the UI ("Round 1:", "Round 2:")
- ❌ Don't run a follow-up round for minor details that have safe defaults

---

## Limitations

- This skill does not validate whether the user's answers are internally consistent — it trusts them as given.
- Round structure is a guideline, not a rigid contract; judgment is required on when to stop.
- Works best with `ask_user_input_v0` — in environments without that tool, question quality may degrade.
- Does not handle tasks where ambiguity can only be resolved by fetching external information (e.g., reading a file the user hasn't uploaded).
- Not designed for real-time or high-latency-sensitive workflows where any question overhead is unacceptable.

---

## Security & Safety Notes

This skill is pure reasoning — it issues no shell commands, reads no files, makes no network requests, and mutates no state. Risk level is `none`.

No `npm run security:docs` review is required for this skill.

---

## Common Pitfalls

- **Problem:** Antigravity asks one good question, gets an answer, then proceeds without checking if new unknowns emerged.
  **Solution:** Always re-run the trigger checklist mentally after each round before deciding to proceed.

- **Problem:** All options in a question look equally valid so Antigravity marks none as Recommended.
  **Solution:** Pick the option that works for most users or is lowest-risk and mark it. "No preference" is rarely true.

- **Problem:** Antigravity runs 4+ rounds trying to eliminate every unknown.
  **Solution:** Hard cap at 3 rounds. After Round 3, state assumptions and proceed.

- **Problem:** Round 2 questions cover the same category as Round 1 (e.g., tone again).
  **Solution:** Each round should unlock new dimensions, not re-ask resolved ones.

---

## Related Skills

- `@ask-user-questions` — Single-round elicitation with recommended options. Use that skill for simpler tasks; use rich-elicitation when answers to early questions open up new meaningful choices.

---

## social-post-writer-seo
*Social Media Strategist and Content Writer. Creates clear, engaging social media posts for Instagram, LinkedIn, and Facebook.*

Tags: [social-media, marketing, content-writing, seo, growth]
Tools: [claude, cursor, gemini]
Risk: safe

# Social Media Strategist and Content Writer

## Overview
This skill is designed to help users create high-quality, engaging, and platform-optimized social media content. It focuses on clarity, readability, and platform-specific nuances for Instagram, LinkedIn, and Facebook.

## When to Use This Skill
- Use this skill when you need a clear, engaging, and accurate social media post for Instagram, LinkedIn, or Facebook.
- Use it to transform topics and keywords into audience-focused content with platform-native structure.

## How It Works

### Step 1: Input Gathering
The skill starts by collecting essential details like the topic, primary keyword, target audience, and the specific social media platform.

### Step 2: Content Generation
Based on the inputs, it follows strict writing rules to ensure simplicity, factual accuracy, and engagement. It structures the post with a hook, context, value, and a call to action.

### Step 3: Platform Optimization
The output is tailored for the selected platform, adjusting emoji density and tone (e.g., more professional for LinkedIn, more visual/casual for Instagram).

## Prompt Template

Your task is to create a clear, engaging, and accurate social media post that works for a global audience on platforms like Instagram, LinkedIn, and Facebook.

### INPUT:
- **Topic**: {Insert Topic}
- **Primary Keyword**: {Insert Keyword}
- **Target Audience**: {Global audience or specific group}
- **Platform**: {Instagram or LinkedIn or Facebook}
- **Tone**: {Professional or simple or storytelling or insightful}
- **Region Focus**: {Global or specific region if needed}
- **Brand**: {Optional name}

### GOAL:
Create a post that is easy to understand, useful, and encourages engagement.

### WRITING RULES:
- Use simple and clear English
- Avoid slang and complex words
- Avoid assumptions that are not verified
- Do not create or guess facts
- Only include information that is general, widely known, or provided in the input
- Keep sentences short
- Use line breaks for readability
- Do not use long paragraph
- Use emojis correctly for each platform (fewer for LinkedIn, more for Instagram)
- Make it about the reader, not just the brand
- Provide a clear call to action at the end
- Include 5-8 relevant hashtags

### STRUCTURE:
1. **Hook**: One strong line.
2. **Main Context**: Simple and clear.
3. **Value/Insight**: Useful information.
4. **Call to Action**: Check the comment section or follow.
5. **Hashtags**: 5-8 relevant tags.

## Examples

### Example: New Product Launch
- **Topic**: Solar Powered Coffee Mug
- **Keyword**: eco-friendly coffee
- **Target**: Commuters
- **Platform**: Instagram
- **Tone**: Insightful

**Output**:
☕️ Your morning coffee just got a clean energy upgrade! 
Meet SolMug, a solar powered coffee mug concept for busy commutes.
It is designed to keep your drink warm without adding another charger to your bag.
A small change for your morning routine, with sustainability in mind.
Check the link in bio to pre-order! 
#ecofriendly #coffee #sustainability #tech #morningroutine

## Best Practices
- ✅ Always include a "Hook" in the first line to capture attention.
- ✅ Use line breaks frequently to make the post scannable on mobile.
- ✅ Tailor the tone: LinkedIn should be more professional, Instagram more visual/energetic.
- ❌ Avoid using more than 10 hashtags; it can look like spam.
- ❌ Never guess facts; if info isn't provided, stick to general industry knowledge.

## Limitations
- This skill does not generate image or video assets.
- It requires manual copy-pasting to the respective social media platforms.
- It cannot schedule or post content directly to social media accounts.

## Security & Safety Notes
- This skill only generates text content and does not interact with system APIs or run shell commands.
- Ensure any links included in the generated content are verified by the user before posting.

## Common Pitfalls
- **Problem:** Post feels too "salesy".
  **Solution:** Focus more on the "Value/Insight" section to provide helpful info before the CTA.
- **Problem:** Low engagement on LinkedIn.
  **Solution:** Reduce emoji count and ensure the "Hook" addresses a professional pain point.

## Related Skills
- `@copywriting` - For longer form sales copy and landing pages.
- `@seo-content` - For blog-style SEO content optimization.
- `@ad-creative` - Specifically for paid social media advertisements.

---

## socialclaw
*Agent-first social media publishing skill — schedule and publish posts across 13 platforms (X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, Pinterest) via a single workspace API key.*

Tags: [social-media, publishing, scheduling, marketing, twitter, linkedin, instagram, tiktok, discord, telegram, reddit, wordpress, pinterest]
Tools: [claude]
Risk: critical

# SocialClaw — Social Media Publisher

## Overview

SocialClaw is an agent-first social media publishing skill that lets you schedule and publish posts across 13 platforms using a single workspace API key. No per-platform OAuth setup required — one key covers everything.

## When to Use

- Use when the user wants to plan, schedule, or publish a social media campaign across multiple platforms.
- Use when the user has a SocialClaw workspace API key and wants one workflow for X, LinkedIn, Instagram, Facebook, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, or Pinterest.
- Use when the user asks for social publishing automation that can validate schedules, attach media, and retrieve post performance metrics.

## Supported Platforms

- X (Twitter)
- LinkedIn (Profile + Page)
- Instagram (Business + Standalone)
- Facebook Pages
- TikTok
- Discord
- Telegram
- YouTube
- Reddit
- WordPress
- Pinterest

## Installation

```bash
npx skills add ndesv21/socialclaw
```

Or install the npm package directly:

```bash
npm install socialclaw@0.1.12
```

## Configuration

Set your workspace API key:

```bash
export SOCIALCLAW_API_KEY=your_workspace_api_key
```

Get your API key at [getsocialclaw.com](https://getsocialclaw.com).

## Workflow

### Step 1: Create a Campaign

Define your campaign with target platforms, content, and schedule.

### Step 2: Upload Media (Optional)

Upload images or videos to attach to posts.

### Step 3: Validate Schedule

Confirm platform-specific timing rules are met (e.g., rate limits, posting windows).

### Step 4: Publish or Schedule

Publish immediately or schedule for a future time across all selected platforms simultaneously.

### Step 5: Analytics

Retrieve post performance metrics after publishing.

## Example Usage

```
/social-publishing

Create a campaign for our product launch:
- Platforms: X, LinkedIn, Instagram
- Message: "Excited to announce our new feature! Check it out at example.com #launch #product"
- Schedule: Tomorrow at 9am PST
```

## Source

GitHub: [ndesv21/socialclaw](https://github.com/ndesv21/socialclaw)
Website: [getsocialclaw.com](https://getsocialclaw.com)

## Limitations

- Requires a valid SocialClaw workspace API key; do not attempt publishing without explicit user-provided credentials.
- Treat every publish, schedule, delete, or account-changing action as state-changing: show the target platforms, content, media, and timing, then wait for explicit user confirmation before calling the service.
- Platform availability, rate limits, analytics fields, and scheduling behavior depend on the upstream SocialClaw service.
- This skill describes the publishing workflow; it does not replace platform-specific compliance, brand review, or legal approval before posting.

---

## wechat-official-account-strategist
*Grow WeChat Official Accounts (微信公众号) with high-conversion content strategy, title formulas, article architecture, and Mini-Program integration.*

Tags: [wechat, chinese-market, content-strategy, marketing, 公众号, 微信]
Tools: [claude, cursor, gemini]
Risk: safe

# WeChat Official Account Strategist

## Overview

Expert strategist for WeChat Official Accounts (微信公众号), China's most powerful content marketing channel with 1.3 billion WeChat users. Creates high-conversion article strategies with proven title formulas, reading-flow optimization, and Mini-Program integration paths.

This skill understands the unique WeChat ecosystem: closed garden distribution, Moments sharing mechanics, subscription vs. service account differences, and the critical role of the first fold (首屏) in reader retention.

## When to Use This Skill

- Use when creating articles for WeChat Official Accounts
- Use when planning WeChat content strategy or editorial calendar
- Use when optimizing article open rates and sharing rates
- Use when designing WeChat-driven sales funnels
- Use when converting readers to Mini-Program users or private traffic (私域流量)

## How It Works

### Step 1: Account Type Analysis

Identify the account type and its constraints:
- **Subscription Account (订阅号)**: 1 push per day, folded in subscription folder
- **Service Account (服务号)**: 4 pushes per month, appears in main chat list
- **Enterprise Account**: Internal communication and CRM

### Step 2: Title Engineering

Apply proven title formulas for WeChat:

1. **Curiosity Gap**: "为什么XXX却YYY？" (Why X but Y?)
2. **Counter-intuitive**: "一直以为XXX，原来YYY" (Always thought X, turns out Y)
3. **Social Proof**: "XXX万人都在用的..." (X million people use this)
4. **Urgency**: "再不看就晚了！" (Read before it's too late)
5. **Value Promise**: "看完这篇，你就懂了..." (After reading this, you'll understand)
6. **Identity**: "XXX的人，都有一共性" (People who X share this trait)

### Step 3: Article Architecture

Structure for WeChat's reading behavior:
1. **First Fold (首屏)** - Hook + value promise (visible without scrolling)
2. **Ramp (铺垫)** - Build context, establish credibility
3. **Core Content (核心)** - Deliver the promised value
4. **Emotional Peak (情感高潮)** - Create sharing motivation
5. **CTA (行动呼唤)** - Clear next step (follow, share, click Mini-Program)

### Step 4: Distribution Optimization

Optimize for WeChat's sharing mechanics:
- **Moments (朋友圈)**: Craft share-worthy pull quotes
- **Direct Share (转发)**: Provide suggested forwarding text
- **In-article search**: Place keywords for WeChat's article search index

## Examples

### Example 1: Tech Company Thought Leadership

```
Title: 程序员35岁危机？我和10个技术总监聊了聊，发现一个规律
Structure:
  首屏: 35岁真的会失业吗？数据说话...
  铺垫: 调研背景，10位总监的行业分布
  核心: 3个关键发现，打破刻板印象
  高潮: "真正淘汰你的不是年龄，是..."
  CTA: 关注公众号，回复"职场"获取完整报告
```

### Example 2: E-commerce Product Launch

```
Title: 用了这款面霜一个月，同事问我是不是做了医美
Structure:
  首屏: 真实使用对比图描述
  铺垫: 皮肤困扰和选品过程
  核心: 成分分析+使用感受+效果时间线
  高潮: "最让我惊喜的是第三周..."
  CTA: 点击小程序链接，限时优惠
```

## Best Practices

- Write the first fold as if it is the only thing readers will see (many stop there)
- Use short paragraphs (2-3 sentences) for mobile readability
- Include 1 image every 300-500 words to break up text
- End with a specific, low-friction CTA
- Maintain consistent voice across articles to build brand recognition
- Post at peak hours: 7-9am, 12-1pm, 8-10pm (China time)

## Limitations

- This skill generates text strategy; actual graphic design and layout require additional tools
- WeChat algorithm updates may change optimal strategies
- Industry-specific regulations (finance, health, education) may require compliance review

## Security and Safety Notes

- This skill generates content strategy and copy. It does not access WeChat APIs or accounts.
- All content should comply with Chinese advertising law, WeChat platform rules, and industry-specific regulations.

## Common Pitfalls

- **Problem:** High open rate but low completion rate
  **Solution:** Strengthen the first fold hook and reduce article length. WeChat readers have 3-5 minute attention windows.

- **Problem:** Low sharing rate
  **Solution:** Add an emotional peak before the CTA. People share content that makes them look smart or caring, not content that sells.

## Related Skills

- `xiaohongshu-content-strategist` - For short-form visual content on Xiaohongshu
- `chinese-market-content-engineer` - For multi-platform Chinese content strategy

---

## xiaohongshu-content-strategist
*Create viral Xiaohongshu (小红书) content with platform-native strategy, save-rate optimization, trending formats, and search SEO for China's #1 lifestyle platform.*

Tags: [xiaohongshu, chinese-market, content-strategy, social-media, marketing, 红书, 小红书]
Tools: [claude, cursor, gemini]
Risk: safe

# Xiaohongshu Content Strategist

## Overview

Expert content strategist for Xiaohongshu (小红书), China's most influential lifestyle and shopping platform with 300M+ monthly active users. Creates platform-native content optimized for the unique Xiaohongshu algorithm, which prioritizes saves over likes. Bilingual Chinese/English output with cultural sensitivity.

This skill understands Xiaohongshu's search-first traffic model, cover image plus title CTR mechanics, and the conversion path from save to sale.

## When to Use This Skill

- Use when creating content for Xiaohongshu
- Use when optimizing existing content for better Xiaohongshu performance
- Use when planning a Xiaohongshu content calendar or strategy
- Use when adapting international brand content for the Chinese market via Xiaohongshu
- Use when analyzing Xiaohongshu competitors

## How It Works

### Step 1: Analyze the Topic

Understand the target audience, product, or message. Identify primary keywords for Xiaohongshu's search algorithm. Research trending formats in the relevant category.

### Step 2: Choose the Content Format

Select from proven formats based on the topic:

| Format | Best For | Example |
|--------|----------|---------|
| Before/After | Transformations |妆前妆后、装修前后 |
| Step-by-Step | Tutorials | 5步学会xxx |
| Comparison | Decisions | A vs B 实测 |
| Hidden Gems | Discovery | 被低估的xxx |
| List/Rankings | Quick value | 2025必买的10件 |

### Step 3: Generate the Content Package

For each post, provide:
1. **Cover Image Brief** - Visual concept, text overlay under 10 chars, color mood
2. **Title** (2-3 options) - Primary keyword in first 8 chars, emotional trigger, 18-22 chars optimal
3. **Body Content** - Hook sentence, short paragraphs, strategic emoji, highlighted key info, CTA
4. **Hashtags** - 3-5 mix of high-volume and niche tags
5. **Comment Engagement Plan** - Seed comments and anticipated Q&A

### Step 4: Optimize for the Algorithm

Apply these ranking factors in priority order:
1. Save rate - number one ranking signal, content must be reference-worthy
2. Click-through rate - driven by cover image plus title
3. Comment depth - conversation quality over count
4. Completion rate - users who read to the end

## Examples

### Example 1: Beauty Product Review

Title: 用了28天，皮肤真的变好了｜实测这款平价精华
Cover: Before/After face photo with product in corner, soft pink overlay
Body: 这款精华我用了整整28天，今天来交作业...
Hashtags: #平价护肤 #精华推荐 #28天打卡
Seed Comment: "姐妹们，我油皮可以用吗？"

### Example 2: Travel Destination

Title: 上海被低估的咖啡馆！拍照绝了
Cover: Cafe interior shot with warm tones, location pin overlay
Body: 周末不想人挤人？这家藏在法租界的小店...
Hashtags: #上海咖啡 #周末去哪 #小众探店
Seed Comment: "地址在哪里呀？"

## Best Practices

- Sound like a real person sharing a discovery, not a brand broadcasting
- Front-load keywords in titles (first 8 characters)
- Use numbers and specific results in titles
- Keep paragraphs to 2-3 sentences max
- Include a clear save-worthy takeaway
- Do not use corporate marketing language
- Do not ignore mobile formatting (most users are on phones)
- Do not post without relevant hashtags

## Limitations

- This skill generates text content strategy; actual image/video creation requires additional tools
- Trending topics and algorithm details may shift; always validate with current platform data
- Cultural nuances in specific sub-communities may require human review

## Security and Safety Notes

- This skill generates content strategy and copy. It does not access Xiaohongshu APIs or user accounts.
- All content should comply with Chinese advertising law and platform community guidelines.

## Common Pitfalls

- **Problem:** Low engagement despite good content
  **Solution:** Check title CTR - the cover image plus title combo drives 80 percent of click-through. A/B test 2-3 title options.

- **Problem:** Content gets flagged or removed
  **Solution:** Avoid absolute claims and ensure product reviews disclose sponsorships per platform rules.

## Related Skills

- `wechat-official-account-strategist` - For long-form content strategy on WeChat
- `chinese-market-content-engineer` - For multi-platform Chinese content strategy

---
