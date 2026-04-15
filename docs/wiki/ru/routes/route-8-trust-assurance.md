---
title: "Маршрут 8: Доверие и обоснование"
sources:
  - sections/routes/route-8-trust-assurance.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - trust-assurance
---

# Маршрут 8: Доверие и обоснование (Trust Assurance)

> Источник: `sections/routes/route-8-trust-assurance.md`

## Краткое описание

Срабатывает на вопросы "можно ли доверять этой метрике?", "как агрегировать уверенность без overclaim?", "какова доказательная база этой системы?". На выходе — профиль уверенности по компонентам (формальность, область, надёжность, доказательства), карта зависимостей и явный список пробелов — чтобы слабые звенья были видны.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке, 3 core.
- **Core-секции:** `B.3` (trust & assurance calculus F-G-R with congruence), `B.3.5` (working-model relations & grounding), `B.1` (universal algebra of aggregation).
- **Полная цепочка:** добавляет `B.1.1` (dependency graph & proofs) и `A.6.B` (boundary norm square).

## Статус

Активен. Используется для задачи `trust_assurance`. Шаблон резонера: "Таблица уверенности по компонентам → Пробелы в доказательствах (где уверенность слабее всего) → Рекомендации".

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
