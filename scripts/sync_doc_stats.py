#!/usr/bin/env python3
"""Keep the hard-coded counts in CLAUDE.md and Readme.md in sync with reality.

The spec grows on every upstream sync, so any number written by hand (spec line
count, section count, metadata entries, FAISS vectors, …) drifts and silently
goes wrong. This script recomputes every such number from FPF-Spec.md +
sections/metadata.json (NO `uv` / FAISS index needed — the vector count equals
the number of metadata entries that have a `file`) and rewrites the docs.

Usage:
    python3 scripts/sync_doc_stats.py            # apply: rewrite the docs in place
    python3 scripts/sync_doc_stats.py --check     # report drift, exit 1 if any (gate)

Run as a step of rebuild_all.sh so the docs can never drift past one rebuild.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ── Stats ─────────────────────────────────────────────────────────────


def compute_stats() -> dict:
    spec = ROOT / "FPF-Spec.md"
    spec_bytes = spec.stat().st_size
    spec_lines = spec.read_bytes().count(b"\n")  # match `wc -l` convention

    meta = json.loads((ROOT / "sections" / "metadata.json").read_text(encoding="utf-8"))
    entries = len(meta)
    keywords = sum(len(v.get("keywords", []) or []) for v in meta.values())
    queries = sum(len(v.get("queries", []) or []) for v in meta.values())
    edges = sum(
        len(lst or [])
        for v in meta.values()
        for lst in (v.get("dependencies", {}) or {}).values()
    )
    with_file = sum(1 for v in meta.values() if v.get("file"))

    sections = ROOT / "sections"
    section_files = sum(
        1
        for p in sections.rglob("*.md")
        if p.name not in ("_index.md", "_xref.md")
        and "routes" not in p.parts
        and "embeddings" not in p.parts
        and p.parent != sections  # skip top-level glossary-quick.md / lexical-rules.md
    )
    content_dirs = sum(
        1
        for d in sections.iterdir()
        if d.is_dir() and d.name not in ("routes", "embeddings")
    )
    section_bytes = sum(
        p.stat().st_size
        for p in sections.rglob("*.md")
        if "embeddings" not in p.parts
    )

    return {
        "spec_lines": spec_lines,
        "spec_mb": round(spec_bytes / 1048576, 1),
        "spec_tokens_m": round(spec_bytes / 4 / 1e6, 1),
        "section_files": section_files,
        "section_mb": round(section_bytes / 1048576),
        "content_dirs": content_dirs,
        "entries": entries,
        "keywords": keywords,
        "queries": queries,
        "edges": edges,
        "vectors": with_file,
        "vec_pct": round(with_file / entries * 100),
        "no_file": entries - with_file,
        "faiss_kb": round(with_file * 1024 * 4 / 1024),
    }


# ── Formatting helpers ────────────────────────────────────────────────


def sp(n: int) -> str:
    """12345 -> '12 345' (Russian thin-space grouping used in the docs)."""
    return f"{n:,}".replace(",", " ")


def en(n: int) -> str:
    return f"{n:,}"


def round_to(n: int, base: int) -> int:
    return int(round(n / base) * base)


def plural_ru(n: int, one: str, few: str, many: str) -> str:
    """Pick the Russian noun form for a count."""
    n100, n10 = n % 100, n % 10
    if 11 <= n100 <= 14:
        return many
    if n10 == 1:
        return one
    if 2 <= n10 <= 4:
        return few
    return many


# ── Replacement rules ─────────────────────────────────────────────────
#
# Each rule: (regex, builder). The regex matches the current fragment with the
# number(s) loose (so it finds the line regardless of the stale value); the
# builder returns the corrected fragment from stats. Apply via re.sub.


def build_rules(s: dict) -> dict[str, list[tuple[re.Pattern, str]]]:
    secs = lambda n: f"{n} {plural_ru(n, 'секцию', 'секции', 'секций')}"      # noqa: E731
    secs_gen = lambda n: f"{n} {plural_ru(n, 'секции', 'секций', 'секций')}"  # noqa: E731
    vec_nom = lambda n: f"{n} {plural_ru(n, 'вектор', 'вектора', 'векторов')}"   # noqa: E731
    vec_prep = lambda n: f"{n} {plural_ru(n, 'векторе', 'векторах', 'векторах')}"  # noqa: E731
    files_ru = lambda n: f"{n} {plural_ru(n, 'файл', 'файла', 'файлов')}"     # noqa: E731

    claude = [
        (re.compile(r"specification \(~[\d,]+ lines\) plus"),
         f"specification (~{en(round_to(s['spec_lines'], 1000))} lines) plus"),
        (re.compile(r"decomposed spec \(~\d+ files\), generated"),
         f"decomposed spec (~{round_to(s['section_files'], 10)} files), generated"),
        (re.compile(r"→ sections/ \(~\d+ files\)"),
         f"→ sections/ (~{round_to(s['section_files'], 10)} files)"),
        (re.compile(r"sections/metadata\.json \(\d+ entries\)"),
         f"sections/metadata.json ({s['entries']} entries)"),
        (re.compile(r"it's ~\d+K lines\. Instead"),
         f"it's ~{round(s['spec_lines'] / 1000)}K lines. Instead"),
    ]

    readme = [
        (re.compile(r"на [\d ]+ строк, которую создаёт"),
         f"на {sp(round_to(s['spec_lines'], 1000))} строк, которую создаёт"),
        (re.compile(r"огромная: [\d.]+ MB текста, ~[\d.]+ миллиона токенов"),
         f"огромная: {s['spec_mb']} MB текста, ~{s['spec_tokens_m']} миллиона токенов"),
        (re.compile(r"среди [\d ]+ строк, особенно"),
         f"среди {sp(round_to(s['spec_lines'], 1000))} строк, особенно"),
        (re.compile(r"разобран на [\d ]+ секци\S+ с поисковым"),
         f"разобран на {secs(s['section_files'])} с поисковым"),
        (re.compile(r"Монолитная спецификация \(\d+K строк\) автоматически"),
         f"Монолитная спецификация ({round(s['spec_lines'] / 1000)}K строк) автоматически"),
        (re.compile(r'FPF-Spec\.md<br/><b>[\d ]+ строк</b>'),
         f'FPF-Spec.md<br/><b>{sp(s["spec_lines"])} строк</b>'),
        (re.compile(r'Sections\["[\d ]+ секци\S+<br/>в \d+ директориях"\]'),
         f'Sections["{secs(s["section_files"])}<br/>в {s["content_dirs"]} директориях"]'),
        (re.compile(r'metadata\.json<br/><b>\d+ записей</b>'),
         f'metadata.json<br/><b>{s["entries"]} записей</b>'),
        (re.compile(r'FAISS индекс<br/><b>[\d ]+ вектор\S* × 1024 dim</b>'),
         f'FAISS индекс<br/><b>{vec_nom(s["vectors"])} × 1024 dim</b>'),
        (re.compile(r"На выходе [\d ]+ файл\S+ в \d+ директориях \(~\d+ MB\)\."),
         f"На выходе {files_ru(s['section_files'])} в {s['content_dirs']} директориях (~{s['section_mb']} MB)."),
        (re.compile(r"\| Записей \| \d+ \|"), f"| Записей | {s['entries']} |"),
        (re.compile(r"\| Ключевых слов \| [\d ]+ \|"), f"| Ключевых слов | {sp(s['keywords'])} |"),
        (re.compile(r"\| Пользовательских запросов \| [\d ]+ \|"),
         f"| Пользовательских запросов | {sp(s['queries'])} |"),
        (re.compile(r"\| Рёбер графа зависимостей \| [\d ]+ \|"),
         f"| Рёбер графа зависимостей | {sp(s['edges'])} |"),
        (re.compile(r"\| Записей с файловыми путями \| \d+ \(\d+%\) \|"),
         f"| Записей с файловыми путями | {s['vectors']} ({s['vec_pct']}%) |"),
        (re.compile(r"выразительность для [\d ]+ секци\S+"),
         f"выразительность для {secs_gen(s['vectors'])}"),
        (re.compile(r"Exact search — при [\d ]+ вектор\S+ compression не нужна"),
         f"Exact search — при {vec_prep(s['vectors'])} compression не нужна"),
        (re.compile(r"\| Проиндексировано секций \| \d+ \(из \d+ записей; \d+ preface/ToC-запись[^|]*\) \|"),
         f"| Проиндексировано секций | {s['vectors']} (из {s['entries']} записей; {s['no_file']} preface/ToC-запись без файла секции не индексируется) |"),
        (re.compile(r"\| Размер файла \| \d+ KB = \d+ × 1024 × 4 bytes \(float32\) \|"),
         f"| Размер файла | {s['faiss_kb']} KB = {s['vectors']} × 1024 × 4 bytes (float32) |"),
        (re.compile(r"Полная спецификация — [\d.]+ MB, ~[\d.]+M токенов\."),
         f"Полная спецификация — {s['spec_mb']} MB, ~{s['spec_tokens_m']}M токенов."),
        (re.compile(r"загружает 3-8 секций из \d+ вместо всего монолита"),
         f"загружает 3-8 секций из {s['section_files']} вместо всего монолита"),
        (re.compile(r"\| Контент спецификации \| 3-8 секций \(~6-50K\) \| 0 \| Все [\d ]+ секци\S+ \(~[\d.]+M\) \|"),
         f"| Контент спецификации | 3-8 секций (~6-50K) | 0 | Все {secs(s['section_files'])} (~{s['spec_tokens_m']}M) |"),
        (re.compile(r"\| \*\*Итого на инфраструктуру\*\* \| \*\*55-104K\*\* \| \*\*0\*\* \| \*\*~[\d.]+M \(не помещается\)\*\* \|"),
         f"| **Итого на инфраструктуру** | **55-104K** | **0** | **~{s['spec_tokens_m']}M (не помещается)** |"),
        (re.compile(r"# Монолитная спецификация \(\d+K строк, не читать напрямую\)"),
         f"# Монолитная спецификация ({round(s['spec_lines'] / 1000)}K строк, не читать напрямую)"),
        (re.compile(r"#   \d+ записей: паттерны, зависимости, ключевые слова"),
         f"#   {s['entries']} записей: паттерны, зависимости, ключевые слова"),
        (re.compile(r"\{\d+ директорий\}/      #   [\d ]+ файл\S+ секций по частям A-K"),
         f"{{{s['content_dirs']} директорий}}/      #   {files_ru(s['section_files'])} секций по частям A-K"),
        (re.compile(r"# Спецификация → [\d ]+ секци\S+"),
         f"# Спецификация → {secs(s['section_files'])}"),
    ]
    return {"CLAUDE.md": claude, "Readme.md": readme}


# ── Apply / check ─────────────────────────────────────────────────────


def process(check: bool) -> int:
    stats = compute_stats()
    rules = build_rules(stats)
    drift = []
    for fname, file_rules in rules.items():
        path = ROOT / fname
        text = path.read_text(encoding="utf-8")
        new = text
        for pat, repl in file_rules:
            if not pat.search(new):
                drift.append(f"  [{fname}] rule did not match (doc edited?): {pat.pattern[:60]}")
                continue
            new = pat.sub(lambda _m, r=repl: r, new, count=1)
        if new != text:
            if check:
                drift.append(f"  [{fname}] stale numbers — run sync_doc_stats.py")
            else:
                path.write_text(new, encoding="utf-8")
                print(f"  updated {fname}")

    if check and drift:
        print("doc stats DRIFT:")
        print("\n".join(drift))
        return 1
    if check:
        print("doc stats: up to date ✓")
    else:
        print(f"doc stats synced: spec {sp(stats['spec_lines'])} lines, "
              f"{stats['section_files']} sections, {stats['entries']} entries, "
              f"{stats['vectors']} vectors")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync hard-coded doc stats with reality")
    ap.add_argument("--check", action="store_true", help="report drift, exit 1 if any")
    args = ap.parse_args()
    sys.exit(process(check=args.check))


if __name__ == "__main__":
    main()
