---
title: Команда агентов
sources:
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - agents/fpf-sync.md
  - skills/fpf/SKILL.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - agents
---

# Команда агентов

## Компоненты

Пять агентов, каждый — markdown-промпт в `agents/`:

| Агент | Модуль | Роль |
|-------|--------|------|
| **Classifier** | [fpf-classifier](../agents/fpf-classifier.md) | Решает, есть ли сигнал к обработке, выбирает тир и маршрут, выставляет бюджет |
| **Retriever** | [fpf-retriever](../agents/fpf-retriever.md) | Загружает минимум секций — цепочка маршрута (Mode A) или семантический поиск (Mode B) |
| **Reasoner** | [fpf-reasoner](../agents/fpf-reasoner.md) | Применяет структуру паттерна к задаче пользователя, пишет на обычном языке |
| **Reviewer** | [fpf-reviewer](../agents/fpf-reviewer.md) | Контроль качества: проверка жаргона, обоснованности, применимости (только Tier 2/3) |
| **Sync** | [fpf-sync](../agents/fpf-sync.md) | Сервисное сопровождение по расписанию: sync с upstream + пересборка + AI-обогащение индексов |

## Поток данных

```
сообщение пользователя
     │
     ▼
┌──────────────┐
│ Classifier   │──► SIGNAL? TIER? BURDEN? ROUTE? BUDGET?
└──────────────┘
     │
     ▼
┌──────────────┐        читает: routes/*.md, metadata.json,
│ Retriever    │───────►         _xref.md, semantic_search.py
└──────────────┘
     │
     ▼  содержимое загруженных секций
┌──────────────┐        читает (только внутри): glossary-quick.md,
│ Reasoner     │───────►                          lexical-rules.md
└──────────────┘
     │                    вывод на обычном языке
     │
     ├──► пользователь  (Tier 1 — простой маршрут)
     │
     ▼  (Tier 2/3 или Tier 1 cross-cutting)
┌──────────────┐
│ Reviewer     │──► STATUS: PASS | CORRECTED
└──────────────┘
     │
     ▼
пользователь


(отдельно, по расписанию, без взаимодействия с пользователем)
┌──────────────┐
│ Sync         │──► git pull upstream + rebuild_all.sh + AI-обогащение индексов
└──────────────┘
```

## Решения

- **Разделение ответственности, композиция конвейером.** У каждого агента одна обязанность с чёткими входом и выходом — Classifier только решает, Retriever только грузит, Reasoner только пишет пользовательскую прозу, Reviewer только валидирует. Это держит промпты короткими и независимо тестируемыми.
- **Адаптивная глубина конвейера.** Простые запросы Tier 1: Retriever → Reasoner (~800 токенов). Маршрутные запросы Tier 1: ~1200–1500 токенов. Семантические Tier 2: добавляется Reviewer (~2000 токенов). Комбинированные Tier 3: все три (~2500 токенов). См. [pipeline-depth](../concepts/pipeline-depth.md).
- **Обычный язык — это контракт, а не пожелание.** Принцип #0 резонера и Check 1 ревьюера вместе обеспечивают полное отсутствие FPF-терминологии в выводе. См. [plain-language-contract](plain-language-contract.md).
- **Sync вне конвейера пользовательских запросов.** Работает по расписанию, никогда не запускается на запросах пользователя. Его коммиты проходят через тот же changelog-хук ([update_changelog](../modules/update_changelog.md)), что и обычные коммиты.

## Связанные статьи

- [skill-entry-point](skill-entry-point.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [plain-language-contract](plain-language-contract.md)
- [burden](../concepts/burden.md)
- [tier](../concepts/tier.md)
- [pipeline-depth](../concepts/pipeline-depth.md)
