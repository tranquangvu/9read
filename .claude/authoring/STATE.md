# STATE.md — AI-track deep expansion: where things stand

**Branch:** `feat/ai-track-deep-expansion` (branched from `main`)
**Plan:** `/Users/bentran/.claude/plans/review-l-i-c-c-ph-n-memoized-lemon.md`
**Contract:** `SPEC.md` · **Markup:** `PATTERNS.md` · **Topic ownership:** `BOUNDARIES.md` · **Checker:** `qa.py`

## The goal

Expand all 12 existing AI-track modules to maximum depth (2,500–3,400 lines each) and add 4 new
ones, because the AI track was measurably the thinnest of the four (1,137 avg lines / 7,488 avg
words) despite holding 9 of 12 `critical: true` modules. Final target: **48 modules**, AI track the
thickest rather than the thinnest.

User decisions, already made — do not re-litigate:
1. Expand the 12 **and** add AI13–AI16.
2. Depth: maximum, 2.5–3×.
3. Labs: keep exactly 4 per module (Lab 4 = evidence artifact), deepen each.
4. External links: **official vendor docs and company engineering blogs only** — not papers, not
   practitioner blogs, not courses. Pre-existing links are grandfathered.

## Progress: 14 of 16 modules complete

| Module | Lines | Status |
|---|---|---|
| AI2 · LLM API Engineering | 2,845 | ✅ green |
| AI3 · Context Engineering | 2,624 | ✅ committed |
| AI4 · RAG & Enterprise Search | 3,063 | ✅ committed (the exemplar) |
| AI6 · Agentic Workflow Design | 2,968 | ✅ committed |
| AI7 · Agent Frameworks & SDKs | 2,543 | ✅ committed |
| AI9 · AI Evaluation & Regression | 2,676 | ✅ committed |
| AI10 · Fine-tuning & Model Adaptation | 2,952 | ✅ committed |
| AI11 · Multimodal AI | 3,319 | ✅ green |
| AI12 · Open-source & Local Models | 2,500 | ✅ committed |
| AI13 · Reasoning Models & Extended Thinking | 3,080 | ✅ committed (new) |
| AI14 · Text-to-SQL & Structured Data | 2,953 | ✅ committed (new) |
| AI15 · Multi-agent Systems | 2,928 | ✅ committed (new) |
| AI16 · Red-teaming & Adversarial Evaluation | 2,901 | ✅ committed (new) |
| AI8 · Tool Calling & MCP | 3,053 | ✅ committed |
| **AI1 · Prompt Engineering** | 2,501 | ⚠️ **7 gates open** |
| **AI5 · Vector Databases** | 2,550 | ⚠️ **5 gates open** |

## What is left — all of it is lab-modal work

Run this to see the live list:
```sh
python3 .claude/authoring/qa.py aifde/modules/ai1.html aifde/modules/ai5.html aifde/modules/ai8.html --density
```

At time of writing:

**ai1** — `temperature=` still in live code (rejected on Opus 5 / Sonnet 5, would 400); lab3 step
numbers are `[1,2,2,3,4]` (must be 1..N, no repeats) and needs ≥8 steps and ≥4 troubleshooting
bullets; lab4 is missing the `📦 Setup` and `🧯 Troubleshooting` sections and needs ≥10 steps.

**ai5** — lab4 missing `🧯 Troubleshooting`, step numbers `[1,2,3,4,4,5]`, needs ≥10 steps,
≥5 `<pre>`, ≥4 troubleshooting bullets.

**ai8** — lab4 missing `🧯 Troubleshooting`, step numbers `[1,2,3,3,4,5]`, needs ≥10 steps,
≥5 `<pre>`, ≥4 troubleshooting bullets.

Note the recurring pattern: **Lab 4 is where agents run out of steam.** It is the evidence-artifact
lab with the highest bar (≥10 steps) and it sits last in the file.

## How to finish

Three near-identical jobs. For each, launch one agent (or do it inline — it is small) with:

> RESUME an interrupted expansion of `aifde/modules/aiN.html`. Do NOT restart or regenerate — the
> file is valid and nearly complete. Read `.claude/authoring/SPEC.md` and `PATTERNS.md`, then fix
> exactly the gates that `python3 .claude/authoring/qa.py aifde/modules/aiN.html --density` reports.
> All remaining work is inside the `<dialog>` lab modals near the end of the file.
> Rules: no tool call emits >400 lines or >30 KB; every edit ends on a closed tag; step numbers
> across `📦 Setup` + `🔬 Steps` must run 1..N with no gaps or repeats; the five modal `<h4>`
> sections are `🎯 Objective`, `📦 Setup`, `🔬 Steps`, `🧯 Troubleshooting`, `✅ Done when` in that
> order, once each. Do not change lab titles, ids, accents or `--lab-color`. Touch exactly one file.

Then **Wave 4 — integration** (the last task):
1. `python3 .claude/authoring/qa.py --all` → expect zero FAILs across all 48.
2. `python3 .claude/authoring/qa.py aifde/modules/ai{1..16}.html --density --table` → zero fails, zero warns.
3. Browser spot-check: serve with `python3 -m http.server 8899`, open 2–3 modules at 375 px and
   1440 px, light and dark, toggle theme mid-page (mermaid must re-render), open all 4 modals,
   walk prev/next AI12 → AI13 → AI14 → AI15 → AI16 → PR1.
4. Commit per module, then merge to `main`.

## Hard-won gotchas — read before touching anything

1. **`data-key` values are localStorage keys** (`fde-check-<page>-<key>`) holding real user
   progress. Never rename, reorder or delete one. New checklist items go *immediately before the
   terminal key*. Rewording a visible label is fine — only the attribute is frozen. `qa.py` Group D
   compares against `datakeys.baseline.json` and is authoritative.
2. **Do not use `git diff | grep '^-'` as a protected-content guard.** A reworded line looks
   identical to a deletion and produces false alarms. This already happened once on AI10.
3. **Never run `qa.py --all --density`.** The density gates are AI-expansion-specific; applying them
   to the 32 FN/PR/FD modules produces hundreds of meaningless failures. Use `--all` for structure,
   and pass explicit AI file paths for density.
4. **Agents die.** A session limit killed five mid-write. The append-only, ends-on-a-closed-tag
   discipline meant 4 of 5 files stayed valid and ~4,300 lines survived. The one break was a
   `callout` div closed with `</p>`. Always resume, never restart.
5. **API correctness is a live issue across the corpus.** `temperature`/`top_p`/`top_k` are rejected
   on Opus 5 and Sonnet 5; `budget_tokens` is removed; assistant prefill 400s. Several modules
   carried advice that would now fail outright — AI9 had 8 code blocks recommending `temperature=0`
   for reproducible evals. `qa.py` warns only on *live* code (commented BEFORE/AFTER migration
   blocks are teaching, not drift). AI13 is the curriculum's source of truth for this.
6. **Grandfathered domains** live in `domains.baseline.json`, snapshotted from the pre-expansion
   tree. The vendor-docs policy only warns on genuinely new off-policy domains.

## Known cosmetic issue, not gated

`ai2`'s *In the field* has 4 paragraphs where `SPEC.md` §4 specifies exactly 3. Predates this
session's work on that file; `qa.py` does not check it. Trim if you care.

## Out of scope, flagged for later

The FDE skill-matrix sheet on Drive still lists 44 skills and will desync now that the curriculum
is 48. See the `fde-skill-matrix-sheet` memory.
