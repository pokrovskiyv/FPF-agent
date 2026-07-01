---
title: "Маршрут 9: Композиция и агрегация"
sources:
  - sections/routes/route-9-composition-aggregation.md
  - scripts/build_routes.py
last_updated: 2026-07-01T07:00:00Z
tags:
  - route
  - tier-1
  - composition-aggregation
---

# Маршрут 9: Композиция и агрегация (Composition Aggregation)

> Источник: `sections/routes/route-9-composition-aggregation.md`

## Краткое описание

Срабатывает, когда KPI-дашборды врут, сумма частей не равна целому или инструмент A агрегирует иначе, чем инструмент B. Маршрут загружает цепочку секций части B, описывающих алгебру агрегации и её системные, эпистемические, контекстно-временные и методные варианты. На выходе — диагностика того, какие инварианты композиции нарушены, карта зависимостей агрегации и конкретные рекомендации по исправлению.

Сам файл маршрута генерируется скриптом `scripts/build_routes.py` из таблицы `ROUTES` (запись `id: 9`, slug `composition-aggregation`); заголовки секций и пути к файлам подставляются из `sections/metadata.json`, поэтому при каждой пересборке цепочка остаётся синхронной со спецификацией.

## Ключевые решения

- **Длина цепочки:** 6 секций при полной загрузке, из них 3 помечены как core.
- **Core-секции** (минимальная загрузка для простых запросов): `B.1` (Holon Aggregation and Part-Whole Construction), `B.1.1` (Dependency Structure and Relation Grounding), `B.1.4` (Contextual and Temporal Aggregation).
- **Полная цепочка** (сложные запросы) добавляет: `B.1.2` (System Aggregation and Holon Delimitation), `B.1.3` (Γ_epist — Knowledge-Specific Aggregation), `B.1.5` (Γ_method — Order-Sensitive Method Composition & Work Enactment).
- **Откат при стагнации:** если загрузка цепочки буксует, проверить соответствующий `_xref.md` на перекрёстные ссылки.

## Статус

Активен. Используется для координационной задачи `composition_aggregation`. Шаблон вывода резонера: «Диагностика (нарушенные инварианты) → Карта зависимостей → Рекомендации по исправлению». Генерируется и поддерживается в актуальном состоянии скриптом `scripts/build_routes.py` в рамках `scripts/rebuild_all.sh`.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций (core или полную)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет анализ агрегации к задаче пользователя
- [route-chain](../concepts/route-chain.md) — как маршруты работают как Tier-1 ретрив
