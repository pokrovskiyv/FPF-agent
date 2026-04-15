---
title: "Маршрут 5: Портфель подходов"
sources:
  - sections/routes/route-5-generator-portfolio.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - generator-portfolio
---

# Маршрут 5: Портфель подходов (Generator Portfolio)

> Источник: `sections/routes/route-5-generator-portfolio.md`

## Краткое описание

Срабатывает на запросы "какое состояние дел в X?", "какие подходы существуют для Y?", "нужен переиспользуемый шаблон, чтобы обозреть область". На выходе — обзор школ/подходов, сравнительная таблица, шаблон для повторного применения и короткий список кандидатов.

## Ключевые решения

- **Длина цепочки:** 7 секций при полной загрузке, 3 core.
- **Core-секции:** `A.0` (onboarding glossary), `G.0` (comparability governance), `G.1` (CG-frame-ready generator).
- **Полная цепочка:** добавляет `G.2` (SoTA harvester & synthesis), `G.5` (multi-method dispatcher), `B.5.2.1` (creative abduction with NQD), `C.17` (creativity-CHR).
- **Самый большой бюджет** вместе с маршрутом 3 (1500 токенов) — обзоры требуют широкого контекста.

## Статус

Активен. Используется для задачи `generator_portfolio`. Шаблон резонера: "Список подходов → Сравнительная таблица → Переиспользуемый шаблон → Короткий список".

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
