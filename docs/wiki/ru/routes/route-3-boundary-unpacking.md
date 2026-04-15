---
title: "Маршрут 3: Разбор контракта"
sources:
  - sections/routes/route-3-boundary-unpacking.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - boundary-unpacking
---

# Маршрут 3: Разбор контракта (Boundary Unpacking)

> Источник: `sections/routes/route-3-boundary-unpacking.md`

## Краткое описание

Срабатывает, когда у пользователя есть контракт, API-спека, SLA или ТЗ, в которых правила, условия, обязанности и требования к доказательствам перемешаны в кашу. На выходе — структурированная разбивка: что правило, что условие доступа, что обязанность, что нужно доказать.

## Ключевые решения

- **Длина цепочки:** 6 секций при полной загрузке, 3 core.
- **Core-секции:** `A.6` (signature stack и дисциплина границ), `A.6.B` (boundary norm square), `A.6.C` (разбор контракта).
- **Полная цепочка:** добавляет relational precision (`A.6.P`), quality-term precision (`A.6.Q`), action invitation precision (`A.6.A`).
- **Самый большой бюджет** среди маршрутов Tier 1 (1500 токенов) — контракты требуют больше контекста.

## Статус

Активен. Используется для задачи `boundary_unpacking`. Шаблон резонера: "Правила / Условия доступа / Обязанности / Требуемые доказательства" — четыре фиксированных квадранта.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
