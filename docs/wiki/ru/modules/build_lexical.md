---
title: build_lexical
sources:
  - scripts/build_lexical.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - lexical-rules
---

# build_lexical

> Источник: `scripts/build_lexical.py`

## Назначение

Извлекает обязательные правила замены терминов из Part K `FPF-Spec.md` и пишет их в `sections/lexical-rules.md`. Эти правила говорят резонеру, какие устаревшие термины (например, "ось", "метрика как существительное", "применимость") обязательно заменяются каноничными внутри — пользователь не видит ни той, ни другой формы, но внутренняя согласованность держится именно на этом словаре замен.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `extract_part_k` | `(spec_path: Path) -> str` | Находит H1, начинающийся с "Part K", возвращает его содержимое до следующего H1 верхнего уровня |
| `parse_replacement_table` | `(content: str) -> list[dict]` | Ищет таблицу "Legacy Term", возвращает строки как `{legacy, replace_with, plain_allowance, reference}` |
| `parse_deprecations` | `(content: str) -> list[str]` | Извлекает устаревшие scope-термины из блока "MUST NOT use" |
| `write_lexical_rules` | `(rules, deprecated, output_path: Path) -> None` | Пишет итоговый markdown (таблица замен + список устаревших) |
| `main` | `() -> None` | Точка входа argparse (`--spec`, `--output`) |

## Алгоритм

1. Потоково читаем `FPF-Spec.md`, включаем флаг `in_part_k` на заголовке Part K, выключаем на следующем H1.
2. Внутри Part K ищем заголовок таблицы замен с "Legacy Term" и собираем строки в словари.
3. Парсим блок устаревших терминов: regex-поиск `*emphasised*` слов внутри абзаца "MUST NOT use".
4. Пишем `sections/lexical-rules.md` с двумя разделами: обязательные замены (таблица) и устаревшие scope-термины (список со зачёркиванием).

## Зависимости

**Импорты:** `argparse`, `re`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** вызывается из `scripts/rebuild_all.sh` (шаг 5). Результат читает резонер при каждом вызове.

## Связанные статьи

- [split_spec](split_spec.md)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет правила внутренне
- [plain-language-contract](../architecture/plain-language-contract.md)
- [build-pipeline](../architecture/build-pipeline.md)
