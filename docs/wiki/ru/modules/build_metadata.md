---
title: build_metadata
sources:
  - scripts/build_metadata.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - metadata
---

# build_metadata

> Источник: `scripts/build_metadata.py`

## Назначение

Парсит оглавление из верхней части `FPF-Spec.md` (строки 7–337) в `sections/metadata.json`. Для каждой записи сохраняет pattern ID, название, статус, ключевые слова, пользовательские вопросы и граф зависимостей (`builds_on`, `coordinates_with` и т.д.), затем сопоставляет pattern ID с файлом секции, сканируя `_index.md`, созданные [split_spec](split_spec.md).

Этот предвычисленный индекс позволяет агенту-ретриверу находить секции по pattern ID, ключевому слову или запросу на обычном языке, не читая весь 5.5 МБ монолит.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `find_section_file` | `(pattern_id: str, sections_dir: Path) -> str` | Находит файл паттерна в три этапа: точное совпадение, подстрочное с проверкой границы слов, откат к родителю (B.2.1 → B.2) |
| `parse_keywords` | `(text: str) -> list[str]` | Извлекает ключевые слова через запятую из ячейки `*Keywords:* ...` |
| `parse_queries` | `(text: str) -> list[str]` | Извлекает пользовательские вопросы в кавычках из `*Queries:* "..."` |
| `parse_dependencies` | `(text: str) -> dict` | Разбирает типы связей (`Builds on:`, `Refines:`, `Used by:` и др.) в словарь списков |
| `_split_table_row` | `(line: str) -> list[str]` | Разделяет строку markdown-таблицы по `|`, игнорируя `|` внутри обратных кавычек |
| `parse_toc` | `(spec_path: Path) -> list[dict]` | Читает секцию оглавления, выдаёт по словарю на запись |
| `resolve_files` | `(entries: list[dict], sections_dir: Path) -> list[dict]` | Добавляет поле `file` через `find_section_file` |
| `build_metadata_dict` | `(entries: list[dict]) -> dict` | Преобразует в словарь `{pattern_id: entry}`, для безымянных генерирует ключи вида `preface_1` |
| `main` | `() -> None` | Точка входа argparse (`--spec`, `--sections`, `--output`) |

## Алгоритм

1. Сканируем `FPF-Spec.md` до `# Table of Content`, читаем строки таблиц до следующего H1.
2. Для каждой строки с ≥3 ячейками определяем короткую (3 ячейки) или полную форму (5 ячеек с pattern ID и зависимостями).
3. Извлекаем ключевые слова, вопросы и зависимости из соответствующих ячеек.
4. После парсинга всех строк вызываем `resolve_files` для добавления пути к файлу. При неудаче — откат к родительскому паттерну.
5. Сериализуем словарь в `sections/metadata.json` c `ensure_ascii=False` (сохраняет русские запросы).

## Зависимости

**Импорты:** `argparse`, `json`, `re`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** вызывается из `scripts/rebuild_all.sh` (шаг 2). Потребляется далее: [build_glossary](build_glossary.md), [build_routes](build_routes.md), [build_xrefs](build_xrefs.md), [build_embeddings](build_embeddings.md), [enrich_metadata](enrich_metadata.md).

## Связанные статьи

- [split_spec](split_spec.md) — создаёт структуру директорий, которую сканирует этот модуль
- [enrich_metadata](enrich_metadata.md) — запускается после для добавления пользовательских ключевых слов
- [build-pipeline](../architecture/build-pipeline.md)
