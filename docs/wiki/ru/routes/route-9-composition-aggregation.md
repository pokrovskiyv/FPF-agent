---
title: "Маршрут 9: Композиция и агрегация"
sources:
  - sections/routes/route-9-composition-aggregation.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - composition-aggregation
---

# Маршрут 9: Композиция и агрегация (Composition Aggregation)

> Источник: `sections/routes/route-9-composition-aggregation.md`

## Краткое описание

Срабатывает, когда KPI-дашборды врут, сумма частей не равна целому, или Tool A агрегирует иначе, чем Tool B. На выходе — диагностика, какие инварианты композиции нарушены, карта зависимостей агрегации и конкретные рекомендации по исправлению.

## Ключевые решения

- **Длина цепочки:** 6 секций при полной загрузке, 3 core.
- **Core-секции:** `B.1` (universal algebra of aggregation Γ), `B.1.1` (dependency graph & proofs), `B.1.4` (contextual & temporal aggregation).
- **Полная цепочка:** добавляет `B.1.2` (system-specific aggregation Γ_sys), `B.1.3` (knowledge-specific aggregation Γ_epist), `B.1.5` (order-sensitive method composition Γ_method).

## Статус

Активен. Используется для задачи `composition_aggregation`. Шаблон резонера: "Диагностика (нарушенные инварианты) → Карта зависимостей → План исправлений".

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
