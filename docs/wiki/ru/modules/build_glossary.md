---
title: build_glossary
sources:
  - scripts/build_glossary.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - glossary
---

# build_glossary

> Источник: `scripts/build_glossary.py`

## Назначение

Извлекает 50 самых частых терминов из ключевых слов `sections/metadata.json` и пишет их в `sections/glossary-quick.md` как таблицу "термин → первичный паттерн". Глоссарий используется агентом-резонером как внутренняя карта ориентации (пользователю не показывается).

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `build_glossary` | `(metadata: dict, top_n: int = 50) -> list[dict]` | Считает частоту ключевых слов по всем записям, запоминает первый паттерн, упомянувший каждое слово, возвращает top-N в формате `{term, pattern_id, pattern_title, frequency}` |
| `write_glossary` | `(glossary: list[dict], output_path: Path) -> None` | Пишет markdown-таблицу `\| Термин \| Первичный паттерн \| Название паттерна \|` |
| `main` | `() -> None` | Точка входа argparse (`--metadata`, `--output`) |

## Алгоритм

1. Загружаем `sections/metadata.json`.
2. Для каждой записи проходим по списку `keywords`: нижний регистр, обрезка, фильтр по длине (3–60 символов).
3. Инкрементируем `Counter` и запоминаем первый pattern ID, в котором встретилось слово.
4. Берём `Counter.most_common(50)`.
5. Пишем трёхколоночную таблицу в `sections/glossary-quick.md`.

Позднее агент [fpf-sync](../agents/fpf-sync.md) запускает AI-обогащение этого файла, добавляя четвёртую колонку с простыми определениями — это уже не задача текущего модуля.

## Зависимости

**Импорты:** `argparse`, `json`, `collections.Counter`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** вызывается из `scripts/rebuild_all.sh` (шаг 4). Читает вывод [build_metadata](build_metadata.md)/[enrich_metadata](enrich_metadata.md).

## Связанные статьи

- [build_metadata](build_metadata.md)
- [enrich_metadata](enrich_metadata.md)
- [fpf-sync](../agents/fpf-sync.md) — обогащает глоссарий определениями на обычном языке
- [build-pipeline](../architecture/build-pipeline.md)
