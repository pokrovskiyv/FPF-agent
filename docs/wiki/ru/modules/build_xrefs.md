---
title: build_xrefs
sources:
  - scripts/build_xrefs.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - cross-references
---

# build_xrefs

> Источник: `scripts/build_xrefs.py`

## Назначение

Строит файл `_xref.md` в каждой директории `sections/` — список входящих перекрёстных ссылок от паттернов **других** Part. Обходит граф зависимостей из `metadata.json` — связи `builds_on`, `refines`, `coordinates_with`, `prerequisite_for`, `constrains`, `informs`, `used_by`, `specialised_by` — и инвертирует их, чтобы каждая директория могла ответить на вопрос "кто от меня зависит?".

Используется ретривером, когда цепочка маршрута не покрывает запрос полностью: он открывает `_xref.md` для поиска паттернов из других Part, ссылающихся на загруженную секцию.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `normalize_pattern_id` | `(raw: str) -> str` | Убирает форматирование, обрезает хвост, через regex проверяет валидный иерархический ID (`A.6.3`, `F.17`, `P-123`) |
| `find_directory_for_pattern` | `(pattern_id, metadata, sections_dir) -> str` | По pattern ID возвращает имя директории верхнего уровня в `sections/` |
| `build_xref_graph` | `(metadata, sections_dir) -> dict` | Инвертирует граф зависимостей в `{target_dir: [{source_pattern, source_dir, target_pattern, relation}]}` |
| `write_xref_files` | `(xrefs, sections_dir) -> int` | Пишет `_xref.md` по директориям, группируя ссылки по исходной директории, с дедупликацией |
| `main` | `() -> None` | Точка входа argparse (`--metadata`, `--sections`) |

## Алгоритм

1. Читаем `metadata.json`.
2. Для каждого исходного паттерна находим его директорию.
3. Для каждого отношения зависимости нормализуем целевой pattern ID и находим его директорию.
4. Пропускаем ссылки внутри одной директории (нам нужны только **межкаталожные**).
5. Аккумулируем `{target_dir: список ссылок}` в defaultdict.
6. Для каждой целевой директории группируем по исходной, дедуплицируем кортежем `(source, relation, target)` и рендерим markdown-таблицу.
7. Пишем `_xref.md` в целевую директорию.

## Зависимости

**Импорты:** `argparse`, `json`, `re`, `collections.defaultdict`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** вызывается из `scripts/rebuild_all.sh` (шаг 7). Читает вывод [build_metadata](build_metadata.md); созданные файлы использует ретривер при расширении через кросс-ссылки (Tier 3).

## Связанные статьи

- [build_metadata](build_metadata.md) — источник графа зависимостей
- [fpf-retriever](../agents/fpf-retriever.md) — использует `_xref.md` для расширения Tier 3
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
