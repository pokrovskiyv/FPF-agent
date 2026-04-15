---
title: "Маршрут 4: Сравнение альтернатив"
sources:
  - sections/routes/route-4-comparison-selection.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - comparison-selection
---

# Маршрут 4: Сравнение альтернатив (Comparison Selection)

> Источник: `sections/routes/route-4-comparison-selection.md`

## Краткое описание

Срабатывает, когда нужно выбрать между альтернативами: "купить, построить или дообучить?", "фреймворк A или B?", "компромиссы непрозрачны". На выходе — таблица критериев решения, рамка сравнения с явно объявленными типами шкал, чек-лист пробелов в данных и рекомендация (или явное "не объявляем победителя — эти ячейки пусты", если данных не хватает).

## Ключевые решения

- **Длина цепочки:** 7 секций при полной загрузке, 3 core.
- **Core-секции:** `A.19` (characteristic space), `G.0` (comparability governance), `A.19.CPM` (unified comparison mechanism).
- **Полная цепочка:** добавляет `A.17` (characteristic rename), `A.18` (minimal CSLC in kernel), `A.19.SelectorMechanism` (selection kernel), `G.5` (multi-method dispatcher).

## Статус

Активен. Используется для задачи `comparison_selection`. Шаблон резонера: "Таблица критериев → Пробелы в данных → Рекомендация". Ключевое проектное ограничение: пустые ячейки остаются пустыми до сбора данных — никаких фальшивых ранжирований.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
