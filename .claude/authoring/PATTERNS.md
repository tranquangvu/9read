# PATTERNS.md — the module markup vocabulary

Every pattern you are allowed to use. **Do not invent classes** — `assets/site.css` is closed for
this project. If a pattern you want isn't here, use the closest one that is.

Tailwind (CDN) is available with a custom palette: `cream/creamdark`, `card/carddark`,
`sand/sanddark`, `ink/inkdark`, `mute/mutedark`, `line/linedark`, `coral{,-deep,-soft,-softdark}`,
`viol{,-soft,-softdark}`; fonts `font-display` (Space Grotesk), `font-body` (Inter), `font-mono`
(JetBrains Mono).

---

## 1. Part section opener

The kicker colour sequence is a **hard convention across all 48 modules**. Part I uses `mt-12`,
Parts II–VI use `mt-14`.

```html
<!-- ═══════════════ PART I ═══════════════ -->
<div class="kicker text-sky-600 dark:text-sky-400 mt-12">Part I · Why &amp; when</div>
<h2 class="font-display text-2xl font-bold mt-2">What problem RAG actually solves</h2>
```

| Part | kicker classes |
|---|---|
| I | `kicker text-sky-600 dark:text-sky-400 mt-12` |
| II | `kicker text-viol mt-14` |
| III | `kicker text-teal-600 dark:text-teal-400 mt-14` |
| IV | `kicker text-amber-600 dark:text-amber-400 mt-14` |
| V | `kicker text-rose-500 mt-14` |
| VI | `kicker text-indigo-500 dark:text-indigo-400 mt-14` |

The kicker names the **territory** (`Ingestion — the unglamorous 60%`). The `<h2>` makes a distinct
**opinionated claim** (`Parse, chunk, enrich, sync`). They never restate each other.

## 2. Headings and prose

```html
<h3 class="font-semibold text-lg mt-7">First h3 in a Part</h3>
<h3 class="font-semibold text-lg mt-8">Every subsequent h3</h3>
<p class="mt-2 text-[15px] leading-relaxed">Under an h3.</p>
<p class="mt-4 text-[15px] leading-relaxed">Directly under an h2, no h3 between.</p>
<p class="mt-3 text-[15px] leading-relaxed">Trailing "so what" after a table/diagram/code block.</p>
```

Inline: `<code class="inline">retry_after</code>`, `<strong>load-bearing claim</strong>`, `<em>emphasis</em>`.

**Cross-module link (violet, code only, no new tab):**
```html
<a href="./ai5.html" class="text-viol underline decoration-viol/40">AI5</a>
```
**External link (coral, new tab):**
```html
<a class="text-coral underline" href="https://docs.anthropic.com/..." target="_blank" rel="noopener">Citations API</a>
```

## 3. Bullet list

```html
<ul class="mt-4 space-y-2 text-[15px] leading-relaxed list-disc pl-5">
  <li><strong>The refusal path is a feature you design</strong>, not an apology: …</li>
</ul>
```

## 4. Table — always inside the scroll wrapper

```html
<div class="mt-4 overflow-x-auto rounded-xl border border-line dark:border-linedark">
  <table class="w-full text-sm bg-card dark:bg-carddark">
    <thead><tr class="text-left text-xs uppercase tracking-wide text-mute dark:text-mutedark border-b border-line dark:border-linedark">
      <th class="px-4 py-3">Approach</th><th class="px-4 py-3">Right when</th><th class="px-4 py-3">Wrong when</th></tr></thead>
    <tbody class="divide-y divide-line dark:divide-linedark align-top">
      <tr><td class="px-4 py-3 font-semibold">RAG</td><td class="px-4 py-3">…</td><td class="px-4 py-3">…</td></tr>
    </tbody>
  </table>
</div>
```
`mt-4` after a paragraph, `mt-3` directly after an `h3`. First column cell is `font-semibold`.
Inside a lab modal use the compact form: `rounded-lg`, `text-xs`, `px-3 py-2`.

## 5. Code block

Span classes: `.cm` comment (grey italic) · `.st` string (amber) · `.kw` keyword (red) ·
`.fn` function/class name (blue) · `.out` expected output (green).

```html
<pre class="code mt-3">RRF_score(chunk) = Σ over retrievers  1 / (60 + rank)
<span class="cm"># 60 is the standard damping constant</span></pre>
```

With a filename tab (use for anything that is a real file — target ≥6 per module):

```html
<div class="mt-4">
  <span class="code-label">rag.py — ingestion</span>
  <pre class="code"><span class="kw">import</span> anthropic, pathlib
<span class="kw">def</span> <span class="fn">chunk</span>(text, size=<span class="st">600</span>):
    <span class="cm"># … </span></pre>
</div>
```

Escape `<`, `>`, `&` inside `<pre>` as `&lt;` `&gt;` `&amp;`.

## 6. Callouts

```html
<div class="mt-4 callout callout-tip"><strong>Score-4 move:</strong> …</div>
```
Variants: `callout-info` (blue, context/aside) · `callout-tip` (green, the score-4-move and
self-check convention) · `callout-warn` (amber, the thing that bites later) · `callout-danger`
(red, the thing that causes an incident). `callout-why` is reserved for the hero — never reuse it.

## 7. Hand-drawn animated SVG

```html
<div class="mt-4 rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark p-5 diagram-card">
  <svg viewBox="0 0 700 210" class="w-full min-w-[620px]" role="img" aria-label="RAG pipelines">
    <text x="12" y="22" font-size="11" font-weight="700" fill="#6E6B64">INGESTION · offline</text>
    <g class="anim-pulse"><rect x="10" y="34" width="120" height="42" rx="9" fill="#2563EB"/>
      <text x="70" y="52" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">Documents</text>
      <text x="70" y="66" text-anchor="middle" fill="#ffffffbb" font-size="9">PDF · wiki · tickets</text></g>
    <g class="anim-pulse d1">…</g><g class="anim-pulse d2">…</g>
    <line x1="130" y1="55" x2="165" y2="55" stroke="#D97757" stroke-width="2" class="anim-flow"/>
  </svg>
</div>
```

Node = `<g class="anim-pulse dN">` + `<rect rx="9">` + bold 11px white title + 9px `#ffffffbb`
subtitle. Connectors = `<line stroke="#D97757" stroke-width="2" class="anim-flow">`.
Node fills reuse the group palette: `#2563EB` blue, `#6d5acd` violet, `#0D9488` teal, `#D97757`
coral, `#DB2777` pink, `#37474F` slate. Static annotations `#6E6B64` / `#A8A49B`.
`min-w-[…]` forces horizontal scroll rather than squashing.

Animation helpers (all auto-disabled under `prefers-reduced-motion`):
- `.anim-pulse` + `.d1 .d2 .d3 .d4` — opacity breathing, staggered 0.4s apart
- `.anim-flow` — marching-ants dashed connector
- `.anim-token` + `.t1 .t2 .t3 .t4` — travels X by `style="--slide:92px"`, for tokens on a wire
- `.anim-bounce` — 4px bob, for a `<text>` callout label

## 8. Mermaid

```html
<div class="mt-3 rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark p-5 diagram-card">
  <pre class="mermaid">
sequenceDiagram
    autonumber
    participant U as User
    participant A as App
    U->>A: "and what about enterprise customers?"
    Note over A: log query, chunks, scores<br/>→ PR1 tracing
  </pre>
</div>
```
`<br/>` inside labels is supported and intentional. Re-themes automatically on dark-mode toggle.

## 9. Two-up concept grid

```html
<div class="mt-4 grid sm:grid-cols-2 gap-3 text-sm">
  <div class="rounded-xl border border-line dark:border-linedark bg-card dark:bg-carddark p-4">
    <div class="font-semibold text-teal-600 dark:text-teal-400">Retrieval metrics
      <span class="font-normal text-xs text-mute dark:text-mutedark">(golden set)</span></div>
    <ul class="mt-2 space-y-1.5 list-disc pl-4 leading-relaxed">
      <li><strong>recall@k</strong> — is the right doc in the top k? The workhorse.</li>
    </ul>
  </div>
</div>
```

## 10. Skill ladder

```html
<h2 class="font-display text-2xl font-bold mt-14">Skill ladder: what each score looks like</h2>
<div class="mt-4 rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark divide-y divide-line dark:divide-linedark text-sm">
  <div class="ladder-row px-5 py-4 flex gap-4 items-start"><span class="score-chip score-0">0</span><div><strong>No exposure.</strong> …</div></div>
  <div class="ladder-row px-5 py-4 flex gap-4 items-start"><span class="score-chip score-1">1</span><div><strong>Awareness.</strong> …</div></div>
  <div class="ladder-row px-5 py-4 flex gap-4 items-start"><span class="score-chip score-2">2</span><div><strong>Works with support.</strong> …</div></div>
  <div class="ladder-row target px-5 py-4 flex gap-4 items-start"><span class="score-chip score-3">3</span><div><strong>Independent production (target).</strong> …</div></div>
  <div class="ladder-row px-5 py-4 flex gap-4 items-start"><span class="score-chip score-4">4</span><div><strong>Leads &amp; coaches.</strong> …</div></div>
</div>
<div class="mt-4 callout callout-tip"><strong>Self-check before claiming 3:</strong> …</div>
```
Labels are fixed. `.target` goes on `score-3` for a Critical module, `score-2` for a Supporting one.

## 11. Lab cards

```html
<div class="mt-5 grid sm:grid-cols-2 gap-4">
  <div class="lab-card rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark p-5" style="--lab-color:#0ea5e9">
    <div class="flex items-center justify-between">
      <span class="text-white text-xs font-bold rounded-md px-2 py-1" style="background:#0ea5e9">LAB 1</span>
      <span class="text-xs text-mute dark:text-mutedark">~2 h</span>
    </div>
    <h3 class="font-semibold mt-3">Minimal RAG, no framework</h3>
    <p class="mt-1.5 text-sm text-mute dark:text-mutedark leading-relaxed">…</p>
    <button data-modal-open="lab1" class="lab-open-btn" aria-label="Open lab"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button>
  </div>
  <!-- … labs 2, 3 with #14b8a6 and #6d5acd … -->
  <div class="lab-card rounded-2xl border-2 border-coral bg-card dark:bg-carddark p-5" style="--lab-color:#D97757">
    <div class="flex items-center justify-between">
      <span class="bg-coral text-white text-xs font-bold rounded-md px-2 py-1">LAB 4 · EVIDENCE</span>
      <span class="text-xs text-mute dark:text-mutedark">~3 h</span>
    </div>
    …
  </div>
</div>
```
Child order inside `.lab-card` is enforced by CSS grid areas: meta `<div>` → `<h3>` → `<p>` → `<button>`.
Accent order is fixed: `#0ea5e9`, `#14b8a6`, `#6d5acd`, `#D97757`.

## 12. Lab modal — after the shell `</div>`, before `</body>`

```html
<dialog id="lab1" class="lab-modal" style="--lab-color:#0ea5e9">
  <div class="modal-head">
    <div>
      <div class="text-[11px] font-bold uppercase tracking-wider opacity-80">Lab 1 · ~2 h</div>
      <div class="font-display font-bold text-lg leading-tight">Minimal RAG, no framework</div>
    </div>
    <button data-modal-close aria-label="Close" title="Close" class="shrink-0 w-9 h-9 rounded-full bg-white/20 hover:bg-white/35 flex items-center justify-center text-base leading-none transition-colors">✕</button>
  </div>
  <div class="modal-body">
    <h4>🎯 Objective</h4>
    <p class="text-sm leading-relaxed mt-1">…</p>

    <h4>📦 Setup</h4>
    <div class="step"><div class="step-n">1</div><div class="step-body">
      Workspace + dependencies:
      <pre class="code">mkdir ai4-labs &amp;&amp; cd ai4-labs &amp;&amp; python3 -m venv .venv &amp;&amp; source .venv/bin/activate</pre>
      <span class="text-mute dark:text-mutedark">Aside in muted text.</span>
    </div></div>

    <h4>🔬 Steps</h4>
    <div class="step"><div class="step-n">2</div><div class="step-body">
      <strong>Ingestion.</strong> Create <code class="inline">rag.py</code>:
      <pre class="code">…</pre>
      Expected: <span class="out">"73 chunks from 10 docs"</span>. Now eyeball 5 random chunks — …
    </div></div>

    <h4>🧯 Troubleshooting</h4>
    <ul class="text-sm space-y-1.5 list-disc pl-5 mt-1 leading-relaxed">
      <li>Voyage 429s → free-tier rate limits; add <code class="inline">time.sleep(1)</code> between batches.</li>
    </ul>

    <h4>✅ Done when</h4>
    <p class="text-sm leading-relaxed mt-1">…</p>
  </div>
</dialog>
```

The five `<h4>`s are a **fixed vocabulary in this exact order, once each** — bare `<h4>`, no classes.
Step numbering is **continuous across Setup and Steps** (Setup is step 1, first Step is 2) and must
form `1..N` with no gaps or repeats. `--lab-color` must match the card's.

## 13. Fixed trailing sections — this exact order

```html
<!-- ═══════════════ skill ladder ═══════════════ -->   Skill ladder: what each score looks like
<!-- ═══════════════ labs ═══════════════ -->           Hands-on labs
<!-- ═══════════════ in the field ═══════════════ -->   In the field
<!-- ═══════════════ pitfalls ═══════════════ -->       Pitfalls &amp; pro tips
<!-- ═══════════════ evidence & resources ═══════════════ -->  Evidence checklist, then Resources
```
All six use `<h2 class="font-display text-2xl font-bold mt-14">`, none has a kicker.

**In the field** — exactly 3 paragraphs in one card:
```html
<div class="mt-4 rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark p-6 text-[15px] leading-relaxed">
  <p><em>Manufacturing customer, 40K documents in SharePoint. The demo dazzled; three weeks in, users say "it can't find things".</em></p>
  <p class="mt-3">The score-2 move is a week of chunk-size fiddling. The score-3 FDE builds a 30-question golden set and measures recall@5: <strong>41%</strong>. … One OCR pass and one BM25 layer later: <strong>87%</strong>.</p>
  <p class="mt-3">The customer's champion forwards that chart to their VP. Renewals are made of moments like this.</p>
</div>
```

**Pitfalls & pro tips** — `✗` cards first, then `✓`:
```html
<div class="mt-4 grid md:grid-cols-2 gap-4 text-sm">
  <div class="rounded-xl border border-line dark:border-linedark bg-card dark:bg-carddark p-5">
    <div class="font-semibold text-rose-500">✗ Tuning without a golden set</div>
    <p class="mt-1.5 leading-relaxed text-mute dark:text-mutedark">…</p>
  </div>
  <div class="rounded-xl border border-line dark:border-linedark bg-card dark:bg-carddark p-5">
    <div class="font-semibold text-emerald-600 dark:text-emerald-400">✓ Log retrieval in production</div>
    <p class="mt-1.5 leading-relaxed text-mute dark:text-mutedark">…</p>
  </div>
</div>
```

**Evidence checklist:**
```html
<div class="mt-4 rounded-2xl border border-line dark:border-linedark bg-card dark:bg-carddark p-6 space-y-3 text-sm">
  <label class="flex gap-3 items-start"><input type="checkbox" class="evidence-box mt-0.5" data-key="minimal"> <span>…</span></label>
  <label class="flex gap-3 items-start"><input type="checkbox" class="evidence-box mt-0.5" data-key="report"> <span class="font-semibold">Produced the … (catalog evidence ✓).</span></label>
</div>
```

**Resources:**
```html
<h2 class="font-display text-2xl font-bold mt-14">Resources</h2>
<ul class="mt-4 space-y-2 text-sm list-disc pl-5">
  <li><a class="text-coral underline" href="https://docs.anthropic.com/en/docs/build-with-claude/citations" target="_blank" rel="noopener">Anthropic — Citations API</a> — span-level attribution as structured output.</li>
  <li><a class="text-coral underline" href="…">Voyage rerank docs</a> · <a class="text-coral underline" href="…">pgvector</a> — the production upgrades for Lab 3 (<a class="text-coral underline" href="./ai5.html">AI5</a>).</li>
</ul>
```
Format is always `<a>Title</a> — one line on why you'd read it / where it's used in this module`.
Vendor docs use the `Vendor — Thing` title form. Two related links may share one `<li>` joined by ` · `.
Internal cross-refs **inside Resources** use coral and no `target="_blank"` (this differs from body prose).

## 14. Page nav and footer — never edit

```html
<nav id="page-nav" class="mt-14 flex gap-4"></nav>
</article>
<footer class="px-6 py-8 text-center text-xs text-mute dark:text-mutedark">
  AIFDE Mastery · AI4 RAG &amp; Enterprise Search
</footer>
```
