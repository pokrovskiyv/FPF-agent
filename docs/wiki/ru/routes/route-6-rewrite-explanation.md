---
title: "Маршрут 6: Пересказ для аудитории"
sources:
  - sections/routes/route-6-rewrite-explanation.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - rewrite-explanation
---

# Маршрут 6: Пересказ для аудитории (Rewrite Explanation)

> Источник: `sections/routes/route-6-rewrite-explanation.md`

## Краткое описание

Срабатывает на "перепиши, не меняя смысл", "объясни для другой аудитории", "сравни две версии на верность смыслу". На выходе — переписанный текст с заметками о том, что сохранено и что изменено, плюс профиль верности — чтобы пересказ не превратился в молчаливый перевод.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке (самый короткий маршрут Tier 1), 3 core.
- **Core-секции:** `A.6.3.CR` (conservative retextualization), `A.6.3.RT` (representation transduction), `E.17.EFP` (explanation faithfulness profile).
- **Полная цепочка:** добавляет `E.17.ID.CR` (comparative reading) и `E.17.AUD.LHR` (local head restoration).

## Статус

Активен. Используется для задачи `rewrite_explanation`. Шаблон резонера: "Переписанный текст → Что сохранено → Что изменено (с обоснованием)".

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
