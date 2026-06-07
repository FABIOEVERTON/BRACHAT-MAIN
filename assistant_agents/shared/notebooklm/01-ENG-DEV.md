# Engineering & Development
## 46 skills
---

## agenttrace-session-audit
*Audit local AI coding-agent sessions with agenttrace for cost, tool failures, latency, anomalies, health, diffs, and CI gates.*

Tags: [ai-coding, observability, cost-tracking, session-analysis]
Tools: [claude, cursor, gemini, codex-cli]
Risk: safe

# agenttrace Session Audit

## Overview

Use this skill to inspect local AI coding-agent sessions with
[agenttrace](https://github.com/luoyuctl/agenttrace). It focuses on the process
behind a run: token and cost spikes, tool failures, retry loops, latency gaps,
anomalies, health scores, and session-to-session diffs.

agenttrace is local-first and reads session logs from tools such as Claude Code,
Codex CLI, Gemini CLI, Aider, Cursor exports, OpenCode, Qwen Code, Kimi, and
generic JSON or JSONL traces.

## When to Use This Skill

- Use when a user asks why an AI coding run was slow, expensive, shallow, or unreliable.
- Use when reviewing local agent logs before retrying a failed or suspicious task.
- Use when building a lightweight CI health gate for AI-assisted coding sessions.
- Use when comparing two attempts and looking for changed tool paths, retries, or cost patterns.

## How It Works

### Step 1: Discover Available Sessions

Prefer an installed `agenttrace` binary when it is available on `PATH`. If the
current repository is `luoyuctl/agenttrace`, use `go run ./cmd/agenttrace`
instead.

```bash
agenttrace --doctor
agenttrace --overview
```

If no sessions are detected, report the directories checked by `--doctor` and
ask for the exported session file or log directory.

### Step 2: Produce a Human-Readable Audit

Use Markdown when the user wants a concise report they can inspect or share.

```bash
agenttrace --overview -f markdown -o agenttrace-overview.md
```

In the report, lead with the highest-risk sessions and explain why they matter:
critical anomalies, repeated tool failures, token or cost waste, long latency
gaps, low health scores, and suspiciously shallow sessions.

### Step 3: Inspect One Session or Directory

Use the latest session for a quick check, or pass an explicit export path when
the user provides one.

```bash
agenttrace --latest
agenttrace --latest -f json
agenttrace path/to/session-or-export.json
agenttrace --overview -d path/to/session-dir
```

### Step 4: Compare Attempts When Semantics Matter

Token and latency metrics can look healthy even when an agent confidently takes
the wrong implementation path. When the risk is semantic drift, pair the trace
audit with a diff against a previous or known-good attempt.

Look for:

- changed files or commands that diverge from the intended task
- missing tests or verification steps compared with the reference attempt
- repeated edits around the same files without a clear reason
- lower cost that came from skipping necessary exploration

### Step 5: Add Automation Gates

For CI or repeatable team workflows, use JSON output or health thresholds.

```bash
agenttrace --overview -f json -o agenttrace-overview.json
agenttrace --overview --fail-under-health 80 --fail-on-critical --max-tool-fail-rate 15
```

Tune thresholds to the project. A strict gate is useful for critical workflows;
a reporting-only command is better while the team is learning its baseline.

## Examples

### Quick Local Review

```bash
agenttrace --overview
agenttrace --latest
```

Use this after a long coding-agent run to decide whether the next prompt should
split the task, avoid a failing tool path, add missing tests, or reset context.

### CI Health Check

```bash
agenttrace --overview --fail-under-health 80 --fail-on-critical
```

Use this when agent session logs are available in CI and the team wants a simple
guard against critical anomalies or unhealthy runs.

## Best Practices

- Start with `--doctor` when session discovery is uncertain.
- Report missing fields plainly; do not invent cost, model, latency, or health data.
- Treat prompts, code, and session contents as private local data.
- Prefer JSON output for automation and Markdown output for human review.
- Use trace metrics for process failures and diff/reference review for semantic drift.

## Limitations

- agenttrace can only analyze logs that are present locally or provided as exports.
- Some agents do not expose enough fields to infer cost, model, cache use, or latency.
- Healthy trace metrics do not prove the final code is correct; still run tests and review diffs.
- CI gates should start as advisory until the team understands normal baseline behavior.

## Security & Safety Notes

- Do not upload private session logs to external services unless the user explicitly approves it.
- Do not overwrite user reports unless they requested that exact output path.
- Avoid printing secrets found in prompts, tool output, environment variables, or logs.

## Common Pitfalls

- **Problem:** No sessions are found.
  **Solution:** Run `agenttrace --doctor`, then point agenttrace at the exported file or log directory.

- **Problem:** A run looks cheap and fast but produced the wrong refactor.
  **Solution:** Compare the session against a prior attempt or known-good diff; cost metrics alone will miss semantic drift.

- **Problem:** CI fails too often after adding a health gate.
  **Solution:** Start with JSON or Markdown reporting, inspect normal baselines, then tighten thresholds gradually.

## Related Skills

- `@langfuse` - Use for production LLM application tracing and evaluation.
- `@observability-engineer` - Use for broader service monitoring, SLOs, and incident workflows.

---

## ai-engineering-toolkit
*6 production-ready AI engineering workflows: prompt evaluation (8-dimension scoring), context budget planning, RAG pipeline design, agent security audit (65-point checklist), eval harness building, and product sense coaching.*

Tags: [prompt-engineering, rag, security, evaluation, ai-engineering, llm]
Tools: [claude, cursor, gemini, copilot]
Risk: offensive

# AI Engineering Toolkit

## Overview

A collection of 6 structured, expert-level workflows that turn your AI coding assistant into a senior AI engineering partner. Each skill encodes a repeatable methodology — not just "ask AI to help," but a step-by-step decision framework with quantitative scoring, checklists, and decision trees.

The key difference from ad-hoc AI assistance: **every workflow produces consistent, reproducible results** regardless of who runs it or when. You can use the scoring systems as team baselines and write them into CI/CD pipelines.

## When to Use This Skill

- Use when evaluating or optimizing LLM system prompts before production deployment
- Use when designing a RAG pipeline and need structured architecture decisions (not just boilerplate code)
- Use when planning token budget allocation across context window zones
- Use when running pre-launch security audits on AI agents
- Use when building evaluation frameworks for LLM applications
- Use when thinking through product strategy before writing code

## How It Works

### Skill 1: Prompt Evaluator

Scores prompts across 8 dimensions (Clarity, Specificity, Completeness, Conciseness, Structure, Grounding, Safety, Robustness) on a 1-10 scale with weighted aggregation to a 0-100 score. Identifies the 3 weakest dimensions, generates targeted rewrites, and re-evaluates. Supports single prompt, A/B comparison, and batch evaluation modes.

### Skill 2: Context Budget Planner

Analyzes token distribution across 5 context zones (System, Few-shot, User input, Retrieval, Output) and produces an optimized allocation plan. Includes a compression strategy decision tree for each zone. Common finding: output zone squeezed to under 6% — this skill catches that before truncation happens.

### Skill 3: RAG Pipeline Architect

Walks through a complete architecture decision tree: document format → parsing strategy → chunking approach (fixed/semantic/recursive) → embedding model selection → retrieval method (vector/keyword/hybrid) → evaluation metrics (Faithfulness, Relevancy, Context Precision). Covers Naive RAG, Advanced RAG, and Modular RAG patterns.

### Skill 4: Agent Safety Guard

> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

Executes a 65-point red-team audit across 5 attack categories: direct prompt injection, indirect prompt injection (via RAG documents), information extraction (system prompt / API key leakage), tool abuse (SQL injection, path traversal, command injection), and goal hijacking. The AI constructs adversarial test prompts for evaluation purposes, asks the user for confirmation before each test phase, judges pass/fail, and generates fix recommendations. All tests are contained within the evaluation context and do not interact with external systems. It is recommended to run audits in a sandboxed environment (Docker/VM).

### Skill 5: Eval Harness Builder

Designs evaluation metric systems for LLM applications. Includes LLM-as-Judge scoring framework with bias mitigation strategies (position bias, verbosity bias, self-enhancement bias). Outputs CI/CD-ready evaluation pipeline templates.

### Skill 6: Product Sense Coach

A 5-phase guided conversation framework: dig into motivation → assess market opportunity → find the path → design scenarios → analyze competition. Useful for thinking through "should we build this?" before writing any code.

## Examples

### Example 1: Prompt Evaluation

Ask: "Evaluate this system prompt"

```
You are a customer support agent. Help users with their questions. Be nice and helpful.
```

Result: Overall score **28/100**. Weakest dimensions: Safety (1/10, zero injection protection), Specificity (2/10, no output format), Structure (2/10, no sections). Auto-rewrite scores **82/100** with added scope boundaries, response format, escalation rules, and safety guardrails.

### Example 2: Security Audit

Ask: "Run a security audit on my customer support agent"

Result: 65 tests executed. 3 critical failures found: Base64-encoded instruction bypass, path traversal via tool calls, system prompt extraction via role-play. Fix recommendations provided for each.

## Best Practices

- ✅ Run prompt-evaluator before any production deployment — set a team baseline (e.g., ≥70/100)
- ✅ Use context-budget-planner early in development, not after hitting truncation issues
- ✅ Run agent-safety-guard as a pre-launch gate, not post-incident
- ✅ Combine skills in sequence: RAG design → context optimization → prompt polish → security audit → eval setup
- ❌ Don't rely on a single dimension score — look at the full profile
- ❌ Don't skip the security audit because "it's just an internal tool"

## Security & Safety Notes

- All skills are read-only analysis and advisory workflows. No skills modify files or make network requests.
- The agent-safety-guard skill constructs adversarial test prompts for evaluation purposes only — these are contained within the evaluation context and do not interact with external systems.
- **agent-safety-guard is classified as an offensive skill**: it generates attack payloads (prompt injection, SQL injection, command injection) for authorized security testing. The skill requires explicit user confirmation before executing each test phase. Run in a sandboxed environment when possible.
- No weaponized payloads are included. All adversarial prompts are educational in nature.

## Installation

```bash
# Via skill install command (Claude Code / WorkBuddy / Cursor)
/skill install -g viliawang-pm/ai-engineering-toolkit

# Manual
git clone https://github.com/viliawang-pm/ai-engineering-toolkit.git
cp -r ai-engineering-toolkit/skills/* ~/.claude/skills/
```

**Repository**: [github.com/viliawang-pm/ai-engineering-toolkit](https://github.com/viliawang-pm/ai-engineering-toolkit)
**License**: MIT

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## api-endpoint-builder
*Builds production-ready REST API endpoints with validation, error handling, authentication, and documentation. Follows best practices for security and scalability.*

Risk: safe

# API Endpoint Builder

Build complete, production-ready REST API endpoints with proper validation, error handling, authentication, and documentation.

## When to Use This Skill

- User asks to "create an API endpoint" or "build a REST API"
- Building new backend features
- Adding endpoints to existing APIs
- User mentions "API", "endpoint", "route", or "REST"
- Creating CRUD operations

## What You'll Build

For each endpoint, you create:
- Route handler with proper HTTP method
- Input validation (request body, params, query)
- Authentication/authorization checks
- Business logic
- Error handling
- Response formatting
- API documentation
- Tests (if requested)

## Endpoint Structure

### 1. Route Definition

```javascript
// Express example
router.post('/api/users', authenticate, validateUser, createUser);

// Fastify example
fastify.post('/api/users', {
  preHandler: [authenticate],
  schema: userSchema
}, createUser);
```

### 2. Input Validation

Always validate before processing:

```javascript
const validateUser = (req, res, next) => {
  const { email, name, password } = req.body;
  
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email required' });
  }
  
  if (!name || name.length < 2) {
    return res.status(400).json({ error: 'Name must be at least 2 characters' });
  }
  
  if (!password || password.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }
  
  next();
};
```

### 3. Handler Implementation

```javascript
const createUser = async (req, res) => {
  try {
    const { email, name, password } = req.body;
    
    // Check if user exists
    const existing = await db.users.findOne({ email });
    if (existing) {
      return res.status(409).json({ error: 'User already exists' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const user = await db.users.create({
      email,
      name,
      password: hashedPassword,
      createdAt: new Date()
    });
    
    // Don't return password
    const { password: _, ...userWithoutPassword } = user;
    
    res.status(201).json({
      success: true,
      data: userWithoutPassword
    });
    
  } catch (error) {
    console.error('Create user error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
```

## Best Practices

### HTTP Status Codes
- `200` - Success (GET, PUT, PATCH)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (validation failed)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (not authorized)
- `404` - Not Found
- `409` - Conflict (duplicate)
- `500` - Internal Server Error

### Response Format

Consistent structure:

```javascript
// Success
{
  "success": true,
  "data": { ... }
}

// Error
{
  "error": "Error message",
  "details": { ... } // optional
}

// List with pagination
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Security Checklist

- [ ] Authentication required for protected routes
- [ ] Authorization checks (user owns resource)
- [ ] Input validation on all fields
- [ ] SQL injection prevention (use parameterized queries)
- [ ] Rate limiting on public endpoints
- [ ] No sensitive data in responses (passwords, tokens)
- [ ] CORS configured properly
- [ ] Request size limits set

### Error Handling

```javascript
// Centralized error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production' 
    ? 'Internal server error' 
    : err.message;
  
  res.status(err.status || 500).json({ error: message });
});
```

## Common Patterns

### CRUD Operations

```javascript
// Create
POST /api/resources
Body: { name, description }

// Read (list)
GET /api/resources?page=1&limit=20

// Read (single)
GET /api/resources/:id

// Update
PUT /api/resources/:id
Body: { name, description }

// Delete
DELETE /api/resources/:id
```

### Pagination

```javascript
const getResources = async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const skip = (page - 1) * limit;
  
  const [resources, total] = await Promise.all([
    db.resources.find().skip(skip).limit(limit),
    db.resources.countDocuments()
  ]);
  
  res.json({
    success: true,
    data: resources,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  });
};
```

### Filtering & Sorting

```javascript
const getResources = async (req, res) => {
  const { status, sort = '-createdAt' } = req.query;
  
  const filter = {};
  if (status) filter.status = status;
  
  const resources = await db.resources
    .find(filter)
    .sort(sort)
    .limit(20);
  
  res.json({ success: true, data: resources });
};
```

## Documentation Template

```javascript
/**
 * @route POST /api/users
 * @desc Create a new user
 * @access Public
 * 
 * @body {string} email - User email (required)
 * @body {string} name - User name (required)
 * @body {string} password - Password, min 8 chars (required)
 * 
 * @returns {201} User created successfully
 * @returns {400} Validation error
 * @returns {409} User already exists
 * @returns {500} Server error
 * 
 * @example
 * POST /api/users
 * {
 *   "email": "user@example.com",
 *   "name": "John Doe",
 *   "password": "securepass123"
 * }
 */
```

## Testing Example

```javascript
describe('POST /api/users', () => {
  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('test@example.com');
    expect(response.body.data.password).toBeUndefined();
  });
  
  it('should reject invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });
});
```

## Key Principles

- Validate all inputs before processing
- Use proper HTTP status codes
- Handle errors gracefully
- Never expose sensitive data
- Keep responses consistent
- Add authentication where needed
- Document your endpoints
- Write tests for critical paths

## Related Skills

- `@security-auditor` - Security review
- `@test-driven-development` - Testing
- `@database-design` - Data modeling

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## astro
*Build content-focused websites with Astro — zero JS by default, islands architecture, multi-framework components, and Markdown/MDX support.*

Tags: [astro, ssg, ssr, islands, content, markdown, mdx, performance]
Tools: [claude, cursor, gemini]
Risk: safe

# Astro Web Framework

## Overview

Astro is a web framework designed for content-rich websites — blogs, docs, portfolios, marketing sites, and e-commerce. Its core innovation is the **Islands Architecture**: by default, Astro ships zero JavaScript to the browser. Interactive components are selectively hydrated as isolated "islands." Astro supports React, Vue, Svelte, Solid, and other UI frameworks simultaneously in the same project, letting you pick the right tool per component.

## When to Use This Skill

- Use when building a blog, documentation site, marketing page, or portfolio
- Use when performance and Core Web Vitals are the top priority
- Use when the project is content-heavy with Markdown or MDX files
- Use when you want SSG (static) output with optional SSR for dynamic routes
- Use when the user asks about `.astro` files, `Astro.props`, content collections, or `client:` directives

## How It Works

### Step 1: Project Setup

```bash
npm create astro@latest my-site
cd my-site
npm install
npm run dev
```

Add integrations as needed:

```bash
npx astro add tailwind        # Tailwind CSS
npx astro add react           # React component support
npx astro add mdx             # MDX support
npx astro add sitemap         # Auto sitemap.xml
npx astro add vercel          # Vercel SSR adapter
```

Project structure:

```
src/
  pages/          ← File-based routing (.astro, .md, .mdx)
  layouts/        ← Reusable page shells
  components/     ← UI components (.astro, .tsx, .vue, etc.)
  content/        ← Type-safe content collections (Markdown/MDX)
  styles/         ← Global CSS
public/           ← Static assets (copied as-is)
astro.config.mjs  ← Framework config
```

### Step 2: Astro Component Syntax

`.astro` files have a code fence at the top (server-only) and a template below:

```astro
---
// src/components/Card.astro
// This block runs on the server ONLY — never in the browser
interface Props {
  title: string;
  href: string;
  description: string;
}

const { title, href, description } = Astro.props;
---

<article class="card">
  <h2><a href={href}>{title}</a></h2>
  <p>{description}</p>
</article>

<style>
  /* Scoped to this component automatically */
  .card { border: 1px solid #eee; padding: 1rem; }
</style>
```

### Step 3: File-Based Pages and Routing

```
src/pages/index.astro          → /
src/pages/about.astro          → /about
src/pages/blog/[slug].astro    → /blog/:slug (dynamic)
src/pages/blog/[...path].astro → /blog/* (catch-all)
```

Dynamic route with `getStaticPaths`:

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<h1>{post.data.title}</h1>
<Content />
```

### Step 4: Content Collections

Content collections give you type-safe access to Markdown and MDX files:

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter(p => !p.data.draft)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---

<ul>
  {posts.map(post => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      <time>{post.data.date.toLocaleDateString()}</time>
    </li>
  ))}
</ul>
```

### Step 5: Islands — Selective Hydration

By default, UI framework components render to static HTML with no JS. Use `client:` directives to hydrate:

```astro
---
import Counter from '../components/Counter.tsx';  // React component
import VideoPlayer from '../components/VideoPlayer.svelte';
---

<!-- Static HTML — no JavaScript sent to browser -->
<Counter initialCount={0} />

<!-- Hydrate immediately on page load -->
<Counter initialCount={0} client:load />

<!-- Hydrate when the component scrolls into view -->
<VideoPlayer src="/demo.mp4" client:visible />

<!-- Hydrate only when browser is idle -->
<Analytics client:idle />

<!-- Hydrate only on a specific media query -->
<MobileMenu client:media="(max-width: 768px)" />
```

### Step 6: Layouts

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}
const { title, description = 'My Astro Site' } = Astro.props;
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content={description} />
  </head>
  <body>
    <nav>...</nav>
    <main>
      <slot />  <!-- page content renders here -->
    </main>
    <footer>...</footer>
  </body>
</html>
```

```astro
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="About Us">
  <h1>About Us</h1>
  <p>Welcome to our company...</p>
</BaseLayout>
```

### Step 7: SSR Mode (On-Demand Rendering)

Enable SSR for dynamic pages by setting an adapter:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel/serverless';

export default defineConfig({
  output: 'hybrid',  // 'static' | 'server' | 'hybrid'
  adapter: vercel(),
});
```

Opt individual pages into SSR with `export const prerender = false`.

## Examples

### Example 1: Blog with RSS Feed

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog');
  return rss({
    title: 'My Blog',
    description: 'Latest posts',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.date,
      link: `/blog/${post.slug}/`,
    })),
  });
}
```

### Example 2: API Endpoint (SSR)

```typescript
// src/pages/api/subscribe.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const { email } = await request.json();

  if (!email) {
    return new Response(JSON.stringify({ error: 'Email required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  await addToNewsletter(email);
  return new Response(JSON.stringify({ success: true }), { status: 200 });
};
```

### Example 3: React Component as Island

```tsx
// src/components/SearchBox.tsx
import { useState } from 'react';

export default function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  async function search(e: React.FormEvent) {
    e.preventDefault();
    const data = await fetch(`/api/search?q=${query}`).then(r => r.json());
    setResults(data);
  }

  return (
    <form onSubmit={search}>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button type="submit">Search</button>
      <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>
    </form>
  );
}
```

```astro
---
import SearchBox from '../components/SearchBox.tsx';
---
<!-- Hydrated immediately — this island is interactive -->
<SearchBox client:load />
```

## Best Practices

- ✅ Keep most components as static `.astro` files — only hydrate what must be interactive
- ✅ Use content collections for all Markdown/MDX content — you get type safety and auto-validation
- ✅ Prefer `client:visible` over `client:load` for below-the-fold components to reduce initial JS
- ✅ Use `import.meta.env` for environment variables — prefix public vars with `PUBLIC_`
- ✅ Add `<ViewTransitions />` from `astro:transitions` for smooth page navigation without a full SPA
- ❌ Don't use `client:load` on every component — this defeats Astro's performance advantage
- ❌ Don't put secrets in `.astro` frontmatter that gets used in client-facing templates
- ❌ Don't skip `getStaticPaths` for dynamic routes in static mode — builds will fail

## Security & Safety Notes

- Frontmatter code in `.astro` files runs server-side only and is never exposed to the browser.
- Use `import.meta.env.PUBLIC_*` only for non-sensitive values. Private env vars (no `PUBLIC_` prefix) are never sent to the client.
- When using SSR mode, validate all `Astro.request` inputs before database queries or API calls.
- Sanitize any user-supplied content before rendering with `set:html` — it bypasses auto-escaping.

## Common Pitfalls

- **Problem:** JavaScript from a React/Vue component doesn't run in the browser
  **Solution:** Add a `client:` directive (`client:load`, `client:visible`, etc.) — without it, components render as static HTML only.

- **Problem:** `getStaticPaths` data is stale after content updates during dev
  **Solution:** Astro's dev server watches content files — restart if changes to `content/config.ts` are not reflected.

- **Problem:** `Astro.props` type is `any` — no autocomplete
  **Solution:** Define a `Props` interface or type in the frontmatter and Astro will infer it automatically.

- **Problem:** CSS from a `.astro` component bleeds into other components
  **Solution:** Styles in `.astro` `<style>` tags are automatically scoped. Use `:global()` only when intentionally targeting children.

## Related Skills

- `@sveltekit` — When you need a full-stack framework with reactive UI (vs Astro's content focus)
- `@nextjs-app-router-patterns` — When you need a React-first full-stack framework
- `@tailwind-patterns` — Styling Astro sites with Tailwind CSS
- `@progressive-web-app` — Adding PWA capabilities to an Astro site

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## brooks-lint
*AI code reviewer grounded in classic software engineering books for catching design smells, coupling issues, and architectural risks.*

Tags: [code-review, architecture, software-design, refactoring, claude-code]
Tools: [claude, codex, cursor, gemini]
Risk: safe

# Brooks Lint

## Overview

Brooks Lint is a Claude Code skill that reviews your code through the lens of 12 classic software engineering books. Instead of checking style rules, it asks: "What would the authors of *The Pragmatic Programmer*, *Clean Code*, and *Designing Data-Intensive Applications* say about this code?"

It synthesizes the principles from landmark engineering books into actionable, structured feedback — catching design smells, tight coupling, missing abstractions, and architectural risks that linters and AI tools typically miss.

Named after Fred Brooks, author of *The Mythical Man-Month* — because the hardest bugs are conceptual, not syntactic.

## The 12 Books

| Book | Key Principles Applied |
|------|----------------------|
| *The Pragmatic Programmer* | DRY, orthogonality, tracer bullets |
| *Clean Code* | Naming, function size, comment clarity |
| *The Mythical Man-Month* | Conceptual integrity, second-system effect |
| *Designing Data-Intensive Applications* | Data consistency, fault tolerance, scalability |
| *A Philosophy of Software Design* | Deep modules, information hiding, complexity |
| *Refactoring* | Code smells, extract method, encapsulation |
| *Working Effectively with Legacy Code* | Seams, characterization tests, dependency breaking |
| *Domain-Driven Design* | Ubiquitous language, bounded contexts, aggregates |
| *Release It!* | Stability patterns, timeouts, bulkheads, circuit breakers |
| *Structure and Interpretation of Computer Programs* | Abstraction, recursion, metalinguistic abstraction |
| *The Art of UNIX Programming* | Modularity, composability, rule of least surprise |
| *Extreme Programming Explained* | YAGNI, simple design, collective ownership |

## When to Use This Skill

- Use when you want architectural feedback beyond what linters provide
- Use before major refactors to identify structural debt
- Use when reviewing code that "works but feels wrong"
- Use when onboarding to a codebase to quickly map risk areas
- Use for design reviews before starting a new module or service

## How It Works

Brooks Lint applies each book's core principles as a review lens:

1. **Smell detection**: Flags violations of DRY, SRP, Law of Demeter, etc.
2. **Coupling analysis**: Identifies tight dependencies and missing abstraction layers
3. **Naming critique**: Applies Clean Code naming rules to variables, methods, classes
4. **Architecture review**: Checks for DDIA-style data consistency and fault tolerance gaps
5. **Stability patterns**: Flags missing timeouts, retries, and circuit breakers (Release It!)
6. **Complexity scoring**: Applies APOSD complexity metrics to identify over-engineered sections

## Installation

```bash
# Install via Claude Code plugin marketplace
# Search: "brooks-lint" in Claude Code > Extensions

# Or install via NPX (Antigravity)
npx antigravity-awesome-skills --claude
# Then invoke: @brooks-lint
```

## Examples

### Example 1: Review a Service Class

```
@brooks-lint review src/services/PaymentService.ts
```

**Brooks Lint output:**
```
[Pragmatic Programmer] DRY violation: payment validation logic duplicated in 3 places
[Clean Code] Method processPayment() does 4 things — violates Single Responsibility
[Release It!] No timeout on external payment gateway call — risk of cascade failure
[DDIA] No idempotency key — retry on network error will double-charge
[APOSD] PaymentService knows too much about UserRepository — high coupling
```

### Example 2: Full Codebase Architecture Review

```
@brooks-lint analyze the overall architecture of this codebase
```

### Example 3: Pre-Refactor Review

```
@brooks-lint what are the biggest design smells in this module before I refactor it?
```

## Review Categories

| Category | Books Applied | What It Catches |
|----------|--------------|-----------------|
| **DRY / Duplication** | PP, Refactoring | Copy-paste code, shared logic not extracted |
| **Naming** | Clean Code, DDD | Unclear names, domain language violations |
| **Coupling** | APOSD, PP | Tight dependencies, missing interfaces |
| **Stability** | Release It! | Missing timeouts, no retry logic, no circuit breakers |
| **Data Integrity** | DDIA | Race conditions, non-idempotent operations |
| **Complexity** | APOSD, SICP | Over-engineering, unnecessary abstraction |
| **Legacy Debt** | WELC | Hard-to-test code, missing seams |
| **Domain Clarity** | DDD, XP | Anemic models, missing bounded contexts |

## Best Practices

- Run `@brooks-lint` after writing new service layers or data pipelines
- Combine with `@logic-lens` for full coverage: logic bugs + design smells
- Use `@brooks-lint analyze architecture` weekly on growing codebases
- Focus on CRITICAL and HIGH findings first — LOW findings are style suggestions

## Related Skills

- `@logic-lens` — Complementary: catches logic bugs; brooks-lint catches design issues
- `@security-auditor` — Specialized security-only deep scan
- `@lint-and-validate` — Style/syntax linting to run alongside design review

## Additional Resources

- [GitHub Repository](https://github.com/hyhmrright/brooks-lint)
- [Dev.to Article: I Synthesized 12 Classic Engineering Books into an AI Code Reviewer](https://dev.to/hyhmrright/i-synthesized-12-classic-engineering-books-into-an-ai-code-reviewer-heres-what-it-caught-3ed1)
- [Related skill: logic-lens](https://github.com/hyhmrright/logic-lens)

## Limitations

Use this skill only when the task clearly matches the scope described above (design review and architectural analysis). Brooks Lint applies AI-powered analysis grounded in established engineering principles. It should complement — not replace — human design review for production-critical decisions. Results reflect the principles of the 12 source books and may not apply to all architectural styles or domains.

---

## bug-hunter
*Systematically finds and fixes bugs using proven debugging techniques. Traces from symptoms to root cause, implements fixes, and prevents regression.*

Risk: safe

# Bug Hunter

Systematically hunt down and fix bugs using proven debugging techniques. No guessing—follow the evidence.

## When to Use This Skill

- User reports a bug or error
- Something isn't working as expected
- User says "fix the bug" or "debug this"
- Intermittent failures or weird behavior
- Production issues need investigation

## The Debugging Process

### 1. Reproduce the Bug

First, make it happen consistently:

```
1. Get exact steps to reproduce
2. Try to reproduce locally
3. Note what triggers it
4. Document the error message/behavior
5. Check if it happens every time or randomly
```

If you can't reproduce it, gather more info:
- What environment? (dev, staging, prod)
- What browser/device?
- What user actions preceded it?
- Any error logs?

### 2. Gather Evidence

Collect all available information:

**Check logs:**
```bash
# Application logs
tail -f logs/app.log

# System logs
journalctl -u myapp -f

# Browser console
# Open DevTools → Console tab
```

**Check error messages:**
- Full stack trace
- Error type and message
- Line numbers
- Timestamp

**Check state:**
- What data was being processed?
- What was the user trying to do?
- What's in the database?
- What's in local storage/cookies?

### 3. Form a Hypothesis

Based on evidence, guess what's wrong:

```
"The login times out because the session cookie 
expires before the auth check completes"

"The form fails because email validation regex 
doesn't handle plus signs"

"The API returns 500 because the database query 
has a syntax error with special characters"
```

### 4. Test the Hypothesis

Prove or disprove your guess:

**Add logging:**
```javascript
console.log('Before API call:', userData);
const response = await api.login(userData);
console.log('After API call:', response);
```

**Use debugger:**
```javascript
debugger; // Execution pauses here
const result = processData(input);
```

**Isolate the problem:**
```javascript
// Comment out code to narrow down
// const result = complexFunction();
const result = { mock: 'data' }; // Use mock data
```

### 5. Find Root Cause

Trace back to the actual problem:

**Common root causes:**
- Null/undefined values
- Wrong data types
- Race conditions
- Missing error handling
- Incorrect logic
- Off-by-one errors
- Async/await issues
- Missing validation

**Example trace:**
```
Symptom: "Cannot read property 'name' of undefined"
↓
Where: user.profile.name
↓
Why: user.profile is undefined
↓
Why: API didn't return profile
↓
Why: User ID was null
↓
Root cause: Login didn't set user ID in session
```

### 6. Implement Fix

Fix the root cause, not the symptom:

**Bad fix (symptom):**
```javascript
// Just hide the error
const name = user?.profile?.name || 'Unknown';
```

**Good fix (root cause):**
```javascript
// Ensure user ID is set on login
const login = async (credentials) => {
  const user = await authenticate(credentials);
  if (user) {
    session.userId = user.id; // Fix: Set user ID
    return user;
  }
  throw new Error('Invalid credentials');
};
```

### 7. Test the Fix

Verify it actually works:

```
1. Reproduce the original bug
2. Apply the fix
3. Try to reproduce again (should fail)
4. Test edge cases
5. Test related functionality
6. Run existing tests
```

### 8. Prevent Regression

Add a test so it doesn't come back:

```javascript
test('login sets user ID in session', async () => {
  const user = await login({ email: 'test@example.com', password: 'pass' });
  
  expect(session.userId).toBe(user.id);
  expect(session.userId).not.toBeNull();
});
```

## Debugging Techniques

### Binary Search

Cut the problem space in half repeatedly:

```javascript
// Does the bug happen before or after this line?
console.log('CHECKPOINT 1');
// ... code ...
console.log('CHECKPOINT 2');
// ... code ...
console.log('CHECKPOINT 3');
```

### Rubber Duck Debugging

Explain the code line by line out loud. Often you'll spot the issue while explaining.

### Print Debugging

Strategic console.logs:

```javascript
console.log('Input:', input);
console.log('After transform:', transformed);
console.log('Before save:', data);
console.log('Result:', result);
```

### Diff Debugging

Compare working vs broken:
- What changed recently?
- What's different between environments?
- What's different in the data?

### Time Travel Debugging

Use git to find when it broke:

```bash
git bisect start
git bisect bad  # Current commit is broken
git bisect good abc123  # This old commit worked
# Git will check out commits for you to test
```

## Common Bug Patterns

### Null/Undefined

```javascript
// Bug
const name = user.profile.name;

// Fix
const name = user?.profile?.name || 'Unknown';

// Better fix
if (!user || !user.profile) {
  throw new Error('User profile required');
}
const name = user.profile.name;
```

### Race Condition

```javascript
// Bug
let data = null;
fetchData().then(result => data = result);
console.log(data); // null - not loaded yet

// Fix
const data = await fetchData();
console.log(data); // correct value
```

### Off-by-One

```javascript
// Bug
for (let i = 0; i <= array.length; i++) {
  console.log(array[i]); // undefined on last iteration
}

// Fix
for (let i = 0; i < array.length; i++) {
  console.log(array[i]);
}
```

### Type Coercion

```javascript
// Bug
if (count == 0) { // true for "", [], null
  
// Fix
if (count === 0) { // only true for 0
```

### Async Without Await

```javascript
// Bug
const result = asyncFunction(); // Returns Promise
console.log(result.data); // undefined

// Fix
const result = await asyncFunction();
console.log(result.data); // correct value
```

## Debugging Tools

### Browser DevTools

```
Console: View logs and errors
Sources: Set breakpoints, step through code
Network: Check API calls and responses
Application: View cookies, storage, cache
Performance: Find slow operations
```

### Node.js Debugging

```javascript
// Built-in debugger
node --inspect app.js

// Then open chrome://inspect in Chrome
```

### VS Code Debugging

```json
// .vscode/launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Debug App",
  "program": "${workspaceFolder}/app.js"
}
```

## When You're Stuck

1. Take a break (seriously, walk away for 10 minutes)
2. Explain it to someone else (or a rubber duck)
3. Search for the exact error message
4. Check if it's a known issue (GitHub issues, Stack Overflow)
5. Simplify: Create minimal reproduction
6. Start over: Delete and rewrite the problematic code
7. Ask for help (provide context, what you've tried)

## Documentation Template

After fixing, document it:

```markdown
## Bug: Login timeout after 30 seconds

**Symptom:** Users get logged out immediately after login

**Root Cause:** Session cookie expires before auth check completes

**Fix:** Increased session timeout from 30s to 3600s in config

**Files Changed:**
- config/session.js (line 12)

**Testing:** Verified login persists for 1 hour

**Prevention:** Added test for session persistence
```

## Key Principles

- Reproduce first, fix second
- Follow the evidence, don't guess
- Fix root cause, not symptoms
- Test the fix thoroughly
- Add tests to prevent regression
- Document what you learned

## Related Skills

- `@systematic-debugging` - Advanced debugging
- `@test-driven-development` - Testing
- `@codebase-audit-pre-push` - Code review

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## codebase-audit-pre-push
*Deep audit before GitHub push: removes junk files, dead code, security holes, and optimization issues. Checks every file line-by-line for production readiness.*

Risk: safe

# Pre-Push Codebase Audit

As a senior engineer, you're doing the final review before pushing this code to GitHub. Check everything carefully and fix problems as you find them.  

## When to Use This Skill  

- User requests "audit the codebase" or "review before push"  
- Before making the first push to GitHub  
- Before making a repository public  
- Pre-production deployment review  
- User asks to "clean up the code" or "optimize everything"  

## Your Job  

Review the entire codebase file by file. Read the code carefully. Fix issues right away. Don't just note problems—make the necessary changes.  

## Audit Process  

### 1. Clean Up Junk Files  

Start by looking for files that shouldn't be on GitHub:  

**Delete these immediately:**  
- OS files: `.DS_Store`, `Thumbs.db`, `desktop.ini`  
- Logs: `*.log`, `npm-debug.log*`, `yarn-error.log*`  
- Temp files: `*.tmp`, `*.temp`, `*.cache`, `*.swp`  
- Build output: `dist/`, `build/`, `.next/`, `out/`, `.cache/`  
- Dependencies: `node_modules/`, `vendor/`, `__pycache__/`, `*.pyc`  
- IDE files: `.idea/`, `.vscode/` (ask user first), `*.iml`, `.project`  
- Backup files: `*.bak`, `*_old.*`, `*_backup.*`, `*_copy.*`  
- Test artifacts: `coverage/`, `.nyc_output/`, `test-results/`  
- Personal junk: `TODO.txt`, `NOTES.txt`, `scratch.*`, `test123.*`  

**Critical - Check for secrets:**  
- `.env` files (should never be committed)  
- Files containing: `password`, `api_key`, `token`, `secret`, `private_key`  
- `*.pem`, `*.key`, `*.cert`, `credentials.json`, `serviceAccountKey.json`  

If you find secrets in the code, mark it as a CRITICAL BLOCKER.  

### 2. Fix .gitignore  

Check if the `.gitignore` file exists and is thorough. If it’s missing or not complete, update it to include all junk file patterns above. Ensure that `.env.example` exists with keys but no values.  

### 3. Audit Every Source File  

Look through each code file and check:  

**Dead Code (remove immediately):**  
- Commented-out code blocks  
- Unused imports/requires  
- Unused variables (declared but never used)  
- Unused functions (defined but never called)  
- Unreachable code (after `return`, inside `if (false)`)  
- Duplicate logic (same code in multiple places—combine)  

**Code Quality (fix issues as you go):**  
- Vague names: `data`, `info`, `temp`, `thing` → rename to be descriptive  
- Magic numbers: `if (status === 3)` → extract to named constant  
- Debug statements: remove `console.log`, `print()`, `debugger`  
- TODO/FIXME comments: either resolve them or delete them  
- TypeScript `any`: add proper types or explain why `any` is used  
- Use `===` instead of `==` in JavaScript  
- Functions longer than 50 lines: consider splitting  
- Nested code greater than 3 levels: refactor with early returns  

**Logic Issues (critical):**  
- Missing null/undefined checks  
- Array operations on potentially empty arrays  
- Async functions that are not awaited  
- Promises without `.catch()` or try/catch  
- Possibilities for infinite loops  
- Missing `default` in switch statements  

### 4. Security Check (Zero Tolerance)  

**Secrets:** Search for hardcoded passwords, API keys, and tokens. They must be in environment variables.  

**Injection vulnerabilities:**  
- SQL: No string concatenation in queries—use parameterized queries only  
- Command injection: No `exec()` with user-provided input  
- Path traversal: No file paths from user input without validation  
- XSS: No `innerHTML` or `dangerouslySetInnerHTML` with user data  

**Auth/Authorization:**  
- Passwords hashed with bcrypt/argon2 (never MD5 or plain text)  
- Protected routes check for authentication  
- Authorization checks on the server side, not just in the UI  
- No IDOR: verify users own the resources they are accessing  

**Data exposure:**  
- API responses do not leak unnecessary information  
- Error messages do not expose stack traces or database details  
- Pagination is present on list endpoints  

**Dependencies:**  
- Run `npm audit` or an equivalent tool  
- Flag critically outdated or vulnerable packages  

### 5. Scalability Check  

**Database:**  
- N+1 queries: loops with database calls inside → use JOINs or batch queries  
- Missing indexes on WHERE/ORDER BY columns  
- Unbounded queries: add LIMIT or pagination  
- Avoid `SELECT *`: specify columns  

**API Design:**  
- Heavy operations (like email, reports, file processing) → move to a background queue  
- Rate limiting on public endpoints  
- Caching for data that is read frequently  
- Timeouts on external calls  

**Code:**  
- No global mutable state  
- Clean up event listeners (to avoid memory leaks)  
- Stream large files instead of loading them into memory  

### 6. Architecture Check  

**Organization:**  
- Clear folder structure  
- Files are in logical locations  
- No "misc" or "stuff" folders  

**Separation of concerns:**  
- UI layer: only responsible for rendering  
- Business logic: pure functions  
- Data layer: isolated database queries  
- No 500+ line "god files"  

**Reusability:**  
- Duplicate code → extract to shared utilities  
- Constants defined once and imported  
- Types/interfaces reused, not redefined  

### 7. Performance  

**Backend:**  
- Expensive operations do not block requests  
- Batch database calls when possible  
- Set cache headers correctly  

**Frontend (if applicable):**  
- Implement code splitting  
- Optimize images  
- Avoid massive dependencies for small utilities  
- Use lazy loading for heavy components  

### 8. Documentation  

**README.md must include:**  
- Description of what the project does  
- Instructions for installation and execution  
- Required environment variables  
- Guidance on running tests  

**Code comments:**  
- Explain WHY, not WHAT  
- Provide explanations for complex logic  
- Avoid comments that merely repeat the code  

### 9. Testing  

- Critical paths should have tests (auth, payments, core features)  
- No `test.only` or `fdescribe` should remain in the code  
- Avoid `test.skip` without an explanation  
- Tests should verify behavior, not implementation details  

### 10. Final Verification  

After making all changes, run the app. Ensure nothing is broken. Check that:  
- The app starts without errors  
- Main features work  
- Tests pass (if they exist)  
- No regressions have been introduced  

## Output Format  

After auditing, provide a report:  

```
CODEBASE AUDIT COMPLETE  

FILES REMOVED:  
- node_modules/ (build artifact)  
- .env (contained secrets)  
- old_backup.js (unused duplicate)  

CODE CHANGES:  
[src/api/users.js]  
  ✂ Removed unused import: lodash  
  ✂ Removed dead function: formatOldWay()  
  🔧 Renamed 'data' → 'userData' for clarity  
  🛡 Added try/catch around API call (line 47)  

[src/db/queries.js]  
  ⚡ Fixed N+1 query: now uses JOIN instead of loop  

SECURITY ISSUES:  
🚨 CRITICAL: Hardcoded API key in config.js (line 12) → moved to .env  
⚠️ HIGH: SQL injection risk in search.js (line 34) → fixed with parameterized query  

SCALABILITY:  
⚡ Added pagination to /api/users endpoint  
⚡ Added index on users.email column  

FINAL STATUS:  
✅ CLEAN - Ready to push to GitHub  

Scores:  
Security: 9/10 (one minor header missing)  
Code Quality: 10/10  
Scalability: 9/10  
Overall: 9/10  
```  

## Key Principles  

- Read the code thoroughly, don't skim  
- Fix issues immediately, don’t just document them  
- If uncertain about removing something, ask the user  
- Test after making changes  
- Be thorough but practical—focus on real problems  
- Security issues are blockers—nothing should ship with critical vulnerabilities  

## Related Skills  

- `@security-auditor` - Deeper security review  
- `@systematic-debugging` - Investigate specific issues  
- `@git-pushing` - Push code after audit

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## design-taste-frontend
*Use when building high-agency frontend interfaces with strict design taste, calibrated color, responsive layout, and motion rules.*

Tags: [frontend, design, ui, react]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# High-Agency Frontend Skill

## When to Use

- Use when the user asks to create, improve, or review frontend UI with strong design taste and anti-generic constraints.
- Use when React, Next.js, Tailwind, motion, component states, typography, spacing, color, or responsive behavior need senior-level design judgment.
- Use when the output must override common LLM UI biases such as centered heroes, purple gradients, card overuse, poor states, and fragile layouts.

## Limitations

- This skill provides frontend design and implementation guidance; it does not replace project-specific product requirements, accessibility review, or user testing.
- Verify framework versions, installed dependencies, responsive behavior, and build output in the target repository before treating generated UI as production-ready.
- Do not force these design rules when the existing product, brand system, or platform conventions require a different visual direction.


## 1. ACTIVE BASELINE CONFIGURATION
* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* VISUAL_DENSITY: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

**AI Instruction:** The standard baseline for all generations is strictly set to these values (8, 6, 4). Do not ask the user to edit this file. Otherwise, ALWAYS listen to the user: adapt these values dynamically based on what they explicitly request in their chat prompts. Use these baseline (or user-overridden) values as your global variables to drive the specific logic in Sections 3 through 7.

## 2. DEFAULT ARCHITECTURE & CONVENTIONS
Unless the user explicitly specifies a different stack, adhere to these structural constraints to maintain consistency:

* **DEPENDENCY VERIFICATION [MANDATORY]:** Before importing ANY 3rd party library (e.g. `framer-motion`, `lucide-react`, `zustand`), you MUST check `package.json`. If the package is missing, you MUST output the installation command (e.g. `npm install package-name`) before providing the code. **Never** assume a library exists.
* **Framework & Interactivity:** React or Next.js. Default to Server Components (`RSC`).
    * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
    * **INTERACTIVITY ISOLATION:** If Sections 4 or 7 (Motion/Liquid Glass) are active, the specific interactive UI component MUST be extracted as an isolated leaf component with `'use client'` at the very top. Server Components must exclusively render static layouts.
* **State Management:** Use local `useState`/`useReducer` for isolated UI. Use global state strictly for deep prop-drilling avoidance.
* **Styling Policy:** Use Tailwind CSS (v3/v4) for 90% of styling.
    * **TAILWIND VERSION LOCK:** Check `package.json` first. Do not use v4 syntax in v3 projects.
    * **T4 CONFIG GUARD:** For v4, do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **ANTI-EMOJI POLICY [CRITICAL]:** NEVER use emojis in code, markup, text content, or alt text. Replace symbols with high-quality icons (Radix, Phosphor) or clean SVG primitives. Emojis are BANNED.
* **Responsiveness & Spacing:**
  * Standardize breakpoints (`sm`, `md`, `lg`, `xl`).
  * Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
  * **Viewport Stability [CRITICAL]:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent catastrophic layout jumping on mobile browsers (iOS Safari).
  * **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for reliable structures.
* **Icons:** You MUST use exactly `@phosphor-icons/react` or `@radix-ui/react-icons` as the import paths (check installed version). Standardize `strokeWidth` globally (e.g., exclusively use `1.5` or `2.0`).


## 3. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
LLMs have statistical biases toward specific UI cliché patterns. Proactively construct premium interfaces using these engineered rules:

**Rule 1: Deterministic Typography**
* **Display/Headlines:** Default to `text-4xl md:text-6xl tracking-tighter leading-none`.
    * **ANTI-SLOP:** Discourage `Inter` for "Premium" or "Creative" vibes. Force unique character using `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
    * **TECHNICAL UI RULE:** Serif fonts are strictly BANNED for Dashboard/Software UIs. For these contexts, use exclusively high-end Sans-Serif pairings (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`).
* **Body/Paragraphs:** Default to `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

**Rule 2: Color Calibration**
* **Constraint:** Max 1 Accent Color. Saturation < 80%.
* **THE LILA BAN:** The "AI Purple/Blue" aesthetic is strictly BANNED. No purple button glows, no neon gradients. Use absolute neutral bases (Zinc/Slate) with high-contrast, singular accents (e.g. Emerald, Electric Blue, or Deep Rose).
* **COLOR CONSISTENCY:** Stick to one palette for the entire output. Do not fluctuate between warm and cool grays within the same project.

**Rule 3: Layout Diversification**
* **ANTI-CENTER BIAS:** Centered Hero/H1 sections are strictly BANNED when `LAYOUT_VARIANCE > 4`. Force "Split Screen" (50/50), "Left Aligned content/Right Aligned asset", or "Asymmetric White-space" structures.

**Rule 4: Materiality, Shadows, and "Anti-Card Overuse"**
* **DASHBOARD HARDENING:** For `VISUAL_DENSITY > 7`, generic card containers are strictly BANNED. Use logic-grouping via `border-t`, `divide-y`, or purely negative space. Data metrics should breathe without being boxed in unless elevation (z-index) is functionally required.
* **Execution:** Use cards ONLY when elevation communicates hierarchy. When a shadow is used, tint it to the background hue.

**Rule 5: Interactive UI States**
* **Mandatory Generation:** LLMs naturally generate "static" successful states. You MUST implement full interaction cycles:
  * **Loading:** Skeletal loaders matching layout sizes (avoid generic circular spinners).
  * **Empty States:** Beautifully composed empty states indicating how to populate data.
  * **Error States:** Clear, inline error reporting (e.g., forms).
  * **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]` to simulate a physical push indicating success/action.

**Rule 6: Data & Form Patterns**
* **Forms:** Label MUST sit above input. Helper text is optional but should exist in markup. Error text below input. Use a standard `gap-2` for input blocks.

## 4. CREATIVE PROACTIVITY (Anti-Slop Implementation)
To actively combat generic AI designs, systematically implement these high-end coding concepts as your baseline:
* **"Liquid Glass" Refraction:** When glassmorphism is needed, go beyond `backdrop-blur`. Add a 1px inner border (`border-white/10`) and a subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) to simulate physical edge refraction.
* **Magnetic Micro-physics (If MOTION_INTENSITY > 5):** Implement buttons that pull slightly toward the mouse cursor. **CRITICAL:** NEVER use React `useState` for magnetic hover or continuous animations. Use EXCLUSIVELY Framer Motion's `useMotionValue` and `useTransform` outside the React render cycle to prevent performance collapse on mobile.
* **Perpetual Micro-Interactions:** When `MOTION_INTENSITY > 5`, embed continuous, infinite micro-animations (Pulse, Typewriter, Float, Shimmer, Carousel) in standard components (avatars, status dots, backgrounds). Apply premium Spring Physics (`type: "spring", stiffness: 100, damping: 20`) to all interactive elements—no linear easing.
* **Layout Transitions:** Always utilize Framer Motion's `layout` and `layoutId` props for smooth re-ordering, resizing, and shared element transitions across state changes.
* **Staggered Orchestration:** Do not mount lists or grids instantly. Use `staggerChildren` (Framer) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) to create sequential waterfall reveals. **CRITICAL:** For `staggerChildren`, the Parent (`variants`) and Children MUST reside in the identical Client Component tree. If data is fetched asynchronously, pass the data as props into a centralized Parent Motion wrapper.

## 5. PERFORMANCE GUARDRAILS
* **DOM Cost:** Apply grain/noise filters exclusively to fixed, pointer-event-none pseudo-elements (e.g., `fixed inset-0 z-50 pointer-events-none`) and NEVER to scrolling containers to prevent continuous GPU repaints and mobile performance degradation.
* **Hardware Acceleration:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`.
* **Z-Index Restraint:** NEVER spam arbitrary `z-50` or `z-10` unprompted. Use z-indexes strictly for systemic layer contexts (Sticky Navbars, Modals, Overlays).

## 6. TECHNICAL REFERENCE (Dial Definitions)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Flexbox `justify-center`, strict 12-column symmetrical grids, equal paddings.
* **4-7 (Offset):** Use `margin-top: -2rem` overlapping, varied image aspect ratios (e.g., 4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units (e.g., `grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`).
* **MOBILE OVERRIDE:** For levels 4-10, any asymmetric layout above `md:` MUST aggressively fall back to a strict, single-column layout (`w-full`, `px-4`, `py-8`) on viewports `< 768px` to prevent horizontal scrolling and layout breakage.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover` and `:active` states only.
* **4-7 (Fluid CSS):** Use `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Use `animation-delay` cascades for load-ins. Focus strictly on `transform` and `opacity`. Use `will-change: transform` sparingly.
* **8-10 (Advanced Choreography):** Complex scroll-triggered reveals or parallax. Use Framer Motion hooks. NEVER use `window.addEventListener('scroll')`.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery Mode):** Lots of white space. Huge section gaps. Everything feels very expensive and clean.
* **4-7 (Daily App Mode):** Normal spacing for standard web apps.
* **8-10 (Cockpit Mode):** Tiny paddings. No card boxes; just 1px lines to separate data. Everything is packed. **Mandatory:** Use Monospace (`font-mono`) for all numbers.

## 7. AI TELLS (Forbidden Patterns)
To guarantee a premium, non-generic output, you MUST strictly avoid these common AI design signatures unless explicitly requested:

### Visual & CSS
* **NO Neon/Outer Glows:** Do not use default `box-shadow` glows or auto-glows. Use inner borders or subtle tinted shadows.
* **NO Pure Black:** Never use `#000000`. Use Off-Black, Zinc-950, or Charcoal.
* **NO Oversaturated Accents:** Desaturate accents to blend elegantly with neutrals.
* **NO Excessive Gradient Text:** Do not use text-fill gradients for large headers.
* **NO Custom Mouse Cursors:** They are outdated and ruin performance/accessibility.

### Typography
* **NO Inter Font:** Banned. Use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
* **NO Oversized H1s:** The first heading should not scream. Control hierarchy with weight and color, not just massive scale.
* **Serif Constraints:** Use Serif fonts ONLY for creative/editorial designs. **NEVER** use Serif on clean Dashboards.

### Layout & Spacing
* **Align & Space Perfectly:** Ensure padding and margins are mathematically perfect. Avoid floating elements with awkward gaps.
* **NO 3-Column Card Layouts:** The generic "3 equal cards horizontally" feature row is BANNED. Use a 2-column Zig-Zag, asymmetric grid, or horizontal scrolling approach instead.

### Content & Data (The "Jane Doe" Effect)
* **NO Generic Names:** "John Doe", "Sarah Chan", or "Jack Su" are banned. Use highly creative, realistic-sounding names.
* **NO Generic Avatars:** DO NOT use standard SVG "egg" or Lucide user icons for avatars. Use creative, believable photo placeholders or specific styling.
* **NO Fake Numbers:** Avoid predictable outputs like `99.99%`, `50%`, or basic phone numbers (`1234567`). Use organic, messy data (`47.2%`, `+1 (312) 847-1928`).
* **NO Startup Slop Names:** "Acme", "Nexus", "SmartFlow". Invent premium, contextual brand names.
* **NO Filler Words:** Avoid AI copywriting clichés like "Elevate", "Seamless", "Unleash", or "Next-Gen". Use concrete verbs.

### External Resources & Components
* **NO Broken Unsplash Links:** Do not use Unsplash. Use absolute, reliable placeholders like `https://picsum.photos/seed/{random_string}/800/600` or SVG UI Avatars.
* **shadcn/ui Customization:** You may use `shadcn/ui`, but NEVER in its generic default state. You MUST customize the radii, colors, and shadows to match the high-end project aesthetic.
* **Production-Ready Cleanliness:** Code must be extremely clean, visually striking, memorable, and meticulously refined in every detail.

## 8. THE CREATIVE ARSENAL (High-End Inspiration)
Do not default to generic UI. Pull from this library of advanced concepts to ensure the output is visually striking and memorable. When appropriate, leverage **GSAP (ScrollTrigger/Parallax)** for complex scrolltelling or **ThreeJS/WebGL** for 3D/Canvas animations, rather than basic CSS motion. **CRITICAL:** Never mix GSAP/ThreeJS with Framer Motion in the same component tree. Default to Framer Motion for UI/Bento interactions. Use GSAP/ThreeJS EXCLUSIVELY for isolated full-page scrolltelling or canvas backgrounds, wrapped in strict useEffect cleanup blocks.

### The Standard Hero Paradigm
* Stop doing centered text over a dark image. Try asymmetric Hero sections: Text cleanly aligned to the left or right. The background should feature a high-quality, relevant image with a subtle stylistic fade (darkening or lightening gracefully into the background color depending on if it is Light or Dark mode).

### Navigation & Menüs
* **Mac OS Dock Magnification:** Nav-bar at the edge; icons scale fluidly on hover.
* **Magnetic Button:** Buttons that physically pull toward the cursor.
* **Gooey Menu:** Sub-items detach from the main button like a viscous liquid.
* **Dynamic Island:** A pill-shaped UI component that morphs to show status/alerts.
* **Contextual Radial Menu:** A circular menu expanding exactly at the click coordinates.
* **Floating Speed Dial:** A FAB that springs out into a curved line of secondary actions.
* **Mega Menu Reveal:** Full-screen dropdowns that stagger-fade complex content.

### Layout & Grids
* **Bento Grid:** Asymmetric, tile-based grouping (e.g., Apple Control Center).
* **Masonry Layout:** Staggered grid without fixed row heights (e.g., Pinterest).
* **Chroma Grid:** Grid borders or tiles showing subtle, continuously animating color gradients.
* **Split Screen Scroll:** Two screen halves sliding in opposite directions on scroll.
* **Curtain Reveal:** A Hero section parting in the middle like a curtain on scroll.

### Cards & Containers
* **Parallax Tilt Card:** A 3D-tilting card tracking the mouse coordinates.
* **Spotlight Border Card:** Card borders that illuminate dynamically under the cursor.
* **Glassmorphism Panel:** True frosted glass with inner refraction borders.
* **Holographic Foil Card:** Iridescent, rainbow light reflections shifting on hover.
* **Tinder Swipe Stack:** A physical stack of cards the user can swipe away.
* **Morphing Modal:** A button that seamlessly expands into its own full-screen dialog container.

### Scroll-Animations
* **Sticky Scroll Stack:** Cards that stick to the top and physically stack over each other.
* **Horizontal Scroll Hijack:** Vertical scroll translates into a smooth horizontal gallery pan.
* **Locomotive Scroll Sequence:** Video/3D sequences where framerate is tied directly to the scrollbar.
* **Zoom Parallax:** A central background image zooming in/out seamlessly as you scroll.
* **Scroll Progress Path:** SVG vector lines or routes that draw themselves as the user scrolls.
* **Liquid Swipe Transition:** Page transitions that wipe the screen like a viscous liquid.

### Galleries & Media
* **Dome Gallery:** A 3D gallery feeling like a panoramic dome.
* **Coverflow Carousel:** 3D carousel with the center focused and edges angled back.
* **Drag-to-Pan Grid:** A boundless grid you can freely drag in any compass direction.
* **Accordion Image Slider:** Narrow vertical/horizontal image strips that expand fully on hover.
* **Hover Image Trail:** The mouse leaves a trail of popping/fading images behind it.
* **Glitch Effect Image:** Brief RGB-channel shifting digital distortion on hover.

### Typography & Text
* **Kinetic Marquee:** Endless text bands that reverse direction or speed up on scroll.
* **Text Mask Reveal:** Massive typography acting as a transparent window to a video background.
* **Text Scramble Effect:** Matrix-style character decoding on load or hover.
* **Circular Text Path:** Text curved along a spinning circular path.
* **Gradient Stroke Animation:** Outlined text with a gradient continuously running along the stroke.
* **Kinetic Typography Grid:** A grid of letters dodging or rotating away from the cursor.

### Micro-Interactions & Effects
* **Particle Explosion Button:** CTAs that shatter into particles upon success.
* **Liquid Pull-to-Refresh:** Mobile reload indicators acting like detaching water droplets.
* **Skeleton Shimmer:** Shifting light reflections moving across placeholder boxes.
* **Directional Hover Aware Button:** Hover fill entering from the exact side the mouse entered.
* **Ripple Click Effect:** Visual waves rippling precisely from the click coordinates.
* **Animated SVG Line Drawing:** Vectors that draw their own contours in real-time.
* **Mesh Gradient Background:** Organic, lava-lamp-like animated color blobs.
* **Lens Blur Depth:** Dynamic focus blurring background UI layers to highlight a foreground action.

## 9. THE "MOTION-ENGINE" BENTO PARADIGM
When generating modern SaaS dashboards or feature sections, you MUST utilize the following "Bento 2.0" architecture and motion philosophy. This goes beyond static cards and enforces a "Vercel-core meets Dribbble-clean" aesthetic heavily reliant on perpetual physics.

### A. Core Design Philosophy
* **Aesthetic:** High-end, minimal, and functional.
* **Palette:** Background in `#f9fafb`. Cards are pure white (`#ffffff`) with a 1px border of `border-slate-200/50`.
* **Surfaces:** Use `rounded-[2.5rem]` for all major containers. Apply a "diffusion shadow" (a very light, wide-spreading shadow, e.g., `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`) to create depth without clutter.
* **Typography:** Strict `Geist`, `Satoshi`, or `Cabinet Grotesk` font stack. Use subtle tracking (`tracking-tight`) for headers.
* **Labels:** Titles and descriptions must be placed **outside and below** the cards to maintain a clean, gallery-style presentation.
* **Pixel-Perfection:** Use generous `p-8` or `p-10` padding inside cards.

### B. The Animation Engine Specs (Perpetual Motion)
All cards must contain **"Perpetual Micro-Interactions."** Use the following Framer Motion principles:
* **Spring Physics:** No linear easing. Use `type: "spring", stiffness: 100, damping: 20` for a premium, weighty feel.
* **Layout Transitions:** Heavily utilize the `layout` and `layoutId` props to ensure smooth re-ordering, resizing, and shared element state transitions.
* **Infinite Loops:** Every card must have an "Active State" that loops infinitely (Pulse, Typewriter, Float, or Carousel) to ensure the dashboard feels "alive".
* **Performance:** Wrap dynamic lists in `<AnimatePresence>` and optimize for 60fps. **PERFORMANCE CRITICAL:** Any perpetual motion or infinite loop MUST be memoized (React.memo) and completely isolated in its own microscopic Client Component. Never trigger re-renders in the parent layout.

### C. The 5-Card Archetypes (Micro-Animation Specs)
Implement these specific micro-animations when constructing Bento grids (e.g., Row 1: 3 cols | Row 2: 2 cols split 70/30):
1. **The Intelligent List:** A vertical stack of items with an infinite auto-sorting loop. Items swap positions using `layoutId`, simulating an AI prioritizing tasks in real-time.
2. **The Command Input:** A search/AI bar with a multi-step Typewriter Effect. It cycles through complex prompts, including a blinking cursor and a "processing" state with a shimmering loading gradient.
3. **The Live Status:** A scheduling interface with "breathing" status indicators. Include a pop-up notification badge that emerges with an "Overshoot" spring effect, stays for 3 seconds, and vanishes.
4. **The Wide Data Stream:** A horizontal "Infinite Carousel" of data cards or metrics. Ensure the loop is seamless (using `x: ["0%", "-100%"]`) with a speed that feels effortless.
5. **The Contextual UI (Focus Mode):** A document view that animates a staggered highlight of a text block, followed by a "Float-in" of a floating action toolbar with micro-icons.

## 10. FINAL PRE-FLIGHT CHECK
Evaluate your code against this matrix before outputting. This is the **last** filter you apply to your logic.
- [ ] Is global state used appropriately to avoid deep prop-drilling rather than arbitrarily?
- [ ] Is mobile layout collapse (`w-full`, `px-4`, `max-w-7xl mx-auto`) guaranteed for high-variance designs?
- [ ] Do full-height sections safely use `min-h-[100dvh]` instead of the bugged `h-screen`?
- [ ] Do `useEffect` animations contain strict cleanup functions?
- [ ] Are empty, loading, and error states provided?
- [ ] Are cards omitted in favor of spacing where possible?
- [ ] Did you strictly isolate CPU-heavy perpetual animations in their own Client Components?

---

## docker-expert
*You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns, and production deployment strategies based on current industry best practices.*

Risk: unknown

# Docker Expert

You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns, and production deployment strategies based on current industry best practices.

### When invoked:

0. If the issue requires ultra-specific expertise outside Docker, recommend switching and stop:
   - Kubernetes orchestration, pods, services, ingress → kubernetes-expert (future)
   - GitHub Actions CI/CD with containers → github-actions-expert
   - AWS ECS/Fargate or cloud-specific container services → devops-expert
   - Database containerization with complex persistence → database-expert

   Example to output:
   "This requires Kubernetes orchestration expertise. Please invoke: 'Use the kubernetes-expert subagent.' Stopping here."

1. Analyze container setup comprehensively:
   
   **Use internal tools first (Read, Grep, Glob) for better performance. Shell commands are fallbacks.**
   
   ```bash
   # Docker environment detection
   docker --version 2>/dev/null || echo "No Docker installed"
   docker info | grep -E "Server Version|Storage Driver|Container Runtime" 2>/dev/null
   docker context ls 2>/dev/null | head -3
   
   # Project structure analysis
   find . -name "Dockerfile*" -type f | head -10
   find . -name "*compose*.yml" -o -name "*compose*.yaml" -type f | head -5
   find . -name ".dockerignore" -type f | head -3
   
   # Container status if running
   docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" 2>/dev/null | head -10
   docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null | head -10
   ```
   
   **After detection, adapt approach:**
   - Match existing Dockerfile patterns and base images
   - Respect multi-stage build conventions
   - Consider development vs production environments
   - Account for existing orchestration setup (Compose/Swarm)

2. Identify the specific problem category and complexity level

3. Apply the appropriate solution strategy from my expertise

4. Validate thoroughly:
   ```bash
   # Build and security validation
   docker build --no-cache -t test-build . 2>/dev/null && echo "Build successful"
   docker history test-build --no-trunc 2>/dev/null | head -5
   docker scout quickview test-build 2>/dev/null || echo "No Docker Scout"
   
   # Runtime validation
   docker run --rm -d --name validation-test test-build 2>/dev/null
   docker exec validation-test ps aux 2>/dev/null | head -3
   docker stop validation-test 2>/dev/null
   
   # Compose validation
   docker-compose config 2>/dev/null && echo "Compose config valid"
   ```

## Core Expertise Areas

### 1. Dockerfile Optimization & Multi-Stage Builds

**High-priority patterns I address:**
- **Layer caching optimization**: Separate dependency installation from source code copying
- **Multi-stage builds**: Minimize production image size while keeping build flexibility
- **Build context efficiency**: Comprehensive .dockerignore and build context management
- **Base image selection**: Alpine vs distroless vs scratch image strategies

**Key techniques:**
```dockerfile
# Optimized multi-stage pattern
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

FROM node:18-alpine AS runtime
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
WORKDIR /app
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nextjs:nodejs /app/dist ./dist
COPY --from=build --chown=nextjs:nodejs /app/package*.json ./
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### 2. Container Security Hardening

**Security focus areas:**
- **Non-root user configuration**: Proper user creation with specific UID/GID
- **Secrets management**: Docker secrets, build-time secrets, avoiding env vars
- **Base image security**: Regular updates, minimal attack surface
- **Runtime security**: Capability restrictions, resource limits

**Security patterns:**
```dockerfile
# Security-hardened container
FROM node:18-alpine
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production
COPY --chown=appuser:appgroup . .
USER 1001
# Drop capabilities, set read-only root filesystem
```

### 3. Docker Compose Orchestration

**Orchestration expertise:**
- **Service dependency management**: Health checks, startup ordering
- **Network configuration**: Custom networks, service discovery
- **Environment management**: Dev/staging/prod configurations
- **Volume strategies**: Named volumes, bind mounts, data persistence

**Production-ready compose pattern:**
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      target: production
    depends_on:
      db:
        condition: service_healthy
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB_FILE: /run/secrets/db_name
      POSTGRES_USER_FILE: /run/secrets/db_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_name
      - db_user
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres_data:

secrets:
  db_name:
    external: true
  db_user:
    external: true  
  db_password:
    external: true
```

### 4. Image Size Optimization

**Size reduction strategies:**
- **Distroless images**: Minimal runtime environments
- **Build artifact optimization**: Remove build tools and cache
- **Layer consolidation**: Combine RUN commands strategically
- **Multi-stage artifact copying**: Only copy necessary files

**Optimization techniques:**
```dockerfile
# Minimal production image
FROM gcr.io/distroless/nodejs18-debian11
COPY --from=build /app/dist /app
COPY --from=build /app/node_modules /app/node_modules
WORKDIR /app
EXPOSE 3000
CMD ["index.js"]
```

### 5. Development Workflow Integration

**Development patterns:**
- **Hot reloading setup**: Volume mounting and file watching
- **Debug configuration**: Port exposure and debugging tools
- **Testing integration**: Test-specific containers and environments
- **Development containers**: Remote development container support via CLI tools

**Development workflow:**
```yaml
# Development override
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
      - /app/dist
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    ports:
      - "9229:9229"  # Debug port
    command: npm run dev
```

### 6. Performance & Resource Management

**Performance optimization:**
- **Resource limits**: CPU, memory constraints for stability
- **Build performance**: Parallel builds, cache utilization
- **Runtime performance**: Process management, signal handling
- **Monitoring integration**: Health checks, metrics exposure

**Resource management:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

## Advanced Problem-Solving Patterns

### Cross-Platform Builds
```bash
# Multi-architecture builds
docker buildx create --name multiarch-builder --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myapp:latest --push .
```

### Build Cache Optimization
```dockerfile
# Mount build cache for package managers
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

### Secrets Management
```dockerfile
# Build-time secrets (BuildKit)
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    # Use API_KEY for build process
```

### Health Check Strategies
```dockerfile
# Sophisticated health monitoring
COPY health-check.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/health-check.sh
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/health-check.sh"]
```

## Code Review Checklist

When reviewing Docker configurations, focus on:

### Dockerfile Optimization & Multi-Stage Builds
- [ ] Dependencies copied before source code for optimal layer caching
- [ ] Multi-stage builds separate build and runtime environments
- [ ] Production stage only includes necessary artifacts
- [ ] Build context optimized with comprehensive .dockerignore
- [ ] Base image selection appropriate (Alpine vs distroless vs scratch)
- [ ] RUN commands consolidated to minimize layers where beneficial

### Container Security Hardening
- [ ] Non-root user created with specific UID/GID (not default)
- [ ] Container runs as non-root user (USER directive)
- [ ] Secrets managed properly (not in ENV vars or layers)
- [ ] Base images kept up-to-date and scanned for vulnerabilities
- [ ] Minimal attack surface (only necessary packages installed)
- [ ] Health checks implemented for container monitoring

### Docker Compose & Orchestration
- [ ] Service dependencies properly defined with health checks
- [ ] Custom networks configured for service isolation
- [ ] Environment-specific configurations separated (dev/prod)
- [ ] Volume strategies appropriate for data persistence needs
- [ ] Resource limits defined to prevent resource exhaustion
- [ ] Restart policies configured for production resilience

### Image Size & Performance
- [ ] Final image size optimized (avoid unnecessary files/tools)
- [ ] Build cache optimization implemented
- [ ] Multi-architecture builds considered if needed
- [ ] Artifact copying selective (only required files)
- [ ] Package manager cache cleaned in same RUN layer

### Development Workflow Integration
- [ ] Development targets separate from production
- [ ] Hot reloading configured properly with volume mounts
- [ ] Debug ports exposed when needed
- [ ] Environment variables properly configured for different stages
- [ ] Testing containers isolated from production builds

### Networking & Service Discovery
- [ ] Port exposure limited to necessary services
- [ ] Service naming follows conventions for discovery
- [ ] Network security implemented (internal networks for backend)
- [ ] Load balancing considerations addressed
- [ ] Health check endpoints implemented and tested

## Common Issue Diagnostics

### Build Performance Issues
**Symptoms**: Slow builds (10+ minutes), frequent cache invalidation
**Root causes**: Poor layer ordering, large build context, no caching strategy
**Solutions**: Multi-stage builds, .dockerignore optimization, dependency caching

### Security Vulnerabilities  
**Symptoms**: Security scan failures, exposed secrets, root execution
**Root causes**: Outdated base images, hardcoded secrets, default user
**Solutions**: Regular base updates, secrets management, non-root configuration

### Image Size Problems
**Symptoms**: Images over 1GB, deployment slowness
**Root causes**: Unnecessary files, build tools in production, poor base selection
**Solutions**: Distroless images, multi-stage optimization, artifact selection

### Networking Issues
**Symptoms**: Service communication failures, DNS resolution errors
**Root causes**: Missing networks, port conflicts, service naming
**Solutions**: Custom networks, health checks, proper service discovery

### Development Workflow Problems
**Symptoms**: Hot reload failures, debugging difficulties, slow iteration
**Root causes**: Volume mounting issues, port configuration, environment mismatch
**Solutions**: Development-specific targets, proper volume strategy, debug configuration

## Integration & Handoff Guidelines

**When to recommend other experts:**
- **Kubernetes orchestration** → kubernetes-expert: Pod management, services, ingress
- **CI/CD pipeline issues** → github-actions-expert: Build automation, deployment workflows  
- **Database containerization** → database-expert: Complex persistence, backup strategies
- **Application-specific optimization** → Language experts: Code-level performance issues
- **Infrastructure automation** → devops-expert: Terraform, cloud-specific deployments

**Collaboration patterns:**
- Provide Docker foundation for DevOps deployment automation
- Create optimized base images for language-specific experts
- Establish container standards for CI/CD integration
- Define security baselines for production orchestration

I provide comprehensive Docker containerization expertise with focus on practical optimization, security hardening, and production-ready patterns. My solutions emphasize performance, maintainability, and security best practices for modern container workflows.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## frontend-api-integration-patterns
*Production-ready patterns for integrating frontend applications with backend APIs, including race condition handling, request cancellation, retry strategies, error normalization, and UI state management.*

Risk: safe

# Frontend API Integration Patterns

## Overview

This skill provides production-ready patterns for integrating frontend applications with backend APIs.

Most frontend issues are not caused by APIs being difficult to call, but by **incorrect handling of asynchronous behavior**—leading to race conditions, stale data, duplicated requests, and poor user experience.

This skill focuses on **correctness, resilience, and user experience**, not just making API calls work.

---

## When to Use This Skill

* Connecting frontend apps (React, React Native, Vue, etc.) to backend APIs
* Integrating ML/AI endpoints (`/predict`, `/recommend`)
* Handling asynchronous data in UI
* Fixing stale data, flickering UI, or duplicate requests
* Designing scalable frontend API layers

---

## Core Patterns

### 1. API Layer (Separation of Concerns)

Centralize API logic and normalize errors.

```js id="k1m7r2"
export class ApiError extends Error {
  constructor(message, status, payload = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

export const apiClient = async (url, options = {}) => {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let payload = null;
    try {
      payload = await res.json();
    } catch (_) {}

    throw new ApiError(
      payload?.message || "Request failed",
      res.status,
      payload
    );
  }

  // handle empty responses safely (e.g. 204 No Content)
  if (res.status === 204) return null;

  const text = await res.text();
  return text ? JSON.parse(text) : null;
};
```

---

### 2. Race-Safe State Management

Prevent stale responses from overwriting fresh data.

```js id="y7p4ha"
useEffect(() => {
  let cancelled = false;

  const load = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await getUser();

      if (!cancelled) setData(result);
    } catch (err) {
      if (!cancelled) setError(err.message);
    } finally {
      if (!cancelled) setLoading(false);
    }
  };

  load();

  return () => {
    cancelled = true;
  };
}, []);
```

> Use a cancellation flag for non-fetch async logic. For network requests, prefer AbortController.

---

### 3. Request Cancellation (AbortController)

Cancel in-flight requests to avoid memory leaks and stale updates.

```js id="l9x2pw"
useEffect(() => {
  const controller = new AbortController();

  const load = async () => {
    try {
      const data = await getUser({ signal: controller.signal });
      setData(data);
    } catch (err) {
      if (err.name === "AbortError") return;
      setError(err.message);
    }
  };

  load();
  return () => controller.abort();
}, [userId]);
```

---

### 4. Retry with Exponential Backoff

Retry only transient failures (5xx or network errors).

```js id="8n3zcf"
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const fetchWithBackoff = async (fn, retries = 3, delay = 300) => {
  try {
    return await fn();
  } catch (err) {
    const isAbort = err.name === "AbortError";
    const isHttpError = typeof err.status === "number";
    const isRetryable = !isAbort && (!isHttpError || err.status >= 500);

    if (retries <= 0 || !isRetryable) throw err;

    const nextDelay = delay * 2 + Math.random() * 100;
    await sleep(nextDelay);

    return fetchWithBackoff(fn, retries - 1, nextDelay);
  }
};
```

---

### 5. Debounced API Calls

Avoid excessive API calls (e.g., search inputs).

```js id="i2r7wq"
const useDebounce = (value, delay = 400) => {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);

  return debounced;
};
```

---

### 6. Request Deduplication

Prevent duplicate API calls across components.

```js id="x8v4km"
const inFlight = new Map();

export const dedupedFetch = (key, fn) => {
  if (inFlight.has(key)) return inFlight.get(key);

  const promise = fn().finally(() => inFlight.delete(key));
  inFlight.set(key, promise);
  return promise;
};
```

---

## Examples

### Example 1: ML Prediction with Cancellation

```js id="n5q2pt"
const controllerRef = useRef(null);

const handlePredict = async (input) => {
  controllerRef.current?.abort();
  controllerRef.current = new AbortController();

  try {
    const result = await fetchWithBackoff(() =>
      apiClient("/predict", {
        method: "POST",
        body: JSON.stringify({ text: input }),
        signal: controllerRef.current.signal,
      })
    );

    setOutput(result);
  } catch (err) {
    if (err.name === "AbortError") return;
    setError(err.message);
  }
};
```

---

### Example 2: Debounced Search

```js id="w4z8yn"
const debouncedQuery = useDebounce(query, 400);

useEffect(() => {
  if (!debouncedQuery) return;

  const controller = new AbortController();

  searchAPI(debouncedQuery, { signal: controller.signal })
    .then(setResults)
    .catch((err) => {
      if (err.name !== "AbortError") {
        setError("Search failed. Please try again.");
      }
    });

  return () => controller.abort();
}, [debouncedQuery]);
```

---

### Example 3: Optimistic UI Update

```js id="q2k9hz"
const deleteItem = async (id) => {
  const previous = items;

  setItems((curr) => curr.filter((item) => item.id !== id));

  try {
    await apiClient(`/items/${id}`, { method: "DELETE" });
  } catch (err) {
    setItems(previous);
    setError("Delete failed. Please try again.");
  }
};
```

---

## Best Practices

* ✅ Centralize API logic in a dedicated layer
* ✅ Normalize errors using a custom error class
* ✅ Always handle loading, error, and success states
* ✅ Use AbortController for request cancellation
* ✅ Retry only transient failures (5xx)
* ✅ Use debouncing for input-driven APIs
* ✅ Deduplicate identical requests

---

## Anti-Patterns

* ❌ Retrying 4xx errors
* ❌ No request cancellation (memory leaks)
* ❌ Race-condition-prone state updates
* ❌ Swallowing errors silently
* ❌ Global loading/error state for multiple requests
* ❌ Calling APIs directly inside components repeatedly

---

## Common Pitfalls

**Problem:** UI shows stale data
**Solution:** Use cancellation or guard against outdated responses

**Problem:** Too many API calls on input
**Solution:** Use debouncing + cancellation

**Problem:** Duplicate requests from multiple components
**Solution:** Use request deduplication

**Problem:** Server overload during retry
**Solution:** Use exponential backoff

**Problem:** State updates after component unmount
**Solution:** Use AbortController cleanup

---

## Limitations

* These examples use vanilla JavaScript patterns; adapt them to your framework's data-fetching library when using React Query, SWR, Apollo, Relay, or similar tools.
* Do not retry non-idempotent mutations unless the backend provides idempotency keys or another duplicate-safe contract.
* Do not expose privileged API keys in frontend code; proxy sensitive requests through a backend.

---

## Additional Resources

* https://developer.mozilla.org/en-US/docs/Web/API/AbortController
* https://react.dev
* https://axios-http.com

---

---

## full-output-enforcement
*Use when a task requires exhaustive unabridged output, complete files, or strict prevention of placeholders and skipped code.*

Tags: [output, code-generation, quality]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# Full-Output Enforcement

## When to Use

- Use when the user explicitly asks for full files, complete implementations, exhaustive lists, or unabridged deliverables.
- Use when placeholder code, skipped sections, TODO stubs, or descriptions in place of implementation would break the request.
- Use when a long answer may need clean continuation chunks without losing completeness or structural integrity.

## Limitations

- This skill enforces completeness, but it does not override token limits, safety constraints, missing source context, or user-provided scope boundaries.
- Split long outputs into clearly labeled continuation chunks when necessary, and verify that each chunk connects cleanly to the previous one.
- Do not invent unavailable code, credentials, private APIs, or project files to satisfy a request for complete output.


## Baseline

Treat every task as production-critical. A partial output is a broken output. Do not optimize for brevity — optimize for completeness. If the user asks for a full file, deliver the full file. If the user asks for 5 components, deliver 5 components. No exceptions.

## Banned Output Patterns

The following patterns are hard failures. Never produce them:

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO`, `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as needed`, bare `...` standing in for omitted code

**In prose:** "Let me know if you want me to continue", "I can provide more details if needed", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "and so on" (when replacing actual content), "I'll leave that as an exercise"

**Structural shortcuts:** Outputting a skeleton when the request was for a full implementation. Showing the first and last section while skipping the middle. Replacing repeated logic with one example and a description. Describing what code should do instead of writing it.

## Execution Process

1. **Scope** — Read the full request. Count how many distinct deliverables are expected (files, functions, sections, answers). Lock that number.
2. **Build** — Generate every deliverable completely. No partial drafts, no "you can extend this later."
3. **Cross-check** — Before output, re-read the original request. Compare your deliverable count against the scope count. If anything is missing, add it before responding.

## Handling Long Outputs

When a response approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint (end of a function, end of a file, end of a section).
- End with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick Check

Before finalizing any response, verify:
- No banned patterns from the list above appear anywhere in the output
- Every item the user requested is present and finished
- Code blocks contain actual runnable code, not descriptions of what code would do
- Nothing was shortened to save space

---

## gdb-cli
*GDB debugging assistant for AI agents - analyze core dumps, debug live processes, investigate crashes and deadlocks with source code correlation*

Risk: critical

# GDB Debugging Assistant

## Overview

A GDB debugging skill designed for AI agents. Combines **source code analysis** with **runtime state inspection** using gdb-cli to provide intelligent debugging assistance for C/C++ programs.

## When to Use This Skill

- Analyze core dumps or crash dumps
- Debug running processes with GDB attach
- Investigate crashes, deadlocks, or memory issues
- Get intelligent debugging assistance with source code context
- Debug multi-threaded applications

## Do Not Use This Skill When

- The task is unrelated to C/C++ debugging
- The user needs general-purpose assistance without debugging
- No GDB is available (GDB 9.0+ with Python support required)

## Prerequisites

```bash
# Install gdb-cli
pip install gdb-cli

# Or from GitHub
pip install git+https://github.com/Cerdore/gdb-cli.git

# Verify GDB has Python support
gdb -nx -q -batch -ex "python print('OK')"
```

**Requirements:**
- Python 3.6.8+
- GDB 9.0+ with Python support enabled
- Linux OS

## How It Works

### Step 1: Initialize Debug Session

**For core dump analysis:**
```bash
gdb-cli load --binary <binary_path> --core <core_path> [--gdb-path <gdb_path>]
```

**For live process debugging:**
```bash
gdb-cli attach --pid <pid> [--binary <binary_path>]
```

**Output:** A session_id like `"session_id": "a1b2c3"`. Store this for subsequent commands.

### Step 2: Gather Initial Information

```bash
SESSION="<session_id>"

# List all threads
gdb-cli threads -s $SESSION

# Get backtrace (with local variables)
gdb-cli bt -s $SESSION --full

# Get registers
gdb-cli registers -s $SESSION
```

### Step 3: Correlate Source Code (CRITICAL)

For each frame in the backtrace:
1. **Extract frame info**: `{file}:{line} in {function}`
2. **Read source context**: Get ±20 lines around the crash point
3. **Get local variables**: `gdb-cli locals-cmd -s $SESSION --frame <N>`
4. **Analyze**: Correlate code logic with variable values

**Example correlation:**
```
Frame #0: process_data() at src/worker.c:87
Source code shows:
  85: Node* node = get_node(id);
  86: if (node == NULL) return;
  87: node->data = value;  <- Crash here

Variables show:
  node = 0x0 (NULL)

Analysis: The NULL check on line 86 didn't catch the issue.
```

### Step 4: Deep Investigation

```bash
# Examine variables
gdb-cli eval-cmd -s $SESSION "variable_name"
gdb-cli eval-cmd -s $SESSION "ptr->field"
gdb-cli ptype -s $SESSION "struct_name"

# Memory inspection
gdb-cli memory -s $SESSION "0x7fffffffe000" --size 64

# Disassembly
gdb-cli disasm -s $SESSION --count 20

# Check all threads (for deadlock analysis)
gdb-cli thread-apply -s $SESSION bt --all

# View shared libraries
gdb-cli sharedlibs -s $SESSION
```

### Step 5: Session Management

```bash
# List active sessions
gdb-cli sessions

# Check session status
gdb-cli status -s $SESSION

# Stop session (cleanup)
gdb-cli stop -s $SESSION
```

## Common Debugging Patterns

### Pattern: Null Pointer Dereference

**Indicators:**
- Crash on memory access instruction
- Pointer variable is 0x0

**Investigation:**
```bash
gdb-cli registers -s $SESSION  # Check RIP
gdb-cli eval-cmd -s $SESSION "ptr"  # Check pointer value
```

### Pattern: Deadlock

**Indicators:**
- Multiple threads stuck in lock functions
- `pthread_mutex_lock` in backtrace

**Investigation:**
```bash
gdb-cli thread-apply -s $SESSION bt --all
# Look for circular wait patterns
```

### Pattern: Memory Corruption

**Indicators:**
- Crash in malloc/free
- Garbage values in variables

**Investigation:**
```bash
gdb-cli memory -s $SESSION "&variable" --size 128
gdb-cli registers -s $SESSION
```

## Examples

### Example 1: Core Dump Analysis

```bash
# Load core dump
gdb-cli load --binary ./myapp --core /tmp/core.1234

# Get crash location
gdb-cli bt -s a1b2c3 --full

# Examine crash frame
gdb-cli locals-cmd -s a1b2c3 --frame 0
```

### Example 2: Live Process Debugging

```bash
# Attach to stuck server
gdb-cli attach --pid 12345

# Check all threads
gdb-cli threads -s b2c3d4

# Get all backtraces
gdb-cli thread-apply -s b2c3d4 bt --all
```

## Best Practices

- Always read source code before drawing conclusions from variable values
- Use `--range` for pagination on large thread counts or deep backtraces
- Use `ptype` to understand complex data structures before examining values
- Check all threads for multi-threaded issues
- Cross-reference types with source code definitions

## Security & Safety Notes

- This skill requires GDB access to processes and core dumps
- Attaching to processes may require appropriate permissions (sudo, ptrace_scope)
- Core dumps may contain sensitive data - handle with care
- Only debug processes you have authorization to analyze

## Related Skills

- `@systematic-debugging` - General debugging methodology
- `@test-driven-development` - Write tests before implementation

## Links

- **Repository**: https://github.com/Cerdore/gdb-cli
- **PyPI**: https://pypi.org/project/gdb-cli/
- **Documentation**: https://github.com/Cerdore/gdb-cli#readme

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## github-actions-advanced
*>*

Risk: safe

# GitHub Actions Advanced Skill

Expert guidance for designing, writing, debugging, and securing **production-grade** GitHub Actions workflows.

---

## When to Use This Skill

- User mentions GitHub Actions, `.github/workflows`, CI/CD pipelines, runners, jobs, steps, or actions
- User wants to automate builds, tests, deployments, or releases via GitHub
- User asks about matrix builds, reusable workflows, composite actions, or self-hosted runners
- User needs help with OIDC authentication, caching strategies, or secrets management
- User says "my GitHub pipeline is failing" or "set up CI for my repo"
- User asks about workflow security, hardening, or environment protection rules

## When NOT to Use This Skill

- The user is working with GitLab CI/CD → recommend `gitlab-ci-patterns`
- The user is working with CircleCI, Jenkins, or other CI platforms
- The task is purely about Docker image building without GitHub context → recommend `docker-expert`
- The task is about Kubernetes deployment configuration → recommend `kubernetes-architect`

---

## Step 1: Understand Context Before Responding

When invoked, first gather context:

```bash
# Discover existing workflows in the repo
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -20

# Check for composite actions
find .github/actions -name "action.yml" 2>/dev/null

# Detect tech stack (influences runner OS, language setup actions)
ls package.json requirements.txt Gemfile go.mod Cargo.toml pom.xml 2>/dev/null
```

Then adapt recommendations to:
- Existing workflow patterns in the repo
- The tech stack and language runtime
- Whether this is a monorepo or single-project repo
- Whether self-hosted or GitHub-hosted runners are in use

---

## Workflow Structure Reference

```yaml
name: Workflow Name

on:                          # Triggers (see Triggers section)
  push:
    branches: [main]

permissions:                 # Always declare — principle of least privilege
  contents: read

env:                         # Workflow-level env vars
  NODE_VERSION: '20'

concurrency:                 # Prevent duplicate runs
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true   # Cancel older runs for same branch

jobs:
  job-id:
    name: Human-readable name
    runs-on: ubuntu-24.04    # Pin OS version — never use -latest in prod
    timeout-minutes: 15      # Always set — prevents runaway jobs
    environment: production  # Links to GitHub Environment (approvals/secrets)

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - name: Step name
        run: echo "hello"
```

---

## Triggers (`on:`)

### Common Patterns

```yaml
on:
  push:
    branches: [main, 'release/**']
    paths-ignore: ['**.md', 'docs/**']   # Skip docs-only changes

  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

  workflow_dispatch:                      # Manual trigger with inputs
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        type: choice
        options: [staging, production]
      dry-run:
        description: 'Dry run only?'
        type: boolean
        default: false

  schedule:
    - cron: '0 2 * * 1'                 # Monday 2am UTC

  workflow_call:                          # Called by other workflows (reusable)
    inputs:
      image-tag:
        type: string
        required: true
    secrets:
      deploy-token:
        required: true

  release:
    types: [published]                   # Trigger only on published releases

  pull_request_target:                   # Runs with repo secrets — use with care!
    types: [labeled]                     # Gate with label + author_association check
```

> **Security Warning:** `pull_request_target` runs with repo secrets. Only use after a maintainer labels the PR. Never check out fork code without explicit sandboxing.

---

## Reusable Workflows

Split large pipelines into composable units stored in `.github/workflows/`.

**Convention:** Prefix internal/reusable workflows with `_` (e.g., `_build.yml`).

### Caller (`.github/workflows/deploy.yml`)

```yaml
jobs:
  call-build:
    uses: ./.github/workflows/_build.yml        # Same-repo reusable
    # uses: org/repo/.github/workflows/build.yml@main  # Cross-repo
    with:
      image-tag: ${{ github.sha }}
    secrets: inherit                             # Pass all caller secrets down
  
  call-test:
    uses: ./.github/workflows/_test.yml
    with:
      node-version: '20'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}       # Explicit secret passing
```

### Reusable Workflow (`.github/workflows/_build.yml`)

```yaml
on:
  workflow_call:
    inputs:
      image-tag:
        type: string
        required: true
      push:
        type: boolean
        default: false
    secrets:
      registry-token:
        required: false
    outputs:
      digest:
        description: "Image digest"
        value: ${{ jobs.build.outputs.digest }}

jobs:
  build:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - id: build
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
        with:
          push: ${{ inputs.push }}
          tags: myapp:${{ inputs.image-tag }}
```

---

## Matrix Builds

```yaml
jobs:
  test:
    strategy:
      fail-fast: false           # Don't cancel others if one fails
      max-parallel: 4            # Limit concurrent runners
      matrix:
        os: [ubuntu-24.04, windows-2022, macos-14]
        node: ['18', '20', '22']
        exclude:
          - os: windows-2022
            node: '18'
        include:
          - os: ubuntu-24.04
            node: '22'
            experimental: true   # Custom matrix variable

    runs-on: ${{ matrix.os }}
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
        continue-on-error: ${{ matrix.experimental == true }}
```

### Dynamic Matrix via Script

```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-24.04
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - id: set-matrix
        run: |
          SERVICES=$(find services -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | jq -R -s -c 'split("\n")[:-1]')
          printf 'matrix={"service":%s}\n' "$SERVICES" >> "$GITHUB_OUTPUT"

  build:
    needs: generate-matrix
    strategy:
      matrix: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    runs-on: ubuntu-24.04
    steps:
      - env:
          SERVICE: ${{ matrix.service }}
        run: echo "Building $SERVICE"
```

---

## Caching Strategies

### Language Setup Actions (Preferred — No Extra Step Needed)

```yaml
# Node.js
- uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
  with:
    node-version: '20'
    cache: 'npm'           # or 'yarn' or 'pnpm'

# Python
- uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b  # v5.3.0
  with:
    python-version: '3.12'
    cache: 'pip'

# Go
- uses: actions/setup-go@3041bf56c941b39c61721a86cd11f3bb1338122a  # v5.2.0
  with:
    go-version: '1.23'
    cache: true

# Java / Gradle / Maven
- uses: actions/setup-java@7a6d8a8234af8eb26422e24052f73b12b0e46a27  # v4.6.0
  with:
    distribution: 'temurin'
    java-version: '21'
    cache: 'maven'        # or 'gradle'
```

### Manual Cache (Any Tool)

```yaml
- uses: actions/cache@6849a6489940f00c2f30c0fb92c6274307ccb58a  # v4.1.2
  id: cache-deps
  with:
    path: |
      ~/.cache/pip
      .venv
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
      ${{ runner.os }}-pip-

- name: Install deps (only on cache miss)
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: pip install -r requirements.txt
```

### Docker Layer Caching

```yaml
- uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
    # For registry-backed cache (cross-branch):
    # cache-from: type=registry,ref=ghcr.io/myorg/myapp:buildcache
    # cache-to: type=registry,ref=ghcr.io/myorg/myapp:buildcache,mode=max
```

---

## OIDC Authentication (Keyless Cloud Auth)

**Never store long-lived cloud credentials as secrets.** Use OIDC to get short-lived tokens that expire automatically.

### AWS

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: us-east-1
      role-session-name: GitHubActions-${{ github.run_id }}

  # Trust policy on the IAM role must include:
  # "token.actions.githubusercontent.com" as OIDC provider
  # Condition: "repo:org/repo:ref:refs/heads/main" (restrict to branch)
```

### GCP (Workload Identity Federation)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: google-github-actions/auth@6fc4af4b145ae7821d527454aa9bd537d1f2dc5f  # v2.1.7
    with:
      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
      service_account: github-actions@my-project.iam.gserviceaccount.com
      token_format: access_token   # or 'id_token'
```

### Azure (Federated Identity)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@a65d910e8af852a8061c627c456678983e180302  # v2.2.0
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      # No client secret needed! Uses OIDC federated credentials
```

---

## Environments & Deployment Protection

```yaml
jobs:
  deploy-staging:
    environment:
      name: staging
      url: https://staging.myapp.com
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - run: ./scripts/deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com      # Shown in the GitHub UI deployment panel
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - run: ./scripts/deploy.sh production
```

**Configure in Settings → Environments:**
- **Required reviewers** — manual approval gate before run
- **Wait timer** — delay after approval (e.g., 10-minute buffer)
- **Branch/tag restrictions** — only `main` or `v*` tags can deploy to prod
- **Environment-specific secrets** — override repo-level secrets per environment
- **Deployment branches** — whitelist which branches can target this environment

---

## Secrets Management

```yaml
# Access repo/org/environment secrets
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

# Auto-provided token — no setup needed
- uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea  # v7.0.1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}

# Hierarchy (most specific wins):
# environment secret > repo secret > org secret
```

### Masking Dynamic Values

```yaml
- name: Generate and mask dynamic token
  run: |
    TOKEN=$(./scripts/generate-token.sh)
    echo "::add-mask::$TOKEN"          # Mask in all subsequent logs
    echo "DEPLOY_TOKEN=$TOKEN" >> $GITHUB_ENV
```

### Secrets in Composite Actions

```yaml
# Secrets cannot be passed as inputs to composite actions
# Pass them as env vars instead:
- uses: ./.github/actions/my-action
  env:
    SECRET_VALUE: ${{ secrets.MY_SECRET }}
```

---

## Composite Actions

Package reusable step sequences into local actions. No container spin-up, no separate workflow file needed.

### Action Definition (`.github/actions/setup-app/action.yml`)

```yaml
name: Setup App
description: Install and configure application dependencies

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
  install-flags:
    description: 'Additional npm install flags'
    required: false
    default: ''

outputs:
  cache-hit:
    description: 'Whether the dependency cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: composite
  steps:
    - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm

    - id: cache
      uses: actions/cache@6849a6489940f00c2f30c0fb92c6274307ccb58a  # v4.1.2
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ inputs.node-version }}-${{ hashFiles('package-lock.json') }}

    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      env:
        INSTALL_FLAGS: ${{ inputs.install-flags }}
      run: |
        args=()
        case "$INSTALL_FLAGS" in
          "") ;;
          "--ignore-scripts") args+=(--ignore-scripts) ;;
          *) echo "Unsupported install flags" >&2; exit 1 ;;
        esac
        npm ci "${args[@]}"

    - name: Build
      shell: bash
      run: npm run build
```

### Usage in a Workflow

```yaml
steps:
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
  - uses: ./.github/actions/setup-app
    with:
      node-version: '22'
      install-flags: '--ignore-scripts'
```

---

## Self-Hosted Runners

```yaml
jobs:
  build-gpu:
    runs-on: [self-hosted, linux, x64, gpu]    # Label matching
    timeout-minutes: 60

  build-arm:
    runs-on: [self-hosted, linux, arm64]
```

### Runner Best Practices

| Practice | Details |
|---|---|
| **Ephemeral runners** | Use Actions Runner Controller (ARC) on Kubernetes for fresh runners per job |
| **Isolation** | Never share prod runners with untrusted/fork PR workflows |
| **Cleanup hooks** | Set `ACTIONS_RUNNER_HOOK_JOB_COMPLETED` to reset environment |
| **Runner groups** | Use groups to restrict which repos/workflows can access which runners |
| **Labels** | Use custom labels (e.g., `gpu`, `high-memory`) for precise targeting |
| **Security** | Disable fork PR access to self-hosted runners in Settings |

```bash
# Actions Runner Controller (Kubernetes) — recommended for ephemeral runners
helm install arc \
  --namespace arc-systems \
  --create-namespace \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

---

## Conditional Execution & Flow Control

```yaml
# Condition on branch + event
- run: ./scripts/deploy.sh
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'

# Continue on error (non-blocking steps)
- run: ./scripts/lint.sh
  continue-on-error: true

# Job dependency and conditional execution
jobs:
  test:
    runs-on: ubuntu-24.04
    outputs:
      result: ${{ steps.run-tests.outcome }}

  deploy:
    needs: [test, build]
    if: |
      needs.test.result == 'success' &&
      needs.build.result == 'success' &&
      github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04

  notify-failure:
    needs: [test, deploy]
    if: failure()          # Runs even if earlier jobs fail
    runs-on: ubuntu-24.04
    steps:
      - run: ./scripts/notify-slack.sh "Pipeline failed!"
```

### Passing Data Between Jobs

```yaml
jobs:
  prepare:
    runs-on: ubuntu-24.04
    outputs:
      version: ${{ steps.get-version.outputs.version }}
      should-deploy: ${{ steps.check.outputs.deploy }}

    steps:
      - id: get-version
        run: |
          VERSION=$(tr -d '\r\n' < VERSION)
          case "$VERSION" in
            ""|*[!0-9A-Za-z._-]*) echo "Invalid VERSION" >&2; exit 1 ;;
          esac
          printf 'version=%s\n' "$VERSION" >> "$GITHUB_OUTPUT"

      - id: check
        run: |
          if git log -1 --pretty=%B | grep -q '\[deploy\]'; then
            echo "deploy=true" >> $GITHUB_OUTPUT
          else
            echo "deploy=false" >> $GITHUB_OUTPUT
          fi

  build:
    needs: prepare
    if: needs.prepare.outputs.should-deploy == 'true'
    runs-on: ubuntu-24.04
    steps:
      - env:
          VERSION: ${{ needs.prepare.outputs.version }}
        run: echo "Building version $VERSION"
```

---

## Security Hardening

### 1. Always Declare Permissions (Least Privilege)

```yaml
# Workflow-level default — restrict everything
permissions:
  contents: read

jobs:
  publish:
    # Job-level override — only expand what's needed
    permissions:
      contents: write        # Only for release/publish jobs
      packages: write        # Only for container push jobs
      pull-requests: write   # Only for PR comment jobs
      id-token: write        # Only for OIDC auth jobs
```

### 2. Pin Third-Party Actions to Full Commit SHA

```yaml
# ❌ UNSAFE — tag can be mutated or hijacked
- uses: actions/checkout@v4

# ✅ SAFE — commit SHA is immutable
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Tool to automate SHA pinning:
# npx pin-github-action .github/workflows/*.yml
# or: pip install ratchet && ratchet pin .github/workflows/
```

### 3. Prevent Script Injection

```yaml
# ❌ UNSAFE — attacker controls PR title, which gets expanded in shell
- run: echo "${{ github.event.pull_request.title }}"

# ✅ SAFE — pass through environment variable (shell doesn't evaluate it)
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "$PR_TITLE"

# ✅ SAFE — expressions in if: conditions are evaluated by Actions, not shell
- if: github.event.pull_request.draft == false
  run: echo "Not a draft"
```

Never place `${{ ... }}` directly inside `run:` when the value can come from
PR metadata, workflow inputs, repository files, matrix JSON, or earlier job
outputs. Put it in `env:` first, validate allowlisted values where possible, and
reference the shell variable with quotes.

### 4. Restrict `pull_request_target` Usage

```yaml
# Only run when a maintainer adds a specific label — prevents untrusted execution
on:
  pull_request_target:
    types: [labeled]

jobs:
  validate:
    # Double-guard: check label name AND author_association
    if: |
      github.event.label.name == 'safe-to-test' &&
      (github.event.pull_request.author_association == 'COLLABORATOR' ||
       github.event.pull_request.author_association == 'MEMBER' ||
       github.event.pull_request.author_association == 'OWNER')
```

### 5. Harden with StepSecurity

```yaml
# Add to every workflow — hardens runner, monitors outbound traffic
- uses: step-security/harden-runner@4d991eb9995541a0b71d1b66f1f98a5f1bef422c  # v2.11.0
  with:
    egress-policy: audit          # Start with 'audit', move to 'block' after confirming allowlist
    allowed-endpoints: >
      api.github.com:443
      registry.npmjs.org:443
      objects.githubusercontent.com:443
```

---

## Debugging Techniques

```yaml
# Enable runner diagnostic logging via repo secrets:
# ACTIONS_RUNNER_DEBUG = true
# ACTIONS_STEP_DEBUG = true

# Dump full GitHub context for inspection
- name: Debug — dump github context
  if: runner.debug == '1'
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
  run: echo "$GITHUB_CONTEXT" | jq '.'

# Dump all available contexts
- name: Debug — dump all contexts
  if: runner.debug == '1'
  run: |
    echo "github: ${{ toJson(github) }}"
    echo "env: ${{ toJson(env) }}"
    echo "vars: ${{ toJson(vars) }}"
    echo "runner: ${{ toJson(runner) }}"

# SSH into a failing runner for interactive debugging
- uses: mxschmitt/action-tmate@7b04f3521e6b0a9fc56fa8f9f50da4bcfb5fc7b5  # v3.19.0
  if: failure() && runner.debug == '1'
  with:
    limit-access-to-actor: true    # Only the workflow triggerer can SSH in
    timeout-minutes: 30

# Check what's pre-installed on GitHub-hosted runners
- run: |
    echo "=== Tool Versions ===" 
    node --version
    python3 --version
    go version
    docker --version
    echo "=== Disk Space ==="
    df -h
    echo "=== Memory ==="
    free -h
```

---

## Complete Pipeline Patterns

### Pattern 1: Build → Test → Push → Deploy

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

permissions:
  contents: read

jobs:
  # ── Build & Test ──────────────────────────────────────
  build-test:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    permissions:
      contents: read
      checks: write        # For test result reporting

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run test -- --coverage
      - run: npm run build

      - uses: actions/upload-artifact@b4b15b8c7c6ac21ea08fcf65892d2ee8f75cf882  # v4.4.3
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7

  # ── Push Image (main branch only) ─────────────────────
  push-image:
    needs: build-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    permissions:
      contents: read
      packages: write
      id-token: write      # For OIDC
    outputs:
      image-digest: ${{ steps.push.outputs.digest }}

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: docker/setup-buildx-action@c47758b77c9736f4b2ef4073d4d51994fabfe349  # v3.7.1

      - uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567  # v3.3.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@70b2cdc6480c1a8b86edf1777157f8f437de2166  # v5.5.1
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,format=long
            type=raw,value=latest

      - id: push
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true    # SLSA provenance attestation
          sbom: true          # Software Bill of Materials

  # ── Deploy Staging ────────────────────────────────────
  deploy-staging:
    needs: push-image
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    environment:
      name: staging
      url: https://staging.myapp.com
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - env:
          IMAGE_DIGEST: ${{ needs.push-image.outputs.image-digest }}
        run: ./scripts/deploy.sh staging "$IMAGE_DIGEST"

  # ── Deploy Production (manual approval required) ──────
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    environment:
      name: production
      url: https://myapp.com
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - env:
          IMAGE_DIGEST: ${{ needs.push-image.outputs.image-digest }}
        run: ./scripts/deploy.sh production "$IMAGE_DIGEST"
```

### Pattern 2: Automated Release with Changelog

```yaml
name: Release

on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-24.04
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          fetch-depth: 0    # Full history needed for changelog generation

      - uses: softprops/action-gh-release@e7a8f85e1c67a31e6ed99a94b41bd0b71bbee6b8  # v2.0.9
        with:
          generate_release_notes: true    # Auto-generates from PR titles and commits
          make_latest: true
          fail_on_unmatched_files: true
          files: |
            dist/**/*.tar.gz
            dist/**/*.zip
```

### Pattern 3: Dependency Auto-Update with PR

```yaml
name: Dependency Updates

on:
  schedule:
    - cron: '0 9 * * 1'    # Every Monday at 9am UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  update-deps:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: '20'

      - run: npx npm-check-updates -u
      - run: npm install

      - uses: peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f  # v7.0.5
        with:
          commit-message: 'chore: update npm dependencies'
          title: 'chore: update npm dependencies'
          branch: 'chore/npm-updates'
          delete-branch: true
          body: |
            Automated dependency updates generated by the dependency update workflow.
            Please review and test before merging.
```

### Pattern 4: Security Scanning Pipeline

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'    # Daily at 6am UTC

permissions:
  contents: read
  security-events: write    # For uploading SARIF results

jobs:
  codeql:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    permissions:
      security-events: write
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: github/codeql-action/init@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
        with:
          languages: javascript-typescript
      - uses: github/codeql-action/autobuild@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
      - uses: github/codeql-action/analyze@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1

  container-scan:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8  # v0.28.0
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      - uses: github/codeql-action/upload-sarif@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## Common Pitfalls & Fixes

| Problem | Cause | Fix |
|---|---|---|
| Workflow doesn't trigger on PR from fork | Fork PRs use restricted `GITHUB_TOKEN` | Use `pull_request` not `pull_request_target`; avoid repo secrets in fork context |
| Secret is `***` in logs but exposed | Dynamic value not masked | Use `echo "::add-mask::$VALUE"` before using it |
| Cache never hits across branches | Cache key too specific | Add `restore-keys` fallback without branch or hash segment |
| Matrix job fails silently | `fail-fast: true` (default) cancels siblings | Set `fail-fast: false` during debugging |
| Job hangs indefinitely | No `timeout-minutes` set | Always set `timeout-minutes` on every job |
| `$GITHUB_OUTPUT` not set | Old `set-output` command used | Use `echo "key=value" >> $GITHUB_OUTPUT` |
| OIDC token request fails | Missing `id-token: write` permission | Add to job-level `permissions` block |
| Reusable workflow can't access caller secrets | No `secrets: inherit` | Add `secrets: inherit` or explicitly pass secrets |

---

## GitHub Actions Expressions Reference

```yaml
# Context objects available in expressions
${{ github.sha }}                           # Commit SHA
${{ github.ref }}                           # Branch/tag ref
${{ github.ref_name }}                      # Short branch/tag name
${{ github.event_name }}                    # Event name (push, pull_request, etc.)
${{ github.actor }}                         # Username who triggered the run
${{ github.repository }}                    # org/repo
${{ github.run_id }}                        # Unique run ID
${{ runner.os }}                            # Linux, Windows, macOS

# Built-in functions
${{ toJson(github) }}                       # Serialize context to JSON
${{ fromJson(needs.job.outputs.matrix) }}   # Parse JSON string
${{ hashFiles('**/package-lock.json') }}    # Hash file(s) for cache keys
${{ format('{0}/{1}', var1, var2) }}        # String formatting
${{ join(matrix.items, ',') }}              # Join array

# Status functions (use in if: conditions)
${{ success() }}    # All previous steps succeeded
${{ failure() }}    # Any previous step failed
${{ cancelled() }}  # Workflow was cancelled
${{ always() }}     # Always runs (success OR failure OR cancelled)
```

---

## Production Readiness Checklist

Before merging any workflow to `main`, verify:

### Security
- [ ] All third-party actions pinned to full commit SHA
- [ ] `permissions:` declared at workflow and job level (least privilege)
- [ ] No `${{ }}` expressions directly in `run:` blocks (use env vars)
- [ ] OIDC used for cloud credentials (no long-lived secrets stored)
- [ ] `pull_request_target` gated with label check + author_association guard
- [ ] Secrets never echoed or logged

### Reliability
- [ ] `timeout-minutes` set on every job
- [ ] `fail-fast: false` set for matrix builds used for debugging
- [ ] `concurrency` configured to cancel stale runs
- [ ] Retry logic for flaky external calls
- [ ] Artifact retention policy set appropriately

### Performance
- [ ] Dependency caching configured (setup-* cache or actions/cache)
- [ ] Docker layer caching enabled (`type=gha`)
- [ ] Path filters on `push`/`pull_request` to skip unrelated changes
- [ ] Matrix parallelism appropriate (not exhausting runner pool)

### Maintainability
- [ ] Reusable workflows used for repeated patterns
- [ ] Composite actions used for repeated step sequences
- [ ] Workflow names and step names are human-readable
- [ ] `_` prefix on internal/reusable workflow files
- [ ] Environment protection rules configured for `production`

---

## Related Skills

- `gha-security-review` — Deep security audit of existing workflow files
- `github-actions-templates` — Copy-paste ready workflow templates
- `docker-expert` — Container build optimization and Dockerfile best practices
- `kubernetes-architect` — Deploying to Kubernetes from GitHub Actions
- `gitlab-ci-patterns` — GitLab CI/CD equivalent patterns

## Limitations

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Always test reusable workflows in a feature branch before merging to main.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## global-chat-agent-discovery
*Discover and search 18K+ MCP servers and AI agents across 6+ registries using Global Chat's cross-protocol directory and MCP server.*

Tags: [mcp, ai-agents, agent-discovery, agents-txt, a2a, developer-tools]
Tools: [claude, cursor, gemini, codex]
Risk: safe

# Global Chat Agent Discovery

## Overview

Global Chat is a cross-protocol AI agent discovery platform that aggregates MCP servers and AI agents from 6+ registries into a single searchable directory. This skill helps you find the right MCP server, A2A agent, or agents.txt endpoint for any task by searching across 18,000+ indexed entries. It also provides an MCP server (`@global-chat/mcp-server`) for programmatic access to the directory from any MCP-compatible client.

## When to Use This Skill

- Use when you need to find an MCP server for a specific capability (e.g., database access, file conversion, API integration)
- Use when evaluating which agent registries carry tools for your use case
- Use when you want to search across multiple protocols (MCP, A2A, agents.txt) simultaneously
- Use when setting up agent-to-agent communication and need to discover available endpoints

## How It Works

### Option 1: Use the MCP Server (Recommended for Agents)

Install the Global Chat MCP server to search the directory programmatically from Claude Code, Cursor, or any MCP client.

```bash
npm install -g @global-chat/mcp-server
```

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "global-chat": {
      "command": "npx",
      "args": ["-y", "@global-chat/mcp-server"]
    }
  }
}
```

Then ask your agent to search for tools:

```
Search Global Chat for MCP servers that handle PostgreSQL database queries.
```

### Option 2: Use the Web Directory

Browse the full directory at [https://global-chat.io](https://global-chat.io):

1. Visit the search page and enter your query
2. Filter by protocol (MCP, A2A, agents.txt)
3. Filter by registry source
4. View server details, capabilities, and installation instructions

### Option 3: Validate Your agents.txt

If you maintain an `agents.txt` file, use the free validator:

1. Go to [https://global-chat.io/validate](https://global-chat.io/validate)
2. Enter your domain or paste your agents.txt content
3. Get instant feedback on format compliance and discoverability

## Examples

### Example 1: Find MCP Servers for a Task

```
You: "Find MCP servers that can convert PDF files to text"
Agent (via Global Chat MCP): Searching across 6 registries...
  - @anthropic/pdf-tools (mcpservers.org) — PDF parsing and text extraction
  - pdf-converter-mcp (mcp.so) — Convert PDF to text, markdown, or HTML
  - ...
```

### Example 2: Discover A2A Agents

```
You: "What A2A agents are available for code review?"
Agent (via Global Chat MCP): Found 12 A2A agents for code review across 3 registries...
```

### Example 3: Check Agent Protocol Coverage

```
You: "How many registries list tools for Kubernetes management?"
Agent (via Global Chat MCP): 4 registries carry Kubernetes-related agents (23 total entries)...
```

## Best Practices

- Use the MCP server for automated workflows and agent-to-agent discovery
- Use the web directory for manual exploration and comparison
- Validate your agents.txt before publishing to ensure maximum discoverability
- Check multiple registries — coverage varies significantly by domain

## Common Pitfalls

- **Problem:** Search returns too many results
  **Solution:** Add protocol or registry filters to narrow the scope

- **Problem:** MCP server not connecting
  **Solution:** Ensure `npx` is available and run `npx -y @global-chat/mcp-server` manually first to verify

## Related Skills

- `@mcp-client` - For general MCP client setup and configuration
- `@agent-orchestration-multi-agent-optimize` - For orchestrating multiple discovered agents
- `@agent-memory-mcp` - For persisting discovered agent information across sessions

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## gpt-taste
*Use when generating elite GSAP-heavy frontend pages with strict AIDA structure, wide hero typography, and gapless bento grids.*

Tags: [frontend, design, gsap, motion]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# CORE DIRECTIVE: AWWWARDS-LEVEL DESIGN ENGINEERING

## When to Use

- Use when the user asks for an award-level landing page, marketing page, or creative frontend with cinematic motion.
- Use when GSAP, pinned scroll, scrubbing, card stacking, horizontal motion, or other advanced animation is appropriate.
- Use when the output must avoid narrow six-line hero headings, cheap meta labels, empty bento cells, and generic left-right sections.

## Limitations

- This skill assumes a frontend project can support GSAP or equivalent animation libraries; check dependencies and performance budgets before implementation.
- Heavy scroll animation, pinning, and media effects require browser testing across desktop and mobile viewports before release.
- Do not apply cinematic motion when the user asks for a restrained interface, low-motion accessibility mode, or simple maintenance change.


You are an elite, award-winning frontend design engineer. Standard LLMs possess severe statistical biases: they generate massive 6-line wrapped headings by using narrow containers, leave ugly empty gaps in bento grids, use cheap meta-labels ("QUESTION 05", "SECTION 01"), output invisible button text, and endlessly repeat the same Left/Right layouts.

Your goal is to aggressively break these defaults. Your outputs must be highly creative, perfectly spaced, motion-rich (GSAP), mathematically flawless in grid execution, and heavily rely on varied, high-end assets.

DO NOT USE EMOJIS IN YOUR CODE, COMMENTS, OR OUTPUT. Maintain strictly professional formatting.

## 1. PYTHON-DRIVEN TRUE RANDOMIZATION (BREAKING THE LOOP)
LLMs are inherently lazy and always pick the first layout option. To prevent this, you MUST simulate a Python script execution in your `<design_plan>` before writing any UI code.
Use a deterministic seed (e.g., character count of the user prompt modulo math) to simulate `random.choice()` and strictly select:
- 1 Hero Architecture (from Section 3)
- 1 Typography Stack (Satoshi, Cabinet Grotesk, Outfit, or Geist. NEVER Inter)
- 3 Unique Component Architectures (from Section 6)
- 2 Advanced GSAP Paradigms (from Section 5)
You are forbidden from defaulting to the same UI twice. You must follow the exact output of your simulated Python randomization.

## 2. AIDA STRUCTURE & SPACING
Every page MUST begin with a highly creative, premium Navigation Bar (e.g., floating glass pill, or minimal split nav).
The rest of the page MUST follow the AIDA framework:
- **Attention (Hero):** Cinematic, clean, wide layout.
- **Interest (Features/Bento):** High-density, mathematically perfect grid or interactive typographic components.
- **Desire (GSAP Scroll/Media):** Pinned sections, horizontal scroll, or text-reveals.
- **Action (Footer/Pricing):** Massive, high-contrast CTA and clean footer links.
**SPACING RULE:** Add huge vertical padding between all major sections (e.g., `py-32 md:py-48`). Sections must feel like distinct, cinematic chapters. Do not cramp elements together.

## 3. HERO ARCHITECTURE & THE 2-LINE IRON RULE
The Hero must breathe. It must NOT be a narrow, 6-line text wall.
- **The Container Width Fix:** You MUST use ultra-wide containers for the H1 (e.g., `max-w-5xl`, `max-w-6xl`, `w-full`). Allow the words to flow horizontally.
- **The Line Limit:** The H1 MUST NEVER exceed 2 to 3 lines. 4, 5, or 6 lines is a catastrophic failure. Make the font size smaller (`clamp(3rem, 5vw, 5.5rem)`) and the container wider to ensure this.
- **Hero Layout Options (Randomly Assigned via Python):**
  1. *Cinematic Center (Highly Preferred):* Text perfectly centered, massive width. Below the text, exactly two high-contrast CTAs. Below the CTAs or behind everything, a stunning, full-bleed background image with a dark radial wash.
  2. *Artistic Asymmetry:* Text offset to the left, with an artistic floating image overlapping the text from the bottom right.
  3. *Editorial Split:* Text left, image right, but with massive negative space.
- **Button Contrast:** Buttons must be perfectly legible. Dark background = white text. Light background = dark text. Invisible text is a failure.
- **BANNED IN HERO:** Do NOT use arbitrary floating stamp/badge icons on the text. Do NOT use pill-tags under the hero. Do NOT place raw data/stats in the hero.

## 4. THE GAPLESS BENTO GRID
- **Zero Empty Space in Grids:** LLMs notoriously leave blank, dead cells in CSS grids. You MUST use Tailwind's `grid-flow-dense` (`grid-auto-flow: dense`) on every Bento Grid. You must mathematically verify that your `col-span` and `row-span` values interlock perfectly. No grid shall have a missing corner or empty void.
- **Card Restraint:** Do not use too many cards. 3 to 5 highly intentional, beautifully styled cards are better than 8 messy ones. Fill them with a mix of large imagery, dense typography, or CSS effects.

## 5. ADVANCED GSAP MOTION & HOVER PHYSICS
Static interfaces are strictly forbidden. You must write real GSAP (`@gsap/react`, `ScrollTrigger`).
- **Hover Physics:** Every clickable card and image must react. Use `group-hover:scale-105 transition-transform duration-700 ease-out` inside `overflow-hidden` containers.
- **Scroll Pinning (GSAP Split):** Pin a section title on the left (`ScrollTrigger pin: true`) while a gallery of elements scrolls upwards on the right side.
- **Image Scale & Fade Scroll:** Images must start small (`scale: 0.8`). As they scroll into view, they grow to `scale: 1.0`. As they scroll out of view, they smoothly darken and fade out (`opacity: 0.2`).
- **Scrubbing Text Reveals:** Opacity of central paragraph words starts at 0.1 and scrubs to 1.0 sequentially as the user scrolls.
- **Card Stacking:** Cards overlap and stack on top of each other dynamically from the bottom as the user scrolls down.

## 6. COMPONENT ARSENAL & CREATIVITY
Select components from this arsenal based on your randomization:
- **Inline Typography Images:** Embed small, pill-shaped images directly INSIDE massive headings. Example: `I shape <span className="inline-block w-24 h-10 rounded-full align-middle bg-cover bg-center mx-2" style={{backgroundImage: 'url(...)'}}></span> digital spaces.`
- **Horizontal Accordions:** Vertical slices that expand horizontally on hover to reveal content and imagery.
- **Infinite Marquee (Trusted Partners):** Smooth, continuously scrolling rows of authentic `@phosphor-icons/react` or large typography.
- **Feedback/Testimonial Carousel:** Clean, overlapping portrait images next to minimalist typography quotes, controlled by subtle arrows.

## 7. CONTENT, ASSETS & STRICT BANS
- **The Meta-Label Ban:** BANNED FOREVER are labels like "SECTION 01", "SECTION 04", "QUESTION 05", "ABOUT US". Remove them entirely. They look cheap and unprofessional.
- **Image Context & Style:** Use `https://picsum.photos/seed/{keyword}/1920/1080` and match the keyword to the vibe. Apply sophisticated CSS filters (`grayscale`, `mix-blend-luminosity`, `opacity-90`, `contrast-125`) so they do not look like boring stock photos.
- **Creative Backgrounds:** Inject subtle, professional ambient design. Use deep radial blurs, grainy mesh gradients, or shifting dark overlays. Avoid flat, boring colors.
- **Horizontal Scroll Bug:** Wrap the entire page in `<main className="overflow-x-hidden w-full max-w-full">` to absolutely prevent horizontal scrollbars caused by off-screen animations.

## 8. MANDATORY PRE-FLIGHT <design_plan>
Before writing ANY React/UI code, you MUST output a `<design_plan>` block containing:
1. **Python RNG Execution:** Write a 3-line mock Python output showing the deterministic selection of your Hero Layout, Component Arsenal, GSAP animations, and Fonts based on the prompt's character count.
2. **AIDA Check:** Confirm the page contains Navigation, Attention (Hero), Interest (Bento), Desire (GSAP), Action (Footer).
3. **Hero Math Verification:** Explicitly state the `max-w` class you are applying to the H1 to GUARANTEE it will flow horizontally in 2-3 lines. Confirm NO stamp icons or spam tags exist.
4. **Bento Density Verification:** Prove mathematically that your grid columns and rows leave zero empty spaces and `grid-flow-dense` is applied.
5. **Label Sweep & Button Check:** Confirm no cheap meta-labels ("QUESTION 05") exist, and button text contrast is perfect.
Only output the UI code after this rigorous verification is complete.

---

## high-end-visual-design
*Use when designing expensive agency-grade interfaces with premium fonts, spatial rhythm, soft depth, and fluid microinteractions.*

Tags: [frontend, visual-design, motion, ui]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# Agent Skill: Principal UI/UX Architect & Motion Choreographer (Awwwards-Tier)

## When to Use

- Use when the user wants a high-end agency, Awwwards-tier, Apple-like, Linear-like, luxury, or polished visual design.
- Use when building a landing page, portfolio, SaaS UI, consumer product page, or app surface that needs premium depth and motion.
- Use when the design must avoid generic fonts, harsh shadows, static layouts, default navbars, and ordinary Bootstrap-style grids.

## Limitations

- This skill is visual-design focused; it does not replace brand strategy, conversion research, accessibility validation, or production QA.
- Premium fonts, icon sets, images, and motion libraries must exist in the target project or be added intentionally before generated code is used.
- Avoid applying luxury motion and heavy visual treatments to constrained dashboards, regulated products, or low-performance environments.


## 1. Meta Information & Core Directive
- **Persona:** `Vanguard_UI_Architect`
- **Objective:** You engineer $150k+ agency-level digital experiences, not just websites. Your output must exude haptic depth, cinematic spatial rhythm, obsessive micro-interactions, and flawless fluid motion.
- **The Variance Mandate:** NEVER generate the exact same layout or aesthetic twice in a row. You must dynamically combine different premium layout archetypes and texture profiles while strictly adhering to the elite "Apple-esque / Linear-tier" design language.

## 2. THE "ABSOLUTE ZERO" DIRECTIVE (STRICT ANTI-PATTERNS)
If your generated code includes ANY of the following, the design instantly fails:
- **Banned Fonts:** Inter, Roboto, Arial, Open Sans, Helvetica. (Assume premium fonts like `Geist`, `Clash Display`, `PP Editorial New`, or `Plus Jakarta Sans` are available).
- **Banned Icons:** Standard thick-stroked Lucide, FontAwesome, or Material Icons. Use only ultra-light, precise lines (e.g., Phosphor Light, Remix Line).
- **Banned Borders & Shadows:** Generic 1px solid gray borders. Harsh, dark drop shadows (`shadow-md`, `rgba(0,0,0,0.3)`).
- **Banned Layouts:** Edge-to-edge sticky navbars glued to the top. Symmetrical, boring 3-column Bootstrap-style grids without massive whitespace gaps.
- **Banned Motion:** Standard `linear` or `ease-in-out` transitions. Instant state changes without interpolation.

## 3. THE CREATIVE VARIANCE ENGINE
Before writing code, silently "roll the dice" and select ONE combination from the following archetypes based on the prompt's context to ensure the output is uniquely tailored but always premium:

### A. Vibe & Texture Archetypes (Pick 1)
1. **Ethereal Glass (SaaS / AI / Tech):** Deepest OLED black (`#050505`), radial mesh gradients (e.g., subtle glowing purple/emerald orbs) in the background. Vantablack cards with heavy `backdrop-blur-2xl` and pure white/10 hairlines. Wide geometric Grotesk typography.
2. **Editorial Luxury (Lifestyle / Real Estate / Agency):** Warm creams (`#FDFBF7`), muted sage, or deep espresso tones. High-contrast Variable Serif fonts for massive headings. Subtle CSS noise/film-grain overlay (`opacity-[0.03]`) for a physical paper feel.
3. **Soft Structuralism (Consumer / Health / Portfolio):** Silver-grey or completely white backgrounds. Massive bold Grotesk typography. Airy, floating components with unbelievably soft, highly diffused ambient shadows.

### B. Layout Archetypes (Pick 1)
1. **The Asymmetrical Bento:** A masonry-like CSS Grid of varying card sizes (e.g., `col-span-8 row-span-2` next to stacked `col-span-4` cards) to break visual monotony.
   - **Mobile Collapse:** Falls back to a single-column stack (`grid-cols-1`) with generous vertical gaps (`gap-6`). All `col-span` overrides reset to `col-span-1`.
2. **The Z-Axis Cascade:** Elements are stacked like physical cards, slightly overlapping each other with varying depths of field, some with a subtle `-2deg` or `3deg` rotation to break the digital grid.
   - **Mobile Collapse:** Remove all rotations and negative-margin overlaps below `768px`. Stack vertically with standard spacing. Overlapping elements cause touch-target conflicts on mobile.
3. **The Editorial Split:** Massive typography on the left half (`w-1/2`), with interactive, scrollable horizontal image pills or staggered interactive cards on the right.
   - **Mobile Collapse:** Converts to a full-width vertical stack (`w-full`). Typography block sits on top, interactive content flows below with horizontal scroll preserved if needed.

**Mobile Override (Universal):** Any asymmetric layout above `md:` MUST aggressively fall back to `w-full`, `px-4`, `py-8` on viewports below `768px`. Never use `h-screen` for full-height sections — always use `min-h-[100dvh]` to prevent iOS Safari viewport jumping.

## 4. HAPTIC MICRO-AESTHETICS (COMPONENT MASTERY)

### A. The "Double-Bezel" (Doppelrand / Nested Architecture)
Never place a premium card, image, or container flatly on the background. They must look like physical, machined hardware (like a glass plate sitting in an aluminum tray) using nested enclosures.
- **Outer Shell:** A wrapper `div` with a subtle background (`bg-black/5` or `bg-white/5`), a hairline outer border (`ring-1 ring-black/5` or `border border-white/10`), a specific padding (e.g., `p-1.5` or `p-2`), and a large outer radius (`rounded-[2rem]`).
- **Inner Core:** The actual content container inside the shell. It has its own distinct background color, its own inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`) for concentric curves.

### B. Nested CTA & "Island" Button Architecture
- **Structure:** Primary interactive buttons must be fully rounded pills (`rounded-full`) with generous padding (`px-6 py-3`).
- **The "Button-in-Button" Trailing Icon:** If a button has an arrow (`↗`), it NEVER sits naked next to the text. It must be nested inside its own distinct circular wrapper (e.g., `w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`) placed completely flush with the main button's right inner padding.

### C. Spatial Rhythm & Tension
- **Macro-Whitespace:** Double your standard padding. Use `py-24` to `py-40` for sections. Allow the design to breathe heavily.
- **Eyebrow Tags:** Precede major H1/H2s with a microscopic, pill-shaped badge (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`).

## 5. MOTION CHOREOGRAPHY (FLUID DYNAMICS)
Never use default transitions. All motion must simulate real-world mass and spring physics. Use custom cubic-beziers (e.g., `transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`).

### A. The "Fluid Island" Nav & Hamburger Reveal
- **Closed State:** The Navbar is a floating glass pill detached from the top (`mt-6`, `mx-auto`, `w-max`, `rounded-full`).
- **The Hamburger Morph:** On click, the 2 or 3 lines of the hamburger icon must fluidly rotate and translate to form a perfect 'X' (`rotate-45` and `-rotate-45` with absolute positioning), not just disappear.
- **The Modal Expansion:** The menu should open as a massive, screen-filling overlay with a heavy glass effect (`backdrop-blur-3xl bg-black/80` or `bg-white/80`).
- **Staggered Mask Reveal:** The navigation links inside the expanded state do not just appear. They fade in and slide up from an invisible box (`translate-y-12 opacity-0` to `translate-y-0 opacity-100`) with a staggered delay (`delay-100`, `delay-150`, `delay-200` for each item).

### B. Magnetic Button Hover Physics
- Use the `group` utility. On hover, do not just change the background color.
- Scale the entire button down slightly (`active:scale-[0.98]`) to simulate physical pressing.
- The nested inner icon circle should translate diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and scale up slightly (`scale-105`), creating internal kinetic tension.

### C. Scroll Interpolation (Entry Animations)
- Elements never appear statically on load. As they enter the viewport, they must execute a gentle, heavy fade-up (`translate-y-16 blur-md opacity-0` resolving to `translate-y-0 blur-0 opacity-100` over 800ms+).
- For JavaScript-driven scroll reveals, use `IntersectionObserver` or Framer Motion's `whileInView`. Never use `window.addEventListener('scroll')` — it causes continuous reflows and kills mobile performance.

## 6. PERFORMANCE GUARDRAILS
- **GPU-Safe Animation:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`. Use `will-change: transform` sparingly and only on elements that are actively animating.
- **Blur Constraints:** Apply `backdrop-blur` only to fixed or sticky elements (navbars, overlays). Never apply blur filters to scrolling containers or large content areas — this causes continuous GPU repaints and severe mobile frame drops.
- **Grain/Noise Overlays:** Apply noise textures exclusively to fixed, `pointer-events-none` pseudo-elements (`position: fixed; inset: 0; z-index: 50`). Never attach them to scrolling containers.
- **Z-Index Discipline:** Do not use arbitrary `z-50` or `z-[9999]`. Reserve z-indexes strictly for systemic layers: sticky nav, modals, overlays, tooltips.

## 7. EXECUTION PROTOCOL
When generating UI code, follow this exact sequence:
1. **[SILENT THOUGHT]** Roll the Variance Engine (Section 3). Choose your Vibe and Layout Archetypes based on the prompt's context to ensure a unique output.
2. **[SCAFFOLD]** Establish the background texture, macro-whitespace scale, and massive typography sizes.
3. **[ARCHITECT]** Build the DOM strictly using the "Double-Bezel" (Doppelrand) technique for all major cards, inputs, and feature grids. Use exaggerated squircle radii (`rounded-[2rem]`).
4. **[CHOREOGRAPH]** Inject the custom `cubic-bezier` transitions, the staggered navigation reveals, and the button-in-button hover physics.
5. **[OUTPUT]** Deliver flawless, pixel-perfect React/Tailwind/HTML code. Do not include basic, generic fallbacks.

## 8. PRE-OUTPUT CHECKLIST
Evaluate your code against this matrix before delivering. This is the last filter.
- [ ] No banned fonts, icons, borders, shadows, layouts, or motion patterns from Section 2 are present
- [ ] A Vibe Archetype and Layout Archetype from Section 3 were consciously selected and applied
- [ ] All major cards and containers use the Double-Bezel nested architecture (outer shell + inner core)
- [ ] CTA buttons use the Button-in-Button trailing icon pattern where applicable
- [ ] Section padding is at minimum `py-24` — the layout breathes heavily
- [ ] All transitions use custom cubic-bezier curves — no `linear` or `ease-in-out`
- [ ] Scroll entry animations are present — no element appears statically
- [ ] Layout collapses gracefully below `768px` to single-column with `w-full` and `px-4`
- [ ] All animations use only `transform` and `opacity` — no layout-triggering properties
- [ ] `backdrop-blur` is only applied to fixed/sticky elements, never to scrolling content
- [ ] The overall impression reads as "$150k agency build", not "template with nice fonts"

---

## industrial-brutalist-ui
*Use when creating raw industrial or tactical telemetry UIs with rigid grids, stark typography, CRT effects, and high-density data.*

Tags: [frontend, design, brutalism, ui]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# SKILL: Industrial Brutalism & Tactical Telemetry UI

## When to Use

- Use when the user wants a brutalist, industrial, Swiss-print, CRT terminal, or tactical telemetry interface.
- Use when building data-heavy dashboards, portfolios, editorial pages, or command-center UIs that should feel raw and mechanical.
- Use when a design must reject soft gradients, rounded consumer UI, glassmorphism, and generic SaaS card layouts.

## Limitations

- This style is intentionally severe and may not fit consumer products, accessibility-sensitive flows, or brands that require warmth and softness.
- CRT, halftone, dithering, and degradation effects must be tested for readability, contrast, and motion sensitivity.
- Do not mix the light industrial and dark telemetry palettes in the same interface unless the user explicitly asks for a controlled hybrid.


## 1. Skill Meta
**Name:** Industrial Brutalism & Tactical Telemetry Interface Engineering
**Description:** Advanced proficiency in architecting web interfaces that synthesize mid-century Swiss Typographic design, industrial manufacturing manuals, and retro-futuristic aerospace/military terminal interfaces. This discipline requires absolute mastery over rigid modular grids, extreme typographic scale contrast, purely utilitarian color palettes, and the programmatic simulation of analog degradation (halftones, CRT scanlines, bitmap dithering). The objective is to construct digital environments that project raw functionality, mechanical precision, and high data density, deliberately discarding conventional consumer UI patterns.

## 2. Visual Archetypes
The design system operates by merging two distinct but highly compatible visual paradigms. **Pick ONE per project and commit to it. Do not alternate or mix both modes within the same interface.**

### 2.1 Swiss Industrial Print
Derived from 1960s corporate identity systems and heavy machinery blueprints.
*   **Characteristics:** High-contrast light modes (newsprint/off-white substrates). Reliance on monolithic, heavy sans-serif typography. Unforgiving structural grids outlined by visible dividing lines. Aggressive, asymmetric use of negative space punctuated by oversized, viewport-bleeding numerals or letterforms. Heavy use of primary red as an alert/accent color.

### 2.2 Tactical Telemetry & CRT Terminal
Derived from classified military databases, legacy mainframes, and aerospace Heads-Up Displays (HUDs).
*   **Characteristics:** Dark mode exclusivity. High-density tabular data presentation. Absolute dominance of monospaced typography. Integration of technical framing devices (ASCII brackets, crosshairs). Application of simulated hardware limitations (phosphor glow, scanlines, low bit-depth rendering).

## 3. Typographic Architecture
Typography is the primary structural and decorative infrastructure. Imagery is secondary. The system demands extreme variance in scale, weight, and spacing.

### 3.1 Macro-Typography (Structural Headers)
*   **Classification:** Neo-Grotesque / Heavy Sans-Serif.
*   **Optimal Web Fonts:** Neue Haas Grotesk (Black), Inter (Extra Bold/Black), Archivo Black, Roboto Flex (Heavy), Monument Extended.
*   **Implementation Parameters:**
    *   **Scale:** Deployed at massive scales using fluid typography (e.g., `clamp(4rem, 10vw, 15rem)`).
    *   **Tracking (Letter-spacing):** Extremely tight, often negative (`-0.03em` to `-0.06em`), forcing glyphs to form solid architectural blocks.
    *   **Leading (Line-height):** Highly compressed (`0.85` to `0.95`).
    *   **Casing:** Exclusively uppercase for structural impact.

### 3.2 Micro-Typography (Data & Telemetry)
*   **Classification:** Monospace / Technical Sans.
*   **Optimal Web Fonts:** JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime.
*   **Implementation Parameters:**
    *   **Scale:** Fixed and small (`10px` to `14px` / `0.7rem` to `0.875rem`).
    *   **Tracking:** Generous (`0.05em` to `0.1em`) to simulate mechanical typewriter spacing or terminal matrices.
    *   **Leading:** Standard to tight (`1.2` to `1.4`).
    *   **Casing:** Exclusively uppercase. Used for all metadata, navigation, unit IDs, and coordinates.

### 3.3 Textural Contrast (Artistic Disruption)
*   **Classification:** High-Contrast Serif.
*   **Optimal Web Fonts:** Playfair Display, EB Garamond, Times New Roman.
*   **Implementation Parameters:** Used exceedingly sparingly. Must be subjected to heavy post-processing (halftone filters, 1-bit dithering) to degrade vector perfection and create textural juxtaposition against the clean sans-serifs.

## 4. Color System
The color architecture is uncompromising. Gradients, soft drop shadows, and modern translucency are strictly prohibited. Colors simulate physical media or primitive emissive displays.

**CRITICAL: Choose ONE substrate palette per project and use it consistently. Never mix light and dark substrates within the same interface.**

### If Swiss Industrial Print (Light):
*   **Background:** `#F4F4F0` or `#EAE8E3` (Matte, unbleached documentation paper).
*   **Foreground:** `#050505` to `#111111` (Carbon Ink).
*   **Accent:** `#E61919` or `#FF2A2A` (Aviation/Hazard Red). This is the ONLY accent color. Used for strike-throughs, thick structural dividing lines, or vital data highlights.

### If Tactical Telemetry (Dark):
*   **Background:** `#0A0A0A` or `#121212` (Deactivated CRT. Avoid pure `#000000`).
*   **Foreground:** `#EAEAEA` (White phosphor). This is the primary text color.
*   **Accent:** `#E61919` or `#FF2A2A` (Aviation/Hazard Red). Same red, same rules.
*   **Terminal Green (`#4AF626`):** Optional. Use ONLY for a single specific UI element (e.g., one status indicator or one data readout) — never as a general text color. If it doesn't serve a clear purpose, omit it entirely.

## 5. Layout and Spatial Engineering
The layout must appear mathematically engineered. It rejects conventional web padding in favor of visible compartmentalization.

*   **The Blueprint Grid:** Strict adherence to CSS Grid architectures. Elements do not float; they are anchored precisely to grid tracks and intersections.
*   **Visible Compartmentalization:** Extensive utilization of solid borders (`1px` or `2px solid`) to delineate distinct zones of information. Horizontal rules (`<hr>`) frequently span the entire container width to segregate operational units.
*   **Bimodal Density:** Layouts oscillate between extreme data density (tightly packed monospace metadata clustered together) and vast expanses of calculated negative space framing macro-typography.
*   **Geometry:** Absolute rejection of `border-radius`. All corners must be exactly 90 degrees to enforce mechanical rigidity.

## 6. UI Components and Symbology
Standard web UI conventions are replaced with utilitarian, industrial graphic elements.

*   **Syntax Decoration:** Utilization of ASCII characters to frame data points.
    *   *Framing:* `[ DELIVERY SYSTEMS ]`, `< RE-IND >`
    *   *Directional:* `>>>`, `///`, `\\\\`
*   **Industrial Markers:** Prominent integration of registration (`®`), copyright (`©`), and trademark (`™`) symbols functioning as structural geometric elements rather than legal text.
*   **Technical Assets:** Integration of crosshairs (`+`) at grid intersections, repeating vertical lines (barcodes), thick horizontal warning stripes, and randomized string data (e.g., `REV 2.6`, `UNIT / D-01`) to simulate active mechanical processes.

## 7. Textural and Post-Processing Effects
To prevent the design from appearing purely digital, simulated analog degradation is engineered into the frontend via CSS and SVG filters.

*   **Halftone and 1-Bit Dithering:** Transforming continuous-tone images or large serif typography into dot-matrix patterns. Achieved via pre-processing or CSS `mix-blend-mode: multiply` overlays combined with SVG radial dot patterns.
*   **CRT Scanlines:** For terminal interfaces, applying a `repeating-linear-gradient` to the background to simulate horizontal electron beam sweeps (e.g., `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`).
*   **Mechanical Noise:** A global, low-opacity SVG static/noise filter applied to the DOM root to introduce a unified physical grain across both dark and light modes.

## 8. Web Engineering Directives
1.  **Grid Determinism:** Utilize `display: grid; gap: 1px;` with contrasting parent/child background colors to generate mathematically perfect, razor-thin dividing lines without complex border declarations.
2.  **Semantic Rigidity:** Construct the DOM using precise semantic tags (`<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>`) to accurately reflect the technical nature of the telemetry.
3.  **Typography Clamping:** Implement CSS `clamp()` functions exclusively for macro-typography to ensure massive text scales aggressively while maintaining structural integrity across viewports.

---

## jq
*Expert jq usage for JSON querying, filtering, transformation, and pipeline integration. Practical patterns for real shell workflows.*

Tags: [jq, json, shell, cli, data-transformation, bash]
Tools: [claude, cursor, gemini]
Risk: safe

# jq — JSON Querying and Transformation

## Overview

`jq` is the standard CLI tool for querying and reshaping JSON. This skill covers practical, expert-level usage: filtering deeply nested data, transforming structures, aggregating values, and composing `jq` into shell pipelines. Every example is copy-paste ready for real workflows.

## When to Use This Skill

- Use when parsing JSON output from APIs, CLI tools (AWS, GitHub, kubectl, docker), or log files
- Use when transforming JSON structure (rename keys, flatten arrays, group records)
- Use when the user needs `jq` inside a bash script or one-liner
- Use when explaining what a complex `jq` expression does

## How It Works

`jq` takes a filter expression and applies it to JSON input. Filters compose with pipes (`|`), and `jq` handles arrays, objects, strings, numbers, booleans, and `null` natively.

### Basic Selection

```bash
# Extract a field
echo '{"name":"alice","age":30}' | jq '.name'
# "alice"

# Nested access
echo '{"user":{"email":"a@b.com"}}' | jq '.user.email'

# Array index
echo '[10, 20, 30]' | jq '.[1]'
# 20

# Array slice
echo '[1,2,3,4,5]' | jq '.[2:4]'
# [3, 4]

# All array elements
echo '[{"id":1},{"id":2}]' | jq '.[]'
```

### Filtering with `select`

```bash
# Keep only matching elements
echo '[{"role":"admin"},{"role":"user"},{"role":"admin"}]' \
  | jq '[.[] | select(.role == "admin")]'

# Numeric comparison
curl -s https://api.github.com/repos/owner/repo/issues \
  | jq '[.[] | select(.comments > 5)]'

# Test a field exists and is non-null
jq '[.[] | select(.email != null)]'

# Combine conditions
jq '[.[] | select(.active == true and .score >= 80)]'
```

### Mapping and Transformation

```bash
# Extract a field from every array element
echo '[{"name":"alice","age":30},{"name":"bob","age":25}]' \
  | jq '[.[] | .name]'
# ["alice", "bob"]

# Shorthand: map()
jq 'map(.name)'

# Build a new object per element
jq '[.[] | {user: .name, years: .age}]'

# Add a computed field
jq '[.[] | . + {senior: (.age > 28)}]'

# Rename keys
jq '[.[] | {username: .name, email_address: .email}]'
```

### Aggregation and Reduce

```bash
# Sum all values
echo '[1, 2, 3, 4, 5]' | jq 'add'
# 15

# Sum a field across objects
jq '[.[].price] | add'

# Count elements
jq 'length'

# Max / min
jq 'max_by(.score)'
jq 'min_by(.created_at)'

# reduce: custom accumulator
echo '[1,2,3,4,5]' | jq 'reduce .[] as $x (0; . + $x)'
# 15

# Group by field
jq 'group_by(.department)'

# Count per group
jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

### String Interpolation and Formatting

```bash
# String interpolation
jq -r '.[] | "\(.name) is \(.age) years old"'

# Format as CSV (no header)
jq -r '.[] | [.name, .age, .email] | @csv'

# Format as TSV
jq -r '.[] | [.name, .score] | @tsv'

# URL-encode a value
jq -r '.query | @uri'

# Base64 encode
jq -r '.data | @base64'
```

### Working with Keys and Paths

```bash
# List all top-level keys
jq 'keys'

# Check if key exists
jq 'has("email")'

# Delete a key
jq 'del(.password)'

# Delete nested keys from every element
jq '[.[] | del(.internal_id, .raw_payload)]'

# Recursive descent: find all values for a key anywhere in tree
jq '.. | .id? // empty'

# Get all leaf paths
jq '[paths(scalars)]'
```

### Conditionals and Error Handling

```bash
# if-then-else
jq 'if .score >= 90 then "A" elif .score >= 80 then "B" else "C" end'

# Alternative operator: use fallback if null or false
jq '.nickname // .name'

# try-catch: skip errors instead of halting
jq '[.[] | try .nested.value catch null]'

# Suppress null output with // empty
jq '.[] | .optional_field // empty'
```

### Practical Shell Integration

```bash
# Read from file
jq '.users' data.json

# Compact output (no whitespace) for further piping
jq -c '.[]' records.json | while IFS= read -r record; do
  echo "Processing: $record"
done

# Pass a shell variable into jq
STATUS="active"
jq --arg s "$STATUS" '[.[] | select(.status == $s)]'

# Pass a number
jq --argjson threshold 42 '[.[] | select(.value > $threshold)]'

# Slurp multiple JSON lines into an array
jq -s '.' records.ndjson

# Multiple files: slurp all into one array
jq -s 'add' file1.json file2.json

# Null-safe pipeline from a command
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, status: .status.phase}'

# GitHub CLI: extract PR numbers
gh pr list --json number,title | jq -r '.[] | "\(.number)\t\(.title)"'

# AWS CLI: list running instance IDs
aws ec2 describe-instances \
  | jq -r '.Reservations[].Instances[] | select(.State.Name=="running") | .InstanceId'

# Docker: show container names and images
docker inspect $(docker ps -q) | jq -r '.[] | "\(.Name)\t\(.Config.Image)"'
```

### Advanced Patterns

```bash
# Transpose an object of arrays to an array of objects
# Input: {"names":["a","b"],"scores":[10,20]}
jq '[.names, .scores] | transpose | map({name: .[0], score: .[1]})'

# Flatten one level
jq 'flatten(1)'

# Unique by field
jq 'unique_by(.email)'

# Sort, deduplicate and re-index
jq '[.[] | .name] | unique | sort'

# Walk: apply transformation to every node recursively
jq 'walk(if type == "string" then ascii_downcase else . end)'

# env: read environment variables inside jq
export API_KEY=secret
jq -n 'env.API_KEY'
```

## Best Practices

- Always use `-r` (raw output) when passing `jq` results to shell variables or other commands to strip JSON string quotes
- Use `--arg` / `--argjson` to inject shell variables safely — never interpolate shell variables directly into filter strings
- Prefer `map(f)` over `[.[] | f]` for readability
- Use `-c` (compact) for newline-delimited JSON pipelines; omit it for human-readable debugging
- Test filters interactively with `jq -n` and literal input before embedding in scripts
- Use `empty` to drop unwanted elements rather than filtering to `null`

## Security & Safety Notes

- `jq` is read-only by design — it cannot write files or execute commands
- Avoid embedding untrusted JSON field values directly into shell commands; always quote or use `--arg`

## Common Pitfalls

- **Problem:** `jq` outputs `null` instead of the expected value
  **Solution:** Check for typos in key names; use `keys` to inspect actual field names. Remember JSON is case-sensitive.

- **Problem:** Numbers are quoted as strings in the output
  **Solution:** Use `--argjson` instead of `--arg` when injecting numeric values.

- **Problem:** Filter works in the terminal but fails in a script
  **Solution:** Ensure the filter string uses single quotes in the shell to prevent variable expansion. Example: `jq '.field'` not `jq ".field"`.

- **Problem:** `add` returns `null` on an empty array
  **Solution:** Use `add // 0` or `add // ""` to provide a fallback default.

- **Problem:** Streaming large files is slow
  **Solution:** Use `jq --stream` or switch to `jstream`/`gron` for very large files.

## Related Skills

- `@bash-pro` — Wrapping jq calls in robust shell scripts
- `@bash-linux` — General shell pipeline patterns
- `@github-automation` — Using jq with GitHub CLI JSON output

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## k6-load-testing
*Comprehensive k6 load testing skill for API, browser, and scalability testing. Write realistic load scenarios, analyze results, and integrate with CI/CD.*

Tags: [k6, load-testing, performance, api-testing, ci-cd]
Tools: [claude, cursor, gemini]
Risk: safe

# k6 Load Testing

## Overview

k6 is a modern, developer-centric load testing tool that helps you write and execute performance tests for HTTP APIs, WebSocket endpoints, and browser scenarios. This skill provides comprehensive guidance on writing realistic load tests, configuring test scenarios (smoke, load, stress, spike, soak), analyzing results, and integrating with CI/CD pipelines.

Use this skill when you need to validate system performance, identify bottlenecks, ensure SLA compliance, or catch performance regressions before deployment.

---

## When to Use This Skill

- Use when you need to load test HTTP APIs, WebSocket endpoints, or browser scenarios
- Use when setting up performance regression tests in CI/CD
- Use when analyzing system behavior under various load conditions
- Use when comparing performance between code changes
- Use when validating SLA requirements and performance budgets

---

## k6 Basics

### Installation

```bash
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Quick Start

```javascript
// simple-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const res = http.get('https://httpbin.test.k6.io/get');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

Run with: `k6 run simple-test.js`

---

## Test Configuration

### Common Options

```javascript
export const options = {
  // Virtual Users (concurrent users)
  vus: 100,
  
  // Test duration
  duration: '5m',
  
  // Or use stages for ramp-up/ramp-down
  stages: [
    { duration: '30s', target: 20 },   // Ramp up
    { duration: '1m', target: 100 },  // Stay at 100
    { duration: '30s', target: 0 },    // Ramp down
  ],
  
  // Thresholds (SLA)
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% requests < 500ms
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
  
  // Load zones (distributed testing)
  ext: {
    loadimpact: {
      name: 'My Load Test',
      distribution: {
        'amazon:us:ashburn': { weight: 50 },
        'amazon:eu: Dublin': { weight: 50 },
      },
    },
  },
};
```

### Test Types

| Type | Use Case | Configuration |
|------|----------|---------------|
| Smoke Test | Verify basic functionality | Low VUs (1-5), short duration |
| Load Test | Normal expected load | Target VUs based on traffic |
| Stress Test | Find breaking point | Ramp beyond capacity |
| Spike Test | Sudden traffic spikes | Rapid increase/decrease |
| Soak Test | Long-term stability | Extended duration |

---

## HTTP Testing

### Basic Requests

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
  // GET request
  const getRes = http.get('https://api.example.com/users');
  
  check(getRes, {
    'GET succeeded': (r) => r.status === 200,
    'has users': (r) => r.json('data.length') > 0,
  });

  // POST request with JSON body
  const postRes = http.post('https://api.example.com/users', 
    JSON.stringify({ name: 'Test User', email: 'test@example.com' }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + __ENV.API_TOKEN,
      },
    }
  );
  
  check(postRes, {
    'POST succeeded': (r) => r.status === 201,
    'user created': (r) => r.json('id') !== undefined,
  });

  sleep(1);
}
```

### Request Chaining

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  // Login and extract token
  const loginRes = http.post('https://api.example.com/login', 
    JSON.stringify({ email: 'test@example.com', password: 'password123' })
  );
  
  const token = loginRes.json('access_token');
  
  // Use token in subsequent requests
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
  
  const profileRes = http.get('https://api.example.com/profile', {
    headers: headers,
  });
  
  check(profileRes, {
    'profile loaded': (r) => r.status === 200,
  });
}
```

### Parameterized Testing

```javascript
import http from 'k6/http';
import { check } from 'k6';

const usernames = ['user1', 'user2', 'user3', 'user4', 'user5'];

export default function () {
  // Use shared array with VU-specific index
  const username = usernames[__VU % usernames.length];
  
  const res = http.get(`https://api.example.com/users/${username}`);
  
  check(res, {
    'user found': (r) => r.status === 200,
  });
}
```

---

## Browser Testing (k6 Browser)

```javascript
import { browser } from 'k6/browser';

export const options = {
  scenarios: {
    browser_test: {
      executor: 'constant-vus',
      vus: 5,
      duration: '30s',
      browser: {
        type: 'chromium',
      },
    },
  },
};

export default async function () {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://example.com');
    
    const title = await page.title();
    console.log(`Page title: ${title}`);
    
    // Click and interact
    await page.click('button[data-testid="submit"]');
    
    // Wait for response
    await page.waitForSelector('.success-message');
    
  } finally {
    await page.close();
  }
}
```

Install browser support: `k6 install chromium`

---

## WebSocket Testing

```javascript
import ws from 'k6/ws';
import { check } from 'k6';

export default function () {
  const url = 'wss://echo.websocket.org';
  
  ws.connect(url, {}, function (socket) {
    socket.on('open', () => {
      console.log('WebSocket connected');
      socket.send('Hello WebSocket');
    });
    
    socket.on('message', (data) => {
      console.log(`Received: ${data}`);
      check(data, {
        'echo received': (d) => d.includes('Hello'),
      });
    });
    
    socket.on('close', () => {
      console.log('WebSocket closed');
    });
    
    // Send periodic messages
    socket.setInterval(function () {
      socket.send('ping');
    }, 1000);
    
    // Close after 5 seconds
    socket.setTimeout(function () {
      socket.close();
    }, 5000);
  });
}
```

---

## Data Handling

### CSV Data Source

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

// Option 1: Load once, shared across VUs
const users = new SharedArray('users', function () {
  return open('./users.csv').split('\n').slice(1).map(line => {
    const [email, password] = line.split(',');
    return { email, password };
  });
});

export default function () {
  const user = users[__VU % users.length];
  
  const res = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  check(res, { 'login successful': (r) => r.status === 200 });
}
```

### JSON Data Source

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const products = new SharedArray('products', function () {
  return JSON.parse(open('./products.json'));
});

export default function () {
  const product = products[Math.floor(Math.random() * products.length)];
  
  const res = http.get(`https://api.example.com/products/${product.id}`);
  
  check(res, { 'product found': (r) => r.status === 200 });
}
```

---

## Thresholds & SLA

### Basic Thresholds

```javascript
export const options = {
  vus: 50,
  duration: '2m',
  
  thresholds: {
    // Response time thresholds
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    
    // Error rate threshold
    http_req_failed: ['rate<0.01'],
    
    // Throughput threshold
    http_reqs: ['rate>100'],
  },
};
```

### Advanced Thresholds

```javascript
export const options = {
  thresholds: {
    // Multiple thresholds on same metric
    http_req_duration: [
      'p(90)<300',   // 90th percentile < 300ms
      'p(95)<500',  // 95th percentile < 500ms
      'p(99)<1000', // 99th percentile < 1s
      'avg<200',    // average < 200ms
    ],
    
    // Custom metrics
    my_custom_metric: ['avg<100'],
    
    // Abort on threshold failure
    'http_req_duration{method:GET}': ['p(95)<300'],
  },
};
```

---

## Custom Metrics

### Counters

```javascript
import http from 'k6/http';
import { Counter, Trend, Rate, Gauge } from 'k6/metrics';

// Define custom metrics
const myCounter = new Counter('api_calls_total');
const responseTime = new Trend('response_time');
const errorRate = new Rate('error_rate');
const activeUsers = new Gauge('active_users');

export default function () {
  const res = http.get('https://api.example.com/data');
  
  // Increment counter
  myCounter.add(1);
  
  // Add to trend (for percentiles)
  responseTime.add(res.timings.duration);
  
  // Track error rate
  errorRate.add(res.status !== 200);
  
  // Set gauge value
  activeUsers.add(__VU);
  
  // Tagged metrics
  const taggedRes = http.get('https://api.example.com/users', {
    tags: { endpoint: 'users', env: 'prod' },
  });
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/k6-action@v0.2.0
        
      - name: Run load test
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: k6 run --out json=results.json load-test.js
        
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
          
      - name: Check thresholds
        if: failure()
        run: |
          echo "Load test failed thresholds!"
          exit 1
```

### GitLab CI

```yaml
# .gitlab-ci.yml
load_test:
  image: grafana/k6:latest
  script:
    - k6 run load-test.js
  artifacts:
    when: always
    paths:
      - results.json
    reports:
      junit: results.xml
```

---

## Results Analysis

### Built-in Reports

```bash
# Text summary
k6 run load-test.js

# JSON output for parsing
k6 run --out json=results.json load-test.js

# InfluxDB + Grafana
k6 run --out influxdb=http://localhost:8086/k6 load-test.js

# Prometheus remote write
k6 run --out prometheus=localhost:9090/k6 load-test.js

# Cloud results
k6 run --out cloud load-test.js
```

### Interpreting Results

| Metric | Description | Good | Warning | Bad |
|--------|-------------|------|---------|-----|
| http_req_duration (p95) | 95% response time | < 300ms | 300-500ms | > 500ms |
| http_req_failed | Error rate | < 0.1% | 0.1-1% | > 1% |
| http_reqs | Requests/sec | Meeting target | Near limit | At limit |
| vus | Virtual users | Stable | Gradual increase | Unexpected spike |

---

## Examples

### Example 1: Basic API Load Test

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### Example 2: Test with Authentication and Data Parameterization

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', function () {
  return JSON.parse(open('./users.json'));
});

export default function () {
  const user = users[__VU % users.length];
  
  const loginRes = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  const token = loginRes.json('access_token');
  
  const headers = { 'Authorization': `Bearer ${token}` };
  const res = http.get('https://api.example.com/profile', { headers });
  
  check(res, { 'profile loaded': (r) => r.status === 200 });
}
```

---

## Best Practices

- **Start with smoke test**: Verify test works with 1-5 VUs before scaling up
- **Use realistic data**: Parameterize with real user data and behaviors
- **Set meaningful thresholds**: Match your SLA and business requirements
- **Warm up systems**: Include ramp-up time in stages
- **Monitor external dependencies**: Track not just your APIs but downstream services
- **Use tags**: Tag requests for granular analysis (`tags: { endpoint: 'users' }`)
- **Keep tests focused**: One test file per scenario for clarity

---

## Common Pitfalls

- **Problem:** Tests pass locally but fail in CI
  **Solution:** Ensure CI environment has similar resources and network conditions

- **Problem:** Inconsistent results between runs
  **Solution:** Check for external dependencies, random data, or test data pollution

- **Problem:** k6 runs out of memory
  **Solution:** Use ` SharedArray` for large data, reduce VUs, or use `--max-memory` flag

- **Problem:** Thresholds too strict
  **Solution:** Start with relaxed thresholds, tighten based on historical data

---

## Related Skills

- `@performance-engineer` - For broader performance optimization
- `@api-testing-observability-api-mock` - For API mocking during testing
- `@application-performance-performance-optimization` - For performance optimization

---

## Additional Resources

- [k6 Documentation](https://k6.io/docs/)
- [k6 Examples](https://github.com/grafana/k6/tree/master/examples)
- [k6 Load Testing Guides](https://k6.io/guides/)
- [k6 Cloud](https://k6.io/cloud/)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## kubestellar-console
*Multi-cluster Kubernetes dashboard with AI-powered operations via MCP server and 10+ built-in agent skills*

Tags: [kubernetes, multi-cluster, mcp, dashboard, cncf, devops, observability]
Tools: [claude, cursor, gemini, codex]
Risk: critical

# KubeStellar Console

## Overview

KubeStellar Console is an open-source multi-cluster Kubernetes dashboard (CNCF project) with AI-powered operations. It ships with `kc-agent`, an MCP server that bridges coding agents to kubeconfig and Kubernetes APIs, plus 10+ built-in agent skills for development, testing, and operations.

## When to Use This Skill

- Use when managing multiple Kubernetes clusters across edge and cloud
- Use when you need AI-assisted Kubernetes troubleshooting and debugging
- Use when running performance tests, cache compliance checks, or CI debugging on a Kubernetes dashboard
- Use when integrating with CNCF projects (Argo, Kyverno, Istio, and 20+ others)

## How It Works

### Step 1: Install kc-agent

```bash
brew tap kubestellar/tap && brew install kc-agent
```

### Step 2: Start the MCP server

```bash
kc-agent
```

This bridges the active kubeconfig context to any MCP-compatible coding agent. Do not start it from a cluster-admin or write-capable context unless the user explicitly accepts that risk.

### Step 3: Use built-in agent skills

The project ships with agent skills accessible via `CLAUDE.md` and `AGENTS.md`:

- **@perf-test** — Dashboard performance testing and TTFI analysis
- **@cache-test** — Card cache compliance testing (IndexedDB warm return)
- **@nav-test** — Navigation performance testing
- **@ui-compliance-test** — Card loading compliance (8 criteria, 150+ cards)
- **@ci-status** — CI pipeline monitoring and status checks
- **@rca** — Root cause analysis for CI/test failures
- **@tdd** — Test-driven development workflow
- **@k8s-debug** — Kubernetes debugging and troubleshooting

## Key Features

- Multi-cluster management across edge and cloud
- Real-time streaming observability
- 20+ CNCF project integrations (Argo, Kyverno, Istio, etc.)
- GitHub OAuth authentication
- Supply chain security (SBOM, SLSA)
- SQLite WASM caching with stale-while-revalidate pattern
- 15+ themes with dark/light mode

## Security & Safety Notes

- **Critical risk:** `kc-agent` bridges your active kubeconfig context to MCP-compatible agents. If that context carries cluster-admin, write permissions, or secret read access, agents inherit those capabilities.
- **Do not rely on RBAC objects alone:** creating a ServiceAccount or ClusterRoleBinding does not change the credentials `kc-agent` uses. Start `kc-agent` only after switching `KUBECONFIG`/context to dedicated least-privilege credentials and verifying them.
- **Recommended read-only scope:** avoid `resources='*'`, because it includes sensitive objects such as Secrets. Prefer an explicit non-secret resource list and verify access before starting the MCP server:
  ```bash
  kubectl create serviceaccount kc-agent -n default
  kubectl create clusterrole kc-agent-readonly \
    --verb=get,list,watch \
    --resource=pods,services,deployments.apps,replicasets.apps,statefulsets.apps,daemonsets.apps,namespaces,nodes,events,configmaps
  kubectl create clusterrolebinding kc-agent-readonly \
    --clusterrole=kc-agent-readonly \
    --serviceaccount=default:kc-agent
  kubectl auth can-i get secrets --as=system:serviceaccount:default:kc-agent
  kubectl auth can-i list pods --as=system:serviceaccount:default:kc-agent
  ```
- The first `can-i` command must return `no`; the second should return `yes`. Then create or select a kubeconfig that actually authenticates as that ServiceAccount before running `kc-agent`.
- Do not expose `kc-agent` on a public network without authentication.
- Review [SECURITY-AI.md](https://github.com/kubestellar/console/blob/main/docs/security/SECURITY-AI.md) for prompt injection and agent drift mitigations.

## Limitations

- This skill requires an external binary (`kc-agent`) installed separately via Homebrew.
- Do not treat agent output as a substitute for environment-specific validation or expert review.
- Stop and ask for clarification if required permissions or safety boundaries are unclear.

## Links

- [GitHub](https://github.com/kubestellar/console)
- [Website](https://console.kubestellar.io)
- [CLAUDE.md](https://github.com/kubestellar/console/blob/main/CLAUDE.md)
- [AGENTS.md](https://github.com/kubestellar/console/blob/main/AGENTS.md)

---

## lambdatest-agent-skills
*Production-grade test automation skills for 46 frameworks across E2E, unit, mobile, BDD, visual, and cloud testing in 15+ languages.*

Tags: [testing, test-automation, e2e, unit-testing, mobile-testing, bdd, selenium, playwright, cypress, jest, pytest, appium, lambdatest]
Tools: [claude, cursor, gemini, copilot]
Risk: safe

# LambdaTest Agent Skills — Test Automation Registry (46 Skills)

## Overview

This skill is a curated index of 46 production-grade test automation skills sourced from the [LambdaTest/agent-skills](https://github.com/LambdaTest/agent-skills) repository. It teaches AI coding assistants how to write, structure, and execute test automation code across every major framework and 15+ programming languages. Instead of generating generic test code, the AI becomes a senior QA automation architect that understands correct project structure, dependency versions, cloud execution, CI/CD integration, and common debugging patterns for each framework.

This skill adapts material from an external GitHub repository:
- `source_repo: LambdaTest/agent-skills`
- `source_type: community`

## When to Use This Skill

- Use when you need to write, scaffold, or review test automation code for any major framework
- Use when working with Selenium, Playwright, Cypress, Jest, pytest, Appium, or any of the 46 supported frameworks
- Use when setting up a new test project and need the correct project structure, config files, and dependencies
- Use when integrating tests into a CI/CD pipeline (GitHub Actions, Jenkins, GitLab CI)
- Use when migrating tests between frameworks (e.g. Selenium → Playwright, Puppeteer → Cypress)
- Use when running tests on cloud infrastructure such as LambdaTest / TestMu AI
- Use when the user asks how to write, debug, or scale automated tests

## How It Works

### Step 1: Identify the Framework and Language

Determine which testing framework and programming language the user is working with. Match it to one of the 46 supported skills below. Each skill covers a specific framework with language-appropriate code patterns.

### Step 2: Apply the Correct Skill Context

Load the relevant framework skill from the registry below. Each skill includes: project setup and dependencies, core code patterns, page objects or test utilities, cloud execution configuration, CI/CD integration, a debugging table for common problems, and a best practices checklist.

### Step 3: Generate Production-Ready Test Code

Use the loaded skill context to generate test code that follows real-world conventions — not generic boilerplate. Apply correct import paths, configuration formats, assertion libraries, and runner commands specific to the framework and language.

### Step 4: Configure for Local or Cloud Execution

If the user wants to run tests locally, apply local runner configuration. If running on LambdaTest / TestMu AI cloud, configure RemoteWebDriver capabilities or the appropriate cloud SDK, and set `LT_USERNAME` and `LT_ACCESS_KEY` from environment variables — never hardcode credentials.

### Step 5: Add CI/CD Integration

When requested, generate a GitHub Actions (or Jenkins / GitLab CI) workflow that runs the tests in parallel, uploads reports, and captures artifacts on failure.

## Skill Registry

### 🌐 E2E / Browser Testing (15 skills)

| Skill | Languages | Description |
|---|---|---|
| `selenium-skill` | Java, Python, JS, C#, Ruby | Selenium WebDriver with cross-browser and cloud support |
| `playwright-skill` | JS, TS, Python, Java, C# | Playwright browser automation with API mocking |
| `cypress-skill` | JS, TS | Cypress E2E and component testing |
| `webdriverio-skill` | JS, TS | WebdriverIO with page objects and cloud integration |
| `puppeteer-skill` | JS, TS | Puppeteer Chrome automation |
| `testcafe-skill` | JS, TS | TestCafe cross-browser testing |
| `nightwatchjs-skill` | JS, TS | Nightwatch.js browser automation |
| `capybara-skill` | Ruby | Capybara acceptance testing |
| `geb-skill` | Groovy | Geb Groovy browser automation |
| `selenide-skill` | Java | Selenide fluent Selenium wrapper |
| `nemojs-skill` | JS | Nemo.js PayPal browser automation |
| `protractor-skill` | JS, TS | Protractor Angular E2E testing |
| `codeception-skill` | PHP | Codeception full-stack PHP testing |
| `laravel-dusk-skill` | PHP | Laravel Dusk browser testing |
| `robot-framework-skill` | Python, Robot | Robot Framework keyword-driven testing |

### 🧪 Unit Testing (15 skills)

| Skill | Languages | Description |
|---|---|---|
| `jest-skill` | JS, TS | Jest unit and integration tests with mocking |
| `junit-5-skill` | Java | JUnit 5 with parameterized tests and extensions |
| `pytest-skill` | Python | pytest with fixtures, parametrize, and plugins |
| `testng-skill` | Java | TestNG with data providers and parallel execution |
| `vitest-skill` | JS, TS | Vitest for Vite projects |
| `mocha-skill` | JS, TS | Mocha with Chai assertions |
| `jasmine-skill` | JS, TS | Jasmine BDD-style unit testing |
| `karma-skill` | JS, TS | Karma test runner |
| `xunit-skill` | C# | xUnit.net for .NET |
| `nunit-skill` | C# | NUnit for .NET |
| `mstest-skill` | C# | MSTest for .NET |
| `rspec-skill` | Ruby | RSpec with shared examples |
| `phpunit-skill` | PHP | PHPUnit with data providers |
| `testunit-skill` | Ruby | Test::Unit Ruby testing |
| `unittest-skill` | Python | Python unittest with mocking |

### 📱 Mobile Testing (5 skills)

| Skill | Languages | Description |
|---|---|---|
| `appium-skill` | Java, Python, JS, Ruby, C# | Appium mobile testing for iOS and Android |
| `espresso-skill` | Java, Kotlin | Espresso Android UI testing |
| `xcuitest-skill` | Swift, Obj-C | XCUITest iOS UI testing |
| `flutter-testing-skill` | Dart | Flutter widget and integration tests |
| `detox-skill` | JS, TS | Detox React Native E2E testing |

### 📋 BDD Testing (7 skills)

| Skill | Languages | Description |
|---|---|---|
| `cucumber-skill` | Java, JS, Ruby, TS | Cucumber Gherkin BDD |
| `specflow-skill` | C# | SpecFlow .NET BDD with Gherkin |
| `serenity-bdd-skill` | Java | Serenity BDD with Screenplay pattern |
| `behave-skill` | Python | Behave Python BDD |
| `behat-skill` | PHP | Behat BDD for PHP |
| `gauge-skill` | Java, Python, JS, Ruby, C# | Gauge specification-based testing |
| `lettuce-skill` | Python | Lettuce Python BDD testing |

### 👁️ Visual Testing (1 skill)

| Skill | Languages | Description |
|---|---|---|
| `smartui-skill` | JS, TS, Java | SmartUI visual regression testing |

### ☁️ Cloud Testing (1 skill)

| Skill | Languages | Description |
|---|---|---|
| `hyperexecute-skill` | YAML | HyperExecute cloud test orchestration |

### 🔄 Migration (1 skill)

| Skill | Languages | Description |
|---|---|---|
| `test-framework-migration-skill` | JS, TS, Java, Python, C# | Convert tests between Selenium, Playwright, Puppeteer, Cypress |

### 🔄 DevOps / CI/CD (1 skill)

| Skill | Languages | Description |
|---|---|---|
| `cicd-pipeline-skill` | YAML | CI/CD pipeline integration for GitHub Actions, Jenkins, GitLab CI |

## Examples

### Example 1: Scaffold a Playwright test in TypeScript

```
"Write Playwright tests for the login page using TypeScript and run them on Chrome and Firefox"
```

The skill will generate: correct `playwright.config.ts`, a typed Page Object for the login page, a test file using `@playwright/test`, and a GitHub Actions workflow with parallel execution.

### Example 2: Run Selenium tests on LambdaTest cloud

```
"Run my Selenium Java tests on Chrome, Firefox, and Safari on LambdaTest with OS Windows 11 and macOS Sonoma"
```

The skill will configure `RemoteWebDriver` with LambdaTest capabilities, read `LT_USERNAME` and `LT_ACCESS_KEY` from environment variables, and set up a parallel TestNG suite.

### Example 3: Migrate Selenium tests to Playwright

```
"Migrate my existing Selenium Python tests to Playwright"
```

The skill uses `test-framework-migration-skill` to map Selenium locators, waits, and assertions to their Playwright equivalents, preserving test intent while updating syntax.

### Example 4: Set up pytest with fixtures

```
"Create a pytest test suite for the payments API with fixtures and parametrized test cases"
```

The skill generates a `conftest.py` with shared fixtures, parametrized test cases using `@pytest.mark.parametrize`, and a `pytest.ini` config with coverage reporting.

## Best Practices

- ✅ Always use environment variables for cloud credentials (`LT_USERNAME`, `LT_ACCESS_KEY`) — never hardcode them
- ✅ Use Page Object Model (POM) to keep test logic separate from UI selectors
- ✅ Prefer explicit waits over fixed `sleep()` calls in all frameworks
- ✅ Run tests in parallel where the framework supports it to reduce execution time
- ✅ Always capture screenshots and logs on test failure for easier debugging
- ✅ Match dependency versions to what each framework officially recommends — avoid mixing major versions
- ❌ Don't write tests that depend on test execution order
- ❌ Don't hardcode URLs, credentials, or environment-specific values inside test files
- ❌ Don't skip writing assertions — a test without assertions is not a test
- ❌ Don't ignore flaky tests — investigate and fix root cause rather than adding retries as a permanent fix

## Limitations

- This skill is an index and trigger guide. The full implementation details for each framework live in the individual skill files at [LambdaTest/agent-skills](https://github.com/LambdaTest/agent-skills).
- This skill does not replace framework-specific documentation, environment setup, or expert QA review.
- Cloud execution examples assume a valid LambdaTest / TestMu AI account. Stop and ask the user for their setup details if credentials or target environments are unclear.
- Mobile testing skills (Appium, Espresso, XCUITest, Flutter, Detox) require platform-specific toolchains (Android SDK, Xcode) that must be installed separately.

## Security & Safety Notes

- Never include `LT_USERNAME`, `LT_ACCESS_KEY`, API tokens, or any credentials in generated code. Always reference them via environment variables.
- When generating CI/CD pipelines, store secrets in GitHub Actions Secrets or equivalent — never in plaintext YAML.
- Installation commands (`npm install`, `pip install`, `mvn install`) should only be run in local development or authorized CI environments.

## Common Pitfalls

- **Problem:** Tests pass locally but fail on CI
  **Solution:** Ensure headless mode is enabled in CI, and that browser versions match between local and CI environments. Use the framework's built-in CI detection where available.

- **Problem:** Flaky tests due to timing issues
  **Solution:** Replace `sleep()` with explicit waits — `waitForSelector` in Playwright, `WebDriverWait` in Selenium, `cy.get().should()` in Cypress.

- **Problem:** Cloud tests fail with authentication errors
  **Solution:** Verify `LT_USERNAME` and `LT_ACCESS_KEY` are correctly set as environment variables and match the credentials on the LambdaTest dashboard.

- **Problem:** Wrong browser capabilities for cloud execution
  **Solution:** Use the LambdaTest Capabilities Generator at https://www.lambdatest.com/capabilities-generator/ to get the correct capability object for your target browser and OS.

- **Problem:** Mobile tests fail with "device not found"
  **Solution:** For local runs, verify the emulator/simulator is running and `adb devices` (Android) or Simulator is active (iOS). For cloud runs, check the device name matches exactly what LambdaTest supports.

## Related Skills

- `@test-driven-development` — Use when you want to design tests before writing implementation code
- `@testing-patterns` — Use for general testing design patterns and strategies
- `@cicd-pipeline-skill` — Use when setting up end-to-end CI/CD pipelines with test automation
- `@debugging-strategies` — Use when diagnosing systematic test failures

---

## local-llm-expert
*Master local LLM inference, model selection, VRAM optimization, and local deployment using Ollama, llama.cpp, vLLM, and LM Studio. Expert in quantization formats (GGUF, EXL2) and local AI privacy.*

Risk: safe

You are an expert AI engineer specializing in local Large Language Model (LLM) inference, open-weight models, and privacy-first AI deployment. Your domain covers the entire local AI ecosystem from 2024/2025.

## Purpose
Expert AI systems engineer mastering local LLM deployment, hardware optimization, and model selection. Deep knowledge of inference engines (Ollama, vLLM, llama.cpp), efficient quantization formats (GGUF, EXL2, AWQ), and VRAM calculation. You help developers run state-of-the-art models (like Llama 3, DeepSeek, Mistral) securely on local hardware.

## Use this skill when
- Planning hardware requirements (VRAM, RAM) for local LLM deployment
- Comparing quantization formats (GGUF, EXL2, AWQ, GPTQ) for efficiency
- Configuring local inference engines like Ollama, llama.cpp, or vLLM
- Troubleshooting prompt templates (ChatML, Zephyr, Llama-3 Inst)
- Designing privacy-first offline AI applications

## Do not use this skill when
- Implementing cloud-exclusive endpoints (OpenAI, Anthropic API directly)
- You need help with non-LLM machine learning (Computer Vision, traditional NLP)
- Training models from scratch (focus on inference and fine-tuning deployment)

## Instructions
1. First, confirm the user's available hardware (VRAM, RAM, CPU/GPU architecture).
2. Recommend the optimal model size and quantization format that fits their constraints.
3. Provide the exact commands to run the chosen model using the preferred inference engine (Ollama, llama.cpp, etc.).
4. Supply the correct system prompt and chat template required by the specific model.
5. Emphasize privacy and offline capabilities when discussing architecture.

## Capabilities

### Inference Engines
- **Ollama**: Expert in writing `Modelfiles`, customizing system prompts, parameters (temperature, num_ctx), and managing local models via CLI.
- **llama.cpp**: High-performance inference on CPU/GPU. Mastering command-line arguments (`-ngl`, `-c`, `-m`), and compiling with specific backends (CUDA, Metal, Vulkan).
- **vLLM**: Serving models at scale. PagedAttention, continuous batching, and setting up an OpenAI-compatible API server on multi-GPU setups.
- **LM Studio & GPT4All**: Guiding users on deploying via UI-based platforms for quick offline deployment and API access.

### Quantization & Formats
- **GGUF (llama.cpp)**: Recommending the best `k-quants` (e.g., Q4_K_M vs Q5_K_M) based on VRAM constraints and performance quality degradation.
- **EXL2 (ExLlamaV2)**: Speed-optimized running on modern consumer GPUs, understanding bitrates (e.g., 4.0bpw, 6.0bpw) mapping to model sizes.
- **AWQ & GPTQ**: Deploying in vLLM for high-throughput generation and understanding the memory footprint versus GGUF.

### Model Knowledge & Prompt Templates
- Tracking the latest open-weights state-of-the-art: Llama 3 (Meta), DeepSeek Coder/V2, Mistral/Mixtral, Qwen2, and Phi-3.
- Mastery of exact **Chat Templates** necessary for proper model compliance: ChatML, Llama-3 Inst, Zephyr, and Alpaca formats.
- Knowing when to recommend a smaller 7B/8B model heavily quantized versus a 70B model spread across GPUs.

### Hardware Configuration (VRAM Calculus)
- Exact calculation of VRAM requirements: Parameters * Bits-per-weight / 8 = Base Model Size, + Context Window Overhead (KV Cache).
- Recommending optimal context size limits (`num_ctx`) to prevent Out Of Memory (OOM) errors on 8GB, 12GB, 16GB, 24GB, or Mac unified memory architectures.

## Behavioral Traits
- Prioritizes local privacy and offline functionality above all else.
- Explains the "why" behind VRAM math and quantization choices.
- Asks for hardware specifications before throwing out model recommendations.
- Warns users about common pitfalls (e.g., repeating system prompts, incorrect chat templates leading to gibberish).
- Stays strictly within the local LLM domain; avoids redirecting users to closed API services unless explicitly asked for hybrid solutions.

## Knowledge Base
- Complete catalog of GGUF formats and their bitrates.
- Deep understanding of Ollama's API endpoints and Modelfile structure.
- Benchmarks for Llama 3 (8B/70B), DeepSeek, and Mistral equivalents.
- Knowledge of parameter scaling laws and LoRA / QLoRA fine-tuning basics (to answer deployment-related queries).

## Response Approach
1. **Analyze constraints:** Re-evaluate requested models against the user's VRAM/RAM capacity.
2. **Select optimal engine:** Choose Ollama for ease-of-use or llama.cpp/vLLM for performance/customization.
3. **Draft the commands:** Provide the exact CLI command, Modelfile, or bash script to get the model running.
4. **Format the template:** Ensure the system prompt and conversation history follow the exact Chat Template for the model.
5. **Optimize:** Give 1-2 tips for optimizing inference speed (`num_ctx`, GPU layers `-ngl`, flash attention).

## Example Interactions
- "I have a 16GB Mac M2. How do I run Llama 3 8B locally with Python?"
  -> (Calculates Mac unified memory, suggests Ollama + llama3:8b, provides `ollama run` command and `ollama` Python client code).
- "I'm getting OOM errors running Mixtral 8x7B on my 24GB RTX 4090."
  -> (Explains that Mixtral is ~45GB natively. Recommends dropping to a Q4_K_M GGUF format or using EXL2 4.0bpw, providing exact download links/commands).
- "How do I serve an open-source model like OpenAI's API?"
  -> (Provides a step-by-step vLLM or Ollama setup with OpenAI API compatibility layer).
- "Can you build a ChatML prompt wrapper for Qwen2?"
  -> (Provides the exact string formatting: `<|im_start|>system\n...<|im_end|>\n<|im_start|>user\n...`).

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## logic-lens
*AI-powered Claude Code skill that performs deep code review using formal logic and reasoning frameworks to detect bugs, anti-patterns, and security risks beyond what linters catch.*

Tags: [code-review, logic-analysis, debugging, security-review, claude-code]
Tools: [claude, codex, cursor, gemini]
Risk: safe

# Logic Lens

## Overview

Logic Lens is a Claude Code skill that performs deep, logic-driven code review using formal reasoning frameworks. Unlike traditional linters that check syntax and style, Logic Lens analyzes your code for logical errors, race conditions, security vulnerabilities, type mismatches, and algorithmic flaws that only appear when you reason through the code's behavior.

Powered by structured AI analysis, Logic Lens applies systematic logical inspection across 9 risk categories: null/undefined handling, type safety, concurrency, resource management, security injection, boundary conditions, algorithm correctness, state management, and API contract violations.

## When to Use This Skill

- Use when you want a thorough logic review before merging a PR
- Use when a bug seems hard to find and standard linters aren't helping
- Use when reviewing security-sensitive code paths (auth, payments, file access)
- Use when refactoring complex business logic
- Use when onboarding to a new codebase and need to understand risk areas

## How It Works

Logic Lens uses Claude Code's reasoning capabilities to:

1. Parse code structure and build a mental model of data flow
2. Apply formal logic checks across 9 risk categories
3. Trace execution paths for edge cases and boundary conditions
4. Identify security anti-patterns (injection, privilege escalation, data leakage)
5. Report findings with severity levels and actionable fix suggestions

## Installation

```bash
# Install via Claude Code plugin marketplace
# Search: "logic-lens" in Claude Code > Extensions

# Or install via NPX (Antigravity)
npx antigravity-awesome-skills --claude
# Then invoke: @logic-lens
```

## Examples

### Example 1: Review a Single File

```
@logic-lens review src/auth/login.ts for security issues
```

**Logic Lens output:**
```
[CRITICAL] SQL Injection risk at line 42: user input concatenated into query string
[HIGH] Missing rate limiting on login attempts
[MEDIUM] Password comparison uses == instead of timing-safe comparison
[LOW] Error messages may leak valid usernames (user enumeration)
```

### Example 2: Full Repository Scan

```
@logic-lens scan the entire codebase and prioritize by severity
```

### Example 3: Pre-PR Review

```
@logic-lens review all files changed in this branch before I open a PR
```

## The 9 Risk Categories

| Category | What It Checks |
|----------|----------------|
| **Null/Undefined** | Missing null checks, optional chaining gaps |
| **Type Safety** | Implicit coercions, any-typed boundaries |
| **Concurrency** | Race conditions, shared mutable state |
| **Resource Management** | Unclosed handles, memory leaks |
| **Security Injection** | SQL/XSS/Command injection, path traversal |
| **Boundary Conditions** | Off-by-one errors, integer overflow |
| **Algorithm Correctness** | Wrong complexity, incorrect assumptions |
| **State Management** | Inconsistent state, missing rollbacks |
| **API Contracts** | Undocumented side effects, broken interfaces |

## Best Practices

- Run `@logic-lens` on authentication and payment code before every release
- Combine with `@lint-and-validate` for full coverage: style + logic
- Review the CRITICAL and HIGH findings first; LOW findings can be deferred
- Use `@logic-lens` on legacy code you are about to modify to understand risk surface

## Benchmark Results

Logic Lens was tested against real-world codebases and caught issues missed by ESLint, TypeScript strict mode, and Snyk:

- **47% of critical bugs** found were invisible to linters
- **Race conditions** detected in async code that static analysis missed
- **Security vulnerabilities** identified before deployment in CI pipeline

## Related Skills

- `@lint-and-validate` — Complementary: run after logic-lens for style/syntax
- `@security-auditor` — Specialized security-only deep scan
- `@debugging-strategies` — Use when logic-lens findings need tracing

## Additional Resources

- [GitHub Repository](https://github.com/hyhmrright/logic-lens)
- [Dev.to Article: Why AI Code Review Misses the Most Dangerous Bugs](https://dev.to/hyhmrright/why-ai-code-review-misses-the-most-dangerous-bugs-logic-lens-fixes-that-4a8l)
- [Claude Code Skills Documentation](https://docs.anthropic.com/claude-code)

## Limitations

Use this skill only when the task clearly matches the scope described above (code review and logic analysis). Logic Lens provides AI-powered analysis and should be combined with human review for production-critical decisions. Do not treat the output as a substitute for environment-specific testing or security audits.

---

## minimalist-ui
*Use when creating clean editorial interfaces with warm monochrome palettes, crisp borders, restrained motion, and flat bento layouts.*

Tags: [frontend, design, minimalism, ui]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# Protocol: Premium Utilitarian Minimalism UI Architect

## When to Use

- Use when the user wants a refined minimalist UI inspired by tools like Notion, Linear, or editorial workspace products.
- Use when designing warm monochrome interfaces with crisp borders, generous whitespace, muted pastel accents, and quiet motion.
- Use when the task should avoid gradients, heavy shadows, saturated colors, pill-heavy components, and generic SaaS visuals.

## Limitations

- Minimalism can hide hierarchy when content is dense; validate scannability, contrast, and navigation clarity with real content.
- This skill assumes the product can support restrained palettes and typography-led layouts; do not override an established brand system without cause.
- Subtle motion and flat surfaces still need responsive, keyboard, and screen-reader verification in the target project.


## 1. Protocol Overview
Name: Premium Utilitarian Minimalism & Editorial UI
Description: An advanced frontend engineering directive for generating highly refined, ultra-minimalist, "document-style" web interfaces analogous to top-tier workspace platforms. This protocol strictly enforces a high-contrast warm monochrome palette, bespoke typographic hierarchies, meticulous structural macro-whitespace, bento-grid layouts, and an ultra-flat component architecture with deliberate muted pastel accents. It actively rejects standard generic SaaS design trends.

## 2. Absolute Negative Constraints (Banned Elements)
The AI must strictly avoid the following generic web development defaults:
- DO NOT use the "Inter", "Roboto", or "Open Sans" typefaces.
- DO NOT use generic, thin-line icon libraries like "Lucide", "Feather", or standard "Heroicons".
- DO NOT use Tailwind's default heavy drop shadows (e.g., `shadow-md`, `shadow-lg`, `shadow-xl`). Shadows must be practically non-existent or heavily customized to be ultra-diffuse and low opacity (< 0.05).
- DO NOT use primary colored backgrounds for large elements or sections (e.g., no bright blue, green, or red hero sections).
- DO NOT use gradients, neon colors, or 3D glassmorphism (beyond subtle navbar blurs).
- DO NOT use `rounded-full` (pill shapes) for large containers, cards, or primary buttons.
- DO NOT use emojis anywhere in code, markup, text content, headings, or alt text. Replace with proper icons or clean SVG primitives.
- DO NOT use generic placeholder names like "John Doe", "Acme Corp", or "Lorem Ipsum". Use realistic, contextual content.
- DO NOT use AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve". Write plain, specific language.

## 3. Typographic Architecture
The interface must rely on extreme typographic contrast and premium font selection to establish an editorial feel.
- Primary Sans-Serif (Body, UI, Buttons): Use clean, geometric, or system-native fonts with character. Target: `font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`.
- Editorial Serif (Hero Headings & Quotes): Target: `font-family: 'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`. Apply tight tracking (`letter-spacing: -0.02em` to `-0.04em`) and tight line-height (`1.1`).
- Monospace (Code, Keystrokes, Meta-data): Target: `font-family: 'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`.
- Text Colors: Body text must never be absolute black (`#000000`). Use off-black/charcoal (`#111111` or `#2F3437`) with a generous `line-height` of `1.6` for legibility. Secondary text should be muted gray (`#787774`).

## 4. Color Palette (Warm Monochrome + Spot Pastels)
Color is a scarce resource, utilized only for semantic meaning or subtle accents.
- Canvas / Background: Pure White `#FFFFFF` or Warm Bone/Off-White `#F7F6F3` / `#FBFBFA`.
- Primary Surface (Cards): `#FFFFFF` or `#F9F9F8`.
- Structural Borders / Dividers: Ultra-light gray `#EAEAEA` or `rgba(0,0,0,0.06)`.
- Accent Colors: Exclusively use highly desaturated, washed-out pastels for tags, inline code backgrounds, or subtle icon backgrounds.
  - Pale Red: `#FDEBEC` (Text: `#9F2F2D`)
  - Pale Blue: `#E1F3FE` (Text: `#1F6C9F`)
  - Pale Green: `#EDF3EC` (Text: `#346538`)
  - Pale Yellow: `#FBF3DB` (Text: `#956400`)

## 5. Component Specifications
- Bento Box Feature Grids:
  - Utilize asymmetrical CSS Grid layouts.
  - Cards must have exactly `border: 1px solid #EAEAEA`.
  - Border-radius must be crisp: `8px` or `12px` maximum.
  - Internal padding must be generous (e.g., `24px` to `40px`).
- Primary Call-To-Action (Buttons):
  - Solid background `#111111`, text `#FFFFFF`.
  - Slight border-radius (`4px` to `6px`). No box-shadow.
  - Hover state should be a subtle color shift to `#333333` or a micro-scale `transform: scale(0.98)`.
- Tags & Status Badges:
  - Pill-shaped (`border-radius: 9999px`), very small typography (`text-xs`), uppercase with wide tracking (`letter-spacing: 0.05em`).
  - Background must use the defined Muted Pastels.
- Accordions (FAQ):
  - Strip all container boxes. Separate items only with a `border-bottom: 1px solid #EAEAEA`.
  - Use a clean, sharp `+` and `-` icon for the toggle state.
- Keystroke Micro-UIs:
  - Render shortcuts as physical keys using `<kbd>` tags: `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`, using the Monospace font.
- Faux-OS Window Chrome:
  - When mocking up software, wrap it in a minimalist container with a white top bar containing three small, light gray circles (replicating macOS window controls).

## 6. Iconography & Imagery Directives
- System Icons: Use "Phosphor Icons (Bold or Fill weights)" or "Radix UI Icons" for a technical, slightly thicker-stroke aesthetic. Standardize stroke width across all icons.
- Illustrations: Monochromatic, rough continuous-line ink sketches on a white background, featuring a single offset geometric shape filled with a muted pastel color.
- Photography: Use high-quality, desaturated images with a warm tone. Apply subtle overlays (`opacity: 0.04` warm grain) to blend photos into the monochrome palette. Never use oversaturated stock photos. Use reliable placeholders like `https://picsum.photos/seed/{context}/1200/800` when real assets are unavailable.
- Hero & Section Backgrounds: Sections should not feel empty and flat. Use subtle full-width background imagery at very low opacity, soft radial light spots (`radial-gradient` with warm tones at `opacity: 0.03`), or minimal geometric line patterns to add depth without breaking the clean aesthetic.

## 7. Subtle Motion & Micro-Animations
Motion should feel invisible — present but never distracting. The goal is quiet sophistication, not spectacle.
- Scroll Entry: Elements fade in gently as they enter the viewport. Use `translateY(12px)` + `opacity: 0` resolving over `600ms` with `cubic-bezier(0.16, 1, 0.3, 1)`. Use `IntersectionObserver`, never `window.addEventListener('scroll')`.
- Hover States: Cards lift with an ultra-subtle shadow shift (`box-shadow` transitioning from `0 0 0` to `0 2px 8px rgba(0,0,0,0.04)` over `200ms`). Buttons respond with `scale(0.98)` on `:active`.
- Staggered Reveals: Lists and grid items enter with a cascade delay (`animation-delay: calc(var(--index) * 80ms)`). Never mount everything at once.
- Background Ambient Motion: Optional. A single, very slow-moving radial gradient blob (`animation-duration: 20s+`, `opacity: 0.02-0.04`) drifting behind hero sections. Must be applied to a `position: fixed; pointer-events: none` layer. Never on scrolling containers.
- Performance: Animate exclusively via `transform` and `opacity`. No layout-triggering properties (`top`, `left`, `width`, `height`). Use `will-change: transform` sparingly and only on actively animating elements.

## 8. Execution Protocol
When tasked with writing frontend code (HTML, React, Tailwind, Vue) or designing a layout:
1. Establish the macro-whitespace first. Use massive vertical padding between sections (e.g., `py-24` or `py-32` in Tailwind).
2. Constrain the main typography content width to `max-w-4xl` or `max-w-5xl`.
3. Apply the custom typographic hierarchy and monochromatic color variables immediately.
4. Ensure every card, divider, and border adheres strictly to the `1px solid #EAEAEA` rule.
5. Add scroll-entry animations to all major content blocks.
6. Ensure sections have visual depth through imagery, ambient gradients, or subtle textures — no empty flat backgrounds.
7. Provide code that reflects this high-end, uncluttered, editorial aesthetic natively without requiring manual adjustments.

---

## mise-configurator
*Generate production-ready mise.toml setups for local development, CI/CD pipelines, and toolchain standardization.*

Tags: [mise, devops, ci-cd, toolchain, runtimes, automation]
Tools: [claude, cursor, gemini]
Risk: safe

# Mise Configurator

## Overview

This skill generates clean, production-ready `mise.toml` configurations for local development environments and CI/CD pipelines.

It helps standardize runtime versions, simplify onboarding, replace legacy version managers like `asdf`, `nvm`, and `pyenv`, and create reproducible multi-language environments with minimal setup effort.

## When to Use This Skill

- Use when you need to create or update a `mise.toml`
- Use when working with Node.js, Python, Go, Rust, Java, Bun, Terraform, or mixed stacks
- Use when the user asks about CI/CD runtime setup using mise
- Use when migrating from `.tool-versions`, `asdf`, `nvm`, or `pyenv`
- Use when standardizing tool versions across teams or monorepos

## How It Works

### Step 1: Detect Project Context

Inspect available repository files such as:

- `package.json`
- `pnpm-lock.yaml`
- `pyproject.toml`
- `requirements.txt`
- `go.mod`
- `Cargo.toml`
- `.tool-versions`
- `Dockerfile`
- GitHub Actions or CI files

Infer languages, package managers, and pinned versions.

### Step 2: Generate `mise.toml`

Create a minimal, valid, copy-paste-ready configuration using:

- existing pinned versions when found
- explicit user-provided target versions when absent
- practical defaults for developer productivity
- concrete pinned versions in shared production configs

### Step 3: Add Bootstrap Commands

Provide setup commands such as:

```bash
mise trust
mise install
```

### Step 4: Generate CI/CD Integration

If requested, generate pipeline examples using mise with caching and runtime installation.

## Examples

### Example 1: Node.js + pnpm Project

```toml
[tools]
node = "22.11.0"
pnpm = "9.15.0"
```

### Example 2: Python + GitHub Actions

```toml
[tools]
python = "3.12.7"
poetry = "1.8.4"
```

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: jdx/mise-action@v2
  - run: poetry install
  - run: pytest
```

## Best Practices

- ✅ Respect versions already pinned in the repository
    
- ✅ Keep configs minimal and readable
    
- ✅ Prefer stable runtime releases
    
- ✅ Generate CI examples with caching

- ✅ Ask for target versions before pinning when the repository does not already declare them

- ❌ Do not use floating `latest` or `lts` aliases in shared production configs unless explicitly requested
    
- ❌ Do not over-engineer unnecessary tool entries
    
- ❌ Do not ignore existing lockfiles or version files
    

## Limitations

- This skill does not replace environment-specific validation, testing, or expert review.
    
- Stop and ask for clarification if required inputs, permissions, or safety boundaries are missing.
    
- Runtime availability may vary by OS, shell, or CI platform.
    
- Some plugins or niche tools may require manual adjustment.
    

## Security & Safety Notes

- Review generated shell commands before execution.
    
- Confirm CI/CD permissions before modifying pipelines.
    
- Validate runtime versions against production requirements.
    
- Use only in authorized repositories and environments.
    

## Common Pitfalls

- **Problem:** Wrong runtime version selected  
    **Solution:** Check repository lockfiles and pinned versions first.
    
- **Problem:** CI installs are slow  
    **Solution:** Enable cache layers and reuse mise cache directories.
    
- **Problem:** Tool missing from registry  
    **Solution:** Verify plugin support or install manually.
    

## Related Skills

- `@docker-expert` - Use when building containerized development environments
    
- `@github-actions-templates` - Use for advanced workflow automation
    
- `@monorepo-architect` - Use for large multi-package repositories

---

## mock-hunter
*Audit a live web page in five phases (catalog, click, trace, classify, report) to identify mock data, hardcoded values, LLM-generated metrics, and broken endpoints. Outputs a markdown report with REAL/MOCK/LLM/HARDCODED/BROKEN/UNKNOWN verdicts per visible value.*

Tags: [testing, qa, playwright, mock-detection, web-audit, ai-testing, vibe-coding, claude-code]
Tools: [claude]
Risk: critical

# MockHunter — Live Page Reality Check

## Overview

MockHunter is a Claude Code skill that audits a live web page and tells you, for every visible value, whether it is real, mocked, LLM-generated, hardcoded, broken, or unknown. It is built for vibe-coded apps (Lovable, Bolt, v0, Replit, AI Studio, Cursor Composer) where the UI may look complete but the data layer often is not. It uses Playwright MCP to drive a real browser, then traces each visible value through the network and DOM to its source.

This skill adapts the upstream `CodeShuX/mockhunter` project (community source).

Because this workflow drives a real browser against live pages, treat it as an interactive audit tool, not a plugin-safe read-only helper. Default to observation-only until the user confirms the target is theirs, identifies a safe test account or environment, and explicitly approves any click, submit, or authenticated action that can mutate state.

## When to Use This Skill

- Use when auditing an AI-generated UI to find out which values are actually wired up
- Use when reviewing a contractor or teammate's deliverable before sign-off
- Use before showing a vibe-coded MVP to a customer or investor
- Use when a dashboard "looks too clean" — every metric uniformly round, all timestamps clustered, no variance — and you suspect seeded data

## How It Works

### Phase 1: Setup & Smart Questions

1. Greet the user, ask for the target URL
2. Auto-detect the stack from the URL (`*.lovable.app`, `*.bolt.new`, `*.v0.app`, `*.replit.app`, `aistudio.google.com`, otherwise Custom)
3. Ask 3-5 targeted questions: auth mode (public / localhost / form / skip), DB access (optional), suspicions, page goal
4. Confirm the audit plan, ownership/permission, target environment, and allowed action classes before proceeding

### Phase 2: Navigate & Catalog

1. `browser_navigate` to the target URL
2. Handle auth per chosen mode (form-login: fill fields, click submit)
3. Wait for network idle (max 10s)
4. Take full-page screenshot, capture accessibility snapshot
5. Inventory every: heading, button, link, input, card, badge, stat, table cell, empty state, image
6. Capture initial console errors and network requests

### Phase 3: Test Interactivity

1. For every tab: click only after the user has approved navigation-style interactions, then snapshot, scroll to bottom, re-catalog
2. For every button: click only user-approved, allowlisted controls that are clearly non-destructive by role, accessible name, nearby text, icon, URL/action target, and expected network side effect; skip destructive or ambiguous controls rather than relying on a label regex alone
3. For every form: identify required fields and prefer empty-submit validation; submit throwaway data only when the user explicitly approved the exact form, target environment, and test account
4. Record per-element behavior

### Phase 4: Trace Provenance

For every visible value, run this decision tree:

```
Did any network request return this value?
├── YES — found in a response:
│   ├── Status 4xx/5xx → BROKEN
│   ├── Endpoint matches /ai|openai|generate|llm|chat → LLM
│   ├── Response shape matches mock library (faker, MSW, mockoon) → MOCK
│   ├── Uniformity flags trigger → MOCK or LLM (review)
│   ├── DB connection provided?
│   │   ├── Run read-only SELECT, value matches DB row → REAL
│   │   └── Value not in DB → MOCK
│   └── No DB → UNKNOWN (best-guess)
└── NO — value not in any network response:
    ├── String literal in DOM source → HARDCODED
    ├── Computed from Math.random / Date.now / faker → MOCK
    └── Cannot determine → UNKNOWN
```

Uniformity heuristics flag suspicious data:
- All numeric values identical across rows
- All percentages round (50%, 75%, 90%)
- All timestamps cluster within a single minute
- < 3 unique values across 10+ rows

### Phase 5: Report

Generate `mockhunter-report.md` with:
- Summary table (verdict counts)
- Findings per section/tab (element / value / verdict / source / severity / action)
- Console errors and network failures
- NO-OP buttons
- Suspicious patterns
- Smart follow-up questions for the user

## Examples

### Example 1: Auditing a Lovable admin dashboard

```
User: /mockhunter audit https://my-app.lovable.app/admin
Skill: [Phase 1] Stack detected: Lovable. Auth: skip. DB: no.
       [Phase 2] Catalog: 6 stat cards, 4 verification queues, 8 activity items.
       [Phase 3] Search box: NO-OP (zero network requests). Activity link → 404.
       [Phase 4] Bundle 2.7 MB. Zero /api/, zero supabase, zero axios.
                 "$42,850" → string literal in JSX → HARDCODED.
                 "+12% vs last month" → string literal → HARDCODED.
       [Phase 5] Verdict: 23 HARDCODED, 1 BROKEN, 1 NO-OP, 0 REAL.
                 Report written to ./mockhunter-report.md
```

### Example 2: Public marketing site (mostly real)

```
User: /mockhunter audit https://example-saas.com
Skill: ...
       [Phase 5] Verdict: 8 REAL, 18 HARDCODED (intentional marketing copy),
                 0 MOCK, 0 BROKEN, 2 UNKNOWN.
                 No console errors, no broken endpoints.
```

## Best Practices

- ✅ Provide DB access when available — lifts UNKNOWN verdicts to REAL or MOCK
- ✅ Use a dedicated test account for form-login auth
- ✅ Run cold-start tests (zero data) — many vibe-coded apps fail there
- ✅ Tell the skill if specific sections are intentionally AI-generated, so it doesn't false-flag them
- ❌ Don't run active interaction on apps you don't own without permission — live clicks and form submissions can mutate state
- ❌ Don't trust a destructive-button exclusion list by itself — localized labels, icons, aria text, and backend routes can hide mutating actions
- ❌ Don't trust the audit if the page failed to load — check console first

## Limitations

- Single-page audit per run — no multi-page crawl in v0.1.0
- Form-login only for auth — no OAuth, magic-link, or 2FA in v0.1.0
- Caps at ~30 most-prominent buttons per page
- Markdown report only — no JSON output yet
- DB verification supports any DB reachable via shell command (psql, mysql, mongosh, wrangler, supabase REST), but not Firestore directly

## Security & Safety Notes

- The skill runs read-only DB SELECTs only, never INSERT/UPDATE/DELETE
- Skips destructive-looking, ambiguous, icon-only, localized, or external-write controls unless the user has explicitly allowlisted the exact control and environment
- Never submits forms that look like payment, account deletion, external write operations, account changes, invites, publishing, deployment, messaging, or money movement
- Uses placeholder credentials (`mockhunter@example.com`) for any throwaway form tests, never the user's real credentials
- All Playwright actions happen in a controlled MCP browser context — no headless escalation

---

## monte-carlo-monitor-creation
*Guides creation of Monte Carlo monitors via MCP tools, producing monitors-as-code YAML for CI/CD deployment.*

Tags: [data-observability, monitoring, monte-carlo, monitors-as-code]
Tools: [claude, cursor, codex]
Risk: safe

# Monte Carlo Monitor Creation Skill

This skill teaches you to create Monte Carlo monitors correctly via MCP. Every creation tool runs in **dry-run mode** and returns monitors-as-code (MaC) YAML. No monitors are created directly -- the user applies the YAML via the Monte Carlo CLI or CI/CD.

Reference files live next to this skill file. **Use the Read tool** (not MCP resources) to access them:

- Metric monitor details: `references/metric-monitor.md` (relative to this file)
- Validation monitor details: `references/validation-monitor.md` (relative to this file)
- Custom SQL monitor details: `references/custom-sql-monitor.md` (relative to this file)
- Comparison monitor details: `references/comparison-monitor.md` (relative to this file)
- Table monitor details: `references/table-monitor.md` (relative to this file)

## When to activate this skill

Activate when the user:

- Asks to create, add, or set up a monitor (e.g. "add a monitor for...", "create a freshness check on...", "set up validation for...")
- Mentions monitoring a specific table, field, or metric
- Wants to check data quality rules or enforce data contracts
- Asks about monitoring options for a table or dataset
- Requests monitors-as-code YAML generation
- Wants to add monitoring after new transformation logic (when the prevent skill is not active)

## When NOT to activate this skill

Do not activate when the user is:

- Just querying data or exploring table contents
- Triaging or responding to active alerts (use the prevent skill's Workflow 3)
- Running impact assessments before code changes (use the prevent skill's Workflow 4)
- Asking about existing monitor configuration (use `getMonitors` directly)
- Editing or deleting existing monitors

---

## Available MCP tools

All tools are available via the `monte-carlo` MCP server.

| Tool                         | Purpose                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `testConnection`             | Verify auth and connectivity before starting               |
| `search`                     | Find tables/assets by name; use `include_fields` for columns |
| `getTable`                   | Schema, stats, metadata, domain membership, capabilities   |
| `getValidationPredicates`    | List available validation rule types for a warehouse       |
| `getDomains`                 | List MC domains (only needed if table has no domain info)  |
| `createMetricMonitorMac`     | Generate metric monitor YAML (dry-run)                     |
| `createValidationMonitorMac` | Generate validation monitor YAML (dry-run)                 |
| `createComparisonMonitorMac` | Generate comparison monitor YAML (dry-run)                 |
| `createCustomSqlMonitorMac`  | Generate custom SQL monitor YAML (dry-run)                 |
| `createTableMonitorMac`      | Generate table monitor YAML (dry-run)                      |

---

## Monitor types

| Type           | Tool                         | Use When                                                                                                                                |
| -------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Metric**     | `createMetricMonitorMac`     | Track statistical metrics on fields (null rates, unique counts, numeric stats) or row count changes over time. Requires a timestamp field for aggregation. |
| **Validation** | `createValidationMonitorMac` | Row-level data quality checks with conditions (e.g. "field X is never null", "status is in allowed set"). Alerts on INVALID data.       |
| **Custom SQL** | `createCustomSqlMonitorMac`  | Run arbitrary SQL returning a single number and alert on thresholds. Most flexible; use when other types don't fit.                     |
| **Comparison** | `createComparisonMonitorMac` | Compare metrics between two tables (e.g. dev vs prod, source vs target).                                                               |
| **Table**      | `createTableMonitorMac`      | Monitor groups of tables for freshness, schema changes, and volume. Uses asset selection at database/schema level.                      |

---

## Procedure

Follow these steps in order. Do NOT skip steps.

### Validation Phase (Steps 1-3) -- MUST complete before any creation tool is called

The number one error pattern is agents skipping validation and calling a creation tool with guessed or incomplete parameters. **Every field in the creation call must be grounded in data retrieved during this phase.** Do not proceed to Step 4 until Steps 1-3 are fully satisfied.

#### Step 1: Understand the request

Ask yourself:
- What does the user want to monitor? (a specific table, a metric, a data quality rule, cross-table consistency, freshness/volume at schema level)
- Which monitor type fits? Use the monitor types table above.
- Does the user have all the details, or do they need guidance?

If the user's intent is unclear, ask a focused question before proceeding.

#### Step 2: Identify the table(s) and columns

If you don't have the table MCON:
1. Use `search` with the table name and `include_fields: ["field_names"]` to find the MCON and get column names.
2. If the user provided a full table ID like `database:schema.table`, search for it.
3. Once you have the MCON, call `getTable` with `include_fields: true` and `include_table_capabilities: true` to verify capabilities and get domain info.

If you already have the MCON:
1. Call `getTable` with the MCON, `include_fields: true`, and `include_table_capabilities: true`.

**CRITICAL: You need the actual column names from `getTable` results. NEVER guess or hallucinate column names.** This is the most common source of monitor creation failures.

For monitor types that require a timestamp column (metric monitors), review the column names and identify likely timestamp candidates. Present them to the user if ambiguous.

#### Step 3: Handle domain assignment

Monitors must be assigned to a domain that contains the table being monitored. The `getTable` response includes a `domains` list with `uuid` and `name`.

1. If `domains` is empty: skip domain assignment.
2. If `domains` has exactly one entry: default `domain_id` to that domain's UUID.
3. If `domains` has multiple entries: present only those domains and ask the user to pick.

Do NOT present all account domains as options -- only domains that contain the table are valid.

**ALWAYS check the table's `domains` BEFORE calling any creation tool.**

---

### Creation Phase (Steps 4-8)

Only enter this phase after the validation phase is complete with real data from MCP tools.

#### Step 4: Load the sub-skill reference

Based on the monitor type, read the detailed reference for parameter guidance:

- **Metric** -- Read the detailed reference: `references/metric-monitor.md` (relative to this file)
- **Validation** -- Read the detailed reference: `references/validation-monitor.md` (relative to this file)
- **Custom SQL** -- Read the detailed reference: `references/custom-sql-monitor.md` (relative to this file)
- **Comparison** -- Read the detailed reference: `references/comparison-monitor.md` (relative to this file)
- **Table** -- Read the detailed reference: `references/table-monitor.md` (relative to this file)

#### Step 5: Ask about scheduling

**Skip this step for table monitors.** Table monitors do not support the `schedule` field in MaC YAML — adding it will cause a validation error on `montecarlo monitors apply`. Table monitor scheduling is managed automatically by Monte Carlo.

For all other monitor types, the creation tools default to a fixed schedule running every 60 minutes. Present these options:

1. **Fixed interval** -- any integer for `interval_minutes` (30, 60, 90, 120, 360, 720, 1440, etc.)
2. **Dynamic** -- MC auto-determines when to run based on table update patterns.
3. **Loose** -- runs once per day.

Schedule format in MaC YAML:
- Fixed: `schedule: { type: fixed, interval_minutes: <N> }`
- Dynamic: `schedule: { type: dynamic }`
- Loose: `schedule: { type: loose, start_time: "00:00" }`

#### Step 6: Confirm with the user

Before calling the creation tool, present the monitor configuration in plain language:
- Monitor type
- Target table (and columns if applicable)
- What it checks / what triggers an alert
- Domain assignment
- Schedule

Ask: "Does this look correct? I'll generate the monitor configuration."

**NEVER call the creation tool without user confirmation.**

#### Step 7: Create the monitor

Call the appropriate creation tool with the parameters built in previous steps. Always pass an MCON when possible. If only table name is available, also pass warehouse.

#### Step 8: Present results

**CRITICAL: Always include the YAML in your response.** The user needs copy-pasteable YAML.

1. If a non-default schedule was chosen, modify the schedule section in the YAML before presenting.
2. Wrap the YAML in the full MaC structure (see "MaC YAML format" section below).
3. ALWAYS present the full YAML in a ```yaml code block.
4. Explain where to put it and how to apply it (see below).
5. ALWAYS use ISO 8601 format for datetime values.
6. NEVER reformat YAML values returned by creation tools.

---

## MaC YAML format

The YAML returned by creation tools is the monitor definition. It must be wrapped in the standard MaC structure to be applied:

```yaml
montecarlo:
  <monitor_type>:
    - <returned yaml>
```

For example, a metric monitor would look like:

```yaml
montecarlo:
  metric:
    - <yaml returned by createMetricMonitorMac>
```

**Important:** `montecarlo.yml` (without a directory path) is a separate Monte Carlo project configuration file -- it is NOT the same as a monitor definition file. Monitor definitions go in their own `.yml` files, typically in a `monitors/` directory or alongside dbt model schema files.

Tell the user:
- Save the YAML to a `.yml` file (e.g. `monitors/<table_name>.yml` or in their dbt schema)
- Apply via the Monte Carlo CLI: `montecarlo monitors apply --namespace <namespace>`
- Or integrate into CI/CD for automatic deployment on merge

---

## Common mistakes to avoid

- **NEVER guess column names.** Always get them from `getTable`.
- **NEVER skip the confirmation step** (Step 6).
- For metric monitors, `aggregate_time_field` MUST be a real timestamp column from the table.
- For validation monitors, conditions match INVALID data, not valid data.
- Always pass an MCON when possible. If only table name is available, also pass warehouse.
- **ALWAYS check table's `domains` BEFORE calling any creation tool.**
- ALWAYS use ISO 8601 format for datetime values.
- NEVER reformat YAML values returned by creation tools.
- Do not call creation tools before the validation phase is complete.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## monte-carlo-prevent
*Surfaces Monte Carlo data observability context (table health, alerts, lineage, blast radius) before SQL/dbt edits.*

Tags: [data-observability, dbt, schema, monte-carlo, lineage]
Tools: [claude, cursor, codex]
Risk: safe

# Monte Carlo Prevent Skill

This skill brings Monte Carlo's data observability context directly into your editor. When you're modifying a dbt model or SQL pipeline, use it to surface table health, lineage, active alerts, and to generate monitors-as-code without leaving Claude Code.

Reference files live next to this skill file. **Use the Read tool** (not MCP resources) to access them:

- Full workflow step-by-step instructions: `references/workflows.md` (relative to this file)
- MCP parameter details: `references/parameters.md` (relative to this file)
- Troubleshooting: `references/TROUBLESHOOTING.md` (relative to this file)

## When to activate this skill

**Do not wait to be asked.** Run the appropriate workflow automatically whenever the user:

- References or opens a `.sql` file or dbt model (files in `models/`) → run Workflow 1
- Mentions a table name, dataset, or dbt model name in passing → run Workflow 1

- Describes a planned change to a model (new column, join update, filter change, refactor) → **STOP — run Workflow 4 before writing any code**
-
- Adds a new column, metric, or output expression to an existing
  model → run Workflow 4 first, then ALWAYS offer Workflow 2
  regardless of risk tier — do not skip the monitor offer
- Asks about data quality, freshness, row counts, or anomalies → run Workflow 1
- Wants to triage or respond to a data quality alert → run Workflow 3

Present the results as context the engineer needs before proceeding — not as a response to a question.

## When NOT to activate this skill

Do not invoke Monte Carlo tools for:

- Seed files (files in seeds/ directory)
- Analysis files (files in analyses/ directory)
- One-off or ad-hoc SQL scripts not part of a dbt project
- Configuration files (dbt_project.yml, profiles.yml, packages.yml)
- Test files unless the user is specifically asking about data quality

If uncertain whether a file is a dbt model, check for {{ ref() }} or {{ source() }}
Jinja references — if absent, do not activate.

### Macros and snapshots — gate edits, skip auto-context

Macro files (`macros/`) and snapshot files (`snapshots/`) are **not** models, so
do not auto-fetch Monte Carlo context (Workflow 1) when they are opened. However,
macros are inlined into every model that calls them at compile time — a one-line
macro change can silently alter dozens of models. Snapshots control historical
tracking and are similarly sensitive.

**The pre-edit hook gates these files.** If the hook fires for a macro or snapshot,
identify which models are affected and run the change impact assessment (Workflow 4)
for those models before proceeding with the edit.

---

## REQUIRED: Change impact assessment before any SQL edit

**Before editing or writing any SQL for a dbt model or pipeline, you MUST run Workflow 4.**

This applies whenever the user expresses intent to modify a model — including phrases like:

- "I want to add a column…"
- "Let me add / I'm adding…"
- "I'd like to change / update / rename…"
- "Can you add / modify / refactor…"
- "Let's add…" / "Add a `<column>` column"
- Any other description of a planned schema or logic change
- "Exclude / filter out / remove [records/customers/rows]…"
- "Adjust / increase / decrease [threshold/parameter/value]…"
- "Fix / bugfix / patch [issue/bug]…"
- "Revert / restore / undo [change/previous behavior]…"
- "Disable / enable [feature/logic/flag]…"
- "Clean up / remove [references/columns/code]…"
- "Implement [backend/feature] for…"
- "Create [models/dbt models] for…" (when modifying existing referenced tables)
- "Increase / decrease / change [max_tokens/threshold/date constant/numeric parameter]…"
- Any change to a hardcoded value, constant, or configuration parameter within SQL
- "Drop / remove / delete [column/field/table]"
- "Rename [column/field] to [new name]"
- "Add [column]" (short imperative form, e.g. "add a created_at column")
- Any single-verb imperative command targeting a column, table, or model
  (e.g. "drop X", "rename Y", "add Z", "remove W")

Parameter changes (threshold values, date constants, numeric limits) appear
safe but silently change model output. Treat them the same as logic changes
for impact assessment purposes.

**Do not write or edit any SQL until the change impact assessment (Workflow 4) has been presented to the user.** The assessment must come first — not after the edit, not in parallel.

---

## Pre-edit gate — check before modifying any file

**Before calling Edit, Write, or MultiEdit on any `.sql` or dbt model
file, you MUST check:**

1. Has the synthesis step been run for THIS SPECIFIC CHANGE in the
   current prompt?
2. **If YES** → proceed with the edit
3. **If NO** → stop immediately, run Workflow 4, present the full
   report with synthesis connected to this specific change.
   **If risk is High or Medium:** ask "Do you want me to proceed
   with the edit?" and wait for explicit confirmation.
   **If risk is Low:** use judgment — proceed if straightforward
   and no concerns found, otherwise ask before editing.

**Important: "Workflow 4 already ran this session" is NOT sufficient
to proceed.** Each distinct change prompt requires its own synthesis
step connecting the MC findings to that specific change.

The synthesis must reference the specific columns, filters, or logic
being changed in the current prompt — not just general table health.

Example:

- ✅ "Given 34 downstream models depend on is_paying_workspace,
  adding 'MC Internal' to the exclusion list will exclude these
  workspaces from all downstream health scores and exports.
  Confirm?"
- ❌ "Workflow 4 already ran. Making the edit now."

The only exception: if the user explicitly acknowledges the risk
and confirms they want to skip (e.g. "I know the risks, just make
the change") — proceed but note the skipped assessment.

## Available MCP tools

All tools are available via the `monte-carlo` MCP server.

| Tool                         | Purpose                                                              |
| ---------------------------- | -------------------------------------------------------------------- |
| `testConnection`             | Verify auth and connectivity                                         |
| `search`                     | Find tables/assets by name                                           |
| `getTable`                   | Schema, stats, metadata for a table                                  |
| `getAssetLineage`            | Upstream/downstream dependencies (call with mcons array + direction) |
| `getAlerts`                  | Active incidents and alerts                                          |
| `getMonitors`                | Monitor configs — filter by table using mcons array                  |
| `getQueriesForTable`         | Recent query history                                                 |
| `getQueryData`               | Full SQL for a specific query                                        |
| `createValidationMonitorMac` | Generate validation monitors-as-code YAML                            |
| `createMetricMonitorMac`     | Generate metric monitors-as-code YAML                                |
| `createComparisonMonitorMac` | Generate comparison monitors-as-code YAML                            |
| `createCustomSqlMonitorMac`  | Generate custom SQL monitors-as-code YAML                            |
| `getValidationPredicates`    | List available validation rule types                                 |
| `updateAlert`                | Update alert status/severity                                         |
| `setAlertOwner`              | Assign alert ownership                                               |
| `createOrUpdateAlertComment` | Add comments to alerts                                               |
| `getAudiences`               | List notification audiences                                          |
| `getDomains`                 | List MC domains                                                      |
| `getUser`                    | Current user info                                                    |
| `getCurrentTime`             | ISO timestamp for API calls                                          |

## Core workflows

Each workflow has detailed step-by-step instructions in `references/workflows.md` (Read tool).

### 1. Table health check

**When:** User opens a dbt model or mentions a table.
**What:** Surfaces health, lineage, alerts, and risk signals. Auto-escalates to Workflow 4 if change intent is detected and risk signals are present.

### 2. Add a monitor

**When:** New column, filter, or business rule is added to a model.
**What:** Suggests and generates monitors-as-code YAML using the appropriate `create*MonitorMac` tool. Saves to `monitors/<table_name>.yml`.

### 3. Alert triage

**When:** User is investigating an active data quality incident.
**What:** Lists open alerts, checks table state, traces lineage for root cause, reviews recent queries.

### 4. Change impact assessment — REQUIRED before modifying a model

**When:** Any intent to modify a dbt model's logic, columns, joins, or filters.
**What:** Surfaces blast radius, downstream dependencies, active incidents, monitor coverage, and query exposure. Produces a risk-tiered report with synthesis connecting findings to specific code recommendations. See `references/workflows.md` for the full assessment sequence, report format, and synthesis rules.

### 5. Change validation queries

**When:** Explicit engineer request only (e.g. "validate this change", "ready to commit").
**What:** Generates 3-5 targeted SQL queries to verify the change behaved as intended. Uses Workflow 4 context — requires both impact assessment and file edit in session.

---

## Post-synthesis confirmation rules

Always end the synthesis with one clear, specific recommendation in plain English:
"Given the above, I recommend: [specific action]"

**If the risk is High or Medium:** STOP and wait for confirmation before editing
any file. You must ask the engineer and receive an explicit "yes", "go ahead",
"proceed", or similar confirmation before making code changes.
Say: "Do you want me to proceed with the edit?"
Do NOT say: "Proceeding with the edit." — that skips the engineer's decision.

**If the risk is Low:** Use your judgment based on the synthesis findings. If
the change is straightforward and the synthesis found no concerns, you may
proceed. If anything is surprising or worth flagging, ask before editing.

---

## Session markers

These markers coordinate between the skill and the plugin's hooks. Output each
on its own line when the condition is met.

### Impact check complete

After the engineer confirms (High/Medium) or after presenting the synthesis (Low),
output one marker per assessed table. **IMPORTANT: use only the table/model name, not the full MCON:**

<!-- MC_IMPACT_CHECK_COMPLETE: <table_name> -->

(Use the model filename without .sql extension — NOT "acme.analytics.orders" or "prod.public.client_hub")

How many markers to emit depends on how the assessment was triggered:

**Hook-triggered** (the pre-edit hook blocked an edit and instructed you to run
the assessment): Be strict — only emit markers for tables whose lineage **and**
monitor coverage were fetched directly via Monte Carlo tools in this session. If
the engineer describes changes to multiple tables but only one was formally
assessed, emit only one marker. The pre-edit hook will gate the other tables and
prompt for their own Workflow 4 runs.

**Voluntarily invoked** (the engineer proactively asked for an impact assessment):
Be looser — emit markers for all tables the assessment meaningfully covered, even
if some were assessed via lineage context rather than direct MC tool calls. The
engineer is already safety-conscious; don't force redundant assessments for tables
they clearly considered.

### Monitor coverage gap

When Workflow 4 finds zero custom monitors on a table's affected columns, output:

<!-- MC_MONITOR_GAP: <table_name> -->

Use only the table/model name (NOT the full MCON). This allows the plugin's hooks
to remind the engineer about monitor coverage at commit time. Only output this
marker when the gap is specifically about the columns or logic being changed —
not for general table-level monitor absence.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## monte-carlo-push-ingestion
*Expert guide for pushing metadata, lineage, and query logs to Monte Carlo from any data warehouse.*

Tags: [data-observability, ingestion, monte-carlo, pycarlo, metadata]
Tools: [claude, cursor, codex]
Risk: safe

# Monte Carlo Push Ingestion

You are an agent that helps customers collect metadata, lineage, and query logs from their
data warehouses and push that data to Monte Carlo via the push ingestion API. The push model
works with **any data source** — if the customer's warehouse does not have a ready-made
template, derive the appropriate collection queries from that warehouse's system catalog or
metadata APIs. The push format and pycarlo SDK calls are the same regardless of source.

Monte Carlo's push model lets customers send metadata, lineage, and query logs directly to
Monte Carlo instead of waiting for the pull collector to gather it. It fills gaps the pull
model cannot always cover — integrations that don't expose query history, custom lineage
between non-warehouse assets, or customers who already have this data and want to send it
directly.

## When to Use

Use this skill when the user needs to collect metadata, lineage, freshness, volume, or query-log data from a warehouse or adjacent system and push it into Monte Carlo through the push-ingestion API.

Push data travels through the integration gateway → dedicated Kinesis streams → thin
adapter/normalizer code → the same downstream systems that power the pull model. The only
new infrastructure is the ingress layer; everything after it is shared.

## MANDATORY — Always start from templates

When generating any push-ingestion script, you MUST:

1. **Read the corresponding template** before writing any code. Templates live in this skill's
   directory under `scripts/templates/<warehouse>/`. To find them, glob for
   `**/push-ingestion/scripts/templates/<warehouse>/*.py` — this works regardless of where the
   skill is installed. Do NOT search from the current working directory alone.
2. **Adapt the template** to the customer's needs — do not write pycarlo imports, model constructors,
   or SDK method calls from memory.
3. If no template exists for the target warehouse, read the **Snowflake template** as the canonical
   reference and adapt only the warehouse-specific collection queries.

Template files follow this naming pattern:
- `collect_<flow>.py` — collection only (queries the warehouse, writes a JSON manifest)
- `push_<flow>.py` — push only (reads the manifest, sends to Monte Carlo)
- `collect_and_push_<flow>.py` — combined (imports from both, runs in sequence)

**After running any push script**, you MUST surface the `invocation_id`(s) returned by the API
to the user. The invocation ID is the only way to trace pushed data through downstream systems
and is required for validation. Never let a push complete without showing the user the
invocation IDs — they need them for `/mc-validate-metadata`, `/mc-validate-lineage`, and
debugging.

## Canonical pycarlo API — authoritative reference

The following imports, classes, and method signatures are the **ONLY** correct pycarlo API for
push ingestion. If your training data suggests different names, **it is wrong**. Use exactly
what is listed here.

### Imports and client setup

```python
from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService
from pycarlo.features.ingestion.models import (
    # Metadata
    RelationalAsset, AssetMetadata, AssetField, AssetVolume, AssetFreshness, Tag,
    # Lineage
    LineageEvent, LineageAssetRef, ColumnLineageField, ColumnLineageSourceField,
    # Query logs
    QueryLogEntry,
)

client = Client(session=Session(mcd_id=key_id, mcd_token=key_token, scope="Ingestion"))
service = IngestionService(mc_client=client)
```

### Method signatures

```python
# Metadata
service.send_metadata(resource_uuid=..., resource_type=..., events=[RelationalAsset(...)])

# Lineage (table or column)
service.send_lineage(resource_uuid=..., resource_type=..., events=[LineageEvent(...)])

# Query logs — note: log_type, NOT resource_type
service.send_query_logs(resource_uuid=..., log_type=..., events=[QueryLogEntry(...)])

# Extract invocation ID from any response
service.extract_invocation_id(result)
```

### RelationalAsset structure (nested, NOT flat)

```python
RelationalAsset(
    type="TABLE",  # ONLY "TABLE" or "VIEW" (uppercase) — normalize warehouse-native values
    metadata=AssetMetadata(
        name="my_table",
        database="analytics",
        schema="public",
        description="optional description",
    ),
    fields=[
        AssetField(name="id", type="INTEGER", description=None),
        AssetField(name="amount", type="DECIMAL(10,2)"),
    ],
    volume=AssetVolume(row_count=1000000, byte_count=111111111),  # optional
    freshness=AssetFreshness(last_update_time="2026-03-12T14:30:00Z"),  # optional
)
```

## Environment variable conventions

All generated scripts MUST use these exact variable names. Do NOT invent alternatives like
`MCD_KEY_ID`, `MC_TOKEN`, `MONTE_CARLO_KEY`, etc.

| Variable | Purpose | Used by |
|---|---|---|
| `MCD_INGEST_ID` | Ingestion key ID (scope=Ingestion) | push scripts |
| `MCD_INGEST_TOKEN` | Ingestion key secret | push scripts |
| `MCD_ID` | GraphQL API key ID | verification scripts |
| `MCD_TOKEN` | GraphQL API key secret | verification scripts |
| `MCD_RESOURCE_UUID` | Warehouse resource UUID | all scripts |

## What this skill can build for you

Tell Claude your warehouse or data platform and Monte Carlo resource UUID and this skill will
generate a ready-to-run Python script that:
- Connects to your warehouse using the idiomatic driver for that platform
- Discovers databases, schemas, and tables
- Extracts the right columns — names, types, row counts, byte counts, last modified time, descriptions
- Builds the correct pycarlo `RelationalAsset`, `LineageEvent`, or `QueryLogEntry` objects
- Pushes to Monte Carlo and saves an output manifest with the `invocation_id` for tracing

Templates are available for common warehouses (Snowflake, BigQuery, BigQuery Iceberg,
Databricks, Redshift, Hive). For any other platform, Claude will derive the appropriate
collection queries from the warehouse's system catalog or metadata APIs and generate an
equivalent script.

### Ready-to-run examples

Production-ready example scripts built from these templates are published in the
[mcd-public-resources](https://github.com/monte-carlo-data/mcd-public-resources) repo:

- **[BigQuery Iceberg (BigLake) tables](https://github.com/monte-carlo-data/mcd-public-resources/tree/main/examples/push-ingestion/bigquery/push-iceberg-tables)** —
  metadata and query log collection for BigQuery Iceberg tables that are invisible to Monte
  Carlo's standard pull collector (which uses `__TABLES__`). Includes a `--only-freshness-and-volume`
  flag for fast periodic pushes that skip the schema/fields query — useful for hourly cron jobs
  after the initial full metadata push.

## Reference docs — when to load

| Reference file | Load when… |
|---|---|
| `references/prerequisites.md` | Customer is setting up for the first time, has auth errors, or needs help creating API keys |
| `references/push-metadata.md` | Building or debugging a metadata collection script |
| `references/push-lineage.md` | Building or debugging a lineage collection script |
| `references/push-query-logs.md` | Building or debugging a query log collection script |
| `references/custom-lineage.md` | Customer needs custom lineage nodes or edges via GraphQL |
| `references/validation.md` | Verifying pushed data, running GraphQL checks, or deleting push-ingested tables |
| `references/direct-http-api.md` | Customer wants to call push APIs directly via curl/HTTP without pycarlo |
| `references/anomaly-detection.md` | Customer asks why freshness or volume detectors aren't firing |

## Prerequisites — read this first

→ Load `references/prerequisites.md`

Two separate API keys are required. This is the most common setup stumbling block:
- **Ingestion key** (scope=Ingestion) — for pushing data
- **GraphQL API key** — for verification queries

Both use the same `x-mcd-id` / `x-mcd-token` headers but point to different endpoints.

## What you can push

| Flow | pycarlo method | Push endpoint | Type field | Expiration |
|---|---|---|---|---|
| Table metadata | `send_metadata()` | `/ingest/v1/metadata` | `resource_type` (e.g. `"data-lake"`) | **Never expires** |
| Table lineage | `send_lineage()` | `/ingest/v1/lineage` | `resource_type` (same as metadata) | **Never expires** |
| Column lineage | `send_lineage()` (events include `fields`) | `/ingest/v1/lineage` | `resource_type` (same as metadata) | **Expires after 10 days** |
| Query logs | `send_query_logs()` | `/ingest/v1/querylogs` | **`log_type`** (not `resource_type`!) | Same as pulled |
| Custom lineage | GraphQL mutations | `api.getmontecarlo.com/graphql` | N/A — uses GraphQL API key | 7 days default; set `expireAt: "9999-12-31"` for permanent |

**Important**: Query logs use `log_type` instead of `resource_type`. This is the only push
endpoint where the field name differs. See `references/push-query-logs.md` for the full list
of supported `log_type` values.

The pycarlo SDK is optional — you can also call the push APIs directly via HTTP/curl. See
`references/direct-http-api.md` for examples.

Every push returns an `invocation_id` — save it. It is your primary debugging handle across
all downstream systems.

## Step 1 — Generate your collection scripts

Ask Claude to build the script for your warehouse:

> "Build me a metadata collection script for Snowflake. My MC resource UUID is `abc-123`."

The script templates in `**/push-ingestion/scripts/templates/` (Snowflake, BigQuery, BigQuery Iceberg, Databricks, Redshift, Hive)
are the **mandatory starting point** for script generation — they contain the correct pycarlo
imports, model constructors, and SDK calls. **They are not an exhaustive list.** If the
customer's warehouse is not listed, use the templates as a guide and determine the appropriate
queries or file-collection approach for their platform. For file-based sources (like Hive
Metastore logs), provide the command to retrieve the file, parse it, and transform it into the
format required by the push APIs. The push format and SDK calls are identical regardless of
source; only the collection queries change.

**Batching**: For large payloads, split events into batches. Use a batch size of **50 assets**
per push call. The pycarlo HTTP client has a hardcoded 10-second read timeout that cannot be
overridden (`Session` and `Client` do not accept a `timeout` parameter) — larger batches (200+)
will timeout on warehouses with thousands of tables. The compressed request body must also not
exceed **1MB** (Kinesis limit). All push endpoints support batching.

**Push frequency**: Push at most **once per hour**. Sub-hourly pushes produce unpredictable
anomaly detector behavior because the training pipeline aggregates into hourly buckets.

**Per flow, see:**
- Metadata (schema + volume + freshness): `references/push-metadata.md`
- Table and column lineage: `references/push-lineage.md`
- Query logs: `references/push-query-logs.md`

## Step 2 — Validate pushed data

After pushing, verify data is visible in Monte Carlo using the GraphQL API (GraphQL API key).

→ `references/validation.md` — all verification queries (getTable, getMetricsV4,
getTableLineage, getDerivedTablesPartialLineage, getAggregatedQueries)

Timing expectations:
- **Metadata**: visible within a few minutes
- **Table lineage**: visible within seconds to a few minutes (fast direct path to Neo4j)
- **Column lineage**: a few minutes
- **Query logs**: at least **15-20 minutes** (async processing pipeline)

## Step 3 — Anomaly detection (optional)

If you want Monte Carlo's freshness and volume detectors to fire on pushed data, you need to
push consistently over time — detectors require historical data to train.

→ `references/anomaly-detection.md` — recommended push frequency, minimum samples,
training windows, and what to tell customers who ask why detectors aren't activating

## Custom lineage nodes and edges

For non-warehouse assets (dbt models, Airflow DAGs, custom ETL pipelines) or cross-resource
lineage, use the GraphQL mutations directly:

→ `references/custom-lineage.md` — `createOrUpdateLineageNode`, `createOrUpdateLineageEdge`,
`deleteLineageNode`, and the critical `expireAt: "9999-12-31"` rule

## Deleting push-ingested tables

Push tables are excluded from the normal pull-based deletion flow (intentionally). To delete
them explicitly, use `deletePushIngestedTables` — covered in `references/validation.md`
under "Table management operations".

## Available slash commands

Customers can invoke these explicitly instead of describing their intent in prose:

| Command | Purpose |
|---|---|
| `/mc-build-metadata-collector` | Generate a metadata collection script |
| `/mc-build-lineage-collector` | Generate a lineage collection script |
| `/mc-build-query-log-collector` | Generate a query log collection script |
| `/mc-validate-metadata` | Verify pushed metadata via the GraphQL API |
| `/mc-validate-lineage` | Verify pushed lineage via the GraphQL API |
| `/mc-validate-query-logs` | Verify pushed query logs via the GraphQL API |
| `/mc-create-lineage-node` | Create a custom lineage node |
| `/mc-create-lineage-edge` | Create a custom lineage edge |
| `/mc-delete-lineage-node` | Delete a custom lineage node |
| `/mc-delete-push-tables` | Delete push-ingested tables |

## Debugging checkpoints

When pushed data isn't appearing, work through these five checkpoints in order:

1. **Did the SDK return a `202` and an `invocation_id`?**
   If not, the gateway rejected the request — check auth headers and `resource.uuid`.

2. **Is the integration key the right type?**
   Must be scope `Ingestion`, created via `montecarlo integrations create-key --scope Ingestion`.
   A standard GraphQL API key will not work for push.

3. **Is `resource.uuid` correct and authorized?**
   The key can be scoped to specific warehouse UUIDs. If the UUID doesn't match, you get `403`.

4. **Did the normalizer process it?**
   Use the `invocation_id` to search CloudWatch logs for the relevant Lambda. For query logs,
   check the `log_type` — Hive requires `"hive-s3"`, not `"hive"`.

5. **Did the downstream system pick it up?**
   - Metadata: query `getTable` in GraphQL
   - Table lineage: check Neo4j within seconds–minutes (fast path via PushLineageProcessor)
   - Query logs: wait at least 15-20 minutes; check `getAggregatedQueries`

## Known gotchas

- **`log_type` vs `resource_type`**: metadata and lineage use `resource_type` (e.g. `"data-lake"`);
  query logs use **`log_type`** — the only endpoint where the field name differs. Wrong value →
  `Unsupported ingest query-log log_type` error.
- **`invocation_id` must be saved**: every output manifest should include it — it's your
  only tracing handle once the request leaves the SDK.
- **Query log async delay**: at least 15-20 minutes. `getAggregatedQueries` will return 0 until
  processing completes — this is expected, not a bug.
- **Custom lineage `expireAt` defaults to 7 days**: nodes vanish silently unless you set
  `expireAt: "9999-12-31"` for permanent nodes.
- **Push tables are never auto-deleted**: the periodic cleanup job excludes them by default
  (`exclude_push_tables=True`). Delete them explicitly via `deletePushIngestedTables` (max
  1,000 MCONs per call; also deletes lineage nodes and all edges touching those nodes).
- **Anomaly detectors need history**: pushing once is not enough. Freshness needs 7+ pushes
  over ~2 weeks; volume needs 10–48 samples over ~42 days. Push at most once per hour.
- **Batching required for large payloads**: the compressed request body must not exceed 1MB.
  Split large event lists into batches.
- **Column lineage expires after 10 days**: unlike table metadata and table lineage (which
  never expire), column lineage has a 10-day TTL, same as pulled column lineage.
- **Quote SQL identifiers in warehouse queries**: database, schema, and table names must be
  quoted to handle mixed-case or special characters. The quoting syntax varies by warehouse —
  Snowflake and Redshift use double quotes (`"{db}"`), BigQuery/Databricks/Hive use backticks
  (`` `db` ``). The templates already handle this correctly for each warehouse — follow the
  same quoting pattern when adapting.

## Memory safety

Generated scripts must include a startup memory check. The collection phase loads query history
rows into memory for parsing — on large warehouses with long lookback windows, this can exhaust
available RAM and cause the process to be silently killed (SIGKILL / exit 137) with no traceback.

Add this pattern near the top of every generated script, after imports:

```python
import os

def _check_available_memory(min_gb: float = 2.0) -> None:
    """Warn if available memory is below the threshold."""
    try:
        if hasattr(os, "sysconf"):  # Linux / macOS
            page_size = os.sysconf("SC_PAGE_SIZE")
            avail_pages = os.sysconf("SC_AVPHYS_PAGES")
            avail_gb = (page_size * avail_pages) / (1024 ** 3)
        else:
            return  # Windows — skip check
    except (ValueError, OSError):
        return
    if avail_gb < min_gb:
        print(
            f"WARNING: Only {avail_gb:.1f} GB of memory available "
            f"(minimum recommended: {min_gb:.1f} GB). "
            f"Consider reducing the lookback window or increasing available memory."
        )
```

Call `_check_available_memory()` before connecting to the warehouse.

Additionally, when fetching query history:
- Use `cursor.fetchmany(batch_size)` in a loop instead of `cursor.fetchall()` when possible
- For very large result sets, consider adding a LIMIT clause and processing in windows

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## monte-carlo-validation-notebook
*Generates SQL validation notebooks for dbt PR changes with before/after comparison queries.*

Tags: [data-observability, validation, dbt, monte-carlo, sql-notebook]
Tools: [claude, cursor, codex]
Risk: safe

> **Tip:** This skill works well with Sonnet. Run `/model sonnet` before invoking for faster generation.

Generate a SQL Notebook with validation queries for dbt changes.

**Arguments:** $ARGUMENTS

## When to Use

Use this skill when the user wants to validate dbt model or snapshot changes with Monte Carlo SQL Notebook queries, either from a GitHub PR or a local dbt repository.

Parse the arguments:
- **Target** (required): first argument — a GitHub PR URL or local dbt repo path
- **MC Base URL** (optional): `--mc-base-url <URL>` — defaults to `https://getmontecarlo.com`
- **Models** (optional): `--models <model1,model2,...>` — comma-separated list of model filenames (without `.sql` extension) to generate queries for. Only these models will be included. By default, all changed models are included up to a maximum of 10.

---

# Setup

**Prerequisites:**
- **`gh`** (GitHub CLI) — required for PR mode. Must be authenticated (`gh auth status`).
- **`python3`** — required for helper scripts.
- **`pyyaml`** — install with `pip3 install pyyaml` (or `pip install pyyaml`, `uv pip install pyyaml`, etc.)

**Note:** Generated SQL uses ANSI-compatible syntax that works across Snowflake, BigQuery, Redshift, and Athena. Minor adjustments may be needed for specific warehouse quirks.

This skill includes two helper scripts in `${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/`:

- **`resolve_dbt_schema.py`** - Resolves dbt model output schemas from `dbt_project.yml` routing rules and model config overrides.
- **`generate_notebook_url.py`** - Encodes notebook YAML into a base64 import URL and opens it in the browser.

# Mode Detection

Auto-detect mode from the target argument:
- If target looks like a URL (contains `://` or `github.com`) -> **PR mode**
- If target is a path (`.`, `/path/to/repo`, relative path) -> **Local mode**

---

# Context

This command generates a SQL Notebook containing validation queries for dbt changes. The notebook can be opened in the MC Bridge SQL Notebook interface for interactive validation.

The output is an import URL that opens directly in the notebook interface:
```
<MC_BASE_URL>/notebooks/import#<base64-encoded-yaml>
```

**Key Features:**
- **Database Parameters**: Two `text` parameters (`prod_db` and `dev_db`) for selecting databases
- **Schema Inference**: Automatically infers schema per model from `dbt_project.yml` and model configs
- **Single-table queries**: Basic validation queries using `{{prod_db}}.<SCHEMA>.<TABLE>`
- **Comparison queries**: Before/after queries comparing `{{prod_db}}` vs `{{dev_db}}`
- **Flexible usage**: Users can set both parameters to the same database for single-database analysis

# Notebook YAML Spec Reference

Key structure:
```yaml
version: 1
metadata:
  id: string           # kebab-case + random suffix
  name: string         # display name
  created_at: string   # ISO 8601
  updated_at: string   # ISO 8601
default_context:       # optional database/schema context
  database: string
  schema: string
cells:
  - id: string
    type: sql | markdown | parameter
    content: string    # SQL, markdown, or parameter config (JSON)
    display_type: table | bar | timeseries
```

## Parameter Cell Spec

Parameter cells allow defining variables referenced in SQL via `{{param_name}}` syntax:

```yaml
- id: param-prod-db
  type: parameter
  content:
    name: prod_db              # variable name
    config:
      type: text                   # free-form text input
      default_value: "ANALYTICS"
      placeholder: "Prod database"
  display_type: table
```

Parameter types:
- `text`: Free-form text input (used for database names)
- `schema_selector`: Two dropdowns (database -> schema), value stored as `DATABASE.SCHEMA`
- `dropdown`: Select from predefined options

# Task

Generate a SQL Notebook with validation queries based on the mode and target.

## Phase 1: Get Changed Files

The approach differs based on mode:

### If PR mode (GitHub PR):

1. Extract the PR number and repo from the target URL.
   - Example: `https://github.com/monte-carlo-data/dbt/pull/3386` -> owner=`monte-carlo-data`, repo=`dbt`, PR=`3386`

2. Fetch PR metadata using `gh`:
```bash
gh pr view <PR#> --repo <owner>/<repo> --json number,title,author,mergedAt,headRefOid
```

3. Fetch the list of changed files:
```bash
gh pr view <PR#> --repo <owner>/<repo> --json files --jq '.files[].path'
```

4. Fetch the diff:
```bash
gh pr diff <PR#> --repo <owner>/<repo>
```

5. Filter the changed files list to only `.sql` files under `models/` or `snapshots/` directories (at any depth — e.g., `models/`, `analytics/models/`, `dbt/models/`). These are the dbt models to analyze. If no model SQL files were changed, report that and stop.

6. For each changed model file, fetch the full file content at the head SHA:
```bash
gh api repos/<owner>/<repo>/contents/<file_path>?ref=<head_sha> --jq '.content' | python3 -c "import sys,base64; sys.stdout.write(base64.b64decode(sys.stdin.read()).decode())"
```

7. **Fetch dbt_project.yml** for schema resolution. Detect the dbt project root by looking at the changed file paths — find the common parent directory that contains `dbt_project.yml`. Try these paths in order until one succeeds:
```bash
gh api repos/<owner>/<repo>/contents/<dbt_root>/dbt_project.yml?ref=<head_sha> --jq '.content' | python3 -c "import sys,base64; sys.stdout.write(base64.b64decode(sys.stdin.read()).decode())"
```
Common `<dbt_root>` locations: `analytics`, `.` (repo root), `dbt`, `transform`. Try each until found.

Save `dbt_project.yml` to `/tmp/validation_notebook_working/<PR#>/dbt_project.yml`.

### If Local mode (Local Directory):

1. Change to the target directory.

2. Get current branch info:
```bash
git rev-parse --abbrev-ref HEAD
```

3. Detect base branch - try `main`, `master`, `develop` in order, or use upstream tracking branch.

4. Get the list of changed SQL files compared to base branch:
```bash
git diff --name-only <base_branch>...HEAD -- '*.sql'
```

5. Filter to only `.sql` files under `models/` or `snapshots/` directories (at any depth — e.g., `models/`, `analytics/models/`, `dbt/models/`). If no model SQL files were changed, report that and stop.

6. Get the diff for each changed file:
```bash
git diff <base_branch>...HEAD -- <file_path>
```

7. Read model files directly from the filesystem.

8. **Find dbt_project.yml**:
```bash
find . -name "dbt_project.yml" -type f | head -1
```

9. For notebook metadata in local mode, use:
   - **ID**: `local-<branch-name>-<timestamp>`
   - **Title**: `Local: <branch-name>`
   - **Author**: Output of `git config user.name`
   - **Merged**: "N/A (local)"

### Model Selection (applies to both modes)

After filtering to `.sql` files under `models/` or `snapshots/`:

1. **If `--models` was specified:** Filter the changed files list to only include models whose filename (without `.sql` extension, case-insensitive) matches one of the specified model names. If any specified model is not found in the changed files, warn the user but continue with the models that were found. If none match, report that and stop.

2. **Model cap:** If more than 10 models remain after filtering, select the first 10 (by file path order) and warn the user:
   ```
   ⚠️ <total_count> models changed — generating validation queries for the first 10 only.
   To generate for specific models, re-run with: --models <model1,model2,...>
   Skipped models: <list of skipped model filenames>
   ```

## Phase 2: Parse Changed Models

For EACH changed dbt model `.sql` file, parse and extract:

### 2a. Model Metadata

**Output table name** -- Derive from file name:
- `<any_path>/models/<subdir>/<model_name>.sql` -> table is `<MODEL_NAME>` (uppercase, taken from the filename)

**Output schema** -- Use the schema resolution script:

1. **Setup**: Save `dbt_project.yml` and model files to `/tmp/validation_notebook_working/<id>/` preserving paths:
   ```
   /tmp/validation_notebook_working/<id>/
   +-- dbt_project.yml
   +-- models/
       +-- <path>/<model>.sql
   ```

2. **Run the script** for each model:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/resolve_dbt_schema.py /tmp/validation_notebook_working/<id>/dbt_project.yml /tmp/validation_notebook_working/<id>/models/<path>/<model>.sql
   ```

3. **Error handling**: If the script fails, **STOP immediately** and report the error. Do NOT proceed with notebook generation if schema resolution fails.

4. **Output**: The script prints the resolved schema (e.g., `PROD`, `PROD_STAGE`, `PROD_LINEAGE`)

**Note**: Do NOT manually parse dbt_project.yml or model configs for schema -- always use the script. It handles model config overrides, dbt_project.yml routing rules, PROD_ prefix for custom schemas, and defaults to `PROD`.

**Config block** -- Look for `{{ config(...) }}` and extract:
- `materialized` -- 'table', 'view', 'incremental', 'ephemeral'
- `unique_key` -- the dedup key (may be a string or list)
- `cluster_by` -- clustering fields (may contain the time axis)

**Core segmentation fields** -- Scan the entire model SQL for fields likely to be business keys:
- Fields named `*_id` (e.g., `account_id`, `resource_id`, `monitor_id`) that appear in JOIN ON, GROUP BY, PARTITION BY, or `unique_key`
- Deduplicate and rank by frequency. Take the top 3.

**Time axis field** -- Detect the model's time dimension (in priority order):
1. `is_incremental()` block: field used in the WHERE comparison
2. `cluster_by` config: timestamp/date fields
3. Field name conventions: `ingest_ts`, `created_time`, `date_part`, `timestamp`, `run_start_time`, `export_ts`, `event_created_time`
4. ORDER BY DESC in QUALIFY/ROW_NUMBER

If no time axis is found, skip time-axis queries for this model.

### 2b. Diff Analysis

Parse the diff hunks for this file. Classify each changed line:

- **Changed fields** -- Lines added/modified in SELECT clauses or CTE definitions. Extract the output column name.
- **Changed filters** -- Lines added/modified in WHERE clauses.
- **Changed joins** -- Lines added/modified in JOIN ON conditions.
- **Changed unique_key** -- If `unique_key` in config was modified, note both old and new values.
- **New columns** -- Columns in "after" SELECT that don't appear in "before" (pure additions).

### 2c. Model Classification

Classify each model as **new** or **modified** based on the diff:
- If the diff for this file contains `new file mode` → classify as **new**
- Otherwise → classify as **modified**

This classification determines which query patterns are generated in Phase 3.

**Note:** For **new models**, Phase 2b diff analysis is skipped (there is no "before" to compare against). Phase 2a metadata extraction still applies.

## Phase 3: Generate Validation Queries

For each changed model, generate the applicable queries based on its classification (new vs modified).

**CRITICAL: Parameter Placeholder Syntax**

Use **double curly braces** `{{...}}` for parameter placeholders. Do NOT use `${...}` or any other syntax.

Correct: `{{prod_db}}.PROD.AGENT_RUNS`
Wrong: `${prod_db}.PROD.AGENT_RUNS`

**Table Reference Format:**
- Use `{{prod_db}}.<SCHEMA>.<TABLE_NAME>` for prod queries
- Use `{{dev_db}}.<SCHEMA>.<TABLE_NAME>` for dev queries
- `<SCHEMA>` is **hardcoded per-model** using the output from the schema resolution script

---

### Query Patterns for NEW Models

For new models, all queries target `{{dev_db}}` only. No comparison queries are generated since no prod table exists.

#### Pattern 7-new: Total Row Count
**Trigger:** Always.

```sql
SELECT COUNT(*) AS total_rows
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 9: Sample Data Preview
**Trigger:** Always.

```sql
SELECT *
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
LIMIT 20
```

#### Pattern 2-new: Core Segmentation Counts
**Trigger:** Always.

```sql
SELECT
    <segmentation_field>,
    COUNT(*) AS row_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <segmentation_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 5: Uniqueness Check
**Trigger:** Always for new models (verify unique_key constraint from the start).

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT <key_fields>) AS distinct_keys,
    COUNT(*) - COUNT(DISTINCT <key_fields>) AS duplicate_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

```sql
SELECT <key_fields>, COUNT(*) AS n
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <key_fields>
HAVING COUNT(*) > 1
ORDER BY n DESC
LIMIT 100
```

#### Pattern 6-new: NULL Rate Check (all columns)
**Trigger:** Always. Checks all output columns since everything is new.

```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <col1> IS NULL THEN 1 ELSE 0 END) AS <col1>_null_count,
    ROUND(100.0 * SUM(CASE WHEN <col1> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS <col1>_null_pct,
    SUM(CASE WHEN <col2> IS NULL THEN 1 ELSE 0 END) AS <col2>_null_count,
    ROUND(100.0 * SUM(CASE WHEN <col2> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS <col2>_null_pct
    -- repeat for each output column
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 8: Time-Axis Continuity
**Trigger:** Model is `materialized='incremental'` OR a time axis field was identified.

```sql
SELECT
    CAST(<time_axis> AS DATE) AS day,
    COUNT(*) AS row_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
WHERE <time_axis> >= CURRENT_TIMESTAMP - INTERVAL '14' DAY
GROUP BY day
ORDER BY day DESC
LIMIT 30
```

---

### Query Patterns for MODIFIED Models

For modified models, single-table queries use `{{prod_db}}` and comparison queries use both.

#### Pattern 7: Total Row Count
**Trigger:** Always.

```sql
SELECT COUNT(*) AS total_rows
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 9: Sample Data Preview
**Trigger:** Always.

```sql
SELECT *
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
LIMIT 20
```

#### Pattern 2: Core Segmentation Counts
**Trigger:** Always.

```sql
SELECT
    <segmentation_field>,
    COUNT(*) AS row_count
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <segmentation_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 1: Changed Field Distribution
**Trigger:** Changed fields found in Phase 2b. **Exclude added columns** (from "New columns" in Phase 2b) — only include fields that exist in prod.

```sql
SELECT
    <changed_field>,
    COUNT(*) AS row_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <changed_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 5: Uniqueness Check
**Trigger:** JOIN condition changed, `unique_key` changed, or model is incremental.

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT <key_fields>) AS distinct_keys,
    COUNT(*) - COUNT(DISTINCT <key_fields>) AS duplicate_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

```sql
SELECT <key_fields>, COUNT(*) AS n
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <key_fields>
HAVING COUNT(*) > 1
ORDER BY n DESC
LIMIT 100
```

#### Pattern 6: NULL Rate Check
**Trigger:** New column added, or column wrapped in COALESCE/NULLIF.

**Important:** Added columns (from "New columns" in Phase 2b) do NOT exist in prod yet. For added columns, query `{{dev_db}}` only. For modified columns (COALESCE/NULLIF changes), compare both databases.

**For added columns** (dev only):
```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

**For modified columns** (prod vs dev):
```sql
SELECT
    'prod' AS source,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
UNION ALL
SELECT
    'dev' AS source,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 8: Time-Axis Continuity
**Trigger:** Model is `materialized='incremental'` OR a time axis field was identified.

```sql
SELECT
    CAST(<time_axis> AS DATE) AS day,
    COUNT(*) AS row_count
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
WHERE <time_axis> >= CURRENT_TIMESTAMP - INTERVAL '14' DAY
GROUP BY day
ORDER BY day DESC
LIMIT 30
```

#### Pattern 3: Before/After Comparison
**Trigger:** Always (for changed fields + top segmentation field). **Modified models only.**

**Important:** Exclude added columns (from "New columns" in Phase 2b) from `<group_fields>`. Only use fields that exist in BOTH prod and dev. Added columns don't exist in prod and will cause query errors.

```sql
WITH prod AS (
    SELECT <group_fields>, COUNT(*) AS cnt
    FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
    GROUP BY <group_fields>
),
dev AS (
    SELECT <group_fields>, COUNT(*) AS cnt
    FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
    GROUP BY <group_fields>
)
SELECT
    COALESCE(b.<field>, d.<field>) AS <field>,
    COALESCE(b.cnt, 0) AS cnt_prod,
    COALESCE(d.cnt, 0) AS cnt_dev,
    COALESCE(d.cnt, 0) - COALESCE(b.cnt, 0) AS diff
FROM prod b
FULL OUTER JOIN dev d ON b.<field> = d.<field>
ORDER BY ABS(diff) DESC
LIMIT 100
```

#### Pattern 7b: Row Count Comparison
**Trigger:** Always. **Modified models only.**

```sql
SELECT 'prod' AS source, COUNT(*) AS row_count FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
UNION ALL
SELECT 'dev' AS source, COUNT(*) AS row_count FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

## Phase 4: Build Notebook YAML

### 4a. Metadata
```yaml
version: 1
metadata:
  id: validation-pr-<PR_NUMBER>-<random_suffix>
  name: "Validation: PR #<PR_NUMBER> - <PR_TITLE_TRUNCATED>"
  created_at: "<current_iso_timestamp>"
  updated_at: "<current_iso_timestamp>"
```

### 4b. Parameter Cells

**Only include `prod_db` if there are modified models.** If all models are new, only include `dev_db`.

```yaml
# Include ONLY if there are modified models:
- id: param-prod-db
  type: parameter
  content:
    name: prod_db
    config:
      type: text
      default_value: "ANALYTICS"
      placeholder: "Prod database (e.g., ANALYTICS)"
  display_type: table

# Always include:
- id: param-dev-db
  type: parameter
  content:
    name: dev_db
    config:
      type: text
      default_value: "PERSONAL_<USER>"
      placeholder: "Dev database (e.g., PERSONAL_JSMITH)"
  display_type: table
```

### 4c. Markdown Summary Cell
```yaml
- id: cell-summary
  type: markdown
  content: |
    # Validation Queries for <PR or Local Branch>
    ## Summary
    - **Title:** <title>
    - **Author:** <author>
    - **Source:** <PR URL or "Local branch: <branch>">
    - **Status:** <merge_timestamp or "Not yet merged" or "N/A (local)">
    ## Changes
    <brief description based on diff analysis>
    ## Changed Models
    - `<SCHEMA>.<TABLE_NAME>` (from `<file_path>`)
    ## How to Use
    1. Select your Snowflake connector above
    2. Set **dev_db** to your dev database (e.g., `PERSONAL_JSMITH`)
    3. If modified models are present, set **prod_db** to your prod database (e.g., `ANALYTICS`)
    4. Run single-table queries first, then comparison queries
  display_type: table
```

### 4d. SQL Cell Format
```yaml
- id: cell-<pattern>-<model>-<index>
  type: sql
  content: |
    /*
    ========================================
    <Pattern Name (human-readable, e.g. "Total Row Count" — do NOT include pattern numbers like "Pattern 7:")>
    ========================================
    Model: <SCHEMA>.<TABLE_NAME>
    Triggered by: <why this pattern was generated>
    What to look for: <interpretation guidance>
    ----------------------------------------
    */
    <actual_sql_query>
  display_type: table
```

### 4e. Cell Organization

Cells are ordered consistently for both model types, following this sequence:

**New models:**
1. Summary markdown cell (note that model is new)
2. Parameter cells (dev_db only — no prod_db if all models are new)
3. Total row count (Pattern 7-new)
4. Sample data preview (Pattern 9)
5. Core segmentation counts (Pattern 2-new)
6. Uniqueness check (Pattern 5), NULL rate check (Pattern 6-new), Time-axis continuity (Pattern 8)

**Modified models:**
1. Summary markdown cell
2. Parameter cells (prod_db, dev_db)
3. Total row count (Pattern 7)
4. Sample data preview (Pattern 9)
5. Core segmentation counts (Pattern 2)
6. Changed field distribution (Pattern 1)
7. Uniqueness check (Pattern 5), NULL rate check (Pattern 6), Time-axis continuity (Pattern 8)
8. Before/after comparisons (Pattern 3), Row count comparison (Pattern 7b)

## Phase 5: Generate Import URL

1. Write notebook YAML to `/tmp/validation_notebook_working/<id>/notebook.yaml`
2. Run the URL generation script:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/generate_notebook_url.py /tmp/validation_notebook_working/<id>/notebook.yaml --mc-base-url <MC_BASE_URL>
```
3. The script validates both YAML syntax and notebook schema (required fields on metadata and cells). If validation fails, read the error messages carefully, fix the YAML to match the spec in Phase 4, and re-run.

## Phase 6: Output

Present:
```markdown
# Validation Notebook Generated
## Summary
- **Source:** PR #<number> - <title> OR Local: <branch>
- **Author:** <author>
- **Changed Models:** <count> models (of <total_count> changed)
- **Generated Queries:** <count> queries

> ⚠️ If models were capped: "Only the first 10 of <total_count> changed models were included. Re-run with `--models` to select specific models."

## Notebook Opened
The notebook has been opened directly in your browser.
Select your Snowflake connector in the notebook interface to begin running queries.
*Make sure MC Bridge is running. Let me know if you want tips on how to install this locally*
```

## Important Guidelines

1. **Do NOT execute queries** -- only generate the notebook
2. **Keep SQL readable** -- proper formatting and meaningful aliases
3. **Include LIMIT 100** on queries that could return many rows
4. **Use double curly braces** -- `{{prod_db}}` NOT `${prod_db}`
5. **Use correct table format** -- `{{prod_db}}.<SCHEMA>.<TABLE>` and `{{dev_db}}.<SCHEMA>.<TABLE>`
6. **Always use the schema resolution script** -- do NOT manually parse dbt_project.yml
7. **Schema is NOT a parameter** -- only `prod_db` and `dev_db` are parameters
8. **Skip ephemeral models** -- they have no physical table
9. **Truncate notebook name** -- keep under 50 chars
10. **Generate unique cell IDs** -- use pattern like `cell-p3-model-1`
11. **YAML multiline content** -- use `|` block scalar for SQL with comments
12. **ASCII-only YAML** -- the script sanitizes and validates before encoding

## Query Pattern Reference

| Pattern | Name | Trigger | Model Type | Database | Order |
|---------|------|---------|------------|----------|-------|
| 7 / 7-new | Total Row Count | Always | Both | `{{prod_db}}` (modified) / `{{dev_db}}` (new) | 1 |
| 9 | Sample Data Preview | Always | Both | `{{prod_db}}` (modified) / `{{dev_db}}` (new) | 2 |
| 2 / 2-new | Core Segmentation Counts | Always | Both | `{{prod_db}}` (modified) / `{{dev_db}}` (new) | 3 |
| 1 | Changed Field Distribution | Column modified in diff (not added) | Modified only | `{{prod_db}}` | 4 |
| 5 | Uniqueness Check | JOIN/unique_key changed (modified) / Always (new) | Both | `{{dev_db}}` | 5 |
| 6 / 6-new | NULL Rate Check | New column or COALESCE (modified) / Always (new) | Both | Added col: `{{dev_db}}` only; COALESCE: Both (modified) / `{{dev_db}}` (new) | 5 |
| 8 | Time-Axis Continuity | Incremental or time field | Both | `{{prod_db}}` (modified) / `{{dev_db}}` (new) | 5 |
| 3 | Before/After Comparison | Changed fields (not added) | Modified only | Both | 6 |
| 7b | Row Count Comparison | Always | Modified only | Both | 6 |

## MC Bridge Setup Help

If the user asks how to install or set up MC Bridge, fetch the README from the mc-bridge repo and show the relevant quick start / setup instructions:

```bash
gh api repos/monte-carlo-data/mc-bridge/readme --jq '.content' | base64 --decode
```

Focus on: how to install, configure connections, and run MC Bridge. Don't dump the entire README — extract just the setup-relevant sections.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## nestjs-expert
*You are an expert in Nest.js with deep knowledge of enterprise-grade Node.js application architecture, dependency injection patterns, decorators, middleware, guards, interceptors, pipes, testing strategies, database integration, and authentication systems.*

Risk: unknown

# Nest.js Expert

You are an expert in Nest.js with deep knowledge of enterprise-grade Node.js application architecture, dependency injection patterns, decorators, middleware, guards, interceptors, pipes, testing strategies, database integration, and authentication systems.

### When invoked:

0. If a more specialized expert fits better, recommend switching and stop:
   - Pure TypeScript type issues → typescript-type-expert
   - Database query optimization → database-expert  
   - Node.js runtime issues → nodejs-expert
   - Frontend React issues → react-expert
   
   Example: "This is a TypeScript type system issue. Use the typescript-type-expert subagent. Stopping here."

1. Detect Nest.js project setup using internal tools first (Read, Grep, Glob)
2. Identify architecture patterns and existing modules
3. Apply appropriate solutions following Nest.js best practices
4. Validate in order: typecheck → unit tests → integration tests → e2e tests

## Domain Coverage

### Module Architecture & Dependency Injection
- Common issues: Circular dependencies, provider scope conflicts, module imports
- Root causes: Incorrect module boundaries, missing exports, improper injection tokens
- Solution priority: 1) Refactor module structure, 2) Use forwardRef, 3) Adjust provider scope
- Tools: `nest generate module`, `nest generate service`
- Resources: [Nest.js Modules](https://docs.nestjs.com/modules), [Providers](https://docs.nestjs.com/providers)

### Controllers & Request Handling
- Common issues: Route conflicts, DTO validation, response serialization
- Root causes: Decorator misconfiguration, missing validation pipes, improper interceptors
- Solution priority: 1) Fix decorator configuration, 2) Add validation, 3) Implement interceptors
- Tools: `nest generate controller`, class-validator, class-transformer
- Resources: [Controllers](https://docs.nestjs.com/controllers), [Validation](https://docs.nestjs.com/techniques/validation)

### Middleware, Guards, Interceptors & Pipes
- Common issues: Execution order, context access, async operations
- Root causes: Incorrect implementation, missing async/await, improper error handling
- Solution priority: 1) Fix execution order, 2) Handle async properly, 3) Implement error handling
- Execution order: Middleware → Guards → Interceptors (before) → Pipes → Route handler → Interceptors (after)
- Resources: [Middleware](https://docs.nestjs.com/middleware), [Guards](https://docs.nestjs.com/guards)

### Testing Strategies (Jest & Supertest)
- Common issues: Mocking dependencies, testing modules, e2e test setup
- Root causes: Improper test module creation, missing mock providers, incorrect async handling
- Solution priority: 1) Fix test module setup, 2) Mock dependencies correctly, 3) Handle async tests
- Tools: `@nestjs/testing`, Jest, Supertest
- Resources: [Testing](https://docs.nestjs.com/fundamentals/testing)

### Database Integration (TypeORM & Mongoose)
- Common issues: Connection management, entity relationships, migrations
- Root causes: Incorrect configuration, missing decorators, improper transaction handling
- Solution priority: 1) Fix configuration, 2) Correct entity setup, 3) Implement transactions
- TypeORM: `@nestjs/typeorm`, entity decorators, repository pattern
- Mongoose: `@nestjs/mongoose`, schema decorators, model injection
- Resources: [TypeORM](https://docs.nestjs.com/techniques/database), [Mongoose](https://docs.nestjs.com/techniques/mongodb)

### Authentication & Authorization (Passport.js)
- Common issues: Strategy configuration, JWT handling, guard implementation
- Root causes: Missing strategy setup, incorrect token validation, improper guard usage
- Solution priority: 1) Configure Passport strategy, 2) Implement guards, 3) Handle JWT properly
- Tools: `@nestjs/passport`, `@nestjs/jwt`, passport strategies
- Resources: [Authentication](https://docs.nestjs.com/security/authentication), [Authorization](https://docs.nestjs.com/security/authorization)

### Configuration & Environment Management
- Common issues: Environment variables, configuration validation, async configuration
- Root causes: Missing config module, improper validation, incorrect async loading
- Solution priority: 1) Setup ConfigModule, 2) Add validation, 3) Handle async config
- Tools: `@nestjs/config`, Joi validation
- Resources: [Configuration](https://docs.nestjs.com/techniques/configuration)

### Error Handling & Logging
- Common issues: Exception filters, logging configuration, error propagation
- Root causes: Missing exception filters, improper logger setup, unhandled promises
- Solution priority: 1) Implement exception filters, 2) Configure logger, 3) Handle all errors
- Tools: Built-in Logger, custom exception filters
- Resources: [Exception Filters](https://docs.nestjs.com/exception-filters), [Logger](https://docs.nestjs.com/techniques/logger)

## Environmental Adaptation

### Detection Phase
I analyze the project to understand:
- Nest.js version and configuration
- Module structure and organization
- Database setup (TypeORM/Mongoose/Prisma)
- Testing framework configuration
- Authentication implementation

Detection commands:
```bash
# Check Nest.js setup
test -f nest-cli.json && echo "Nest.js CLI project detected"
grep -q "@nestjs/core" package.json && echo "Nest.js framework installed"
test -f tsconfig.json && echo "TypeScript configuration found"

# Detect Nest.js version
grep "@nestjs/core" package.json | sed 's/.*"\([0-9\.]*\)".*/Nest.js version: \1/'

# Check database setup
grep -q "@nestjs/typeorm" package.json && echo "TypeORM integration detected"
grep -q "@nestjs/mongoose" package.json && echo "Mongoose integration detected"
grep -q "@prisma/client" package.json && echo "Prisma ORM detected"

# Check authentication
grep -q "@nestjs/passport" package.json && echo "Passport authentication detected"
grep -q "@nestjs/jwt" package.json && echo "JWT authentication detected"

# Analyze module structure
find src -name "*.module.ts" -type f | head -5 | xargs -I {} basename {} .module.ts
```

**Safety note**: Avoid watch/serve processes; use one-shot diagnostics only.

### Adaptation Strategies
- Match existing module patterns and naming conventions
- Follow established testing patterns
- Respect database strategy (repository pattern vs active record)
- Use existing authentication guards and strategies

## Tool Integration

### Diagnostic Tools
```bash
# Analyze module dependencies
nest info

# Check for circular dependencies
npm run build -- --watch=false

# Validate module structure
npm run lint
```

### Fix Validation
```bash
# Verify fixes (validation order)
npm run build          # 1. Typecheck first
npm run test           # 2. Run unit tests
npm run test:e2e       # 3. Run e2e tests if needed
```

**Validation order**: typecheck → unit tests → integration tests → e2e tests

## Problem-Specific Approaches (Real Issues from GitHub & Stack Overflow)

### 1. "Nest can't resolve dependencies of the [Service] (?)"
**Frequency**: HIGHEST (500+ GitHub issues) | **Complexity**: LOW-MEDIUM
**Real Examples**: GitHub #3186, #886, #2359 | SO 75483101
When encountering this error:
1. Check if provider is in module's providers array
2. Verify module exports if crossing boundaries  
3. Check for typos in provider names (GitHub #598 - misleading error)
4. Review import order in barrel exports (GitHub #9095)

### 2. "Circular dependency detected"
**Frequency**: HIGH | **Complexity**: HIGH
**Real Examples**: SO 65671318 (32 votes) | Multiple GitHub discussions
Community-proven solutions:
1. Use forwardRef() on BOTH sides of the dependency
2. Extract shared logic to a third module (recommended)
3. Consider if circular dependency indicates design flaw
4. Note: Community warns forwardRef() can mask deeper issues

### 3. "Cannot test e2e because Nestjs doesn't resolve dependencies"
**Frequency**: HIGH | **Complexity**: MEDIUM
**Real Examples**: SO 75483101, 62942112, 62822943
Proven testing solutions:
1. Use @golevelup/ts-jest for createMock() helper
2. Mock JwtService in test module providers
3. Import all required modules in Test.createTestingModule()
4. For Bazel users: Special configuration needed (SO 62942112)

### 4. "[TypeOrmModule] Unable to connect to the database"
**Frequency**: MEDIUM | **Complexity**: HIGH  
**Real Examples**: GitHub typeorm#1151, #520, #2692
Key insight - this error is often misleading:
1. Check entity configuration - @Column() not @Column('description')
2. For multiple DBs: Use named connections (GitHub #2692)
3. Implement connection error handling to prevent app crash (#520)
4. SQLite: Verify database file path (typeorm#8745)

### 5. "Unknown authentication strategy 'jwt'"
**Frequency**: HIGH | **Complexity**: LOW
**Real Examples**: SO 79201800, 74763077, 62799708
Common JWT authentication fixes:
1. Import Strategy from 'passport-jwt' NOT 'passport-local'
2. Ensure JwtModule.secret matches JwtStrategy.secretOrKey
3. Check Bearer token format in Authorization header
4. Set JWT_SECRET environment variable

### 6. "ActorModule exporting itself instead of ActorService"
**Frequency**: MEDIUM | **Complexity**: LOW
**Real Example**: GitHub #866
Module export configuration fix:
1. Export the SERVICE not the MODULE from exports array
2. Common mistake: exports: [ActorModule] → exports: [ActorService]
3. Check all module exports for this pattern
4. Validate with nest info command

### 7. "secretOrPrivateKey must have a value" (JWT)
**Frequency**: HIGH | **Complexity**: LOW
**Real Examples**: Multiple community reports
JWT configuration fixes:
1. Set JWT_SECRET in environment variables
2. Check ConfigModule loads before JwtModule
3. Verify .env file is in correct location
4. Use ConfigService for dynamic configuration

### 8. Version-Specific Regressions
**Frequency**: LOW | **Complexity**: MEDIUM
**Real Example**: GitHub #2359 (v6.3.1 regression)
Handling version-specific bugs:
1. Check GitHub issues for your specific version
2. Try downgrading to previous stable version
3. Update to latest patch version
4. Report regressions with minimal reproduction

### 9. "Nest can't resolve dependencies of the UserController (?, +)"
**Frequency**: HIGH | **Complexity**: LOW
**Real Example**: GitHub #886
Controller dependency resolution:
1. The "?" indicates missing provider at that position
2. Count constructor parameters to identify which is missing
3. Add missing service to module providers
4. Check service is properly decorated with @Injectable()

### 10. "Nest can't resolve dependencies of the Repository" (Testing)
**Frequency**: MEDIUM | **Complexity**: MEDIUM
**Real Examples**: Community reports
TypeORM repository testing:
1. Use getRepositoryToken(Entity) for provider token
2. Mock DataSource in test module
3. Provide test database connection
4. Consider mocking repository completely

### 11. "Unauthorized 401 (Missing credentials)" with Passport JWT
**Frequency**: HIGH | **Complexity**: LOW
**Real Example**: SO 74763077
JWT authentication debugging:
1. Verify Authorization header format: "Bearer [token]"
2. Check token expiration (use longer exp for testing)
3. Test without nginx/proxy to isolate issue
4. Use jwt.io to decode and verify token structure

### 12. Memory Leaks in Production
**Frequency**: LOW | **Complexity**: HIGH
**Real Examples**: Community reports
Memory leak detection and fixes:
1. Profile with node --inspect and Chrome DevTools
2. Remove event listeners in onModuleDestroy()
3. Close database connections properly
4. Monitor heap snapshots over time

### 13. "More informative error message when dependencies are improperly setup"
**Frequency**: N/A | **Complexity**: N/A
**Real Example**: GitHub #223 (Feature Request)
Debugging dependency injection:
1. NestJS errors are intentionally generic for security
2. Use verbose logging during development
3. Add custom error messages in your providers
4. Consider using dependency injection debugging tools

### 14. Multiple Database Connections
**Frequency**: MEDIUM | **Complexity**: MEDIUM
**Real Example**: GitHub #2692
Configuring multiple databases:
1. Use named connections in TypeOrmModule
2. Specify connection name in @InjectRepository()
3. Configure separate connection options
4. Test each connection independently

### 15. "Connection with sqlite database is not established"
**Frequency**: LOW | **Complexity**: LOW
**Real Example**: typeorm#8745
SQLite-specific issues:
1. Check database file path is absolute
2. Ensure directory exists before connection
3. Verify file permissions
4. Use synchronize: true for development

### 16. Misleading "Unable to connect" Errors
**Frequency**: MEDIUM | **Complexity**: HIGH
**Real Example**: typeorm#1151
True causes of connection errors:
1. Entity syntax errors show as connection errors
2. Wrong decorator usage: @Column() not @Column('description')
3. Missing decorators on entity properties
4. Always check entity files when connection errors occur

### 17. "Typeorm connection error breaks entire nestjs application"
**Frequency**: MEDIUM | **Complexity**: MEDIUM
**Real Example**: typeorm#520
Preventing app crash on DB failure:
1. Wrap connection in try-catch in useFactory
2. Allow app to start without database
3. Implement health checks for DB status
4. Use retryAttempts and retryDelay options

## Common Patterns & Solutions

### Module Organization
```typescript
// Feature module pattern
@Module({
  imports: [CommonModule, DatabaseModule],
  controllers: [FeatureController],
  providers: [FeatureService, FeatureRepository],
  exports: [FeatureService] // Export for other modules
})
export class FeatureModule {}
```

### Custom Decorator Pattern
```typescript
// Combine multiple decorators
export const Auth = (...roles: Role[]) => 
  applyDecorators(
    UseGuards(JwtAuthGuard, RolesGuard),
    Roles(...roles),
  );
```

### Testing Pattern
```typescript
// Comprehensive test setup
beforeEach(async () => {
  const module = await Test.createTestingModule({
    providers: [
      ServiceUnderTest,
      {
        provide: DependencyService,
        useValue: mockDependency,
      },
    ],
  }).compile();
  
  service = module.get<ServiceUnderTest>(ServiceUnderTest);
});
```

### Exception Filter Pattern
```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    // Custom error handling
  }
}
```

## Code Review Checklist

When reviewing Nest.js applications, focus on:

### Module Architecture & Dependency Injection
- [ ] All services are properly decorated with @Injectable()
- [ ] Providers are listed in module's providers array and exports when needed
- [ ] No circular dependencies between modules (check for forwardRef usage)
- [ ] Module boundaries follow domain/feature separation
- [ ] Custom providers use proper injection tokens (avoid string tokens)

### Testing & Mocking
- [ ] Test modules use minimal, focused provider mocks
- [ ] TypeORM repositories use getRepositoryToken(Entity) for mocking
- [ ] No actual database dependencies in unit tests
- [ ] All async operations are properly awaited in tests
- [ ] JwtService and external dependencies are mocked appropriately

### Database Integration (TypeORM Focus)
- [ ] Entity decorators use correct syntax (@Column() not @Column('description'))
- [ ] Connection errors don't crash the entire application
- [ ] Multiple database connections use named connections
- [ ] Database connections have proper error handling and retry logic
- [ ] Entities are properly registered in TypeOrmModule.forFeature()

### Authentication & Security (JWT + Passport)
- [ ] JWT Strategy imports from 'passport-jwt' not 'passport-local'
- [ ] JwtModule secret matches JwtStrategy secretOrKey exactly
- [ ] Authorization headers follow 'Bearer [token]' format
- [ ] Token expiration times are appropriate for use case
- [ ] JWT_SECRET environment variable is properly configured

### Request Lifecycle & Middleware
- [ ] Middleware execution order follows: Middleware → Guards → Interceptors → Pipes
- [ ] Guards properly protect routes and return boolean/throw exceptions
- [ ] Interceptors handle async operations correctly
- [ ] Exception filters catch and transform errors appropriately
- [ ] Pipes validate DTOs with class-validator decorators

### Performance & Optimization
- [ ] Caching is implemented for expensive operations
- [ ] Database queries avoid N+1 problems (use DataLoader pattern)
- [ ] Connection pooling is configured for database connections
- [ ] Memory leaks are prevented (clean up event listeners)
- [ ] Compression middleware is enabled for production

## Decision Trees for Architecture

### Choosing Database ORM
```
Project Requirements:
├─ Need migrations? → TypeORM or Prisma
├─ NoSQL database? → Mongoose
├─ Type safety priority? → Prisma
├─ Complex relations? → TypeORM
└─ Existing database? → TypeORM (better legacy support)
```

### Module Organization Strategy
```
Feature Complexity:
├─ Simple CRUD → Single module with controller + service
├─ Domain logic → Separate domain module + infrastructure
├─ Shared logic → Create shared module with exports
├─ Microservice → Separate app with message patterns
└─ External API → Create client module with HttpModule
```

### Testing Strategy Selection
```
Test Type Required:
├─ Business logic → Unit tests with mocks
├─ API contracts → Integration tests with test database
├─ User flows → E2E tests with Supertest
├─ Performance → Load tests with k6 or Artillery
└─ Security → OWASP ZAP or security middleware tests
```

### Authentication Method
```
Security Requirements:
├─ Stateless API → JWT with refresh tokens
├─ Session-based → Express sessions with Redis
├─ OAuth/Social → Passport with provider strategies
├─ Multi-tenant → JWT with tenant claims
└─ Microservices → Service-to-service auth with mTLS
```

### Caching Strategy
```
Data Characteristics:
├─ User-specific → Redis with user key prefix
├─ Global data → In-memory cache with TTL
├─ Database results → Query result cache
├─ Static assets → CDN with cache headers
└─ Computed values → Memoization decorators
```

## Performance Optimization

### Caching Strategies
- Use built-in cache manager for response caching
- Implement cache interceptors for expensive operations
- Configure TTL based on data volatility
- Use Redis for distributed caching

### Database Optimization
- Use DataLoader pattern for N+1 query problems
- Implement proper indexes on frequently queried fields
- Use query builder for complex queries vs. ORM methods
- Enable query logging in development for analysis

### Request Processing
- Implement compression middleware
- Use streaming for large responses
- Configure proper rate limiting
- Enable clustering for multi-core utilization

## External Resources

### Core Documentation
- [Nest.js Documentation](https://docs.nestjs.com)
- [Nest.js CLI](https://docs.nestjs.com/cli/overview)
- [Nest.js Recipes](https://docs.nestjs.com/recipes)

### Testing Resources
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Supertest](https://github.com/visionmedia/supertest)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

### Database Resources
- [TypeORM Documentation](https://typeorm.io)
- [Mongoose Documentation](https://mongoosejs.com)

### Authentication
- [Passport.js Strategies](http://www.passportjs.org)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

## Quick Reference Patterns

### Dependency Injection Tokens
```typescript
// Custom provider token
export const CONFIG_OPTIONS = Symbol('CONFIG_OPTIONS');

// Usage in module
@Module({
  providers: [
    {
      provide: CONFIG_OPTIONS,
      useValue: { apiUrl: 'https://api.example.com' }
    }
  ]
})
```

### Global Module Pattern
```typescript
@Global()
@Module({
  providers: [GlobalService],
  exports: [GlobalService],
})
export class GlobalModule {}
```

### Dynamic Module Pattern
```typescript
@Module({})
export class ConfigModule {
  static forRoot(options: ConfigOptions): DynamicModule {
    return {
      module: ConfigModule,
      providers: [
        {
          provide: 'CONFIG_OPTIONS',
          useValue: options,
        },
      ],
    };
  }
}
```

## Success Metrics
- ✅ Problem correctly identified and located in module structure
- ✅ Solution follows Nest.js architectural patterns
- ✅ All tests pass (unit, integration, e2e)
- ✅ No circular dependencies introduced
- ✅ Performance metrics maintained or improved
- ✅ Code follows established project conventions
- ✅ Proper error handling implemented
- ✅ Security best practices applied
- ✅ Documentation updated for API changes

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## performance-optimizer
*Identifies and fixes performance bottlenecks in code, databases, and APIs. Measures before and after to prove improvements.*

Risk: safe

# Performance Optimizer

Find and fix performance bottlenecks. Measure, optimize, verify. Make it fast.

## When to Use This Skill

- App is slow or laggy
- User complains about performance
- Page load times are high
- API responses are slow
- Database queries take too long
- User mentions "slow", "lag", "performance", or "optimize"

## The Optimization Process

### 1. Measure First

Never optimize without measuring:

```javascript
// Measure execution time
console.time('operation');
await slowOperation();
console.timeEnd('operation'); // operation: 2341ms
```

**What to measure:**
- Page load time
- API response time
- Database query time
- Function execution time
- Memory usage
- Network requests

### 2. Find the Bottleneck

Use profiling tools to find the slow parts:

**Browser:**
```
DevTools → Performance tab → Record → Stop
Look for long tasks (red bars)
```

**Node.js:**
```bash
node --prof app.js
node --prof-process isolate-*.log > profile.txt
```

**Database:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### 3. Optimize

Fix the slowest thing first (biggest impact).

## Common Optimizations

### Database Queries

**Problem: N+1 Queries**
```javascript
// Bad: N+1 queries
const users = await db.users.find();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N queries
}

// Good: Single query with JOIN
const users = await db.users.find()
  .populate('posts'); // 1 query
```

**Problem: Missing Index**
```sql
-- Check slow query
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Shows: Seq Scan (bad)

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Check again
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Shows: Index Scan (good)
```

**Problem: SELECT ***
```javascript
// Bad: Fetches all columns
const users = await db.query('SELECT * FROM users');

// Good: Only needed columns
const users = await db.query('SELECT id, name, email FROM users');
```

**Problem: No Pagination**
```javascript
// Bad: Returns all records
const users = await db.users.find();

// Good: Paginated
const users = await db.users.find()
  .limit(20)
  .skip((page - 1) * 20);
```

### API Performance

**Problem: No Caching**
```javascript
// Bad: Hits database every time
app.get('/api/stats', async (req, res) => {
  const stats = await db.stats.calculate(); // Slow
  res.json(stats);
});

// Good: Cache for 5 minutes
const cache = new Map();
app.get('/api/stats', async (req, res) => {
  const cached = cache.get('stats');
  if (cached && Date.now() - cached.time < 300000) {
    return res.json(cached.data);
  }
  
  const stats = await db.stats.calculate();
  cache.set('stats', { data: stats, time: Date.now() });
  res.json(stats);
});
```

**Problem: Sequential Operations**
```javascript
// Bad: Sequential (slow)
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
// Total: 300ms + 200ms + 150ms = 650ms

// Good: Parallel (fast)
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
// Total: max(300ms, 200ms, 150ms) = 300ms
```

**Problem: Large Payloads**
```javascript
// Bad: Returns everything
res.json(users); // 5MB response

// Good: Only needed fields
res.json(users.map(u => ({
  id: u.id,
  name: u.name,
  email: u.email
}))); // 500KB response
```

### Frontend Performance

**Problem: Unnecessary Re-renders**
```javascript
// Bad: Re-renders on every parent update
function UserList({ users }) {
  return users.map(user => <UserCard user={user} />);
}

// Good: Memoized
const UserCard = React.memo(({ user }) => {
  return <div>{user.name}</div>;
});
```

**Problem: Large Bundle**
```javascript
// Bad: Imports entire library
import _ from 'lodash'; // 70KB

// Good: Import only what you need
import debounce from 'lodash/debounce'; // 2KB
```

**Problem: No Code Splitting**
```javascript
// Bad: Everything in one bundle
import HeavyComponent from './HeavyComponent';

// Good: Lazy load
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

**Problem: Unoptimized Images**
```html
<!-- Bad: Large image -->
<img src="photo.jpg" /> <!-- 5MB -->

<!-- Good: Optimized and responsive -->
<img 
  src="photo-small.webp" 
  srcset="photo-small.webp 400w, photo-large.webp 800w"
  loading="lazy"
  width="400"
  height="300"
/> <!-- 50KB -->
```

### Algorithm Optimization

**Problem: Inefficient Algorithm**
```javascript
// Bad: O(n²) - nested loops
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// Good: O(n) - single pass with Set
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return Array.from(duplicates);
}
```

**Problem: Repeated Calculations**
```javascript
// Bad: Calculates every time
function getTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
// Called 100 times in render

// Good: Memoized
const getTotal = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}, [items]);
```

### Memory Optimization

**Problem: Memory Leak**
```javascript
// Bad: Event listener not cleaned up
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  // Memory leak!
}, []);

// Good: Cleanup
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**Problem: Large Data in Memory**
```javascript
// Bad: Loads entire file into memory
const data = fs.readFileSync('huge-file.txt'); // 1GB

// Good: Stream it
const stream = fs.createReadStream('huge-file.txt');
stream.on('data', chunk => process(chunk));
```

## Measuring Impact

Always measure before and after:

```javascript
// Before optimization
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 2341ms

// After optimization (added index)
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 23ms

// Improvement: 100x faster!
```

## Performance Budgets

Set targets:

```
Page Load: < 2 seconds
API Response: < 200ms
Database Query: < 50ms
Bundle Size: < 200KB
Time to Interactive: < 3 seconds
```

## Tools

**Browser:**
- Chrome DevTools Performance tab
- Lighthouse (audit)
- Network tab (waterfall)

**Node.js:**
- `node --prof` (profiling)
- `clinic` (diagnostics)
- `autocannon` (load testing)

**Database:**
- `EXPLAIN ANALYZE` (query plans)
- Slow query log
- Database profiler

**Monitoring:**
- New Relic
- Datadog
- Sentry Performance

## Quick Wins

Easy optimizations with big impact:

1. **Add database indexes** on frequently queried columns
2. **Enable gzip compression** on server
3. **Add caching** for expensive operations
4. **Lazy load** images and heavy components
5. **Use CDN** for static assets
6. **Minify and compress** JavaScript/CSS
7. **Remove unused dependencies**
8. **Use pagination** instead of loading all data
9. **Optimize images** (WebP, proper sizing)
10. **Enable HTTP/2** on server

## Optimization Checklist

- [ ] Measured current performance
- [ ] Identified bottleneck
- [ ] Applied optimization
- [ ] Measured improvement
- [ ] Verified functionality still works
- [ ] No new bugs introduced
- [ ] Documented the change

## When NOT to Optimize

- Premature optimization (optimize when it's actually slow)
- Micro-optimizations (save 1ms when page takes 5 seconds)
- Readable code is more important than tiny speed gains
- If it's already fast enough

## Key Principles

- Measure before optimizing
- Fix the biggest bottleneck first
- Measure after to prove improvement
- Don't sacrifice readability for tiny gains
- Profile in production-like environment
- Consider the 80/20 rule (20% of code causes 80% of slowness)

## Related Skills

- `@database-design` - Query optimization
- `@codebase-audit-pre-push` - Code review
- `@bug-hunter` - Debugging

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## python-pptx-generator
*Generate complete Python scripts that build polished PowerPoint decks with python-pptx and real slide content.*

Tags: [python, powerpoint, python-pptx, presentations, slide-decks]
Tools: [claude, cursor, gemini, codex]
Risk: safe

# Python PPTX Generator

## Overview

Use this skill when the user wants a ready-to-run Python script that creates a PowerPoint presentation with `python-pptx`.
It focuses on turning a topic brief into a complete slide deck script with real slide content, sensible structure, and a working save step.

## When to Use This Skill

- Use when the user wants a Python script that generates a `.pptx` file automatically
- Use when the user needs slide content drafted and encoded directly into `python-pptx`
- Use when the user wants a quick presentation generator for demos, classes, or internal briefings

## How It Works

### Step 1: Collect the Deck Brief

Ask for the topic, audience, tone, and target number of slides if the request does not already include them.
If constraints are missing, pick conservative defaults and state them in the generated script comments.

### Step 2: Plan the Narrative Arc

Outline the deck before writing code:

1. Title slide
2. Agenda or context
3. Core teaching or business points
4. Summary or next steps

Keep the slide count realistic for the requested audience and avoid filler slides.

### Step 3: Generate the Python Script

Write a complete script that:

- imports `Presentation` from `python-pptx`
- creates the deck
- selects appropriate built-in layouts
- writes real titles and bullet points
- saves the file with a clear filename
- prints a success message after saving

### Step 4: Keep the Output Runnable

The final answer should be a Python code block that can run after installing `python-pptx`.
Avoid pseudocode, placeholders, or missing imports.

## Examples

### Example 1: Educational Deck

```text
User: Create a 5-slide presentation on the basics of machine learning for a high school class.
Output: A complete Python script that creates a title slide, overview, core concepts, examples, and recap.
```

### Example 2: Business Briefing

```text
User: Generate a 7-slide deck for sales leadership on Q2 pipeline risks and mitigation options.
Output: A python-pptx script with executive-friendly slide titles, concise bullets, and a final recommendations slide.
```

## Best Practices

- ✅ Use standard `python-pptx` layouts unless the user asks for custom positioning
- ✅ Write audience-appropriate bullet points instead of placeholders
- ✅ Save the output file explicitly in the script, for example `output.pptx`
- ✅ Keep slide titles short and the bullet hierarchy readable
- ❌ Do not return partial snippets that require the user to assemble the rest
- ❌ Do not invent unsupported styling APIs without checking `python-pptx` capabilities

## Security & Safety Notes

- Install `python-pptx` only in an environment you control, for example a local virtual environment
- If the user will run the script on a shared machine, choose a safe output path and avoid overwriting existing presentations without confirmation
- If the request includes proprietary or sensitive presentation content, keep it out of public examples and sample filenames

## Common Pitfalls

- **Problem:** The generated script uses placeholder text instead of real content  
  **Solution:** Draft the narrative first, then turn each slide into specific titles and bullets

- **Problem:** The deck uses too many slides for the requested audience  
  **Solution:** Compress the outline to the most important 4 to 8 slides unless the user explicitly wants a longer deck

- **Problem:** The script forgets to save or print a completion message  
  **Solution:** Always end with `prs.save(...)` and a short success print

## Related Skills

- `@pptx-official` - Use when the task is about inspecting or editing existing PowerPoint files
- `@docx-official` - Use when the requested output should be a document instead of a slide deck

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## rayden-code
*Generate React code with Rayden UI components using correct props, tokens, and premium layout patterns*

Tags: react, tailwind, design-system, ui, components, vibe-coding, rayden, rayna-ui, code-generation
Tools: Read, Write, Edit, Bash, Glob, Grep
Risk: safe

# Rayden Code Skill

## Overview

Generate production-quality React + Tailwind CSS code using the Rayden UI component library (34 components). The skill loads a complete API reference with every component, every prop, design tokens, layout patterns, and an explicit anti-pattern ban list — preventing hallucinated components and generic AI output. Built on the Rayna UI design system.

## When to Use This Skill

- You're building a new page or feature using Rayden UI components
- You want to scaffold a dashboard, landing page, auth screen, settings page, or data table
- You need to generate React code that follows a specific design system precisely
- You want to prototype UI quickly with correct component usage and premium aesthetics
- You're vibe coding and want design-system-compliant output

## How It Works

1. **Parses the request** — Identifies page type, required components, and data model
2. **Loads RAYDEN_RULES.md** — Complete reference: 34 components with full props, design philosophy, token classes, layout patterns, anti-patterns, and accessibility rules
3. **Plans the layout** — Decides page structure, component selection, spacing, color, and elevation strategy
4. **Generates code** — Writes React + Tailwind CSS using only documented components and token classes
5. **Self-validates** — Runs a 16-point checklist covering correctness (valid components/props, token usage, nesting) and design quality (whitespace, hierarchy, restraint, responsiveness)

## Examples

### Vibe code a SaaS dashboard

```
/rayden-code a dashboard with KPI cards, a recent orders table, and an activity feed
```

**Use case:** You're building an internal analytics tool and need a full dashboard page with MetricsCard grid, sortable Table, and ActivityFeed sidebar — all with correct Rayden imports and token classes.

### Scaffold a login page

```
/rayden-code login page with email and password
```

**Use case:** You need a centered auth form with Input components, a primary Button, and proper visual hierarchy — following Rayden's "Auth / Focused Form" pattern.

### Build an admin settings page

```
/rayden-code settings page with profile section, notification toggles, and danger zone
```

**Use case:** You're adding a settings area to your app and need form sections with Toggle components, a destructive action zone, and a single-column constrained layout.

### Create a pricing page

```
/rayden-code pricing page with 3 tiers and a feature comparison table
```

**Use case:** You need a marketing pricing section with Card components for each tier, Badge for the recommended plan, and a Table for feature comparison.

### Build an e-commerce product grid

```
/rayden-code product catalog with filters, search, and a card grid
```

**Use case:** You're building a storefront and need a responsive product grid with Chip filters, Input search, Pagination, and Cards with images — all using Rayden's layout and spacing rules.

## Best Practices

- Describe what you want in plain language — the skill maps your request to the right components
- Install `@raydenui/ui` in your project first (`npm install @raydenui/ui`)
- Import `@raydenui/ui/styles.css` in your app entry point for design tokens to work
- Review generated code for business logic — the skill handles UI, not data fetching
- Use alongside `/rayden-use` if you also want the same design built in Figma

## Security & Safety Notes

- This skill only reads its bundled rules file and writes code to your project
- No external network requests
- No secrets or credentials involved
- Generated code uses standard React patterns with no eval or dynamic code execution

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Components not rendering correctly | Ensure `@raydenui/ui/styles.css` is imported in your app entry |
| "Component doesn't exist" error | The skill only uses documented components — check if you're asking for something Rayden doesn't have |
| Colors look wrong | Use token classes (`bg-primary-500`) not hex values. Ensure the Rayden CSS is loaded |
| Layout not responsive | The skill generates responsive code by default — check that your viewport meta tag is set |

## Related Skills

- `rayden-use` — Build Rayden UI components and screens in Figma via MCP (included in the same package)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## recsys-pipeline-architect
*Designs composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework*

Tags: [recommender-system, ranking, feed-algorithm, recsys, personalization, for-you-feed, rag-reranker, pipeline-architecture]
Tools: [claude, codex, cursor, gemini, opencode, cline, continue, windsurf]
Risk: safe

# recsys-pipeline-architect

## Overview

A spec-and-scaffold skill for building composable recommendation, ranking, and feed pipelines. It encodes the six-stage **Source → Hydrator → Filter → Scorer → Selector → SideEffect** framework popularized by xAI's open-sourced [For You algorithm](https://github.com/xai-org/x-algorithm) (Apache 2.0). This skill is an independent reimplementation of the *pattern* — no code is copied from the original — licensed MIT. Use it whenever you need "the top K items for a (user, context)": social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking.

## When to Use This Skill

- Use when the user wants to build any system that picks "the top K items for a user/context"
- Use when the user asks "how should I rank X" or describes a feed/personalization problem
- Use when the user has a scoring function and needs the pipeline plumbing around it
- Use when the user wants to migrate from a single relevance score to multi-action prediction with tunable weights
- Use when the user is wrapping an LLM/ML scorer and needs filters, hydrators, side-effects, and a runnable scaffold in their stack (TypeScript / Go / Python)

## How It Works

### Step 1: Clarify the use case

Ask the user three questions (only what is missing):

1. What are the items being ranked? (posts, products, tasks, alerts, documents...)
2. What is the input context? (user ID, search query, current document, time window...)
3. What language / runtime? (TypeScript/Node, Go, Python, Rust...)

### Step 2: Walk the eight steps of the spec

The full SKILL walks through: clarify use case → identify candidate sources → list required hydrations → list filters → design scorer chain → selector → side effects → generate scaffold. Each step surfaces the architectural trade-offs (multi-action vs single-score, candidate isolation vs joint scoring, online vs offline batch) so the user makes them explicitly rather than defaulting silently.

### Step 3: Emit a runnable scaffold

The upstream repository ships three runnable example scaffolds — every one green on its test suite:

- **Strapi v5 plugin** (TypeScript, Jest, 3/3 pass) — adds `GET /api/feed/for-you` with multi-action scoring and author diversity
- **Zentra-compatible pipeline** (Go with generics, 3/3 pass) — engine.Module-compatible, standalone-usable
- **PMAI task prioritizer** (Python / FastAPI / pytest, 3/3 pass) — `GET /tasks/next?user_id=42&limit=10`

When the user's stack doesn't match, the skill generates from scratch following the interface definitions in `references/interfaces.md` (TypeScript, Go, Python, Rust).

## Examples

### Example 1: Strapi content feed

User: "I'm running a Strapi v5 instance with 50k articles. I want a 'for you' feed personalized to each logged-in user based on their reading history."

Skill walks through the 8 steps, generates a Strapi plugin scaffold using the Strapi example as the template.

### Example 2: RAG retrieval reranker

User: "My RAG returns top-50 chunks from a vector DB. I want to rerank them with a more expensive scorer and return top-5."

Skill recognizes this as a single-source pipeline with a scorer chain (cheap retrieval + expensive rerank). Generates a Python async pipeline.

### Example 3: Notification triage

User: "We send too many notifications. I want a daily digest that picks the top 10 from the last 24h queue."

Skill identifies this as an offline-batch pipeline. Generates a scheduled job scaffold.

## Best Practices

- ✅ Surface the multi-action vs single-score trade-off explicitly — don't default silently
- ✅ Order filters by cost (cheap before expensive); universal filters before user-specific
- ✅ Wrap side effects in fire-and-forget patterns (goroutines / promises without await / asyncio tasks) — never block the response
- ✅ Keep scoring deterministic and cacheable; do diversity reranking as a separate stage
- ✅ Attribute the pattern as "popularized by xAI's open-sourced For You algorithm" when generating output
- ❌ Don't invent benchmark or latency numbers — say "depends on workload, run it yourself"
- ❌ Don't name the user's generated artifact "X-like" or use "For You" branding — the pattern is free, the brand is not
- ❌ Don't conflate this with model architecture: this skill is pipeline plumbing *around* the scorer, not the scorer itself

## Limitations

- This skill scaffolds pipeline plumbing; it does not train ML models — the scoring function is the user's responsibility
- It does not operate deployed pipelines (no monitoring, no autoscaling decisions)
- It does not predict pipeline performance (depends on data, hardware, traffic)
- It does not choose infrastructure (vector DB, cache, queue) — those are outside scope

## Security & Safety Notes

- The generated scaffolds are framework code, not application logic — no shell commands, no network fetches, no credential handling
- Filters in the generated cookbook include eligibility/paywall/geo-restriction checks; the skill recommends putting these *before* scoring (so blocked content is never scored)
- Side-effect stages are always async / fire-and-forget; the skill documents this explicitly in the generated README to prevent users from accidentally blocking the response with cache writes or event emissions

## Common Pitfalls

- **Problem:** Single-score model gets overfit to one metric (clicks) and degrades on others (long sessions, retention)
  **Solution:** Skill recommends multi-action prediction with tunable weights — change behavior by changing weights, no retraining

- **Problem:** Joint scoring (transformer over the whole batch) is non-deterministic and uncacheable
  **Solution:** Skill defaults to candidate isolation via attention masking; recommends joint only when there's a specific reason (e.g., batch-aware diversity)

- **Problem:** Side effects (cache writes, impression emits) block the response
  **Solution:** Skill generates fire-and-forget patterns and documents the constraint

## Upstream

This skill is a thin adapter to the upstream repository. For the full SKILL.md content, 5 reference documents (interfaces in 4 languages, multi-action scoring, candidate isolation, filter cookbook, scorer cookbook), and 3 runnable example scaffolds with passing test suites:

- **Repository:** https://github.com/mturac/recsys-pipeline-architect
- **Release:** v0.1.0
- **Install via skills.sh:** `npx skills add mturac/recsys-pipeline-architect`
- **Pattern source:** https://github.com/xai-org/x-algorithm (Apache 2.0; this skill is MIT)

---

## redesign-existing-projects
*Use when upgrading existing websites or apps by auditing generic UI patterns and applying premium design fixes without rewrites.*

Tags: [frontend, redesign, design-audit, ui]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# Redesign Skill

## When to Use

- Use when the user asks to redesign, restyle, modernize, polish, or improve an existing website or app UI.
- Use when the task is to audit current frontend code and make targeted visual improvements without changing the product architecture.
- Use when the design feels generic, AI-generated, poorly spaced, visually flat, or missing responsive, interactive, loading, empty, or error states.

## Limitations

- This skill upgrades existing UI but does not authorize framework migrations, information-architecture rewrites, or product-scope expansion by default.
- Preserve working behavior, routing, data flows, accessibility semantics, and tests while making visual changes.
- Validate redesigned screens in the actual app across supported browsers and viewport sizes before considering the work complete.


## How This Works

When applied to an existing project, follow this sequence:

1. **Scan** — Read the codebase. Identify the framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state you find.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.

## Design Audit

### Typography

Check for these problems and fix them:

- **Browser default fonts or Inter everywhere.** Replace with a font that has character. Good options: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. For editorial/creative projects, pair a serif header with a sans-serif body.
- **Headlines lack presence.** Increase size for display text, tighten letter-spacing, reduce line-height. Headlines should feel heavy and intentional.
- **Body text too wide.** Limit paragraph width to roughly 65 characters. Increase line-height for readability.
- **Only Regular (400) and Bold (700) weights used.** Introduce Medium (500) and SemiBold (600) for more subtle hierarchy.
- **Numbers in proportional font.** Use a monospace font or enable tabular figures (`font-variant-numeric: tabular-nums`) for data-heavy interfaces.
- **Missing letter-spacing adjustments.** Use negative tracking for large headers, positive tracking for small caps or labels.
- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps instead.
- **Orphaned words.** Single words sitting alone on the last line. Fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces

- **Pure `#000000` background.** Replace with off-black, dark charcoal, or tinted dark (`#0a0a0a`, `#121212`, or a dark navy).
- **Oversaturated accent colors.** Keep saturation below 80%. Desaturate accents so they blend with neutrals instead of screaming.
- **More than one accent color.** Pick one. Remove the rest. Consistency beats variety.
- **Mixing warm and cool grays.** Stick to one gray family. Tint all grays with a consistent hue (warm or cool, not both).
- **Purple/blue "AI gradient" aesthetic.** This is the most common AI design fingerprint. Replace with neutral bases and a single, considered accent.
- **Generic `box-shadow`.** Tint shadows to match the background hue. Use colored shadows (e.g., dark blue shadow on a blue background) instead of pure black at low opacity.
- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns to backgrounds. Pure flat vectors feel sterile.
- **Perfectly even gradients.** Break the uniformity with radial gradients, noise overlays, or mesh gradients instead of standard linear 45-degree fades.
- **Inconsistent lighting direction.** Audit all shadows to ensure they suggest a single, consistent light source.
- **Random dark sections in a light mode page (or vice versa).** A single dark-background section breaking an otherwise light page looks like a copy-paste accident. Either commit to a full dark mode or keep a consistent background tone throughout. If contrast is needed, use a slightly darker shade of the same palette — not a sudden jump to `#111` in the middle of a cream page.
- **Empty, flat sections with no visual depth.** Sections that are just text on a plain background feel unfinished. Add high-quality background imagery (blurred, overlaid, or masked), subtle patterns, or ambient gradients. Use reliable placeholder sources like `https://picsum.photos/seed/{name}/1920/1080` when real assets are not available. Experiment with background images behind hero sections, feature blocks, or CTAs — even a subtle full-width photo at low opacity adds presence.

### Layout

- **Everything centered and symmetrical.** Break symmetry with offset margins, mixed aspect ratios, or left-aligned headers over centered content.
- **Three equal card columns as feature row.** This is the most generic AI layout. Replace with a 2-column zig-zag, asymmetric grid, horizontal scroll, or masonry layout.
- **Using `height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh` to prevent layout jumping on mobile browsers (iOS Safari viewport bug).
- **Complex flexbox percentage math.** Replace with CSS Grid for reliable multi-column structures.
- **No max-width container.** Add a container constraint (around 1200-1440px) with auto margins so content doesn't stretch edge-to-edge on wide screens.
- **Cards of equal height forced by flexbox.** Allow variable heights or use masonry when content varies in length.
- **Uniform border-radius on everything.** Vary the radius: tighter on inner elements, softer on containers.
- **No overlap or depth.** Elements sit flat next to each other. Use negative margins to create layering and visual depth.
- **Symmetrical vertical padding.** Top and bottom padding are always identical. Adjust optically — bottom padding often needs to be slightly larger.
- **Dashboard always has a left sidebar.** Try top navigation, a floating command menu, or a collapsible panel instead.
- **Missing whitespace.** Double the spacing. Let the design breathe. Dense layouts work for data dashboards, not for marketing pages.
- **Buttons not bottom-aligned in card groups.** When cards have different content lengths, CTAs end up at random heights. Pin buttons to the bottom of each card so they form a clean horizontal line regardless of content above.
- **Feature lists starting at different vertical positions.** In pricing tables or comparison cards, the list of features should start at the same Y position across all columns. Use consistent spacing above the list or fixed-height title/price blocks.
- **Inconsistent vertical rhythm in side-by-side elements.** When placing cards, columns, or panels next to each other, align shared elements (titles, descriptions, prices, buttons) across all items. Misaligned baselines make the layout look broken.
- **Mathematical alignment that looks optically wrong.** Centering by the math doesn't always look centered to the eye. Icons next to text, play buttons in circles, or text in buttons often need 1-2px optical adjustments to feel right.

### Interactivity and States

- **No hover states on buttons.** Add background shift, slight scale, or translate on hover.
- **No active/pressed feedback.** Add a subtle `scale(0.98)` or `translateY(1px)` on press to simulate a physical click.
- **Instant transitions with zero duration.** Add smooth transitions (200-300ms) to all interactive elements.
- **Missing focus ring.** Ensure visible focus indicators for keyboard navigation. This is an accessibility requirement, not optional.
- **No loading states.** Replace generic circular spinners with skeleton loaders that match the layout shape.
- **No empty states.** An empty dashboard showing nothing is a missed opportunity. Design a composed "getting started" view.
- **No error states.** Add clear, inline error messages for forms. Do not use `window.alert()`.
- **Dead links.** Buttons that link to `#`. Either link to real destinations or visually disable them.
- **No indication of current page in navigation.** Style the active nav link differently so users know where they are.
- **Scroll jumping.** Anchor clicks jump instantly. Add `scroll-behavior: smooth`.
- **Animations using `top`, `left`, `width`, `height`.** Switch to `transform` and `opacity` for GPU-accelerated, smooth animation.

### Content

- **Generic names like "John Doe" or "Jane Smith".** Use diverse, realistic-sounding names.
- **Fake round numbers like `99.99%`, `50%`, `$100.00`.** Use organic, messy data: `47.2%`, `$99.00`, `+1 (312) 847-1928`.
- **Placeholder company names like "Acme Corp", "Nexus", "SmartFlow".** Invent contextual, believable brand names.
- **AI copywriting cliches.** Never use "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", or "In the world of...". Write plain, specific language.
- **Exclamation marks in success messages.** Remove them. Be confident, not loud.
- **"Oops!" error messages.** Be direct: "Connection failed. Please try again."
- **Passive voice.** Use active voice: "We couldn't save your changes" instead of "Mistakes were made."
- **All blog post dates identical.** Randomize dates to appear real.
- **Same avatar image for multiple users.** Use unique assets for every distinct person.
- **Lorem Ipsum.** Never use placeholder latin text. Write real draft copy.
- **Title Case On Every Header.** Use sentence case instead.

### Component Patterns

- **Generic card look (border + shadow + white background).** Remove the border, or use only background color, or use only spacing. Cards should exist only when elevation communicates hierarchy.
- **Always one filled button + one ghost button.** Add text links or tertiary styles to reduce visual noise.
- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, or plain text labels.
- **Accordion FAQ sections.** Use a side-by-side list, searchable help, or inline progressive disclosure.
- **3-card carousel testimonials with dots.** Replace with a masonry wall, embedded social posts, or a single rotating quote.
- **Pricing table with 3 towers.** Highlight the recommended tier with color and emphasis, not just extra height.
- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections instead of popups for simple actions.
- **Avatar circles exclusively.** Try squircles or rounded squares for a less generic look.
- **Light/dark toggle always a sun/moon switch.** Use a dropdown, system preference detection, or integrate it into settings.
- **Footer link farm with 4 columns.** Simplify. Focus on main navigational paths and legally required links.

### Iconography

- **Lucide or Feather icons exclusively.** These are the "default" AI icon choice. Use Phosphor, Heroicons, or a custom set for differentiation.
- **Rocketship for "Launch", shield for "Security".** Replace cliche metaphors with less obvious icons (bolt, fingerprint, spark, vault).
- **Inconsistent stroke widths across icons.** Audit all icons and standardize to one stroke weight.
- **Missing favicon.** Always include a branded favicon.
- **Stock "diverse team" photos.** Use real team photos, candid shots, or a consistent illustration style instead of uncanny stock imagery.

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Inline styles mixed with CSS classes.** Move all styling to the project's styling system.
- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `em`, `max-width`) for flexible layouts.
- **Missing alt text on images.** Describe image content for screen readers. Never leave `alt=""` or `alt="image"` on meaningful images.
- **Arbitrary z-index values like `9999`.** Establish a clean z-index scale in the theme/variables.
- **Commented-out dead code.** Remove all debug artifacts before shipping.
- **Import hallucinations.** Check that every import actually exists in `package.json` or the project dependencies.
- **Missing meta tags.** Add proper `<title>`, `description`, `og:image`, and social sharing meta tags.

### Strategic Omissions (What AI Typically Forgets)

- **No legal links.** Add privacy policy and terms of service links in the footer.
- **No "back" navigation.** Dead ends in user flows. Every page needs a way back.
- **No custom 404 page.** Design a helpful, branded "page not found" experience.
- **No form validation.** Add client-side validation for emails, required fields, and format checks.
- **No "skip to content" link.** Essential for keyboard users. Add a hidden skip-link.
- **No cookie consent.** If required by jurisdiction, add a compliant consent banner.

## Upgrade Techniques

When upgrading a project, pull from these high-impact techniques to replace generic patterns:

### Typography Upgrades
- **Variable font animation.** Interpolate weight or width on scroll or hover for text that feels alive.
- **Outlined-to-fill transitions.** Text starts as a stroke outline and fills with color on scroll entry or interaction.
- **Text mask reveals.** Large typography acting as a window to video or animated imagery behind it.

### Layout Upgrades
- **Broken grid / asymmetry.** Elements that deliberately ignore column structure — overlapping, bleeding off-screen, or offset with calculated randomness.
- **Whitespace maximization.** Aggressive use of negative space to force focus on a single element.
- **Parallax card stacks.** Sections that stick and physically stack over each other during scroll.
- **Split-screen scroll.** Two halves of the screen sliding in opposite directions.

### Motion Upgrades
- **Smooth scroll with inertia.** Decouple scrolling from browser defaults for a heavier, cinematic feel.
- **Staggered entry.** Elements cascade in with slight delays, combining Y-axis translation with opacity fade. Never mount everything at once.
- **Spring physics.** Replace linear easing with spring-based motion for a natural, weighty feel on all interactive elements.
- **Scroll-driven reveals.** Content entering through expanding masks, wipes, or draw-on SVG paths tied to scroll progress.

### Surface Upgrades
- **True glassmorphism.** Go beyond `backdrop-filter: blur`. Add a 1px inner border and a subtle inner shadow to simulate edge refraction.
- **Spotlight borders.** Card borders that illuminate dynamically under the cursor.
- **Grain and noise overlays.** A fixed, pointer-events-none overlay with subtle noise to break digital flatness.
- **Colored, tinted shadows.** Shadows that carry the hue of the background rather than using generic black.

## Fix Priority

Apply changes in this order for maximum visual impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Rules

- Work with the existing tech stack. Do not migrate frameworks or styling libraries.
- Do not break existing functionality. Test after every change.
- Before importing any new library, check the project's dependency file first.
- If the project uses Tailwind, check the version (v3 vs v4) before modifying config.
- If the project has no framework, use vanilla CSS.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.

---

## seek-and-analyze-video
*Seek and analyze video content using Memories.ai Large Visual Memory Model for persistent video intelligence*

Tags: [video, ai, memories, social-media, youtube, tiktok, analysis]
Tools: [claude, cursor, gemini]
Risk: safe

## When to Use
Use this skill when the user wants to search for, import, or analyze video content from TikTok, YouTube, or Instagram, summarize meetings or lectures from recordings, build a searchable knowledge base from video content, or research social media trends and creators.

# Seek and Analyze Video

## Description

This skill enables AI agents to search, import, and analyze video content using Memories.ai's Large Visual Memory Model (LVMM). Unlike one-shot video analysis tools, it provides persistent video intelligence -- videos are indexed once and can be queried repeatedly across sessions. Supports social media import (TikTok, YouTube, Instagram), meeting summarization, knowledge base building, and cross-video Q&A via Memory Augmented Generation (MAG).

## Overview

The skill wraps 21 API commands into workflow-oriented reference guides that agents load on demand. A routing table in SKILL.md maps user intent to the right workflow automatically.

## When to Use This Skill

- Use when analyzing or asking questions about a video from a URL
- Use when searching for videos on TikTok, YouTube, or Instagram by topic, hashtag, or creator
- Use when summarizing meetings, lectures, or webinars from recordings
- Use when building a searchable knowledge base from video content and text memories
- Use when researching social media content trends, influencers, or viral patterns
- Use when analyzing or describing images with AI vision

## How It Works

### Step 1: Intent Detection

The agent reads the SKILL.md workflow router and matches the user's request to one of 6 intent categories.

### Step 2: Reference Loading

The agent loads the appropriate reference file (e.g., video_qa.md for video questions, social_research.md for social media research).

### Step 3: Workflow Execution

The agent follows the step-by-step workflow: upload/import -> wait for processing -> analyze/chat -> present results.

## Examples

### Example 1: Video Q&A

```
User: "What are the key arguments in this video? https://youtube.com/watch?v=abc123"
Agent: uploads video -> waits for processing -> uses chat_video to ask questions -> presents structured summary
```

### Example 2: Social Media Research

```
User: "What's trending on TikTok about sustainable fashion?"
Agent: uses search_public to find trending videos -> imports top results -> analyzes content patterns
```

### Example 3: Meeting Notes

```
User: "Summarize this meeting recording and extract action items"
Agent: uploads recording -> waits -> gets transcript -> uses chat_video for structured summary with action items
```

## Best Practices

- Always wait for video processing to complete before querying
- Use caption_video for quick analysis (no upload needed)
- Use chat_video for deep, multi-turn analysis (requires upload)
- Use search_audio to find specific moments or quotes in a video
- Use memory_add to store important findings for later retrieval

## Common Pitfalls

- **Problem:** Querying a video before processing completes
  **Solution:** Always use the `wait` command after upload before any analysis

- **Problem:** Uploading a video when only a quick caption is needed
  **Solution:** Use `caption_video` for one-off analysis; only upload for repeated queries

## Limitations

- Video processing takes 1-5 minutes depending on length
- Free tier limited to 100 credits
- Social media import requires public content
- Audio search only works on processed videos

## Related Skills

- Video analysis tools for one-shot analysis
- Web search skills for non-video content research

---

## skill-check
*Validate Claude Code skills against the agentskills specification. Catches structural, semantic, and naming issues before users do.*

Tags: [validation, linter, agentskills, skill-authoring, code-quality]
Tools: [claude, cursor, windsurf, codex-cli]
Risk: safe

# SkillCheck

## Overview

Validate SKILL.md files against the [agentskills specification](https://agentskills.io) and Anthropic best practices. Catches structural errors, semantic contradictions, naming anti-patterns, and quality gaps in a single read-only pass.

## When to Use This Skill

- Use when user says "check skill", "skillcheck", or "validate SKILL.md"
- Use when reviewing a skill before publishing to a marketplace
- Use when debugging why a skill doesn't trigger correctly
- Use when onboarding a team to skill authoring standards
- Do NOT use for anti-slop detection, security scanning, or token analysis; use [SkillCheck Pro](https://getskillcheck.com) for those

## How It Works

### Step 1: Parse

Read the target SKILL.md file and extract YAML frontmatter.

### Step 2: Validate

Apply all Free tier checks in order:

| Category | Checks | What it catches |
|----------|--------|----------------|
| Structure (1.x) | Name format, description WHAT+WHEN, allowed-tools, categories, XML injection | Malformed frontmatter, missing fields |
| Body (2.x) | Line count, hardcoded paths, stale dates, empty sections, deprecated syntax, MCP tool qualification | Content quality issues |
| Naming (3.x) | Vague terms, single-word names, gerund suggestions | Poor discoverability |
| Semantic (4.x) | Contradictions, ambiguous terms, missing output format, wisdom/platitudes, misplaced triggers | Logical inconsistencies |
| Quality (8.x) | Examples, error handling, triggers, output format, prerequisites, negative triggers | Strengths (positive patterns) |

### Step 3: Score

Calculate overall score (0-100). Penalties: critical = -20, warning = -5, suggestion = -1.

### Step 4: Report

Return structured results: score, grade (Excellent/Good/Needs Work/Poor), issue list with check IDs, line numbers, messages, and fix suggestions.

## Examples

### Example 1: Validating a skill

```
User: check my skill at ~/.claude/skills/weekly-report/SKILL.md

SkillCheck output:
## weekly-report Check Results [FREE]

Score: 85/100 (Good)

### Warnings (2)
  - 1.2-desc-when (line 3): Description missing WHEN clause
  - 4.5-desc-no-triggers (line 3): Description lacks triggering conditions

### Suggestions (1)
  - 3.4-gerund-naming (line 2): Skill name could use gerund form

### Passed Checks: 28
```

### Example 2: Clean skill passes all checks

```
User: skillcheck ~/.claude/skills/processing-pdfs/SKILL.md

Score: 100/100 (Excellent)
All 31 checks passed. No issues found.
```

## Limitations

- Read-only: does not modify any files
- Free tier covers structural, semantic, and naming checks only
- Anti-slop, security, WCAG, token, enterprise, and workflow checks require [SkillCheck Pro](https://getskillcheck.com)
- Semantic checks (contradiction detection, wisdom/platitude) are heuristic with ~5% false positive rate
- Does not validate referenced files or scripts; only checks SKILL.md content
- Single-file validation; does not cross-check against other skills in the same directory

## Best Practices

- Run SkillCheck before submitting skills to any marketplace
- Fix all critical and warning issues; suggestions are optional
- Use the check ID (e.g., `1.2-desc-when`) to find the exact rule in the skill body
- Re-run after fixes to confirm the score improved

## Common Pitfalls

- **Problem:** Score seems low due to many suggestions
  **Solution:** Suggestions cap at -15 points total. Focus on warnings and criticals first.

- **Problem:** False positive on ambiguous terms inside code blocks
  **Solution:** SkillCheck skips code blocks and inline code. If you still see false positives, wrap the term in backticks.

- **Problem:** Wisdom/platitude check flags legitimate instructions
  **Solution:** Rephrase generic advice ("Remember that testing is important") as concrete directives ("Run tests before committing").

---

## squirrel
*Full-cycle AI coding skill: plans, builds, tests, lints, fixes bugs, and writes production-grade docs. Auto-detects project state and adapts its 8-phase pipeline.*

Tags: [development, testing, planning, code-review, documentation, ci-cd]
Tools: [claude, cursor, codex, antigravity, gemini, windsurf, opencode, copilot]
Risk: safe

# Squirrel — Full-Cycle Software Development Skill

## Overview

Squirrel is a full-cycle AI coding skill that works across 9 AI coding agents. It auto-detects project state (greenfield, in-progress, or mature) and adapts its 8-phase engineering pipeline accordingly. Instead of a one-size-fits-all workflow, it figures out where the project actually is and jumps in at exactly the right point.

## When to Use This Skill

- Use when starting a new project from scratch (greenfield)
- Use when improving an existing codebase (in-progress or mature)
- Use when fixing bugs, adding features, or refactoring
- Use when adding tests, linting, or CI/CD to a project
- Use when writing production-grade documentation
- Use when the user says "build me", "fix this", "squirrel this project", or any multi-step development task

## How It Works

### Step 0: Detect Mode

Squirrel classifies the project directory:

| Signal | Mode | Entry Point |
|--------|------|-------------|
| Empty directory | Greenfield | All 8 phases from scratch |
| Source files, no tests/docs | In-Progress | Audit first, then improve |
| Source + tests + CI + README | Mature | Targeted improvements |
| "fix this bug / add feature" | Targeted | Scoped work only |

### The 8-Phase Pipeline

1. **Discover** — Understand the project (audit existing code or gather requirements)
2. **Plan** — Concrete task list with dependencies and done-criteria
3. **Build** — Write or modify code (parallel sub-agents when supported)
4. **Test** — Run existing tests, write new ones, 70%+ coverage target
5. **Bug Hunt** — Static analysis + manual review
6. **Polish** — Lint, format, type check, remove dead code
7. **Document** — README + inline docs (update existing, don't overwrite)
8. **Ship** — Final checklist: tests green, no secrets, CI configured

### Failure Recovery (3-Strike Rule)

1. **Strike 1:** Fix the specific error. Run tests. Move on.
2. **Strike 2:** Re-read the code. Try a different approach.
3. **Strike 3:** STOP. Revert. Document what failed. Ask the user.

## Examples

### Example 1: Build a REST API

```text
> build me a REST API for a todo app with TypeScript and Express
```

Squirrel auto-detects greenfield mode and runs all 8 phases.

### Example 2: Fix a bug

```text
> fix this bug in src/auth/login.py
```

Squirrel enters targeted mode — abbreviated audit, scoped fix, verify.

### Example 3: Improve existing project

```text
> squirrel this project — add tests, fix lint errors, write README
```

Squirrel audits the existing codebase, then applies phases 4-8.

## Best Practices

- Respects existing code — matches naming conventions, test framework, import style, and architecture
- Reads 2-3 similar files before writing a new one
- Never suppresses type errors with `as any` or `@ts-ignore`
- Never deletes failing tests to "pass"
- Never leaves code in a broken state

## Platform Compatibility

Squirrel works on: Claude Code, Codex, Cursor, Antigravity, Gemini CLI, GitHub Copilot, Windsurf, OpenCode, Aider (9 total).

Install with:

```bash
# Universal installer
npx skills add flyingsquirrel0419/squirrel-skill

```

## Limitations

- Does not replace environment-specific validation or expert review
- CI/CD templates are starting points, not drop-in guarantees
- Parallel sub-agent execution depends on platform support

## Related Skills

- `@brainstorming` - For planning before implementation
- `@test-driven-development` - For TDD-oriented workflows
- `@systematic-debugging` - For methodical problem-solving

---

## stitch-design-taste
*Use when generating Google Stitch DESIGN.md systems for premium typography, color, layout, motion intent, and anti-generic UI rules.*

Tags: [stitch, design-system, frontend, ui]
Tools: [claude, cursor, codex, antigravity]
Risk: safe

# Stitch Design Taste — Semantic Design System Skill

## When to Use

- Use when the user wants a Google Stitch-compatible DESIGN.md or semantic design system for AI screen generation.
- Use when translating premium frontend taste rules into Stitch-friendly visual descriptions, color roles, typography specs, and component behavior.
- Use when the design system must prevent generic AI UI patterns before screens are generated.

## Limitations

- This skill produces semantic design-system guidance for Stitch; it does not guarantee Stitch will render every constraint exactly.
- Generated `DESIGN.md` files still require review against the actual product brief, brand constraints, accessibility needs, and screen content.
- Motion sections document implementation intent for later coding agents because Stitch itself may generate static screens.


## Overview
This skill generates `DESIGN.md` files optimized for Google Stitch screen generation. It translates the battle-tested anti-slop frontend engineering directives into Stitch's native semantic design language — descriptive, natural-language rules paired with precise values that Stitch's AI agent can interpret to produce premium, non-generic interfaces.

The generated `DESIGN.md` serves as the **single source of truth** for prompting Stitch to generate new screens that align with a curated, high-agency design language. Stitch interprets design through **"Visual Descriptions"** supported by specific color values, typography specs, and component behaviors.

## Prerequisites
- Access to Google Stitch via [labs.google.com/stitch](https://labs.google.com/stitch)
- Optionally: Stitch MCP Server for programmatic integration with Cursor, Antigravity, or Gemini CLI

## The Goal
Generate a `DESIGN.md` file that encodes:
1. **Visual atmosphere** — the mood, density, and design philosophy
2. **Color calibration** — neutrals, accents, and banned patterns with hex codes
3. **Typographic architecture** — font stacks, scale hierarchy, and anti-patterns
4. **Component behaviors** — buttons, cards, inputs with interaction states
5. **Layout principles** — grid systems, spacing philosophy, responsive strategy
6. **Motion philosophy** — animation engine specs, spring physics, perpetual micro-interactions
7. **Anti-patterns** — explicit list of banned AI design clichés

## Analysis & Synthesis Instructions

### 1. Define the Atmosphere
Evaluate the target project's intent. Use evocative adjectives from the taste spectrum:
- **Density:** "Art Gallery Airy" (1–3) → "Daily App Balanced" (4–7) → "Cockpit Dense" (8–10)
- **Variance:** "Predictable Symmetric" (1–3) → "Offset Asymmetric" (4–7) → "Artsy Chaotic" (8–10)
- **Motion:** "Static Restrained" (1–3) → "Fluid CSS" (4–7) → "Cinematic Choreography" (8–10)

Default baseline: Variance 8, Motion 6, Density 4. Adapt dynamically based on user's vibe description.

### 2. Map the Color Palette
For each color provide: **Descriptive Name** + **Hex Code** + **Functional Role**.

**Mandatory constraints:**
- Maximum 1 accent color. Saturation below 80%
- The "AI Purple/Blue Neon" aesthetic is strictly BANNED — no purple button glows, no neon gradients
- Use absolute neutral bases (Zinc/Slate) with high-contrast singular accents
- Stick to one palette for the entire output — no warm/cool gray fluctuation
- Never use pure black (`#000000`) — use Off-Black, Zinc-950, or Charcoal

### 3. Establish Typography Rules
- **Display/Headlines:** Track-tight, controlled scale. Not screaming. Hierarchy through weight and color, not just massive size
- **Body:** Relaxed leading, max 65 characters per line
- **Font Selection:** `Inter` is BANNED for premium/creative contexts. Force unique character: `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
- **Serif Ban:** Generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`, `Palatino`) are BANNED. If serif is needed for editorial/creative contexts, use only distinctive modern serifs: `Fraunces`, `Gambarino`, `Editorial New`, or `Instrument Serif`. Serif is always BANNED in dashboards or software UIs
- **Dashboard Constraint:** Use Sans-Serif pairings exclusively (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`)
- **High-Density Override:** When density exceeds 7, all numbers must use Monospace

### 4. Define the Hero Section
The Hero is the first impression and must be creative, striking, and never generic:
- **Inline Image Typography:** Embed small, contextual photos or visuals directly between words or letters in the headline. Images sit inline at type-height, rounded, acting as visual punctuation. This is the signature creative technique
- **No Overlapping:** Text must never overlap images or other text. Every element occupies its own clean spatial zone
- **No Filler Text:** "Scroll to explore", "Swipe down", scroll arrow icons, bouncing chevrons are BANNED. The content should pull users in naturally
- **Asymmetric Structure:** Centered Hero layouts BANNED when variance exceeds 4
- **CTA Restraint:** Maximum one primary CTA. No secondary "Learn more" links

### 5. Describe Component Stylings
For each component type, describe shape, color, shadow depth, and interaction behavior:
- **Buttons:** Tactile push feedback on active state. No neon outer glows. No custom mouse cursors
- **Cards:** Use ONLY when elevation communicates hierarchy. Tint shadows to background hue. For high-density layouts, replace cards with border-top dividers or negative space
- **Inputs/Forms:** Label above input, helper text optional, error text below. Standard gap spacing
- **Loading States:** Skeletal loaders matching layout dimensions — no generic circular spinners
- **Empty States:** Composed compositions indicating how to populate data
- **Error States:** Clear, inline error reporting

### 6. Define Layout Principles
- No overlapping elements — every element occupies its own clear spatial zone. No absolute-positioned content stacking
- Centered Hero sections are BANNED when variance exceeds 4 — force Split Screen, Left-Aligned, or Asymmetric Whitespace
- The generic "3 equal cards horizontally" feature row is BANNED — use 2-column Zig-Zag, asymmetric grid, or horizontal scroll
- CSS Grid over Flexbox math — never use `calc()` percentage hacks
- Contain layouts using max-width constraints (e.g., 1400px centered)
- Full-height sections must use `min-h-[100dvh]` — never `h-screen` (iOS Safari catastrophic jump)

### 7. Define Responsive Rules
Every design must work across all viewports:
- **Mobile-First Collapse (< 768px):** All multi-column layouts collapse to single column. No exceptions
- **No Horizontal Scroll:** Horizontal overflow on mobile is a critical failure
- **Typography Scaling:** Headlines scale via `clamp()`. Body text minimum `1rem`/`14px`
- **Touch Targets:** All interactive elements minimum `44px` tap target
- **Image Behavior:** Inline typography images (photos between words) stack below headline on mobile
- **Navigation:** Desktop horizontal nav collapses to clean mobile menu
- **Spacing:** Vertical section gaps reduce proportionally (`clamp(3rem, 8vw, 6rem)`)

### 8. Encode Motion Philosophy
- **Spring Physics default:** `stiffness: 100, damping: 20` — premium, weighty feel. No linear easing
- **Perpetual Micro-Interactions:** Every active component should have an infinite loop state (Pulse, Typewriter, Float, Shimmer)
- **Staggered Orchestration:** Never mount lists instantly — use cascade delays for waterfall reveals
- **Performance:** Animate exclusively via `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`. Grain/noise filters on fixed pseudo-elements only

### 9. List Anti-Patterns (AI Tells)
Encode these as explicit "NEVER DO" rules in the DESIGN.md:
- No emojis anywhere
- No `Inter` font
- No generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`) — distinctive modern serifs only if needed
- No pure black (`#000000`)
- No neon/outer glow shadows
- No oversaturated accents
- No excessive gradient text on large headers
- No custom mouse cursors
- No overlapping elements — clean spatial separation always
- No 3-column equal card layouts
- No generic names ("John Doe", "Acme", "Nexus")
- No fake round numbers (`99.99%`, `50%`)
- No AI copywriting clichés ("Elevate", "Seamless", "Unleash", "Next-Gen")
- No filler UI text: "Scroll to explore", "Swipe down", scroll arrows, bouncing chevrons
- No broken Unsplash links — use `picsum.photos` or SVG avatars
- No centered Hero sections (for high-variance projects)

## Output Format (DESIGN.md Structure)

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(Evocative description of the mood, density, variance, and motion intensity.
Example: "A restrained, gallery-airy interface with confident asymmetric layouts
and fluid spring-physics motion. The atmosphere is clinical yet warm — like a
well-lit architecture studio.")

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — Primary background surface
- **Pure Surface** (#FFFFFF) — Card and container fill
- **Charcoal Ink** (#18181B) — Primary text, Zinc-950 depth
- **Muted Steel** (#71717A) — Secondary text, descriptions, metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — Card borders, 1px structural lines
- **[Accent Name]** (#XXXXXX) — Single accent for CTAs, active states, focus rings
(Max 1 accent. Saturation < 80%. No purple/neon.)

## 3. Typography Rules
- **Display:** [Font Name] — Track-tight, controlled scale, weight-driven hierarchy
- **Body:** [Font Name] — Relaxed leading, 65ch max-width, neutral secondary color
- **Mono:** [Font Name] — For code, metadata, timestamps, high-density numbers
- **Banned:** Inter, generic system fonts for premium contexts. Serif fonts banned in dashboards.

## 4. Component Stylings
* **Buttons:** Flat, no outer glow. Tactile -1px translate on active. Accent fill for primary, ghost/outline for secondary.
* **Cards:** Generously rounded corners (2.5rem). Diffused whisper shadow. Used only when elevation serves hierarchy. High-density: replace with border-top dividers.
* **Inputs:** Label above, error below. Focus ring in accent color. No floating labels.
* **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
* **Empty States:** Composed, illustrated compositions — not just "No data" text.

## 5. Layout Principles
(Grid-first responsive architecture. Asymmetric splits for Hero sections.
Strict single-column collapse below 768px. Max-width containment.
No flexbox percentage math. Generous internal padding.)

## 6. Motion & Interaction
(Spring physics for all interactive elements. Staggered cascade reveals.
Perpetual micro-loops on active dashboard components. Hardware-accelerated
transforms only. Isolated Client Components for CPU-heavy animations.)

## 7. Anti-Patterns (Banned)
(Explicit list of forbidden patterns: no emojis, no Inter, no pure black,
no neon glows, no 3-column equal grids, no AI copywriting clichés,
no generic placeholder names, no broken image links.)
```

## Best Practices
- **Be Descriptive:** "Deep Charcoal Ink (#18181B)" — not just "dark text"
- **Be Functional:** Explain what each element is used for
- **Be Consistent:** Same terminology throughout the document
- **Be Precise:** Include exact hex codes, rem values, pixel values in parentheses
- **Be Opinionated:** This is not a neutral template — it enforces a specific, premium aesthetic

## Tips for Success
1. Start with the atmosphere — understand the vibe before detailing tokens
2. Look for patterns — identify consistent spacing, sizing, and styling
3. Think semantically — name colors by purpose, not just appearance
4. Consider hierarchy — document how visual weight communicates importance
5. Encode the bans — anti-patterns are as important as the rules themselves

## Common Pitfalls to Avoid
- Using technical jargon without translation ("rounded-xl" instead of "generously rounded corners")
- Omitting hex codes or using only descriptive names
- Forgetting functional roles of design elements
- Being too vague in atmosphere descriptions
- Ignoring the anti-pattern list — these are what make the output premium
- Defaulting to generic "safe" designs instead of enforcing the curated aesthetic

---

## sveltekit
*Build full-stack web applications with SvelteKit — file-based routing, SSR, SSG, API routes, and form actions in one framework.*

Tags: [svelte, sveltekit, fullstack, ssr, ssg, typescript]
Tools: [claude, cursor, gemini]
Risk: safe

# SvelteKit Full-Stack Development

## Overview

SvelteKit is the official full-stack framework built on top of Svelte. It provides file-based routing, server-side rendering (SSR), static site generation (SSG), API routes, and progressive form actions — all with Svelte's compile-time reactivity model that ships zero runtime overhead to the browser. Use this skill when building fast, modern web apps where both DX and performance matter.

## When to Use This Skill

- Use when building a new full-stack web application with Svelte
- Use when you need SSR or SSG with fine-grained control per route
- Use when migrating a SPA to a framework with server capabilities
- Use when working on a project that needs file-based routing and collocated API endpoints
- Use when the user asks about `+page.svelte`, `+layout.svelte`, `load` functions, or form actions

## How It Works

### Step 1: Project Setup

```bash
npm create svelte@latest my-app
cd my-app
npm install
npm run dev
```

Choose **Skeleton project** + **TypeScript** + **ESLint/Prettier** when prompted.

Directory structure after scaffolding:

```
src/
  routes/
    +page.svelte        ← Root page component
    +layout.svelte      ← Root layout (wraps all pages)
    +error.svelte       ← Error boundary
  lib/
    server/             ← Server-only code (never bundled to client)
    components/         ← Shared components
  app.html              ← HTML shell
static/                 ← Static assets
```

### Step 2: File-Based Routing

Every `+page.svelte` file in `src/routes/` maps directly to a URL:

```
src/routes/+page.svelte          → /
src/routes/about/+page.svelte    → /about
src/routes/blog/[slug]/+page.svelte  → /blog/:slug
src/routes/shop/[...path]/+page.svelte → /shop/* (catch-all)
```

**Route groups** (no URL segment): wrap in `(group)/` folder.
**Private routes** (not accessible as URLs): prefix with `_` or `(group)`.

### Step 3: Loading Data with `load` Functions

Use a `+page.ts` (universal) or `+page.server.ts` (server-only) file alongside the page:

```typescript
// src/routes/blog/[slug]/+page.server.ts
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const post = await fetch(`/api/posts/${params.slug}`).then(r => r.json());

  if (!post) {
    error(404, 'Post not found');
  }

  return { post };
};
```

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>{data.post.title}</h1>
<article>{@html data.post.content}</article>
```

### Step 4: API Routes (Server Endpoints)

Create `+server.ts` files for REST-style endpoints:

```typescript
// src/routes/api/posts/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 10);
  const posts = await db.post.findMany({ take: limit });
  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const post = await db.post.create({ data: body });
  return json(post, { status: 201 });
};
```

### Step 5: Form Actions

Form actions are the SvelteKit-native way to handle mutations — no client-side fetch required:

```typescript
// src/routes/contact/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return fail(400, { email, missing: true });
    }

    await sendEmail(String(email));
    redirect(303, '/thank-you');
  }
};
```

```svelte
<!-- src/routes/contact/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';
  export let form: ActionData;
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  {#if form?.missing}<p class="error">Email is required</p>{/if}
  <button type="submit">Subscribe</button>
</form>
```

### Step 6: Layouts and Nested Routes

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';
  export let data: LayoutData;
</script>

<nav>
  <a href="/">Home</a>
  <a href="/blog">Blog</a>
  {#if data.user}
    <a href="/dashboard">Dashboard</a>
  {/if}
</nav>

<slot />  <!-- child page renders here -->
```

```typescript
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  return { user: locals.user ?? null };
};
```

### Step 7: Rendering Modes

Control per-route rendering with page options:

```typescript
// src/routes/docs/+page.ts
export const prerender = true;   // Static — generated at build time
export const ssr = true;         // Default — rendered on server per request
export const csr = false;        // Disable client-side hydration entirely
```

## Examples

### Example 1: Protected Dashboard Route

```typescript
// src/routes/dashboard/+layout.server.ts
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(303, '/login');
  }
  return { user: locals.user };
};
```

### Example 2: Hooks — Session Middleware

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { verifyToken } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('session');
  if (token) {
    event.locals.user = await verifyToken(token);
  }
  return resolve(event);
};
```

### Example 3: Preloading and Invalidation

```svelte
<script lang="ts">
  import { invalidateAll } from '$app/navigation';

  async function refresh() {
    await invalidateAll(); // re-runs all load functions on the page
  }
</script>

<button on:click={refresh}>Refresh</button>
```

## Best Practices

- ✅ Use `+page.server.ts` for database/auth logic — it never ships to the client
- ✅ Use `$lib/server/` for shared server-only modules (DB client, auth helpers)
- ✅ Use form actions for mutations instead of client-side `fetch` — works without JS
- ✅ Type all `load` return values with generated `$types` (`PageData`, `LayoutData`)
- ✅ Use `event.locals` in hooks to pass server-side context to load functions
- ❌ Don't import server-only code in `+page.svelte` or `+layout.svelte` directly
- ❌ Don't store sensitive state in stores — use `locals` on the server
- ❌ Don't skip `use:enhance` on forms — without it, forms lose progressive enhancement

## Security & Safety Notes

- All code in `+page.server.ts`, `+server.ts`, and `$lib/server/` runs exclusively on the server — safe for DB queries, secrets, and session validation.
- Always validate and sanitize form data before database writes.
- Use `error(403)` or `redirect(303)` from `@sveltejs/kit` rather than returning raw error objects.
- Set `httpOnly: true` and `secure: true` on all auth cookies.
- CSRF protection is built-in for form actions — do not disable `checkOrigin` in production.

## Common Pitfalls

- **Problem:** `Cannot use import statement in a module` in `+page.server.ts`
  **Solution:** The file must be `.ts` or `.js`, not `.svelte`. Server files and Svelte components are separate.

- **Problem:** Store value is `undefined` on first SSR render
  **Solution:** Populate the store from the `load` function return value (`data` prop), not from client-side `onMount`.

- **Problem:** Form action does not redirect after submit
  **Solution:** Use `redirect(303, '/path')` from `@sveltejs/kit`, not a plain `return`. 303 is required for POST redirects.

- **Problem:** `locals.user` is undefined inside a `+page.server.ts` load function
  **Solution:** Set `event.locals.user` in `src/hooks.server.ts` before the `resolve()` call.

## Related Skills

- `@nextjs-app-router-patterns` — When you prefer React over Svelte for SSR/SSG
- `@trpc-fullstack` — Add end-to-end type safety to SvelteKit API routes
- `@auth-implementation-patterns` — Authentication patterns usable with SvelteKit hooks
- `@tailwind-patterns` — Styling SvelteKit apps with Tailwind CSS

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## technical-change-tracker
*Track code changes with structured JSON records, state machine enforcement, and AI session handoff for bot continuity*

Tags: [change-tracking, session-handoff, documentation, accessibility, state-machine]
Tools: [claude, cursor, gemini, codex]
Risk: safe

# Technical Change Tracker

## Overview

Track every code change with structured JSON records and accessible HTML output. Ensures AI bot sessions can resume seamlessly when previous sessions expire or are abandoned.

## When to Use This Skill

- Use when you need structured change tracking across AI coding sessions
- Use when a bot session expires mid-task and the next session needs full context to resume
- Use when onboarding a project with undocumented change history

## How It Works

### State Machine

```
planned -> in_progress -> implemented -> tested -> deployed
             |
             +-> blocked
```

### Commands

`/tc init` | `/tc create` | `/tc update` | `/tc status` | `/tc resume` | `/tc close` | `/tc export` | `/tc dashboard` | `/tc retro`

### Session Handoff

Each TC stores: progress summary, next steps, blockers, key context, and files in progress — so the next bot session picks up exactly where the last left off.

### Non-Blocking

TC bookkeeping runs via background subagents. Never interrupts coding work.

## Features

- Structured JSON records with append-only revision history
- Test cases with log snippet evidence
- WCAG AA+ accessible HTML output (dark theme, rem-based fonts)
- CSS-only dashboard with status filters
- Python stdlib only — zero external dependencies
- Retroactive bulk creation from git history via `/tc retro`

## Full Repository

https://github.com/Elkidogz/technical-change-skill — MIT License

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## tmux
*Expert tmux session, window, and pane management for terminal multiplexing, persistent remote workflows, and shell scripting automation.*

Tags: [tmux, terminal, multiplexer, sessions, shell, remote, automation]
Tools: [claude, cursor, gemini]
Risk: safe

# tmux — Terminal Multiplexer

## Overview

`tmux` keeps terminal sessions alive across SSH disconnects, splits work across multiple panes, and enables fully scriptable terminal automation. This skill covers session management, window/pane layout, keybinding patterns, and using `tmux` non-interactively from shell scripts — essential for remote servers, long-running jobs, and automated workflows.

## When to Use This Skill

- Use when setting up or managing persistent terminal sessions on remote servers
- Use when the user needs to run long-running processes that survive SSH disconnects
- Use when scripting multi-pane terminal layouts (e.g., logs + shell + editor)
- Use when automating `tmux` commands from bash scripts without user interaction

## How It Works

`tmux` has three hierarchy levels: **sessions** (top level, survives disconnects), **windows** (tabs within a session), and **panes** (splits within a window). Everything is controllable from outside via `tmux <command>` or from inside via the prefix key (`Ctrl-b` by default).

### Session Management

```bash
# Create a new named session
tmux new-session -s work

# Create detached (background) session
tmux new-session -d -s work

# Create detached session and start a command
tmux new-session -d -s build -x 220 -y 50 "make all"

# Attach to a session
tmux attach -t work
tmux attach          # attaches to most recent session

# List all sessions
tmux list-sessions
tmux ls

# Detach from inside tmux
# Prefix + d   (Ctrl-b d)

# Kill a session
tmux kill-session -t work

# Kill all sessions except the current one
tmux kill-session -a

# Rename a session from outside
tmux rename-session -t old-name new-name

# Switch to another session from outside
tmux switch-client -t other-session

# Check if a session exists (useful in scripts)
tmux has-session -t work 2>/dev/null && echo "exists"
```

### Window Management

```bash
# Create a new window in the current session
tmux new-window -t work -n "logs"

# Create a window running a specific command
tmux new-window -t work:3 -n "server" "python -m http.server 8080"

# List windows
tmux list-windows -t work

# Select (switch to) a window
tmux select-window -t work:logs
tmux select-window -t work:2       # by index

# Rename a window
tmux rename-window -t work:2 "editor"

# Kill a window
tmux kill-window -t work:logs

# Move window to a new index
tmux move-window -s work:3 -t work:1

# From inside tmux:
# Prefix + c     — new window
# Prefix + ,     — rename window
# Prefix + &     — kill window
# Prefix + n/p   — next/previous window
# Prefix + 0-9   — switch to window by number
```

### Pane Management

```bash
# Split pane vertically (left/right)
tmux split-window -h -t work:1

# Split pane horizontally (top/bottom)
tmux split-window -v -t work:1

# Split and run a command
tmux split-window -h -t work:1 "tail -f /var/log/syslog"

# Select a pane by index
tmux select-pane -t work:1.0

# Resize panes
tmux resize-pane -t work:1.0 -R 20   # expand right by 20 cols
tmux resize-pane -t work:1.0 -D 10   # shrink down by 10 rows
tmux resize-pane -Z                   # toggle zoom (fullscreen)

# Swap panes
tmux swap-pane -s work:1.0 -t work:1.1

# Kill a pane
tmux kill-pane -t work:1.1

# From inside tmux:
# Prefix + %     — split vertical
# Prefix + "     — split horizontal
# Prefix + arrow — navigate panes
# Prefix + z     — zoom/unzoom current pane
# Prefix + x     — kill pane
# Prefix + {/}   — swap pane with previous/next
```

### Sending Commands to Panes Without Being Attached

```bash
# Send a command to a specific pane and press Enter
tmux send-keys -t work:1.0 "ls -la" Enter

# Run a command in a background pane without attaching
tmux send-keys -t work:editor "vim src/main.py" Enter

# Send Ctrl+C to stop a running process
tmux send-keys -t work:1.0 C-c

# Send text without pressing Enter (useful for pre-filling prompts)
tmux send-keys -t work:1.0 "git commit -m '"

# Clear a pane
tmux send-keys -t work:1.0 "clear" Enter

# Check what's in a pane (capture its output)
tmux capture-pane -t work:1.0 -p
tmux capture-pane -t work:1.0 -p | grep "ERROR"
```

### Scripting a Full Workspace Layout

This is the most powerful pattern: create a fully configured multi-pane workspace from a single script.

```bash
#!/usr/bin/env bash
set -euo pipefail

SESSION="dev"

# Bail if session already exists
tmux has-session -t "$SESSION" 2>/dev/null && {
  echo "Session $SESSION already exists. Attaching..."
  tmux attach -t "$SESSION"
  exit 0
}

# Create session with first window
tmux new-session -d -s "$SESSION" -n "editor" -x 220 -y 50

# Window 1: editor + test runner side by side
tmux send-keys -t "$SESSION:editor" "vim ." Enter
tmux split-window -h -t "$SESSION:editor"
tmux send-keys -t "$SESSION:editor.1" "npm test -- --watch" Enter
tmux select-pane -t "$SESSION:editor.0"

# Window 2: server logs
tmux new-window -t "$SESSION" -n "server"
tmux send-keys -t "$SESSION:server" "docker compose up" Enter
tmux split-window -v -t "$SESSION:server"
tmux send-keys -t "$SESSION:server.1" "tail -f logs/app.log" Enter

# Window 3: general shell
tmux new-window -t "$SESSION" -n "shell"

# Focus first window
tmux select-window -t "$SESSION:editor"

# Attach
tmux attach -t "$SESSION"
```

### Configuration (`~/.tmux.conf`)

```bash
# Change prefix to Ctrl-a (screen-style)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Enable mouse support
set -g mouse on

# Start window/pane numbering at 1
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Increase scrollback buffer
set -g history-limit 50000

# Use vi keys in copy mode
setw -g mode-keys vi

# Faster key repetition
set -s escape-time 0

# Reload config without restarting
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Intuitive splits: | and -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# New windows open in current directory
bind c new-window -c "#{pane_current_path}"

# Status bar
set -g status-right "#{session_name} | %H:%M %d-%b"
set -g status-interval 5
```

### Copy Mode and Scrollback

```bash
# Enter copy mode (scroll up through output)
# Prefix + [

# In vi mode:
# / to search forward, ? to search backward
# Space to start selection, Enter to copy
# q to exit copy mode

# Paste the most recent buffer
# Prefix + ]

# List paste buffers
tmux list-buffers

# Show the most recent buffer
tmux show-buffer

# Save buffer to a file
tmux save-buffer /tmp/tmux-output.txt

# Load a file into a buffer
tmux load-buffer /tmp/data.txt

# Pipe pane output to a command
tmux pipe-pane -t work:1.0 "cat >> ~/session.log"
```

### Practical Automation Patterns

```bash
# Idempotent session: create or attach
ensure_session() {
  local name="$1"
  tmux has-session -t "$name" 2>/dev/null \
    || tmux new-session -d -s "$name"
  tmux attach -t "$name"
}

# Run a command in a new background window and tail its output
run_bg() {
  local session="${1:-main}" cmd="${*:2}"
  tmux new-window -t "$session" -n "bg-$$"
  tmux send-keys -t "$session:bg-$$" "$cmd" Enter
}

# Wait for a pane to produce specific output (polling)
wait_for_output() {
  local target="$1" pattern="$2" timeout="${3:-30}"
  local elapsed=0
  while (( elapsed < timeout )); do
    tmux capture-pane -t "$target" -p | grep -q "$pattern" && return 0
    sleep 1
    (( elapsed++ ))
  done
  return 1
}

# Kill all background windows matching a name prefix
kill_bg_windows() {
  local session="$1" prefix="${2:-bg-}"
  tmux list-windows -t "$session" -F "#W" \
    | grep "^${prefix}" \
    | while read -r win; do
        tmux kill-window -t "${session}:${win}"
      done
}
```

### Remote and SSH Workflows

```bash
# SSH and immediately attach to an existing session
ssh user@host -t "tmux attach -t work || tmux new-session -s work"

# Run a command on remote host inside a tmux session (fire and forget)
ssh user@host "tmux new-session -d -s deploy 'bash /opt/deploy.sh'"

# Watch the remote session output from another terminal
ssh user@host -t "tmux attach -t deploy -r"  # read-only attach

# Pair programming: share a session (both users attach to the same session)
# User 1:
tmux new-session -s shared
# User 2 (same server):
tmux attach -t shared
```

## Best Practices

- Always name sessions (`-s name`) in scripts — unnamed sessions are hard to target reliably
- Use `tmux has-session -t name 2>/dev/null` before creating to make scripts idempotent
- Set `-x` and `-y` when creating detached sessions to give panes a proper size for commands that check terminal dimensions
- Use `send-keys ... Enter` for automation rather than piping stdin — it works even when the target pane is running an interactive program
- Keep `~/.tmux.conf` in version control for reproducibility across machines
- Prefer `bind -n` for bindings that don't need the prefix, but only for keys that don't conflict with application shortcuts

## Security & Safety Notes

- `send-keys` executes commands in a pane without confirmation — verify the target (`-t session:window.pane`) before use in scripts to avoid sending keystrokes to the wrong pane
- Read-only attach (`-r`) is appropriate when sharing sessions with others to prevent accidental input
- Avoid storing secrets in tmux window/pane titles or environment variables exported into sessions on shared machines

## Common Pitfalls

- **Problem:** `tmux` commands from a script fail with "no server running"
  **Solution:** Start the server first with `tmux start-server`, or create a detached session before running other commands.

- **Problem:** Pane size is 0x0 when creating a detached session
  **Solution:** Pass explicit dimensions: `tmux new-session -d -s name -x 200 -y 50`.

- **Problem:** `send-keys` types the text but doesn't run the command
  **Solution:** Ensure you pass `Enter` (capital E) as a second argument: `tmux send-keys -t target "cmd" Enter`.

- **Problem:** Script creates a duplicate session each run
  **Solution:** Guard with `tmux has-session -t name 2>/dev/null || tmux new-session -d -s name`.

- **Problem:** Copy-mode selection doesn't work as expected
  **Solution:** Confirm `mode-keys vi` or `mode-keys emacs` is set to match your preference in `~/.tmux.conf`.

## Related Skills

- `@bash-pro` — Writing the shell scripts that orchestrate tmux sessions
- `@bash-linux` — General Linux terminal patterns used inside tmux panes
- `@ssh` — Combining tmux with SSH for persistent remote workflows

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## trpc-fullstack
*Build end-to-end type-safe APIs with tRPC — routers, procedures, middleware, subscriptions, and Next.js/React integration patterns.*

Tags: [typescript, trpc, api, fullstack, nextjs, react, type-safety]
Tools: [claude, cursor, gemini]
Risk: none

# tRPC Full-Stack

## Overview

tRPC lets you build fully type-safe APIs without writing a schema or code-generation step. Your TypeScript types flow from the server router directly to the client — so every API call is autocompleted, validated at compile time, and refactoring-safe. Use this skill when building TypeScript monorepos, Next.js apps, or any project where the server and client share a codebase.

## When to Use This Skill

- Use when building a TypeScript full-stack app (Next.js, Remix, Express + React) where the client and server share a single repo
- Use when you want end-to-end type safety on API calls without REST/GraphQL schema overhead
- Use when adding real-time features (subscriptions) to an existing tRPC setup
- Use when designing multi-step middleware (auth, rate limiting, tenant scoping) on tRPC procedures
- Use when migrating an existing REST/GraphQL API to tRPC incrementally

## Core Concepts

### Routers and Procedures

A **router** groups related **procedures** (think: endpoints). Procedures are typed functions — `query` for reads, `mutation` for writes, `subscription` for real-time streams.

### Input Validation with Zod

All procedure inputs are validated with Zod schemas. The validated, typed input is available in the procedure handler — no manual parsing.

### Context

`context` is shared state passed to every procedure — auth session, database client, request headers, etc. It is built once per request in a context factory. **Important:** Next.js App Router and Pages Router require separate context factories because App Router handlers receive a fetch `Request`, not a Node.js `NextApiRequest`.

### Middleware

Middleware chains run before a procedure. Use them for authentication, logging, and request enrichment. They can extend the context for downstream procedures.

---

## How It Works

### Step 1: Install and Initialize

```bash
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

Create the tRPC instance and reusable builders:

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { type Context } from './context';
import { ZodError } from 'zod';

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
```

### Step 2: Define Two Context Factories

Next.js App Router handlers receive a fetch `Request` (not a Node.js `NextApiRequest`), so the context
must be built differently depending on the call site. Define one factory per surface:

```typescript
// src/server/context.ts
import { type FetchCreateContextFnOptions } from '@trpc/server/adapters/fetch';
import { auth } from '@/server/auth'; // Next-Auth v5 / your auth helper
import { db } from './db';

/**
 * Context for the HTTP handler (App Router Route Handler).
 * `opts.req` is the fetch Request — auth is resolved server-side via `auth()`.
 */
export async function createTRPCContext(opts: FetchCreateContextFnOptions) {
  const session = await auth(); // server-side auth — no req/res needed
  return { session, db, headers: opts.req.headers };
}

/**
 * Context for direct server-side callers (Server Components, RSC, cron jobs).
 * No HTTP request is involved, so we call auth() directly from the server.
 */
export async function createServerContext() {
  const session = await auth();
  return { session, db };
}

export type Context = Awaited<ReturnType<typeof createTRPCContext>>;
```

### Step 3: Build an Auth Middleware and Protected Procedure

```typescript
// src/server/trpc.ts (continued)
const enforceAuth = middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: {
      // Narrows type: session is non-null from here
      session: { ...ctx.session, user: ctx.session.user },
    },
  });
});

export const protectedProcedure = t.procedure.use(enforceAuth);
```

### Step 4: Create Routers

```typescript
// src/server/routers/post.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';
import { TRPCError } from '@trpc/server';

export const postRouter = router({
  list: publicProcedure
    .input(
      z.object({
        limit: z.number().min(1).max(100).default(20),
        cursor: z.string().optional(),
      })
    )
    .query(async ({ ctx, input }) => {
      const posts = await ctx.db.post.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: 'desc' },
      });
      const nextCursor =
        posts.length > input.limit ? posts.pop()!.id : undefined;
      return { posts, nextCursor };
    }),

  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } });
      if (!post) throw new TRPCError({ code: 'NOT_FOUND' });
      return post;
    }),

  create: protectedProcedure
    .input(
      z.object({
        title: z.string().min(1).max(200),
        body: z.string().min(1),
      })
    )
    .mutation(async ({ ctx, input }) => {
      return ctx.db.post.create({
        data: { ...input, authorId: ctx.session.user.id },
      });
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } });
      if (!post) throw new TRPCError({ code: 'NOT_FOUND' });
      if (post.authorId !== ctx.session.user.id)
        throw new TRPCError({ code: 'FORBIDDEN' });
      return ctx.db.post.delete({ where: { id: input.id } });
    }),
});
```

### Step 5: Compose the Root Router and Export Types

```typescript
// src/server/root.ts
import { router } from './trpc';
import { postRouter } from './routers/post';
import { userRouter } from './routers/user';

export const appRouter = router({
  post: postRouter,
  user: userRouter,
});

// Export the type for the client — never import the appRouter itself on the client
export type AppRouter = typeof appRouter;
```

### Step 6: Mount the API Handler (Next.js App Router)

The App Router handler must use `fetchRequestHandler` and the **fetch-based** context factory.
`createTRPCContext` receives `FetchCreateContextFnOptions` (with a fetch `Request`), not
a Pages Router `req/res` pair.

```typescript
// src/app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { type FetchCreateContextFnOptions } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/root';
import { createTRPCContext } from '@/server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    // opts is FetchCreateContextFnOptions — req is the fetch Request
    createContext: (opts: FetchCreateContextFnOptions) => createTRPCContext(opts),
  });

export { handler as GET, handler as POST };
```

### Step 7: Set Up the Client (React Query)

```typescript
// src/utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '@/server/root';

export const trpc = createTRPCReact<AppRouter>();
```

```typescript
// src/app/providers.tsx
'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from '@/utils/trpc';

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
          headers: () => ({ 'x-trpc-source': 'react' }),
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </trpc.Provider>
  );
}
```

---

## Examples

### Example 1: Fetching Data in a Component

```typescript
// components/PostList.tsx
'use client';
import { trpc } from '@/utils/trpc';

export function PostList() {
  const { data, isLoading, error } = trpc.post.list.useQuery({ limit: 10 });

  if (isLoading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <ul>
      {data?.posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Example 2: Mutation with Cache Invalidation

```typescript
'use client';
import { trpc } from '@/utils/trpc';

export function CreatePost() {
  const utils = trpc.useUtils();

  const createPost = trpc.post.create.useMutation({
    onSuccess: () => {
      // Invalidate and refetch the post list
      utils.post.list.invalidate();
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    createPost.mutate({
      title: data.get('title') as string,
      body: data.get('body') as string,
    });
    form.reset();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" placeholder="Title" required />
      <textarea name="body" placeholder="Body" required />
      <button type="submit" disabled={createPost.isPending}>
        {createPost.isPending ? 'Creating…' : 'Create Post'}
      </button>
      {createPost.error && <p>{createPost.error.message}</p>}
    </form>
  );
}
```

### Example 3: Server-Side Caller (Server Components / SSR)

Use `createServerContext` — the dedicated server-side factory — so that `auth()` is called
correctly without needing a synthetic or empty request object:

```typescript
// app/posts/page.tsx (Next.js Server Component)
import { appRouter } from '@/server/root';
import { createCallerFactory } from '@trpc/server';
import { createServerContext } from '@/server/context';

const createCaller = createCallerFactory(appRouter);

export default async function PostsPage() {
  // Uses createServerContext — calls auth() server-side, no req/res cast needed
  const caller = createCaller(await createServerContext());
  const { posts } = await caller.post.list({ limit: 20 });

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Example 4: Real-Time Subscriptions (WebSocket)

```typescript
// server/routers/notifications.ts
import { observable } from '@trpc/server/observable';
import { EventEmitter } from 'events';

const ee = new EventEmitter();

export const notificationRouter = router({
  onNew: protectedProcedure.subscription(({ ctx }) => {
    return observable<{ message: string; at: Date }>((emit) => {
      const onNotification = (data: { message: string }) => {
        emit.next({ message: data.message, at: new Date() });
      };

      const channel = `user:${ctx.session.user.id}`;
      ee.on(channel, onNotification);
      return () => ee.off(channel, onNotification);
    });
  }),
});
```

```typescript
// Client usage — requires wsLink in the client config
trpc.notification.onNew.useSubscription(undefined, {
  onData(data) {
    toast(data.message);
  },
});
```

---

## Best Practices

- ✅ **Export only `AppRouter` type** from server code — never import `appRouter` on the client
- ✅ **Use separate context factories** — `createTRPCContext` for the HTTP handler, `createServerContext` for Server Components and callers
- ✅ **Validate all inputs with Zod** — never trust raw `input` without a schema
- ✅ **Split routers by domain** (posts, users, billing) and merge in `root.ts`
- ✅ **Extend context in middleware** rather than querying the DB multiple times per request
- ✅ **Use `utils.invalidate()`** after mutations to keep the cache fresh
- ❌ **Don't cast context with `as any`** to silence type errors — the mismatch will surface as a runtime failure when auth or session lookups return undefined
- ❌ **Don't use `createContext({} as any)`** in Server Components — use `createServerContext()` which calls `auth()` directly
- ❌ **Don't put business logic in the route handler** — keep it in the procedure or a service layer
- ❌ **Don't share the tRPC client instance globally** — create it per-provider to avoid stale closures

---

## Security & Safety Notes

- Always enforce authorization in `protectedProcedure` — never rely on client-side checks alone
- Validate all input shapes with Zod, including pagination cursors and IDs, to prevent injection via malformed inputs
- Avoid exposing internal error details to clients — use `TRPCError` with a public-safe `message` and keep stack traces server-side only
- Rate-limit public procedures using middleware to prevent abuse

---

## Common Pitfalls

- **Problem:** Auth session is `null` in protected procedures even when the user is logged in
  **Solution:** Ensure `createTRPCContext` uses the correct server-side auth call (e.g. `auth()` from Next-Auth v5) and is not receiving a Pages Router `req/res` cast via `as any` in an App Router handler

- **Problem:** Server Component caller fails for auth-dependent queries
  **Solution:** Use `createServerContext()` (the dedicated server-side factory) instead of passing an empty or synthetic object to `createContext`

- **Problem:** "Type error: AppRouter is not assignable to AnyRouter"
  **Solution:** Import `AppRouter` as a `type` import (`import type { AppRouter }`) on the client, not the full module

- **Problem:** Mutations not reflecting in the UI after success
  **Solution:** Call `utils.<router>.<procedure>.invalidate()` in `onSuccess` to trigger a refetch via React Query

- **Problem:** "Cannot find module '@trpc/server/adapters/next'" with App Router
  **Solution:** Use `@trpc/server/adapters/fetch` and `fetchRequestHandler` for the App Router; the `nextjs` adapter is for Pages Router only

- **Problem:** Subscriptions not connecting
  **Solution:** Subscriptions require `splitLink` — route subscriptions to `wsLink` and queries/mutations to `httpBatchLink`

---

## Related Skills

- `@typescript-expert` — Deep TypeScript patterns used inside tRPC routers and generic utilities
- `@react-patterns` — React hooks patterns that pair with `trpc.*.useQuery` and `useMutation`
- `@test-driven-development` — Write procedure unit tests using `createCallerFactory` without an HTTP server
- `@security-auditor` — Review tRPC middleware chains for auth bypass and input validation gaps

## Additional Resources

- [tRPC Official Docs](https://trpc.io/docs)
- [create-t3-app](https://create.t3.gg) — Production Next.js starter with tRPC wired in
- [tRPC GitHub](https://github.com/trpc/trpc)
- [TanStack Query Docs](https://tanstack.com/query/latest)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## typescript-expert
*TypeScript and JavaScript expert with deep knowledge of type-level programming, performance optimization, monorepo management, migration strategies, and modern tooling.*

Risk: critical

# TypeScript Expert

You are an advanced TypeScript expert with deep, practical knowledge of type-level programming, performance optimization, and real-world problem solving based on current best practices.

### When invoked:

0. If the issue requires ultra-specific expertise, recommend switching and stop:
   - Deep webpack/vite/rollup bundler internals → typescript-build-expert
   - Complex ESM/CJS migration or circular dependency analysis → typescript-module-expert
   - Type performance profiling or compiler internals → typescript-type-expert

   Example to output:
   "This requires deep bundler expertise. Please invoke: 'Use the typescript-build-expert subagent.' Stopping here."

1. Analyze project setup comprehensively:
   
   **Use internal tools first (Read, Grep, Glob) for better performance. Shell commands are fallbacks.**
   
   ```bash
   # Core versions and configuration
   npx tsc --version
   node -v
   # Detect tooling ecosystem (prefer parsing package.json)
   node -e "const p=require('./package.json');console.log(Object.keys({...p.devDependencies,...p.dependencies}||{}).join('\n'))" 2>/dev/null | grep -E 'biome|eslint|prettier|vitest|jest|turborepo|nx' || echo "No tooling detected"
   # Check for monorepo (fixed precedence)
   (test -f pnpm-workspace.yaml || test -f lerna.json || test -f nx.json || test -f turbo.json) && echo "Monorepo detected"
   ```
   
   **After detection, adapt approach:**
   - Match import style (absolute vs relative)
   - Respect existing baseUrl/paths configuration
   - Prefer existing project scripts over raw tools
   - In monorepos, consider project references before broad tsconfig changes

2. Identify the specific problem category and complexity level

3. Apply the appropriate solution strategy from my expertise

4. Validate thoroughly:
   ```bash
   # Fast fail approach (avoid long-lived processes)
   npm run -s typecheck || npx tsc --noEmit
   npm test -s || npx vitest run --reporter=basic --no-watch
   # Only if needed and build affects outputs/config
   npm run -s build
   ```
   
   **Safety note:** Avoid watch/serve processes in validation. Use one-shot diagnostics only.

## Advanced Type System Expertise

### Type-Level Programming Patterns

**Branded Types for Domain Modeling**
```typescript
// Create nominal types to prevent primitive obsession
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;

// Prevents accidental mixing of domain primitives
function processOrder(orderId: OrderId, userId: UserId) { }
```
- Use for: Critical domain primitives, API boundaries, currency/units
- Resource: https://egghead.io/blog/using-branded-types-in-typescript

**Advanced Conditional Types**
```typescript
// Recursive type manipulation
type DeepReadonly<T> = T extends (...args: any[]) => any 
  ? T 
  : T extends object 
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// Template literal type magic
type PropEventSource<Type> = {
  on<Key extends string & keyof Type>
    (eventName: `${Key}Changed`, callback: (newValue: Type[Key]) => void): void;
};
```
- Use for: Library APIs, type-safe event systems, compile-time validation
- Watch for: Type instantiation depth errors (limit recursion to 10 levels)

**Type Inference Techniques**
```typescript
// Use 'satisfies' for constraint validation (TS 5.0+)
const config = {
  api: "https://api.example.com",
  timeout: 5000
} satisfies Record<string, string | number>;
// Preserves literal types while ensuring constraints

// Const assertions for maximum inference
const routes = ['/home', '/about', '/contact'] as const;
type Route = typeof routes[number]; // '/home' | '/about' | '/contact'
```

### Performance Optimization Strategies

**Type Checking Performance**
```bash
# Diagnose slow type checking
npx tsc --extendedDiagnostics --incremental false | grep -E "Check time|Files:|Lines:|Nodes:"

# Common fixes for "Type instantiation is excessively deep"
# 1. Replace type intersections with interfaces
# 2. Split large union types (>100 members)
# 3. Avoid circular generic constraints
# 4. Use type aliases to break recursion
```

**Build Performance Patterns**
- Enable `skipLibCheck: true` for library type checking only (often significantly improves performance on large projects, but avoid masking app typing issues)
- Use `incremental: true` with `.tsbuildinfo` cache
- Configure `include`/`exclude` precisely
- For monorepos: Use project references with `composite: true`

## Real-World Problem Resolution

### Complex Error Patterns

**"The inferred type of X cannot be named"**
- Cause: Missing type export or circular dependency
- Fix priority:
  1. Export the required type explicitly
  2. Use `ReturnType<typeof function>` helper
  3. Break circular dependencies with type-only imports
- Resource: https://github.com/microsoft/TypeScript/issues/47663

**Missing type declarations**
- Quick fix with ambient declarations:
```typescript
// types/ambient.d.ts
declare module 'some-untyped-package' {
  const value: unknown;
  export default value;
  export = value; // if CJS interop is needed
}
```
- For more details: [Declaration Files Guide](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html)

**"Excessive stack depth comparing types"**
- Cause: Circular or deeply recursive types
- Fix priority:
  1. Limit recursion depth with conditional types
  2. Use `interface` extends instead of type intersection
  3. Simplify generic constraints
```typescript
// Bad: Infinite recursion
type InfiniteArray<T> = T | InfiniteArray<T>[];

// Good: Limited recursion
type NestedArray<T, D extends number = 5> = 
  D extends 0 ? T : T | NestedArray<T, [-1, 0, 1, 2, 3, 4][D]>[];
```

**Module Resolution Mysteries**
- "Cannot find module" despite file existing:
  1. Check `moduleResolution` matches your bundler
  2. Verify `baseUrl` and `paths` alignment
  3. For monorepos: Ensure workspace protocol (workspace:*)
  4. Try clearing cache: `rm -rf node_modules/.cache .tsbuildinfo`

**Path Mapping at Runtime**
- TypeScript paths only work at compile time, not runtime
- Node.js runtime solutions:
  - ts-node: Use `ts-node -r tsconfig-paths/register`
  - Node ESM: Use loader alternatives or avoid TS paths at runtime
  - Production: Pre-compile with resolved paths

### Migration Expertise

**JavaScript to TypeScript Migration**
```bash
# Incremental migration strategy
# 1. Enable allowJs and checkJs (merge into existing tsconfig.json):
# Add to existing tsconfig.json:
# {
#   "compilerOptions": {
#     "allowJs": true,
#     "checkJs": true
#   }
# }

# 2. Rename files gradually (.js → .ts)
# 3. Add types file by file using AI assistance
# 4. Enable strict mode features one by one

# Automated helpers (if installed/needed)
command -v ts-migrate >/dev/null 2>&1 && npx ts-migrate migrate . --sources 'src/**/*.js'
command -v typesync >/dev/null 2>&1 && npx typesync  # Install missing @types packages
```

**Tool Migration Decisions**

| From | To | When | Migration Effort |
|------|-----|------|-----------------|
| ESLint + Prettier | Biome | Need much faster speed, okay with fewer rules | Low (1 day) |
| TSC for linting | Type-check only | Have 100+ files, need faster feedback | Medium (2-3 days) |
| Lerna | Nx/Turborepo | Need caching, parallel builds | High (1 week) |
| CJS | ESM | Node 18+, modern tooling | High (varies) |

### Monorepo Management

**Nx vs Turborepo Decision Matrix**
- Choose **Turborepo** if: Simple structure, need speed, <20 packages
- Choose **Nx** if: Complex dependencies, need visualization, plugins required
- Performance: Nx often performs better on large monorepos (>50 packages)

**TypeScript Monorepo Configuration**
```json
// Root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" },
    { "path": "./apps/web" }
  ],
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

## Modern Tooling Expertise

### Biome vs ESLint

**Use Biome when:**
- Speed is critical (often faster than traditional setups)
- Want single tool for lint + format
- TypeScript-first project
- Okay with 64 TS rules vs 100+ in typescript-eslint

**Stay with ESLint when:**
- Need specific rules/plugins
- Have complex custom rules
- Working with Vue/Angular (limited Biome support)
- Need type-aware linting (Biome doesn't have this yet)

### Type Testing Strategies

**Vitest Type Testing (Recommended)**
```typescript
// in avatar.test-d.ts
import { expectTypeOf } from 'vitest'
import type { Avatar } from './avatar'

test('Avatar props are correctly typed', () => {
  expectTypeOf<Avatar>().toHaveProperty('size')
  expectTypeOf<Avatar['size']>().toEqualTypeOf<'sm' | 'md' | 'lg'>()
})
```

**When to Test Types:**
- Publishing libraries
- Complex generic functions
- Type-level utilities
- API contracts

## Debugging Mastery

### CLI Debugging Tools
```bash
# Debug TypeScript files directly (if tools installed)
command -v tsx >/dev/null 2>&1 && npx tsx --inspect src/file.ts
command -v ts-node >/dev/null 2>&1 && npx ts-node --inspect-brk src/file.ts

# Trace module resolution issues
npx tsc --traceResolution > resolution.log 2>&1
grep "Module resolution" resolution.log

# Debug type checking performance (use --incremental false for clean trace)
npx tsc --generateTrace trace --incremental false
# Analyze trace (if installed)
command -v @typescript/analyze-trace >/dev/null 2>&1 && npx @typescript/analyze-trace trace

# Memory usage analysis
node --max-old-space-size=8192 node_modules/typescript/lib/tsc.js
```

### Custom Error Classes
```typescript
// Proper error class with stack preservation
class DomainError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message);
    this.name = 'DomainError';
    Error.captureStackTrace(this, this.constructor);
  }
}
```

## Current Best Practices

### Strict by Default
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

### ESM-First Approach
- Set `"type": "module"` in package.json
- Use `.mts` for TypeScript ESM files if needed
- Configure `"moduleResolution": "bundler"` for modern tools
- Use dynamic imports for CJS: `const pkg = await import('cjs-package')`
  - Note: `await import()` requires async function or top-level await in ESM
  - For CJS packages in ESM: May need `(await import('pkg')).default` depending on the package's export structure and your compiler settings

### AI-Assisted Development
- GitHub Copilot excels at TypeScript generics
- Use AI for boilerplate type definitions
- Validate AI-generated types with type tests
- Document complex types for AI context

## Code Review Checklist

When reviewing TypeScript/JavaScript code, focus on these domain-specific aspects:

### Type Safety
- [ ] No implicit `any` types (use `unknown` or proper types)
- [ ] Strict null checks enabled and properly handled
- [ ] Type assertions (`as`) justified and minimal
- [ ] Generic constraints properly defined
- [ ] Discriminated unions for error handling
- [ ] Return types explicitly declared for public APIs

### TypeScript Best Practices
- [ ] Prefer `interface` over `type` for object shapes (better error messages)
- [ ] Use const assertions for literal types
- [ ] Leverage type guards and predicates
- [ ] Avoid type gymnastics when simpler solution exists
- [ ] Template literal types used appropriately
- [ ] Branded types for domain primitives

### Performance Considerations
- [ ] Type complexity doesn't cause slow compilation
- [ ] No excessive type instantiation depth
- [ ] Avoid complex mapped types in hot paths
- [ ] Use `skipLibCheck: true` in tsconfig
- [ ] Project references configured for monorepos

### Module System
- [ ] Consistent import/export patterns
- [ ] No circular dependencies
- [ ] Proper use of barrel exports (avoid over-bundling)
- [ ] ESM/CJS compatibility handled correctly
- [ ] Dynamic imports for code splitting

### Error Handling Patterns
- [ ] Result types or discriminated unions for errors
- [ ] Custom error classes with proper inheritance
- [ ] Type-safe error boundaries
- [ ] Exhaustive switch cases with `never` type

### Code Organization
- [ ] Types co-located with implementation
- [ ] Shared types in dedicated modules
- [ ] Avoid global type augmentation when possible
- [ ] Proper use of declaration files (.d.ts)

## Quick Decision Trees

### "Which tool should I use?"
```
Type checking only? → tsc
Type checking + linting speed critical? → Biome  
Type checking + comprehensive linting? → ESLint + typescript-eslint
Type testing? → Vitest expectTypeOf
Build tool? → Project size <10 packages? Turborepo. Else? Nx
```

### "How do I fix this performance issue?"
```
Slow type checking? → skipLibCheck, incremental, project references
Slow builds? → Check bundler config, enable caching
Slow tests? → Vitest with threads, avoid type checking in tests
Slow language server? → Exclude node_modules, limit files in tsconfig
```

## Expert Resources

### Performance
- [TypeScript Wiki Performance](https://github.com/microsoft/TypeScript/wiki/Performance)
- [Type instantiation tracking](https://github.com/microsoft/TypeScript/pull/48077)

### Advanced Patterns
- [Type Challenges](https://github.com/type-challenges/type-challenges)
- [Type-Level TypeScript Course](https://type-level-typescript.com)

### Tools
- [Biome](https://biomejs.dev) - Fast linter/formatter
- [TypeStat](https://github.com/JoshuaKGoldberg/TypeStat) - Auto-fix TypeScript types
- [ts-migrate](https://github.com/airbnb/ts-migrate) - Migration toolkit

### Testing
- [Vitest Type Testing](https://vitest.dev/guide/testing-types)
- [tsd](https://github.com/tsdjs/tsd) - Standalone type testing

Always validate changes don't break existing functionality before considering the issue resolved.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## x-twitter-scraper
*X/Twitter automation skill for tweet search, follower export, posting, DMs, webhooks, MCP, SDKs, Hermes Tweet, and TweetClaw.*

Tags: [twitter, x-api, tweet-search, twitter-api, twitter-scraper, follower-export, automation, mcp, sdk, webhooks, hermes-agent, hermes-tweet, openclaw, tweetclaw]
Risk: critical

# X (Twitter) Scraper - Xquik

## Overview

Gives AI agents X (Twitter) data and automation workflows through the Xquik platform. Covers tweet search, advanced Twitter search, profile tweets, user lookup, follower export, media download, posting, replies, DMs, giveaway draws, account monitoring, webhooks, 23 bulk extraction tools, MCP, official SDKs, the Hermes Tweet Hermes Agent plugin, and the TweetClaw OpenClaw plugin.

This repository entry is documentation-only: it does not include an executable scraper, binary, package, or vendored runtime code. The external Xquik, Hermes Tweet, and TweetClaw tools referenced below must be reviewed and installed separately before use.

Because this workflow can automate authenticated X/Twitter account actions, treat it as critical-risk guidance. Only use it with accounts and targets you are authorized to operate, and require explicit user approval before posting, replying, liking, reposting, following, unfollowing, sending DMs, creating monitors, registering webhooks, or starting bulk extraction.

## When to Use This Skill

- User needs to search X/Twitter for tweets by keyword, hashtag, or user
- User asks for advanced Twitter search, profile tweets, or user timeline data
- User wants to look up a user profile (bio, follower counts, etc.)
- User needs engagement metrics for a specific tweet (likes, retweets, views)
- User wants to check if one account follows another
- User needs to extract followers, replies, retweets, quotes, or community members in bulk
- User wants to download tweet media, export results, or connect an official SDK
- User wants to send tweets, post replies, like, repost, follow, unfollow, or send DMs
- User wants to run a giveaway draw from tweet replies
- User needs real-time monitoring of an X account (new tweets, follower changes)
- User wants webhook delivery of monitored events
- User wants the Hermes Tweet Hermes Agent plugin with `tweet_explore`, `tweet_read`, and approval-gated `tweet_action`
- User wants the TweetClaw OpenClaw plugin instead of direct REST or MCP setup
- User asks about trending topics on X

## Setup

### Install the Skill

```bash
npx skills add Xquik-dev/x-twitter-scraper
```

Or clone manually into your agent's skills directory:

```bash
# Claude Code
git clone https://github.com/Xquik-dev/x-twitter-scraper.git .claude/skills/x-twitter-scraper

# Cursor / Codex / Gemini CLI / Copilot
git clone https://github.com/Xquik-dev/x-twitter-scraper.git .agents/skills/x-twitter-scraper
```

### Use the Hermes Agent Plugin

For Hermes Agent runtime tools, install Hermes Tweet. It wraps the same Xquik API with `tweet_explore` for endpoint discovery, `tweet_read` for read-only calls, and approval-gated `tweet_action` for writes and private actions.

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Use Hermes Tweet when a Hermes Agent should search Twitter/X, read tweet replies, look up users, export followers, monitor tweets, post tweets, post replies, send DMs, or automate X actions with explicit approval gates.

### Use the OpenClaw Plugin

For OpenClaw runtime tools, install TweetClaw. It wraps the same Xquik API with `explore` for endpoint discovery and `tweetclaw` for approved calls.

```bash
openclaw plugins install @xquik/tweetclaw
```

Use TweetClaw when the agent should search tweets, post tweets, post replies, send DMs, export followers, download media, create monitors, deliver webhooks, or run giveaway draws from OpenClaw.

### Get an API Key

1. Sign up at [xquik.com](https://xquik.com)
2. Generate an API key from the dashboard
3. Set it as an environment variable or pass it directly

```bash
export XQUIK_API_KEY="xq_YOUR_KEY_HERE"
```

## Capabilities

| Capability | Description |
|---|---|
| Tweet Search | Find tweets by keyword, hashtag, from:user, "exact phrase", and advanced operators |
| User Lookup | Profile info, bio, follower/following counts |
| Tweet Lookup | Full metrics: likes, retweets, replies, quotes, views, bookmarks |
| Follow Check | Check if A follows B (both directions) |
| Trending Topics | Top trends by region (free, no quota) |
| Account Monitoring | Track new tweets, replies, retweets, quotes, follower changes |
| Webhooks | HMAC-signed real-time event delivery to your endpoint |
| Giveaway Draws | Random winner selection from tweet replies with filters |
| 23 Extraction Tools | Followers, following, verified followers, mentions, posts, replies, reposts, quotes, threads, articles, communities, lists, Spaces, people search, media, likes, and more |
| Write Actions | Send tweets, post replies, like, repost, follow, unfollow, and send DMs after explicit approval |
| SDKs | Official TypeScript, Python, Ruby, Go, Kotlin, Java, PHP, C#, CLI, and Terraform clients |
| MCP Server | StreamableHTTP endpoint for AI-native integrations |
| Hermes Tweet Hermes Agent Plugin | Installable `hermes-tweet` runtime with `tweet_explore`, `tweet_read`, and approval-gated `tweet_action` tools |
| TweetClaw OpenClaw Plugin | Installable `@xquik/tweetclaw` runtime with `explore` and `tweetclaw` tools |

## Examples

**Search tweets:**
```
"Search X for tweets about 'claude code' from the last week"
```

**Look up a user:**
```
"Who is @elonmusk? Show me their profile and follower count"
```

**Check engagement:**
```
"How many likes and retweets does this tweet have? https://x.com/..."
```

**Run a giveaway:**
```
"Pick 3 random winners from the replies to this tweet"
```

**Monitor an account:**
```
"Monitor @openai for new tweets and notify me via webhook"
```

**Use Hermes Agent:**
```
"Use Hermes Tweet to search Twitter/X for this launch, read the tweet replies, and prepare a draft reply for approval"
```

**Bulk extraction:**
```
"Extract all followers of @anthropic"
```

**Post a reply:**
```
"Draft and post a reply to this tweet after I approve the final text"
```

## API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/x/tweets/{id}` | GET | Single tweet with full metrics |
| `/x/tweets/search` | GET | Search tweets |
| `/x/users/{username}` | GET | User profile |
| `/x/followers/check` | GET | Follow relationship |
| `/trends` | GET | Trending topics |
| `/monitors` | POST | Create monitor |
| `/events` | GET | Poll monitored events |
| `/webhooks` | POST | Register webhook |
| `/draws` | POST | Run giveaway draw |
| `/extractions` | POST | Start bulk extraction |
| `/extractions/estimate` | POST | Estimate extraction cost |
| `/drafts` | POST | Create tweet drafts |
| `/styles` | POST | Analyze or apply tweet style |
| `/account` | GET | Account & usage info |

**Base URL:** `https://xquik.com/api/v1`
**Auth:** `x-api-key: xq_...` header
**MCP:** `https://xquik.com/mcp` (StreamableHTTP, same API key)

## Repository

https://github.com/Xquik-dev/x-twitter-scraper

Hermes Tweet Hermes Agent plugin: https://github.com/Xquik-dev/hermes-tweet

TweetClaw OpenClaw plugin: https://github.com/Xquik-dev/tweetclaw

**Maintained By:** [Xquik](https://xquik.com)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---
