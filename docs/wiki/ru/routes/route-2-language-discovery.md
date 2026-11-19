---
title: "Маршрут 2: Язык и терминология"
sources:
  - sections/routes/route-2-language-discovery.md
  - scripts/build_routes.py
last_updated: 2026-11-15T07:00:00Z
tags:
  - route
  - tier-1
  - language-discovery
---

# Маршрут 2: Язык и терминология (Language Discovery)

> Источник: `sections/routes/route-2-language-discovery.md`

## Краткое описание

Срабатывает на формулировки вроде: «не можем договориться о терминах», «каждый вкладывает в это слово своё значение», «есть смутная идея, пока не могу её сформулировать», «зреет беспокойство, которое не получается назвать». На выходе маршрут даёт таблицу значений спорных терминов по командам, отмеченные зоны риска (где одно и то же слово несёт расходящиеся смыслы) и заметку-сохранение, чтобы ранние идеи не отбросили, пока словарь стабилизируется.

Это маршрут Tier 1: цепочка секций работает как кэш, поэтому Retriever загружает её напрямую по `id`, не обращаясь к семантическому поиску.

## Ключевые решения

- **Длина цепочки:** 7 секций при полной загрузке, 3 помечены как core. Описана в `scripts/build_routes.py` (`ROUTES`, запись `id: 2`, `slug: "language-discovery"`).
- **Core-секции:** `C.2.2a` (Language-State Chart over CharacteristicSpace: где находится термин на шкале от размытого до устоявшегося), `A.16` (Language-State Moves: как продвигать термин к стабильному определению), `A.16.1` (PreArticulationCuePack: сохранить раннюю интуицию, не выбирая ещё маршрут).
- **Полная цепочка добавляет:** `C.2.LS` (Language-State Facet Profile: публикация трактовок и условий использования), `A.16.2` (Reopen, SketchBackoff, Respecify или Retire языкового состояния), `B.4.1` (Publish Candidate Routes for a Stabilized Cue), `B.5.2.0` (Question Form for Entering Abduction).
- **Стратегия загрузки:** минимальная загрузка использует первые 3 core-секции для простых запросов; полная — все 7 для сложных. При обнаружении застоя (stagnation) Retriever сверяется с `_xref.md` на предмет перекрёстных ссылок.

Файл маршрута генерируется механически функцией `build_route_file()` из `scripts/build_routes.py`: ID паттернов сопоставляются с `sections/metadata.json`, откуда подставляются заголовок и путь к файлу каждой секции, а заголовки обрезаются до 60 символов. Перегенерация маршрута входит в `scripts/rebuild_all.sh` — править `sections/routes/route-2-language-discovery.md` вручную нельзя.

## Цепочка секций

| # | Паттерн | Заголовок | Core? |
|---|---------|-----------|-------|
| 1 | C.2.2a | Language-State Chart over CharacteristicSpace | YES |
| 2 | C.2.LS | Language-State Facet Profile: Publish Readings and Use Conditions | |
| 3 | A.16 | Language-State Moves: Choose the Next Publication and Use of a Term | YES |
| 4 | A.16.1 | PreArticulationCuePack: Preserve an Early Cue Before Choosing a Route | YES |
| 5 | A.16.2 | Reopen, SketchBackoff, Respecify, or Retire a Language-State | |
| 6 | B.4.1 | Publish Candidate Routes for a Stabilized Cue (RoutedCueSet) | |
| 7 | B.5.2.0 | Question Form for Entering Abduction | |

## Статус

Активен. Используется для задачи (burden) `language_discovery`. Шаблон вывода резонера: «Значения термина по командам → отмеченные зоны риска → рекомендация (о каких терминах договариваться в первую очередь)», с заметкой-сохранением для идей, которые ещё находятся в стадии до-артикуляции.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу `language_discovery` и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций по `id` (кэш Tier 1)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет цепочку и формирует таблицу значений по командам
- [route-chain](../concepts/route-chain.md) — как строятся и загружаются цепочки маршрутов
