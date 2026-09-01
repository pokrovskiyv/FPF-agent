---
title: "Маршрут 5: Портфель подходов"
sources:
  - sections/routes/route-5-generator-portfolio.md
  - scripts/build_routes.py
last_updated: 2026-09-01T00:00:00Z
tags:
  - route
  - tier-1
  - generator-portfolio
---

# Маршрут 5: Портфель подходов (Generator Portfolio)

> Источник: `sections/routes/route-5-generator-portfolio.md`

## Краткое описание

Маршрут 5 срабатывает на запросы «какое состояние дел в X?», «какие подходы существуют для Y?», «нужен переиспользуемый шаблон, чтобы обозреть область / портфель подходов». Он загружает упорядоченную цепочку секций, чтобы резонер выдал обзор школ и подходов, сравнительную таблицу, переиспользуемый шаблон поиска и короткий список того, что стоит развивать. Как и все десять входных маршрутов, он генерируется скриптом `scripts/build_routes.py` из статической таблицы `ROUTES` и достраивается из `sections/metadata.json` (оттуда берутся заголовки и пути к файлам).

## Ключевые решения

- **Сопоставление задачи:** slug маршрута `generator-portfolio` (id `5`); триггер user-says — «What's the state of the art in X? / need a reusable search scaffold / portfolio of approaches».
- **Длина цепочки:** 7 секций при полной загрузке, 3 помечены как core.
- **Core-секции** (минимальная загрузка для простых запросов):
  - `A.0` — Onboarding Glossary (NQD & E/E-LOG)
  - `G.0` — CG-Spec — Frame Standard & Comparability Governance
  - `G.1` — CG-Frame-Ready Generator
- **Полная цепочка** добавляет (для сложных запросов):
  - `G.2` — SoTA Harvester & Synthesis
  - `G.5` — Multi-Method Dispatcher & MethodFamily Registry
  - `B.5.2.1` — Creative Abduction with NQD
  - `C.17` — Creativity-CHR — Characterising Generative Novelty & Value
- **Стратегия загрузки:** минимальная загрузка — первые 3 core-секции; полная загрузка — все 7 секций в порядке цепочки; при обнаружении застоя (stagnation) ретривер обращается к перекрёстным ссылкам в `_xref.md`.

## Статус

Активен. Генерируется скриптом `scripts/build_routes.py` (запись с `id: 5`, `slug: generator-portfolio` в таблице `ROUTES`) и используется командой агентов для задачи координации `generator_portfolio`. Резонер выдаёт результат маршрута на понятном языке: список подходов → сравнительная таблица → переиспользуемый шаблон → короткий список. Идентификаторы секций в цепочке (`A.0`, `G.0`, `G.1`, `G.2`, `G.5`, `B.5.2.1`, `C.17`) синхронизируются со спецификацией через `sections/metadata.json`; повторная генерация маршрутов после синхронизации с upstream заново подставляет их заголовки и пути к файлам.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций (core или полную)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет секции, выдаёт результат на понятном языке
- [route-chain](../concepts/route-chain.md) — как устроены маршруты и цепочки секций
