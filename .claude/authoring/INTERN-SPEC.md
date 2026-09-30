# INTERN-SPEC.md — AI-Native Engineer Internship module contract

The second program on the site (`intern/`). The pages use the same markup vocabulary as AIFDE, so
everything in `PATTERNS.md` applies. The differences are below. Where the two documents disagree,
this one wins for `intern/`.

## Audience and voice
- The reader is an intern who knows basic programming from university: variables, loops, functions,
  OOP and a little SQL. They have not shipped production software.
- A coding agent (Claude Code) writes most of their code. **Teach judgement, not syntax.** Aim for:
  - *what* the concept is
  - *why* it exists
  - *how to recognise* good and bad versions of it in code an agent wrote
  - *how to verify* it works
- Code blocks are for **reading**: short and annotated, with the interesting line called out in a
  `.cm` comment. Keep them to about 25 lines or fewer. Never paste a whole framework tutorial.
- Plain English, second person, opinionated. The concrete example is a Golden Owl-style client
  project: a booking app, e-commerce, a SaaS dashboard.

## Source layout
- Write fragments in `.claude/authoring/intern_src/<code>.html`. Build them with
  `python3 .claude/authoring/intern_build.py <code>` (or `--all`). The build writes
  `intern/modules/<code>.html`. **Never edit the built page by hand.** Edit the fragment and rebuild.
- The build supplies the head, sidebar, badges (Core/Elective, target score, "~N days"), page-nav and
  footer from the `INTERN_MODULES` registry in `assets/site.js`.
- Fragment format:
  ```
  <!-- meta: days=2 -->
        <h1 class="font-display text-2xl md:text-3xl font-bold mt-4 tracking-tight">Title</h1>
        <p class="mt-3 text-[15px] md:text-base text-mute dark:text-mutedark leading-relaxed">Lead…</p>
        <div class="mt-6 callout callout-why"><strong>Why it matters when AI writes the code:</strong> …</div>
  <!-- @@BODY@@ -->
        … Part I … Part IV, the Claude Code section, the trailing sections, and the Resources <ul> …
  ```
- Write in chunks of 400 lines or fewer (create the file, then append).
- A module whose page doesn't exist yet carries `soon: true` in `INTERN_MODULES`. The site then lists
  it as "Coming soon" without a link, and prev/next skips it. **When you ship a page, remove its `soon`
  flag in the same change.** QA fails if a linked module has no page, or if a written page is still marked
  soon.

## Page structure (in this order)
1. Hero: `h1`, lead paragraph, and `callout-why` with the label
   **"Why it matters when AI writes the code:"**.
2. **Exactly 4 Parts**, using the kicker classes for Parts I–IV from PATTERNS §1. Each Part has
   ≥2 `h3`s.
3. `<h2>Working with Claude Code</h2>` (no kicker), with:
   - 2–4 example prompts in `<pre class="code">`
   - a two-up grid: **"Let the agent do"** on the left and **"You must check"** on the right
   - a `callout-warn` listing red flags in AI output for this topic
4. `Skill ladder: what each score looks like`. Labels are 0 No exposure · 1 Awareness ·
   2 Works with support · 3 Works independently · 4 Leads &amp; coaches. `.target` goes on 3 for a Core
   module and on 2 for an Elective one. Follow it with a `callout-tip` "Self-check before claiming 3:" (or "claiming 2:" for an Elective module).
5. `Pitfalls &amp; pro tips`: 4–6 cards, ✗ first and then ✓.
6. `Evidence checklist`: 4–6 `evidence-box` items with stable `data-key`s. The **last** item is
   `font-semibold`, ends with `(mentor evidence ✓)`, and is a small practice task. This task
   replaces labs: it should take a few hours, produce an artifact the intern can show (PR, diagram,
   URL, report), and be possible with Claude Code.
7. `Resources`: 5–8 links to official docs only, in the format from PATTERNS §13.

**No lab cards, no `<dialog>`, no "In the field" section.**

## Density gates (checked by `qa.py --program intern`)
- 500–1,200 lines once built
- ≥3 diagrams, counting SVG `role="img"` and Mermaid together
- ≥3 tables
- ≥6 code blocks
- ≥4 callouts, including at least one `callout-warn`
- 5–8 resources

## Links
- Cross-module links inside the program use `./<code>.html` with the violet style. Link generously
  to the module that owns a topic, for example database design goes to `./sd1.html`.
- Links into AIFDE are allowed for "go deeper" pointers: `../../aifde/modules/fn7.html`.
- External links go to official docs only, always with `target="_blank" rel="noopener"`.

## Topic ownership (avoid duplication)
| Topic | Owner |
|---|---|
| Tickets, task breakdown, estimation, Scrum / Kanban at an agency | CO1 |
| Local setup, version managers, lockfiles, semver, env config, vetting and auditing dependencies | CO5 |
| Naming, functions, code smells, DRY / YAGNI / KISS, safe refactoring, tech debt, practical Big-O | CO6 |
| Claude Code basics (install, CLAUDE.md, permissions, slash commands, context) | AG2 |
| Plan mode, specs, verification loops | AG3 |
| Skills, subagents, hooks, MCP servers in Claude Code, headless / CI | AG5 |
| RAG, tool use, MCP as a protocol, memory, agent loop concepts | AG6 |
| ERD, normalisation, indexes, transactions, migrations | SD1 |
| C4, sequence, deployment, flow diagrams, Mermaid | CO7 |
| Layered / MVC / clean / hexagonal, dependency rule, where business logic lives | SD2 |
| Modular monolith vs microservices, service boundaries, event-driven, sync vs async communication | SD3 |
| GoF creational + structural (factory, builder, singleton vs DI, adapter, decorator, facade, proxy) | SD4 |
| GoF behavioral (strategy, observer, command, state, template method, chain of responsibility / middleware) | SD5 |
| Repository, unit of work, service layer, DTO/mapper, CQRS, transactional outbox, saga | SD6 |
| Cache-aside / write-through, TTL, invalidation, HTTP/CDN caching, Redis | SD7 |
| Queues, background jobs, retries, DLQ, scheduling, pub/sub, idempotent consumers | SD8 |
| Sessions vs JWT, OAuth/OIDC, RBAC/ABAC, IDOR, OWASP Top 10, secrets | SD9 |
| Timeouts, retries/backoff, circuit breaker, rate limiting, idempotency keys, horizontal scaling, read replicas, observability basics | SD10 |
| End-to-end system design walk-throughs combining SD1–SD10 | SD11 |
| Soft delete, audit trail, JSONB, hierarchies, multi-tenancy models and isolation | SD12 |
| Postgres full-text / trigram search, search engines, reporting, materialized views, OLTP vs OLAP | SD13 |
| Money types, payment gateways and state machine, webhooks, reconciliation, ledger | SD14 |
| Third-party API integration, webhooks in and out, data sync, bulk import/export, long-running operations | SD15 |
| Realtime transport and scaling, time zones and scheduling, geo search | SD16 |
| PII and data protection law, retention and deletion, field encryption, feature flags and config | SD17 |
| REST design, validation, errors, OpenAPI | BE1 |
| Unit and integration tests | QA1 |
| Playwright and Playwright MCP | QA2 |
| Definition of Done, PR evidence, CI gates | QA3 |
| Docker and GitHub Actions | OP2 |
| Ownership, questioning business logic, verifying your own work, bug-bash and regression, after-release follow-up and incidents | PP1 |
| Product thinking, trade-offs, prioritisation and focus, responsible AI use, ethics, deliberate learning and self-assessment | PP2 |
| Written and async communication, status and estimates, clients, demos and English, cross-functional work and feedback, mentoring | PP3 |
| EC2, Lambda, ECS auto scaling, SQS/SNS/EventBridge, ElastiCache, SES, CloudWatch alarms, CloudTrail/GuardDuty, KMS, backup/DR, AWS cost management | OP5 |
| CSS layout, Tailwind, class composition (cn/cva), shadcn/ui in code, dark mode, motion | FE3 |
| React Hook Form + Zod, Server Action forms, optimistic UI, URL state, pagination, uploads, realtime on the client | FE4 |
| Vitest + React Testing Library + MSW, a11y checks, frontend lint/type/CI gates | FE5 |
| Core Web Vitals, bundle size, hydration errors, error monitoring, SEO, i18n, frontend security | FE6 |
| Riverpod / Bloc in depth, go_router tabs and redirects, Flutter forms, theming, adaptive layout, l10n, a11y | MB2 |
| Dio interceptors and token refresh, secure storage, offline-first, push notifications, deep links, permissions, device features | MB3 |
| Flutter unit / widget / golden / integration tests, Patrol, analyzer and CI gates | MB4 |
| Flutter performance, crash reporting, mobile CI/CD, store release and rollout, forced update, OTA | MB5 |

## API code
Anthropic API examples use `claude-opus-5-5` / `claude-sonnet-5-5` / `claude-haiku-4-5-20251001`
with no `temperature`, and adaptive thinking where thinking is shown.
