#!/usr/bin/env python3
"""qa.py — structural + density QA for AIFDE module pages.

Read-only. Exits non-zero if any FAIL is reported.

    python3 .claude/authoring/qa.py --all
    python3 .claude/authoring/qa.py aifde/modules/ai4.html
    python3 .claude/authoring/qa.py --all --density      # add the density gates
    python3 .claude/authoring/qa.py --registry           # registry + counts only
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = ROOT / "aifde" / "modules"
SITE_JS = ROOT / "assets" / "site.js"
INDEX = ROOT / "aifde" / "index.html"
BASELINE = Path(__file__).parent / "datakeys.baseline.json"

FAILS: list[str] = []
WARNS: list[str] = []


def fail(page: str, msg: str) -> None:
    FAILS.append(f"FAIL {page}: {msg}")


def warn(page: str, msg: str) -> None:
    WARNS.append(f"WARN {page}: {msg}")


# ── registry ────────────────────────────────────────────────────────────────
def load_modules() -> list[dict]:
    src = SITE_JS.read_text()
    block = re.search(r"const MODULES = \[(.*?)\n\];", src, re.S).group(1)
    out = []
    for code, name, crit in re.findall(
        r'\{\s*code:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*critical:\s*(true|false)\s*\}', block
    ):
        out.append({"code": code, "name": name, "critical": crit == "true"})
    return out


KICKERS = [
    ("I", "kicker text-sky-600 dark:text-sky-400 mt-12"),
    ("II", "kicker text-viol mt-14"),
    ("III", "kicker text-teal-600 dark:text-teal-400 mt-14"),
    ("IV", "kicker text-amber-600 dark:text-amber-400 mt-14"),
    ("V", "kicker text-rose-500 mt-14"),
    ("VI", "kicker text-indigo-500 dark:text-indigo-400 mt-14"),
]

SCAFFOLD = [
    "<!DOCTYPE html>", '<html lang="en">', "localStorage.getItem('fde-theme')",
    "../../assets/site.css", "../../assets/site.js", "mermaid",
    'id="overlay"', 'id="sidebar"', 'id="module-nav"', 'id="menu-btn"',
    "data-theme-toggle", "data-group-chip", 'id="page-nav"',
]

TRAILING_H2 = [
    "Skill ladder: what each score looks like",
    None,  # "Hands-on labs" or "Hands-on practice"
    "In the field",
    "Pitfalls &amp; pro tips",
    "Evidence checklist",
    "Resources",
]

MODAL_H4 = ["🎯 Objective", "📦 Setup", "🔬 Steps", "🧯 Troubleshooting", "✅ Done when"]

BALANCED = "div article table thead tbody tr dialog pre svg ul ol nav aside main label".split()

LAB_ACCENTS = ["#0ea5e9", "#14b8a6", "#6d5acd", "#D97757"]

VENDOR_OK = re.compile(
    r"^(docs\.|developer\.|developers\.|platform\.|learn\.|cloud\.|api\.|code\.|"
    r"[a-z0-9-]+\.)?(anthropic|claude|openai|aws\.amazon|google|microsoft|databricks|snowflake|"
    r"postgresql|duckdb|modelcontextprotocol|qdrant|vllm|ollama|langchain|llamaindex|pinecone|"
    r"weaviate|redis|supabase|huggingface|voyageai|ragas|promptfoo|langfuse|braintrust|temporal|"
    r"pydantic|fastapi|github|litellm|opentelemetry|vercel|ai-sdk|lmarena|ann-benchmarks|"
    r"astral|livekit|pipecat|together|unsloth|sre\.google|nist|owasp|oauth|openid|ietf|"
    r"martinfowler|simonwillison|hamel|palantir|trychroma|chroma)\.",
)

DENSITY_GATES = [
    ("lines", 2500, 3400), ("words", 19000, None), ("parts", 6, 6),
    ("h3", 28, None), ("code", 26, None), ("code_label", 6, None),
    ("tables", 8, None), ("svg_diagrams", 4, None), ("mermaid", 2, None),
    ("callouts", 10, None), ("twoup", 3, None), ("xlinks", 8, None),
    ("resources", 8, 12),
]


def metrics(html: str) -> dict:
    body = html.split("LAB MODALS")[0]
    return {
        "lines": html.count("\n") + 1,
        "words": len(re.sub(r"<[^>]+>", " ", html).split()),
        "parts": sum(html.count(k) for _, k in KICKERS),
        "h3": len(re.findall(r'<h3 class="font-semibold text-lg mt-\d', html)),
        "code": body.count('<pre class="code'),
        "code_label": html.count('<span class="code-label"'),
        "tables": html.count("overflow-x-auto rounded-xl border"),
        "svg_diagrams": len(re.findall(r'<svg[^>]*role="img"', html)),
        "mermaid": html.count('<pre class="mermaid"'),
        "callouts": len(re.findall(r"callout callout-(info|tip|warn|danger)", html)),
        "twoup": html.count("grid sm:grid-cols-2 gap-3"),
        "xlinks": len(set(re.findall(r'href="\./(\w+)\.html" class="text-viol', html))),
        "resources": _resource_li(html),
    }


def _resource_li(html: str) -> int:
    m = re.search(r"<h2[^>]*>Resources</h2>\s*<ul[^>]*>(.*?)</ul>", html, re.S)
    return m.group(1).count("<li>") if m else 0


def check_structure(path: Path, mods: dict, do_density: bool) -> None:
    page = path.stem
    html = path.read_text()
    code = page.upper()
    meta = mods.get(code)
    if not meta:
        fail(page, f"{code} not in MODULES registry")
        return

    for s in SCAFFOLD:
        if s not in html:
            fail(page, f"missing scaffolding: {s}")

    for tag in BALANCED:
        o = len(re.findall(rf"<{tag}[\s>]", html))
        c = html.count(f"</{tag}>")
        if o != c:
            fail(page, f"tag imbalance <{tag}>: {o} open vs {c} close")

    # Parts must appear in the canonical colour order. Requiring all SIX is an
    # expansion gate (--density); the legacy corpus legitimately has 5-part modules.
    pos = []
    for roman, cls in KICKERS:
        i = html.find(cls)
        if i < 0:
            if do_density:
                fail(page, f"missing Part {roman} kicker ({cls})")
        else:
            pos.append((roman, i))
            if html.count(cls) > 1:
                fail(page, f"Part {roman} kicker appears {html.count(cls)}×")
    if pos != sorted(pos, key=lambda t: t[1]):
        fail(page, "Part kickers are out of order")

    # modal pairing
    opens = set(re.findall(r'data-modal-open="(\w+)"', html))
    dialogs = set(re.findall(r'<dialog id="(\w+)"', html))
    want = {"lab1", "lab2", "lab3", "lab4"}
    if opens != want:
        fail(page, f"data-modal-open = {sorted(opens)}, want lab1..lab4")
    if dialogs != want:
        fail(page, f"dialog ids = {sorted(dialogs)}, want lab1..lab4")

    # lab accents
    for i, accent in enumerate(LAB_ACCENTS, 1):
        if f"--lab-color:{accent}" not in html:
            fail(page, f"lab {i} accent {accent} missing")
    if "LAB 4 · EVIDENCE" not in html:
        fail(page, "LAB 4 · EVIDENCE badge missing")
    if "border-2 border-coral" not in html:
        fail(page, "lab 4 card is not border-2 border-coral")

    # trailing h2s in order
    last = -1
    for want_h2 in TRAILING_H2:
        if want_h2 is None:
            i = max(html.find("Hands-on labs"), html.find("Hands-on practice"))
            label = "Hands-on labs/practice"
        else:
            i = html.find(f">{want_h2}</h2>")
            label = want_h2
        if i < 0:
            fail(page, f"missing trailing section: {label}")
        elif i < last:
            fail(page, f"trailing section out of order: {label}")
        else:
            last = i

    # ladder + badges vs critical flag
    chips = re.findall(r'<span class="score-chip score-(\d)">', html)
    if chips != ["0", "1", "2", "3", "4"]:
        fail(page, f"ladder chips = {chips}, want 0..4")
    targets = re.findall(r'ladder-row target[^>]*>\s*<span class="score-chip score-(\d)"', html)
    want_target = "3" if meta["critical"] else "2"
    if targets != [want_target]:
        fail(page, f"ladder .target on {targets}, want ['{want_target}'] (critical={meta['critical']})")
    if meta["critical"]:
        if "badge-critical" not in html or "Target score: 3 / 4" not in html:
            fail(page, "critical module missing badge-critical / 'Target score: 3 / 4'")
    else:
        if "Target score: 2 / 4" not in html:
            fail(page, "supporting module missing 'Target score: 2 / 4'")
    if not re.search(r'badge badge-accent">[^<]*· 4 labs<', html):
        fail(page, "badge-accent must end with '· 4 labs'")

    # modal internals
    for lab in sorted(want):
        m = re.search(rf'<dialog id="{lab}".*?</dialog>', html, re.S)
        if not m:
            continue
        d = m.group(0)
        h4s = re.findall(r"<h4>([^<]+)</h4>", d)
        if do_density:
            # AI-track expansion uses the exact vocabulary; the FD track has its own wording.
            if h4s != MODAL_H4:
                fail(page, f"{lab} h4 sections = {h4s}, want {MODAL_H4}")
        else:
            # Legacy corpus: 📦 and 🧯 are optional, and 📦 may repeat. Require the
            # present sections to be an ordered subsequence with 🎯 / 🔬 / ✅ mandatory.
            emoji = [h[0] for h in h4s if h and h[0] in "🎯📦🔬🧯✅"]
            deduped = [e for i, e in enumerate(emoji) if i == 0 or e != emoji[i - 1]]
            canon = ["🎯", "📦", "🔬", "🧯", "✅"]
            it = iter(canon)
            if not all(e in it for e in deduped):
                fail(page, f"{lab} modal sections out of canonical order: {deduped}")
            for need in ("🎯", "🔬", "✅"):
                if need not in deduped:
                    fail(page, f"{lab} modal missing mandatory section {need}")
        steps = [int(n) for n in re.findall(r'<div class="step-n">(\d+)</div>', d)]
        if steps != list(range(1, len(steps) + 1)):
            fail(page, f"{lab} step numbers not 1..N: {steps}")
        if do_density:
            need = 10 if lab == "lab4" else 8
            if len(steps) < need:
                fail(page, f"{lab} has {len(steps)} steps, need ≥{need}")
            if d.count("<pre") < 5:
                fail(page, f"{lab} has {d.count('<pre')} <pre>, need ≥5")
            ts = re.search(r"<h4>🧯 Troubleshooting</h4>(.*?)<h4>", d, re.S)
            n = ts.group(1).count("<li>") if ts else 0
            if n < 4:
                fail(page, f"{lab} troubleshooting has {n} bullets, need ≥4")

    # footer
    if f"AIFDE Mastery · {code} " not in html:
        fail(page, f"footer must read 'AIFDE Mastery · {code} <Name>'")

    # links
    for target in set(re.findall(r'href="\./(\w+)\.html"', html)):
        if not (MODULES_DIR / f"{target}.html").exists():
            fail(page, f"dead internal link ./{target}.html")
        elif target.upper() not in mods:
            fail(page, f"link ./{target}.html not in MODULES registry")
    # Only <a> elements — <link rel=preconnect> / <script src> are infrastructure.
    # Match the whole opening tag: target/rel usually follow href.
    for tag in re.findall(r"<a\s[^>]*>", html):
        m = re.search(r'href="(https?://[^"]+)"', tag)
        if not m:
            continue
        href = m.group(1)
        if 'target="_blank"' not in tag or 'rel="noopener"' not in tag:
            fail(page, f"external link missing target/rel: {href[:70]}")
        host = re.sub(r"^https?://", "", href).split("/")[0]
        if not VENDOR_OK.match(host):
            warn(page, f"non-allowlisted domain: {host}")
    if re.search(r'<a[^>]*href="#?"', html):
        fail(page, "empty href")

    # Stale API shapes — only inside code blocks. Naming a removed parameter in
    # prose is how a module teaches the deprecation; that is not drift.
    # Commented-out lines are excluded too: showing a removed parameter in a
    # "BEFORE / AFTER" migration block is how you teach a deprecation.
    code_only = "\n".join(re.findall(r'<pre class="code[^"]*">(.*?)</pre>', html, re.S))
    live = "\n".join(ln for ln in re.sub(r"<[^>]+>", "", code_only).splitlines()
                     if not ln.lstrip().startswith(("#", "//")))
    for bad in ("budget_tokens", "temperature=", "top_p=", "top_k="):
        if bad in live:
            warn(page, f"stale API param in live code: {bad}")
    for m in re.findall(r"claude-[a-z0-9.-]*-20\d{6}", html):
        if m != "claude-haiku-4-5-20251001":
            warn(page, f"date-suffixed model id: {m}")

    if do_density:
        mx = metrics(html)
        for key, lo, hi in DENSITY_GATES:
            v = mx[key]
            if lo is not None and v < lo:
                fail(page, f"{key}={v}, need ≥{lo}")
            if hi is not None and v > hi:
                fail(page, f"{key}={v}, need ≤{hi}")
        for variant in ("info", "tip", "warn", "danger"):
            if f"callout callout-{variant}" not in html:
                fail(page, f"no callout-{variant}")
        # h3 per part
        bounds = [html.find(c) for _, c in KICKERS] + [html.find("Skill ladder: what each")]
        for i, (roman, _) in enumerate(KICKERS):
            if bounds[i] < 0 or bounds[i + 1] < 0:
                continue
            seg = html[bounds[i]:bounds[i + 1]]
            n = len(re.findall(r'<h3 class="font-semibold text-lg mt-\d', seg))
            if n < 4:
                fail(page, f"Part {roman} has {n} h3, need ≥4")


def check_datakeys(paths: list[Path]) -> None:
    if not BASELINE.exists():
        warn("baseline", "datakeys.baseline.json missing — skipping regression check")
        return
    base = json.loads(BASELINE.read_text())
    slug = re.compile(r"^[a-z][a-z0-9-]{1,19}$")
    for p in paths:
        page = p.stem
        html = p.read_text()
        now = re.findall(r'data-key="([^"]+)"', html)
        if len(now) != len(set(now)):
            fail(page, "duplicate data-key values")
        for k in now:
            if not slug.fullmatch(k):
                fail(page, f"data-key '{k}' does not match ^[a-z][a-z0-9-]{{2,19}}$")
        old = base.get(page)
        if not old:
            continue
        missing = [k for k in old if k not in now]
        if missing:
            fail(page, f"data-key(s) deleted or renamed: {missing}  ← DESTROYS USER PROGRESS")
            continue
        if [k for k in now if k in old] != old:
            fail(page, "pre-existing data-key relative order changed")
        if now[-1] != old[-1]:
            fail(page, f"terminal data-key changed: '{old[-1]}' → '{now[-1]}'")
        m = re.findall(r'data-key="[^"]+"[^>]*>\s*<span([^>]*)>([^<]*)', html)
        if m and "font-semibold" not in m[-1][0]:
            fail(page, "final checklist item lost font-semibold")
        if "(catalog evidence ✓)" not in html:
            fail(page, "missing '(catalog evidence ✓)' marker")


def check_registry(mods: list[dict]) -> None:
    codes = [m["code"] for m in mods]
    files = {p.stem.upper() for p in MODULES_DIR.glob("*.html")}
    for c in codes:
        if c not in files:
            fail("registry", f"{c} in MODULES but aifde/modules/{c.lower()}.html missing")
    for f in files:
        if f not in codes:
            fail("registry", f"{f.lower()}.html on disk but not in MODULES")
    n = len(codes)
    per = {g: sum(1 for c in codes if re.match(rf"^{g}\d+$", c)) for g in ("FN", "AI", "PR", "FD")}
    idx = INDEX.read_text()
    js = SITE_JS.read_text()
    for label, needle in (
        ("index skills", f"{n} skills in 4 tracks"),
        ("index pill", f'px-4 py-1.5">{n} modules<'),
        ("site.js blurb", f"A {n}-module curriculum"),
        ("index AI count", f'AI Application Engineering <span class="text-mute dark:text-mutedark font-normal text-sm">· {per["AI"]} modules'),
    ):
        src = js if "site.js" in label else idx
        if needle not in src:
            fail("registry", f"{label} out of date — expected '{needle}'")
    print(f"registry: {n} modules  FN={per['FN']} AI={per['AI']} PR={per['PR']} FD={per['FD']}")


def check_orphans(mods: list[dict]) -> None:
    for code in ("AI13", "AI14", "AI15", "AI16"):
        if code not in {m["code"] for m in mods}:
            continue
        tgt = f'href="./{code.lower()}.html"'
        inbound = [p.stem for p in MODULES_DIR.glob("*.html")
                   if p.stem != code.lower() and tgt in p.read_text()]
        if len(inbound) < 3:
            fail("links", f"{code} has {len(inbound)} inbound links ({inbound}), need ≥3")


def print_table(paths: list[Path]) -> None:
    keys = [k for k, _, _ in DENSITY_GATES]
    print("\n" + "page".ljust(6) + "".join(k[:6].rjust(8) for k in keys))
    for p in sorted(paths):
        mx = metrics(p.read_text())
        print(p.stem.ljust(6) + "".join(str(mx[k]).rjust(8) for k in keys))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--density", action="store_true", help="enforce the density gates")
    ap.add_argument("--registry", action="store_true", help="registry checks only")
    ap.add_argument("--table", action="store_true", help="print the density table")
    a = ap.parse_args()

    mods = load_modules()
    by_code = {m["code"]: m for m in mods}
    check_registry(mods)
    if a.registry:
        return _report()

    paths = ([MODULES_DIR / f"{m['code'].lower()}.html" for m in mods] if a.all
             else [Path(f) for f in a.files])
    paths = [p for p in paths if p.exists()]
    if not paths:
        print("no files to check"); return 1

    for p in paths:
        check_structure(p, by_code, a.density)
    check_datakeys(paths)
    check_orphans(mods)
    if a.table:
        print_table(paths)
    return _report(len(paths))


def _report(n: int = 0) -> int:
    for w in WARNS:
        print(w)
    for f in FAILS:
        print(f)
    print(f"\n{n} file(s) · {len(FAILS)} fail · {len(WARNS)} warn")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
