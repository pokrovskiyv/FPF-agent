---
title: "Маршрут 2: Язык и терминология"
sources:
  - sections/routes/route-2-language-discovery.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - language-discovery
---

# Маршрут 2: Язык и терминология (Language Discovery)

> Источник: `sections/routes/route-2-language-discovery.md`

## Краткое описание

Срабатывает на формулировки вроде: "не можем договориться о терминах", "у каждого своё понимание слова", "есть смутная идея, не могу сформулировать", "это слово вызывает путаницу". На выходе — таблица значений по командам, отмеченные зоны риска и заметка-сохранение, чтобы ранние идеи не потерялись, пока словарь стабилизируется.

## Ключевые решения

- **Длина цепочки:** 7 секций при полной загрузке, 3 core.
- **Core-секции:** `C.2.2a` (карта языковых состояний), `A.16` (языковая трансдукция), `A.16.1` (pre-articulation cue pack).
- **Полная цепочка:** добавляет thin-owner профиль (`C.2.LS`), обработку reopen/backoff (`A.16.2`), цикл observe→notice→stabilize→route (`B.4.1`) и абдуктивный промпт (`B.5.2.0`).

## Статус

Активен. Используется для задачи `language_discovery`. Шаблон резонера: "Значения термина по командам → Рекомендация, о каких терминах договариваться в первую очередь".

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
