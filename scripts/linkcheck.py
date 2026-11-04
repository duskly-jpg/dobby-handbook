#!/usr/bin/env python3
"""Docs internal-link checker — CI gate for the GitHub Pages site in docs/.

Checks that every relative href/src referenced from docs/*.html and
docs/**/*.md resolves to a real file in the repository, and that the
hard-coded raw.githubusercontent.com eval URL matches the actual file.
External http(s) links are skipped (no network).
"""
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
EVAL_REL = "eval/dobbyeval_v0.json"
RAW_PREFIX = "https://raw.githubusercontent.com/duskly-jpg/dobby-handbook/main/"

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def resolve(base: Path, target: str) -> Path | None:
    """Resolve a relative link against the referencing file's directory."""
    p = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0].strip())
    if not p:
        return None
    return (base / p).resolve()


def main() -> int:
    if not DOCS.is_dir():
        err(f"{DOCS} missing")
        return report()

    pages = sorted(DOCS.rglob("*.html")) + sorted(DOCS.rglob("*.md"))
    print(f"scanning {len(pages)} pages under docs/")
    n_links = 0
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'(?:href|src|data-page)="([^"]+)"', text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "data:", "#")):
                # hard-coded raw URL to our own repo: verify the path exists
                if target.startswith(RAW_PREFIX):
                    rel = target[len(RAW_PREFIX):].split("#")[0].split("?")[0]
                    if not (ROOT / rel).is_file():
                        err(f"{page.relative_to(ROOT)}: raw URL points to missing file: {rel}")
                continue
            dest = resolve(page.parent, target)
            if dest is None:
                continue
            n_links += 1
            if not dest.exists():
                err(f"{page.relative_to(ROOT)}: broken internal link -> {target}")

    if n_links == 0:
        err("no internal links found — checker wired to nothing?")
    else:
        print(f"ok: {n_links} internal links checked")

    if not (ROOT / EVAL_REL).is_file():
        err(f"site links eval set but {EVAL_REL} missing")
    else:
        print(f"ok: {EVAL_REL} present")

    return report()


def report() -> int:
    if errors:
        print(f"FAIL: {len(errors)} violation(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS: docs internal links valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
