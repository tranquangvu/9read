#!/usr/bin/env python3
"""intern_build.py — wrap an intern module body fragment in the shared page shell.

Source:  .claude/authoring/intern_src/<code>.html   (fragment, see INTERN-SPEC.md)
Output:  intern/modules/<code>.html                 (full static page, committed)

    python3 .claude/authoring/intern_build.py ag3        # one module
    python3 .claude/authoring/intern_build.py --all      # every fragment present

The fragment starts with a one-line meta comment:
    <!-- meta: days=3 -->
then the hero content (h1, lead <p>, callout-why), then the line
    <!-- @@BODY@@ -->
then everything from Part I down to and including the Resources <ul>.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = HERE / "intern_src"
OUT = ROOT / "intern" / "modules"
HEAD = (HERE / "intern_head.html").read_text()
SITE_JS = (ROOT / "assets" / "site.js").read_text()


def registry() -> dict:
    block = re.search(r"const INTERN_MODULES = \[(.*?)\n\];", SITE_JS, re.S).group(1)
    return {c: (n, k == "true") for c, n, k in re.findall(
        r'code:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*critical:\s*(true|false)', block)}


def esc(s: str) -> str:
    return s.replace("&", "&amp;")


def build(code: str, reg: dict) -> Path:
    src = (SRC / f"{code.lower()}.html").read_text()
    name, core = reg[code.upper()]
    m = re.match(r"\s*<!-- meta: days=([\d.–-]+) -->\n", src)
    if not m:
        raise SystemExit(f"{code}: missing '<!-- meta: days=N -->' first line")
    days = m.group(1)
    hero, body = src[m.end():].split("<!-- @@BODY@@ -->", 1)
    unit = "day" if days == "1" else "days"
    badges = (
        '<span class="badge badge-critical">Core</span>\n'
        '          <span class="badge badge-neutral">Target score: 3 / 4</span>' if core else
        '<span class="badge badge-neutral">Elective</span>\n'
        '          <span class="badge badge-neutral">Target score: 2 / 4</span>'
    )
    page = HEAD.replace("@@TITLE@@", f"{code.upper()} · {esc(name)} — AI-Native Developer Internship")
    page += f"""
<div class="min-h-screen lg:flex">
  <div id="overlay" class="hidden fixed inset-0 bg-black/40 z-30 lg:hidden"></div>
  <aside id="sidebar" class="fixed z-40 inset-y-0 left-0 w-72 -translate-x-full lg:translate-x-0 transition-transform bg-card dark:bg-carddark border-r border-line dark:border-linedark flex flex-col">
    <div class="px-5 py-5 border-b border-line dark:border-linedark">
      <a href="../index.html" class="block">
        <div class="font-display text-lg font-bold leading-tight">AI-Native Developer</div>
        <div class="text-xs text-mute dark:text-mutedark mt-0.5">9-week Internship Program</div>
      </a>
    </div>
    <nav id="module-nav" class="flex-1 overflow-y-auto px-2 py-3"></nav>
  </aside>

  <main class="flex-1 lg:ml-72 min-w-0">
    <!-- floating controls (no header bar) -->
    <button id="menu-btn" aria-label="Toggle menu" class="fixed top-3 left-3 z-20 w-10 h-10 rounded-full border border-line dark:border-linedark bg-card/80 dark:bg-carddark/80 backdrop-blur flex items-center justify-center text-sm hover:border-coral hover:bg-sand dark:hover:bg-sanddark transition-colors"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/></svg></button>
    <button data-theme-toggle class="fixed top-3 right-3 z-20 w-10 h-10 rounded-full border border-line dark:border-linedark bg-card/80 dark:bg-carddark/80 backdrop-blur flex items-center justify-center hover:border-coral hover:bg-sand dark:hover:bg-sanddark transition-colors" aria-label="Toggle theme">
      <span data-theme-icon class="inline-flex align-middle"></span>
    </button>

    <div>
      <article class="max-w-[52rem] mx-auto px-6 pt-20 lg:pt-12 pb-2 prose-fde">
        <div class="flex flex-wrap items-center gap-1.5">
          <span data-group-chip class="badge"></span>
          {badges}
          <span class="badge badge-accent">~{days} {unit} · guided practice</span>
        </div>
{hero.strip(chr(10))}
      </article>
    </div>

    <article class="max-w-[52rem] mx-auto px-6 pb-12 prose-fde">
{body.strip(chr(10))}

      <nav id="page-nav" class="mt-14 flex gap-4"></nav>
    </article>

    <footer class="px-6 py-8 text-center text-xs text-mute dark:text-mutedark">
      AI-Native Developer Internship · {code.upper()} {esc(name)}
    </footer>
  </main>
</div>

</body>
</html>
"""
    out = OUT / f"{code.lower()}.html"
    out.write_text(page)
    return out


def main() -> None:
    reg = registry()
    args = sys.argv[1:]
    codes = [p.stem for p in sorted(SRC.glob("*.html"))] if args == ["--all"] else args
    OUT.mkdir(parents=True, exist_ok=True)
    for c in codes:
        print("built", build(c, reg).relative_to(ROOT))


if __name__ == "__main__":
    main()
