---
title: Глубина конвейера
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - pipeline
  - adaptive-compute
---

# Глубина конвейера (Pipeline Depth)

## Определение

**Глубина конвейера** — количество агентов, задействованных на данном запросе. Меньшая глубина = меньше вычислений и быстрее ответ. Большая добавляет ревьюера для контроля качества. Глубину выбирает классификатор вместе с ярусом.

Минимальная глубина: ретривер → резонер. Полная: ретривер → резонер → ревьюер.

## Как это работает в системе

Таблица стратегий классификатора (см. [fpf-classifier](../agents/fpf-classifier.md)) сопоставляет каждому сочетанию burden/tier конкретную глубину и бюджет:

| Ярус | Примеры burden | Конвейер | Бюджет |
|------|---------------|----------|--------|
| 1 | `term_lookup` | retriever → reasoner | ~800 токенов |
| 1 | `project_alignment`, `language_discovery` | retriever → reasoner | ~1200 токенов |
| 1 | `boundary_unpacking`, `generator_portfolio`, `ethical_assurance`, `trust_assurance` | retriever → reasoner | ~1500 токенов |
| 2 | `semantic` (любой Tier 2) | retriever → reasoner → reviewer | ~2000 токенов |
| 3 | `cross_cutting` | retriever → reasoner → reviewer | ~2500 токенов |

Классификатор выдаёт поля `PIPELINE` и `BUDGET` в своём структурированном выводе; скилл запускает агентов соответствующе.

## Почему адаптивно

Запускать ревьюера на каждом запросе — значит примерно удвоить вычисления без пользы на простых поисках, где шаблонной дисциплины резонера достаточно. Запуск на Tier 2/3 критичен: секции собираются динамически, у резонера больше пространства для дрейфа или галлюцинаций.

Это отражает общий паттерн оркестрации AI — "платить за вычисления только там, где это покупает точность", знакомый по speculative decoding и mixture-of-experts routing.

## Связанные статьи

- [tier](tier.md)
- [agent-team](../architecture/agent-team.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-reviewer](../agents/fpf-reviewer.md)
