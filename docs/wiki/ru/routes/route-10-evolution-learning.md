---
title: "Маршрут 10: Эволюция и обучение"
sources:
  - sections/routes/route-10-evolution-learning.md
  - scripts/build_routes.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - route
  - tier-1
  - evolution-learning
---

# Маршрут 10: Эволюция и обучение (Evolution Learning)

> Источник: `sections/routes/route-10-evolution-learning.md`

## Краткое описание

Срабатывает, когда дизайн устарел, а этого никто не замечает; петля обратной связи между эксплуатацией и дизайном не работает; lessons learned постоянно повторяются. На выходе пользователь получает карту текущего цикла с точкой разрыва, план замыкания петли и индикаторы здоровья цикла. Маршрут — один из десяти маршрутов входа Tier-1, генерируемых скриптом `scripts/build_routes.py` (запись `id: 10`, slug `evolution-learning`), который подставляет заголовок и путь к файлу для каждого pattern ID из `sections/metadata.json`.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке, 3 core (заданы как `chain` и `core` в записи маршрута внутри `build_routes.py`).
- **Core-секции:** `B.4` (Canonical Evolution Loop), `B.4.1` (Observe → Notice → Stabilize → Route), `B.5.1` (Explore → Shape → Evidence → Operate).
- **Полная цепочка:** добавляет `A.4` (Temporal Duality & Open-Ended Evolution Principle) и `G.11` (Telemetry-Driven Refresh & Decay Orchestrator).
- **Стратегия загрузки:** минимальная загрузка берёт первые 3 core-секции для простых запросов; полная — все 5 для сложных; при обнаружении стагнации ретривер проверяет `_xref.md` на перекрёстные ссылки.

## Статус

Активен. Используется для задачи `evolution_learning`. Форма вывода резонера: «Карта текущего цикла → Точка разрыва → План замыкания петли → Индикаторы здоровья цикла». Файл перегенерируется при каждом запуске `scripts/build_routes.py` (часть конвейера пересборки), поэтому правки вносятся в генератор и метаданные, а не напрямую в файл маршрута.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу `evolution_learning` и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций (сначала core, затем полную)
- [fpf-reasoner](../agents/fpf-reasoner.md) — применяет загруженные секции и выдаёт вывод на языке пользователя
- [route-chain](../concepts/route-chain.md) — объясняет механизм «маршрут как кэш» (Tier 1)
