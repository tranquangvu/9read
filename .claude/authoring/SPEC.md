# SPEC.md — the expansion contract

You are expanding (or building) one module of the AIFDE Mastery curriculum to **maximum depth**.
`qa.py` enforces everything below. **If qa.py fails, you are not done.**

Read `PATTERNS.md` for the markup vocabulary and `BOUNDARIES.md` for what your module owns
versus what belongs to a sibling module.

---

## 0. The two production modes

### Mode A — expanding an existing module (AI1–AI12)
**Never regenerate the file.** Expand in place with anchored `Edit` calls. The file already
contains unique section markers:

```
<!-- ═══════════════ PART I ═══════════════ -->   … through PART VI
<!-- ═══════════════ skill ladder ═══════════════ -->
<!-- ═══════════════ labs ═══════════════ -->
<!-- ═══════════════ in the field ═══════════════ -->
<!-- ═══════════════ pitfalls ═══════════════ -->
<!-- ═══════════════ evidence & resources ═══════════════ -->
<!-- ═══════════════════════ LAB MODALS ═══════════════════════ -->
```

Anchor every edit on these. In-place editing means you never emit the invariants that could be
damaged (`data-key`s, badges, ladder `.target`, modal ids, footer) — they stay correct by construction.

Runbook:
1. Read the target file in full.
2. Read `PATTERNS.md`. Do **not** read a 3,000-line exemplar — it costs 70K tokens.
3. Emit your Part-by-Part outline in your response before writing anything.
4–9. One `Edit` per Part, I → VI.
10. `Edit`: expand *In the field* + *Pitfalls* (grid grows to 8 cards).
11. `Edit`: evidence checklist — **append new items immediately before the terminal row** (§3).
12. `Edit`: Resources `<ul>` → 8–12 links.
13–16. One `Edit` per lab modal.
17. Run qa.py; fix until green.

### Mode B — building a new module (AI13–AI16)
The file already exists as a stub with the full scaffold, hero, all six Parts, all trailing
sections and 4 lab modals. Expand each Part and each modal in place exactly as in Mode A.
Copy the `<head>` and shell verbatim from a sibling — do not "improve" them.

### The hard write limit
**No single tool call may emit more than 400 lines or 30 KB.** A 3,000-line file cannot be written
in one call — it will be truncated mid-tag. If a Part needs more than 400 lines, split it into two
edits at an `<h3>` boundary. Every edit must end on a closed tag so the file is always valid HTML.

Run qa.py after edits 7, 11 and 15 — catching a structural break early is far cheaper than a
repair pass at the end. If you are killed mid-module, a fresh agent resumes from where the file
currently ends; it never restarts.

---

## 1. Countable gates

| # | Gate | Threshold |
|---|---|---|
| 1 | Total lines | 2,500 – 3,400 |
| 2 | Total words | ≥ 19,000 (blocks line-padding) |
| 3 | Parts | **exactly 6**, kicker classes in the exact colour order, Part I `mt-12`, II–VI `mt-14` |
| 4 | `<h3 class="font-semibold text-lg mt-*">` | ≥ 4 per Part, ≥ 28 total |
| 5 | `<pre class="code">` in the body (excluding modals) | ≥ 26 |
| 6 | `<span class="code-label">` | ≥ 6 |
| 7 | Tables in the `overflow-x-auto rounded-xl` wrapper | ≥ 8 |
| 8 | Inline `<svg role="img">` in a `.diagram-card` | ≥ 4, each using ≥ 2 anim classes |
| 9 | `<pre class="mermaid">` | ≥ 2 |
| 10 | Callouts | ≥ 10, with ≥ 1 each of `callout-info`, `-tip`, `-warn`, `-danger` |
| 11 | Two-up grids `grid sm:grid-cols-2 gap-3` | ≥ 3 |
| 12 | Cross-module links | ≥ 8 distinct target modules, 100 % resolving |
| 13 | Resources `<li>` | 8 – 12 |
| 14 | Lab cards | exactly 4, accents `#0ea5e9` `#14b8a6` `#6d5acd` `#D97757`, card 4 `border-2 border-coral` + `LAB 4 · EVIDENCE` |
| 15 | `<dialog id="labN">` | exactly 4, ids `lab1`–`lab4`, set-equal to `data-modal-open`, `--lab-color` matching its card |
| 16 | Steps per modal | ≥ 8 (Lab 4: ≥ 10); `.step-n` values form `1..N` with no gaps/repeats |
| 17 | `<pre>` per modal | ≥ 5 |
| 18 | Modal `<h4>` | exactly `🎯 Objective`, `📦 Setup`, `🔬 Steps`, `🧯 Troubleshooting`, `✅ Done when` — in order, once each |
| 19 | Troubleshooting bullets per modal | ≥ 4 |
| 20 | Trailing `<h2>`s | present in order: Skill ladder → Hands-on labs → In the field → Pitfalls & pro tips → Evidence checklist → Resources |
| 21 | Ladder | 5 rows, chips `score-0`…`score-4` ascending, exactly one `.target` — on `score-3` if the module is Critical, `score-2` if Supporting |
| 22 | Hero badges | Critical → `badge-critical` "Critical skill" + "Target score: 3 / 4"; Supporting → `badge-neutral` "Supporting skill" + "Target score: 2 / 4". `badge-accent` ends with `· 4 labs` |
| 23 | Evidence checklist | 7 – 9 items, obeying §3 |
| 24 | Structure | doctype, tag balance, all scaffolding ids, footer `AIFDE Mastery · <CODE> <Name>` |

Gate 3 matters: modules currently at 5 Parts must gain a sixth. That new Part is where genuinely
new material goes — not a rename of an existing one.

---

## 2. Do not touch

`<head>` · anti-FOUC script · Tailwind config · shell markup (`#overlay`, `#sidebar`,
`#module-nav`, `#menu-btn`, `[data-theme-toggle]`) · `#page-nav` · footer string ·
`data-modal-open` / `<dialog id>` values · **existing `data-key` values** · the Critical/Supporting
badge and the ladder `.target` row · `assets/site.js` · `assets/site.css` · `aifde/index.html` ·
**any module file other than your own**.

**No new CSS.** `assets/site.css` is closed. Inventing a class is out of spec.

---

## 3. The `data-key` rule — the one that destroys user data

`data-key` values are localStorage keys (`fde-check-<page>-<key>`). Users have ticked these boxes.

- **Never** rename, reorder, delete or renumber an existing key.
- New checklist items go **immediately before the final row** (usually `data-key="report"`), so the
  catalog-evidence item stays last and keeps its `font-semibold` and `(catalog evidence ✓)`.
- New keys are new lowercase slugs matching `^[a-z][a-z0-9-]{2,19}$`, unique within the page, and
  semantically tied to the new Parts or labs — e.g. `effort-sweep`, `attack-corpus`.

If you find yourself typing a key that already exists, stop — you are about to wipe someone's progress.

---

## 4. Voice contract

This prevents drift more effectively than any count.

- The kicker names the territory; the `<h2>` makes a distinct opinionated claim. No `<h2>` is a bare
  noun phrase, and the two never restate each other.
- Every `<h3>` topic earns its place with: **a paragraph of argument → worked code or a table → one
  concrete number or named artifact.** A topic with only prose is not finished.
- Prefer a real worked example over a description of an example. Show the bad output *and* the good one.
- "In the field" is exactly 3 paragraphs: italic scenario · score-2 vs score-3 contrast with **two
  bolded numbers that differ** · the business payoff.
- Score-4 moves are things you would *decline* to build, not more things to add.
- No marketing register. No "leverage", "utilize", "seamless", "robust solution". No emoji outside
  the fixed modal `<h4>` vocabulary.
- Code must be runnable and typo-free. Always show expected output via `<span class="out">`.
- Numbers must be plausible and internally consistent — if you say recall went 41 % → 87 %, the
  later text must not say 89 %.

---

## 5. External links policy

**Official vendor documentation and company engineering blogs only.** Not research papers, not
practitioner blogs, not courses, not listicles.

Good: `docs.anthropic.com`, `platform.claude.com`, `docs.aws.amazon.com`, `cloud.google.com`,
`learn.microsoft.com`, `docs.databricks.com`, `docs.snowflake.com`, `postgresql.org`, `duckdb.org`,
`modelcontextprotocol.io`, `www.anthropic.com/engineering/*`, `qdrant.tech`, `docs.vllm.ai`,
`ollama.com`, official `github.com/<org>` READMEs for the OSS project itself.

Existing links already in a Resources list are **grandfathered** — leave them unless dead. Just
don't add more of that kind.

Every external link: `class="text-coral underline"` + `target="_blank" rel="noopener"`.

---

## 6. Anthropic API — single source of truth

All code examples must match this. Deviating creates 16 modules that contradict each other.

- Model ids: `claude-opus-5` (default), `claude-sonnet-5` (high volume), `claude-haiku-4-5`
  (cheap/fast). **Never append a date suffix.**
- Extended thinking: `thinking={"type": "adaptive"}` plus
  `output_config={"effort": "low"|"medium"|"high"|"xhigh"|"max"}`.
  **`budget_tokens` has been removed and returns 400** on Opus 5 / Sonnet 5 / Opus 4.7+.
- `temperature`, `top_p`, `top_k` are **rejected** on Opus 5 and Sonnet 5 — never put them in an example.
- Assistant-turn prefill returns 400 — use structured outputs (`output_config={"format": {...}}`) instead.
- Stream when `max_tokens` exceeds ~16000; collect with `.get_final_message()`.
- Handle `stop_reason == "refusal"` before reading `content`.
- Prompt caching is a **prefix** match; mark with `cache_control: {"type": "ephemeral"}`.

---

## 7. Definition of done

1. `python3 .claude/authoring/qa.py aifde/modules/<yours>.html` exits 0.
2. Every gate in §1 is met — not approximately, exactly.
3. You touched exactly one file.
4. You can name, for each of your six Parts, the concrete artifact a reader ends up with.
