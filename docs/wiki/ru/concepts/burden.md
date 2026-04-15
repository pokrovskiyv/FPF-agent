---
title: Burden
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
  - scripts/build_routes.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - classification
---

# Burden

## Определение

В этом проекте **burden** — это имя координационной задачи пользователя. Метка, которую классификатор присваивает после прочтения сообщения — одно из одиннадцати значений: 10 распознанных типов плюс `semantic` (ни один маршрут не подошёл). После назначения burden определяет, какой файл маршрута загрузит ретривер и какой шаблон ответа применит резонер.

"Burden" — намеренно нейтральный внутренний термин проекта. Пользовательскому выводу он **не** показывается — см. [plain-language-contract](../architecture/plain-language-contract.md).

## Как это работает в системе

Классификация burden происходит на втором этапе классификатора. В его промпте есть триггер-таблица:

| Burden | Примеры сигналов | Маршрут |
|--------|-----------------|---------|
| `project_alignment` | "команды не понимают друг друга", "кто за что" | route-1 |
| `language_discovery` | "не договориться о терминах", "смутная идея" | route-2 |
| `boundary_unpacking` | "контракт — каша", "SLA неясен" | route-3 |
| `comparison_selection` | "выбрать из вариантов", "как решить" | route-4 |
| `generator_portfolio` | "state of the art", "обзор области" | route-5 |
| `rewrite_explanation` | "перепиши для другой аудитории" | route-6 |
| `ethical_assurance` | "скрытые предубеждения", "конфликт ценностей" | route-7 |
| `trust_assurance` | "можно ли доверять метрике", "overclaim" | route-8 |
| `composition_aggregation` | "KPI врут", "сумма ≠ целое" | route-9 |
| `evolution_learning` | "дизайн устарел", "петля обратной связи" | route-10 |
| `term_lookup` | явный pattern ID (A.6, E.17, UTS) | поиск в metadata.json |
| `semantic` | сигнал есть, маршрут не совпал | семантический откат |
| `cross_cutting` | совпадают несколько burden | комбинация (Tier 3) |

У резонера есть по одному шаблону ответа на каждый burden — см. [fpf-reasoner](../agents/fpf-reasoner.md).

## Почему именно эти 10

Список burden выведен из наблюдаемого использования FPF-паттернов. Каждый burden соответствует кластеру связанных паттернов в спеке, которые вместе дают полный ответ на соответствующий тип вопроса. Новый burden потребует нового файла маршрута и нового шаблона резонера.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md)
- [route-chain](route-chain.md)
- [tier](tier.md)
- [build_routes](../modules/build_routes.md)
- Статьи маршрутов в `routes/`
