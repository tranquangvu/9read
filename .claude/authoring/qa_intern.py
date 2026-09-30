#!/usr/bin/env python3
"""qa_intern.py — structural + density QA for the AI-Native Developer Internship (intern/).

Read-only. Exits non-zero on any FAIL. Normally invoked through qa.py:

    python3 .claude/authoring/qa.py --program intern --all
    python3 .claude/authoring/qa.py --program intern intern/modules/ag3.html
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = ROOT / "intern" / "modules"
INDEX = ROOT / "intern" / "index.html"
SITE_JS = ROOT / "assets" / "site.js"

FAILS: list[str] = []
WARNS: list[str] = []
fail = lambda p, m: FAILS.append(f"FAIL {p}: {m}")
warn = lambda p, m: WARNS.append(f"WARN {p}: {m}")

KICKERS = [
    ("I", "kicker text-sky-600 dark:text-sky-400 mt-12"),
    ("II", "kicker text-viol mt-14"),
    ("III", "kicker text-teal-600 dark:text-teal-400 mt-14"),
    ("IV", "kicker text-amber-600 dark:text-amber-400 mt-14"),
]
TRAILING = ["Working with Claude Code", "Skill ladder: what each score looks like",
            "Pitfalls &amp; pro tips", "Evidence checklist", "Resources"]
SCAFFOLD = ["<!DOCTYPE html>", "../../assets/site.css", "../../assets/site.js", "mermaid",
            'id="sidebar"', 'id="module-nav"', 'id="menu-btn"', "data-theme-toggle",
            "data-group-chip", 'id="page-nav"', "callout callout-why"]
BALANCED = "div article table thead tbody tr pre svg ul ol nav aside main label".split()
GATES = [("lines", 500, 1200), ("diagrams", 3, None), ("tables", 3, None),
         ("code", 6, None), ("callouts", 4, None), ("resources", 5, 8)]


def load_modules() -> list[dict]:
    block = re.search(r"const INTERN_MODULES = \[(.*?)\n\];", SITE_JS.read_text(), re.S).group(1)
    return [{"code": c, "name": n, "critical": k == "true", "soon": bool(z)} for c, n, k, z in re.findall(
        r'code:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*critical:\s*(true|false)(,\s*soon:\s*true)?', block)]


def metrics(html: str) -> dict:
    m = re.search(r"<h2[^>]*>Resources</h2>\s*<ul[^>]*>(.*?)</ul>", html, re.S)
    return {
        "lines": html.count("\n") + 1,
        "diagrams": len(re.findall(r'<svg[^>]*role="img"', html)) + html.count('<pre class="mermaid"'),
        "tables": html.count("overflow-x-auto rounded-xl border"),
        "code": html.count('<pre class="code'),
        "callouts": len(re.findall(r"callout callout-(info|tip|warn|danger)", html)),
        "resources": m.group(1).count("<li>") if m else 0,
    }


def check_page(path: Path, mods: dict) -> None:
    page, html = path.stem, path.read_text()
    meta = mods.get(page.upper())
    if not meta:
        return fail(page, "not in INTERN_MODULES registry")
    for s in SCAFFOLD:
        if s not in html:
            fail(page, f"missing scaffolding: {s}")
    for tag in BALANCED:
        o, c = len(re.findall(rf"<{tag}[\s>]", html)), html.count(f"</{tag}>")
        if o != c:
            fail(page, f"tag imbalance <{tag}>: {o} open vs {c} close")
    if "<dialog" in html or "lab-card" in html:
        fail(page, "labs are not used in the intern program")
    if "Why it matters when AI writes the code:" not in html:
        fail(page, "callout-why must start 'Why it matters when AI writes the code:'")

    pos = []
    for roman, cls in KICKERS:
        n = html.count(cls)
        if n != 1:
            fail(page, f"Part {roman} kicker appears {n}×, want 1")
        pos.append(html.find(cls))
    if "kicker text-rose-500" in html:
        fail(page, "intern modules have exactly 4 Parts")
    if pos != sorted(pos):
        fail(page, "Part kickers out of order")
    bounds = pos + [html.find(">Working with Claude Code</h2>")]
    for i, (roman, _) in enumerate(KICKERS):
        if min(bounds[i], bounds[i + 1]) < 0:
            continue
        if len(re.findall(r'<h3 class="font-semibold text-lg', html[bounds[i]:bounds[i + 1]])) < 2:
            fail(page, f"Part {roman} needs ≥2 h3")

    last = -1
    for h in TRAILING:
        i = html.find(f">{h}</h2>")
        if i < 0:
            fail(page, f"missing section: {h}")
        elif i < last:
            fail(page, f"section out of order: {h}")
        else:
            last = i
    cc = html[html.find(">Working with Claude Code</h2>"):html.find(">Skill ladder:")]
    for need in ("Let the agent do", "You must check", "callout callout-warn"):
        if need not in cc:
            fail(page, f"Claude Code section missing '{need}'")

    chips = re.findall(r'<span class="score-chip score-(\d)">', html)
    if chips != list("01234"):
        fail(page, f"ladder chips = {chips}")
    tgt = re.findall(r'ladder-row target[^>]*>\s*<span class="score-chip score-(\d)"', html)
    want = "3" if meta["critical"] else "2"
    if tgt != [want]:
        fail(page, f"ladder target on {tgt}, want ['{want}']")

    keys = re.findall(r'data-key="([^"]+)"', html)
    if not 4 <= len(keys) <= 6:
        fail(page, f"{len(keys)} checklist items, want 4–6")
    if len(keys) != len(set(keys)):
        fail(page, "duplicate data-key")
    for k in keys:
        if not re.fullmatch(r"[a-z][a-z0-9-]{1,19}", k):
            fail(page, f"bad data-key '{k}'")
    items = re.findall(r'data-key="[^"]+"[^>]*>\s*<span([^>]*)>(.*?)</span>\s*</label>', html, re.S)
    if items and ("font-semibold" not in items[-1][0] or "(mentor evidence ✓)" not in items[-1][1]):
        fail(page, "last checklist item must be font-semibold and end '(mentor evidence ✓)'")

    if f"AI-Native Developer Internship · {page.upper()} " not in html:
        fail(page, "footer mismatch — rebuild with intern_build.py")

    for t in set(re.findall(r'href="\./(\w+)\.html"', html)):
        if t.upper() not in mods:
            fail(page, f"dead internal link ./{t}.html")
    for t in set(re.findall(r'href="\.\./\.\./aifde/modules/(\w+)\.html"', html)):
        if not (ROOT / "aifde" / "modules" / f"{t}.html").exists():
            fail(page, f"dead AIFDE link {t}.html")
    for tag in re.findall(r"<a\s[^>]*>", html):
        if re.search(r'href="https?://', tag) and ('target="_blank"' not in tag or 'rel="noopener"' not in tag):
            fail(page, "external link missing target/rel")
    code_only = re.sub(r"<[^>]+>", "", "\n".join(re.findall(r'<pre class="code[^"]*">(.*?)</pre>', html, re.S)))
    for bad in ("budget_tokens", "temperature="):
        if bad in code_only:
            warn(page, f"stale API param in code: {bad}")

    mx = metrics(html)
    for key, lo, hi in GATES:
        if lo is not None and mx[key] < lo:
            fail(page, f"{key}={mx[key]}, need ≥{lo}")
        if hi is not None and mx[key] > hi:
            fail(page, f"{key}={mx[key]}, need ≤{hi}")
    if "callout callout-warn" not in html:
        fail(page, "no callout-warn")


def check_registry(mods: list[dict], strict: bool) -> None:
    codes = [m["code"] for m in mods]
    files = {p.stem.upper() for p in MODULES_DIR.glob("*.html")}
    soon = [m["code"] for m in mods if m["soon"]]
    for m in mods:
        if not m["soon"] and m["code"] not in files:
            fail("registry", f"{m['code']} is linked but intern/modules/{m['code'].lower()}.html is missing — write it or mark soon: true")
        if m["soon"] and m["code"] in files:
            fail("registry", f"{m['code']} has a page but is still marked soon: true — remove the flag")
    if soon:
        (fail if strict else warn)("registry", f"not yet written ({len(soon)}): {', '.join(soon)}")
    for p in MODULES_DIR.glob("*.html"):
        for t in set(re.findall(r'href="\./(\w+)\.html"', p.read_text())):
            if t.upper() in soon:
                warn(p.stem, f"links to unwritten module ./{t}.html (404 until it ships)")
    for f in files - set(codes):
        fail("registry", f"{f.lower()}.html on disk but not in INTERN_MODULES")
    idx = INDEX.read_text()
    groups = re.findall(r'id="group-(\w+)"', idx)
    n = len(codes)
    for needle in (f"{n} modules in {len(groups)} tracks", f'px-4 py-1.5">{n} modules<'):
        if needle not in idx:
            fail("registry", f"index count out of date — expected '{needle}'")
    for g in groups:
        k = sum(1 for c in codes if re.match(rf"^{g}\d+$", c))
        if not re.search(rf'gbg-{g}"></span>\s*<h3[^>]*>[^<]*<span[^>]*>· {k} module', idx):
            fail("registry", f"index track {g} count should be {k}")
    print(f"registry: {n} modules, {len(files)} written, {len(groups)} tracks")


def main(argv: list[str]) -> int:
    all_ = "--all" in argv
    table = "--table" in argv
    files = [a for a in argv if not a.startswith("--")]
    mods = load_modules()
    check_registry(mods, strict="--strict" in argv)
    by = {m["code"]: m for m in mods}
    paths = sorted(MODULES_DIR.glob("*.html")) if all_ else [Path(f) for f in files]
    for p in paths:
        check_page(p, by)
    if table:
        keys = [g[0] for g in GATES]
        print("\npage ".ljust(7) + "".join(k[:8].rjust(10) for k in keys))
        for p in paths:
            mx = metrics(p.read_text())
            print(p.stem.ljust(6) + "".join(str(mx[k]).rjust(10) for k in keys))
    for w in WARNS:
        print(w)
    for f in FAILS:
        print(f)
    print(f"\n{len(paths)} file(s) · {len(FAILS)} fail · {len(WARNS)} warn")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
