---
title: "Маршрут 4: Сравнение альтернатив"
sources:
  - sections/routes/route-4-comparison-selection.md
  - scripts/build_routes.py
last_updated: 2026-09-01T00:00:00Z
tags:
  - route
  - tier-1
  - comparison-selection
---

# Маршрут 4: Сравнение альтернатив (Comparison Selection)

> Источник: `sections/routes/route-4-comparison-selection.md`

## Краткое описание

Срабатывает, когда нужно выбрать между альтернативами: «купить, построить или дообучить?», «фреймворк A или B?», «компромиссы непрозрачны». На выходе — таблица критериев решения, рамка сравнения с явно объявленными типами шкал, чек-лист пробелов в данных и рекомендация (или явное «не объявляем победителя — эти ячейки пусты», если данных не хватает). Это один из десяти маршрутов входа уровня Tier-1, которые генерирует `scripts/build_routes.py`; его цепочка секций указывает на механику сравнения и выбора в ядре (Часть A) и в наборе паттернов (Часть G).

## Ключевые решения

- **Длина цепочки:** 7 секций при полной загрузке, 3 core. Заданы в `build_routes.py` полями `chain` и `core` для маршрута `comparison-selection`.
- **Core-секции (минимальная загрузка):** `A.19` (CharacteristicSpace & Dynamics Hook), `G.0` (Frame Standard & Comparability Governance, CG-Spec), `A.19.CPM` (Unified Comparison Mechanism).
- **Полная цепочка (в порядке загрузки):** `A.17` (Canonical "Characteristic" & rename, A.CHR-NORM) → `A.18` (Minimal CSLC in Kernel, A.CSLC-KERNEL) → `A.19` (CharacteristicSpace) → `G.0` (Comparability Governance) → `A.19.CPM` (Unified Comparison Mechanism) → `A.19.SelectorMechanism` (Unified Selection Kernel) → `G.5` (Multi-Method Dispatcher & MethodFamily Registry).
- **Стратегия загрузки:** минимальная загрузка читает первые 3 core-секции для простого запроса; полная — все 7 для сложного; при застое смотрим перекрёстные ссылки в `_xref.md`.

## Статус

Активен. Используется для задачи `comparison_selection`. Шаблон резонера: «Таблица критериев → Пробелы в данных → Рекомендация». Ключевое проектное ограничение: пустые ячейки остаются пустыми до сбора данных — никаких ложных ранжирований. Файл маршрута пересобирается скриптом `scripts/build_routes.py` из `sections/metadata.json`, поэтому заголовки секций и пути к файлам в цепочке синхронизируются со спецификацией при каждой пересборке.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу `comparison_selection` и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций (сначала core, затем полную)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет рамку сравнения и строит таблицу критериев
- [route-chain](../concepts/route-chain.md) — объясняет, как маршруты собираются и используются
