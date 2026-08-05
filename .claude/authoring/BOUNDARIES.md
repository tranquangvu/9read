# BOUNDARIES.md — who owns what

The AI track now has 16 modules and several adjacent topics. Duplication is the main quality risk:
two modules explaining the same thing at different depths makes both feel padded. Each contract
below is binding on **both** sides — the module that owns a topic goes deep; the neighbour writes
one sentence and a link.

The link form for a hand-off is:
```html
<a href="./ai15.html" class="text-viol underline decoration-viol/40">AI15</a>
```

---

## AI15 Multi-agent Systems ↔ AI6 Agentic Workflow Design ↔ AI7 Frameworks

| Owns | Topic |
|---|---|
| **AI6** | The single agent loop; the five workflow patterns (chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer); planning and reflection; state, checkpointing, resume, cancellation; human-in-the-loop approval |
| **AI15** | Two or more agents with **separate context windows**: role decomposition, handoff protocols as typed contracts, shared state and write conflicts, termination and spend ceilings, replaying and evaluating multi-agent traces |
| **AI7** | Which framework implements any of the above, and the cost of that abstraction |

AI6's "orchestrator–workers" is a *single* model driving sub-tasks. The moment each worker has its
own context window and its own system prompt, it is AI15's territory.

- **AI6 must add** a callout: when to escalate from an orchestrator-workers workflow to genuine
  multi-agent, and the price you pay for it.
- **AI15 must open** Part I with "read AI6 first — you probably don't need this", and its evidence
  lab must be honest enough to conclude "stay single-agent" when the numbers say so.

## AI16 Red-teaming ↔ AI9 Evaluation ↔ PR4 Guardrails & Security

| Owns | Topic |
|---|---|
| **AI9** | The quality harness: golden datasets, grader taxonomy, LLM-as-judge calibration, CI regression gates, online eval |
| **PR4** | The **controls**: input/output filters, injection mitigations, allow/deny policy, secret handling, the security architecture |
| **AI16** | **Adversarial evaluation as a discipline**: attack taxonomy, generating an attack corpus, severity rubrics, automating the red-team in CI, agentic attack surfaces, disclosure and re-test cadence |

AI16 **reuses AI9's harness shape** rather than inventing a second one — say so explicitly and link.
Every AI16 finding maps to a PR4 control as its fix; AI16 never re-teaches the control.

- **AI9's Part V** covers safety as one of several *harder targets* and hands off to AI16 for depth.
- **AI16** never explains how to build a golden set from scratch — it links to AI9.

## AI13 Reasoning Models ↔ AI1 Prompt Engineering ↔ AI2 LLM API Engineering

| Owns | Topic |
|---|---|
| **AI1** | Chain-of-thought and every other prompting technique for **non-reasoning** models; prompts as code |
| **AI2** | The Messages API parameter reference, streaming mechanics, the tool-use loop |
| **AI13** | Adaptive thinking and the effort control; when reasoning **loses**; prompting differences; interleaved thinking in an agent loop; thinking-token economics; verifying the answer rather than the trace |

- **AI1** keeps its CoT section but adds one line: on a reasoning model, explicit CoT prompting is
  largely redundant → AI13.
- **AI2** keeps the parameter table but points the `thinking` / `effort` fields at AI13 for the
  decision, and must carry the "`budget_tokens` is removed, `temperature` is rejected" warning.

## AI14 Text-to-SQL ↔ AI4 RAG ↔ AI5 Vector Databases ↔ FN6 SQL

| Owns | Topic |
|---|---|
| **FN6** | SQL as a language and analytical thinking |
| **AI4** | Retrieval over **unstructured** text |
| **AI5** | The vector store as infrastructure |
| **AI14** | LLM-generated SQL over **structured** data: schema linking, generate–validate–repair, read-only governance, execution accuracy, and the router that decides SQL vs RAG per question |

- **AI14** assumes FN6-level SQL and does not teach joins.
- **AI4** gains a pointer: when the question is "how many / what's the trend", retrieval is the wrong
  tool → AI14.
- The **router** lives in AI14, described from both sides.

---

## Inbound links to the new modules (assign during your rewrite)

Each new module needs ≥3 inbound links so it is reachable from more than the sidebar. If your
module is listed on the left, you must link to the module on the right at least once, in prose,
where it is genuinely relevant:

| Your module | Must link to |
|---|---|
| AI1, AI2, AI6, AI9 | **AI13** |
| AI4, AI5, AI8, AI9 | **AI14** |
| AI3, AI6, AI7 | **AI15** |
| AI3, AI8, AI9 | **AI16** |

---

## The general rule

If you find yourself writing more than one paragraph plus one code block about something another
module owns, stop and replace it with a sentence and a link. Depth in the wrong module reads as
padding in both.
