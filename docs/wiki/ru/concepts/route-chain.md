---
title: Цепочка маршрута
sources:
  - scripts/build_routes.py
  - sections/routes/route-1-project-alignment.md
last_updated: 2026-07-15T17:17:20Z
tags:
  - concept
  - retrieval
  - routes
---

# Цепочка маршрута (Route Chain)

## Определение

**Цепочка маршрута** — упорядоченный список файлов секций, которые ретривер загружает для данного burden. Каждый из 10 маршрутов в `sections/routes/` кодирует одну цепочку: сначала core-секции (отмеченные `YES` в колонке Core — обычно 3, они грузятся для простых запросов), затем дополнительные секции, которые загружаются только когда нужно больше контекста.

Цепочки подобраны вручную — не выведены автоматически — и представляют заведомо хорошую стартовую точку для каждой задачи.

## Как это работает в системе

Цепочки определены как Python-словари в начале [build_routes](../modules/build_routes.md):

```python
{
    "id": 1,
    "slug": "project-alignment",
    "user_says": "Teams don't understand each other...",
    "user_gets": "Map of who owns what...",
    "chain": ["A.1.1", "A.15", "A.15.2", "A.15.3", "B.5.1", "F.11", "F.9", "F.17"],
    "core": ["A.1.1", "A.15", "B.5.1"],
}
```

`build_routes.py` превращает каждый словарь в файл `sections/routes/route-{id}-{slug}.md` функцией `build_route_file()`. В сгенерированном файле — таблица (`| # | Pattern | Title | File | Core? |`), которая разрешает каждый pattern ID в заголовок и путь к файлу из `sections/metadata.json` и помечает core-подмножество значением `YES`. Завершающий блок **Loading Strategy** указывает минимальную загрузку (core-секции) и полную (все секции цепочки).

Например, [Маршрут 1: Project Alignment](../routes/route-1-project-alignment.md) разрешается так:

- **Core (минимальная загрузка):** `A.1.1` (U.BoundedContext Semantic Frame), `A.15` (Role-Method-Work Alignment), `B.5.1` (Explore → Shape → Evidence → Operate).
- **Полная цепочка (8 секций):** три core-секции плюс `A.15.2` (U.WorkPlan), `A.15.3` (SlotFillingsPlanItem), `F.11` (Method Quartet Harmonisation), `F.9` (Alignment & Bridge across Contexts) и `F.17` (Unified Term Sheet).

Во время выполнения ретривер (Mode A, Tier 1):
1. Читает файл маршрута.
2. Сначала грузит core-секции.
3. Если вопрос требует больше контекста — идёт по полной цепочке по порядку.
4. Останавливается при исчерпании бюджета или при достаточном покрытии.

Для пересекающих запросов (Tier 3) ретривер также использует цепочку, но дополняет её семантическими результатами Mode B.

## Почему порядок важен

Порядок в цепочке содержателен: core-паттерны идут первыми, общие — раньше частных, паттерны границ — раньше операционных. Иерархические pattern ID (`A.6` перед `A.6.B`) это усиливают — после дедупликации ретривер сортирует итоги по pattern ID, давая резонеру естественное чтение от общего к частному.

## Связанные статьи

- [fpf-retriever](../agents/fpf-retriever.md)
- [build_routes](../modules/build_routes.md)
- [burden](burden.md)
- [tier](tier.md)
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- Статьи маршрутов в `routes/`
