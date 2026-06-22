# Studies Agents — LLM-Powered Learning System

## Mission

Transform LLM-based study from passive Q&A into a structured intellectual mastery
system. The foundation combines two complementary resources:

### Core Files (`materials/`)

| File | Purpose |
|------|---------|
| `0_PROMPT_PROFOUND_STUDY.md` | **Intellectual Mastery Protocol v4** — 16-section system prompt that turns any LLM into an elite tutor. Implements 5 modes (Mastery, Decision, Briefing, Interview, Exploration), Trivium+Quadrivium pedagogy, adversarial retrieval, spaced repetition, and mastery testing. |
| `ultimate_learning_methods.md` | **Ultimate Compendium of Learning Methods** — 50+ techniques from neuroscience (Bjork, Roediger), elite universities (Feynman, Oxford tutorial, Harvard case), geniuses (da Vinci, Tesla, Franklin), military (AAR, crawl-walk-run, red teaming), religious traditions (Havruta, Lectio Divina, Ratio Studiorum), sports, and more. |
| `0_PROMPT_PROFOUND_STUDY.md` | Clean `.md` version — ready for NotebookLM upload as source file. |

### How They Relate

- `ultimate_learning_methods.md` = the **research** — what the world knows about learning
- `0_PROMPT_PROFOUND_STUDY.md` = the **executable** — an LLM system prompt that encodes the best of those methods into a teachable protocol

The protocol distills methods from the compendium into operational sections:
- **§7 Trivium** (Grammar→Logic→Rhetoric) = Socratic method + Feynman technique
- **§8 Quadrivium** (Arithmetic→Geometry→Music→Astronomy) = dual coding + structural comprehension
- **§9 Adversarial Retrieval** = red teaming + Talmudic havruta + Tibetan debate
- **§4.3 Remediation Loop** = mastery learning (Bloom) + deliberate practice
- **§11 Retention** = spaced repetition + sleep consolidation + interleaving
- **§5 Expert Schema** = Von Neumann's structural comprehension approach

### NotebookLM Integration

The clean prompt (`0_PROMPT_PROFOUND_STUDY.md`) should be uploaded to ALL NotebookLM
notebooks as a source file named **0_PROMPT_PROFOUND_STUDY**.

Existing notebooks:
- ENGLISH_STUDIES — @john
- PUBLIC_EXAMINATIONS_STUDIES — @temer
- POLITICS_STUDIES — @aristotle
- TORAH_STUDIES — @Parashat_bot
- CERT_AIGP_STUDIES — @badge
- CERT_OCI_AI_FOUNDATIONS_ONE — @badge
- CERT_OCI_FOUNDATIONS — @badge
- CERT_OCI_GENERATIVE_AI_PROFESSIONAL — @badge
- CERT_OCI_ARCHITECT_PROFESSIONAL — @badge
- CERT_OCI_MULTICLOUD_ARCHITECT_PROFESSIONAL — @badge

### Agent Directory Structure

- `badge/` — Certification studies (OCI, AIGP)
- `john/` — English studies
- `temer/` — Concurso TCU (12 disciplines)
- `aristotle/` — Philosophy studies
- `dev/` — Python/development studies
- `calculus/` — ML/engineering math
- `showcase/` — Portfolio studies
- `certifications/` — Certificate resources
- `materials/` — Shared study materials & system prompts
- `portuguese/` — (DEPRECATED)
- `eduardo/` — (DEPRECATED)
