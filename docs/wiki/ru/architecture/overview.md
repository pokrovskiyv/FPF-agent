---
title: Обзор
sources:
  - CLAUDE.md
  - Readme.md
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - overview
---

# Обзор

## Что это за репозиторий

Спецификация **First Principles Framework (FPF)** (~61 000 строк, 5.5 МБ, ~1.3 млн токенов) плюс **Claude Code Skill**, применяющий паттерны FPF к координационным задачам пользователя, при этом сама терминология FPF никогда не попадает наружу.

В проекте четыре подвижных части на диске:

| Слой | Где лежит | Что содержит |
|------|-----------|--------------|
| **Монолит спеки** | `FPF-Spec.md` | Источник истины от upstream; напрямую не редактируется |
| **Декомпозированные секции** | `sections/` | ~240 генерируемых файлов + metadata.json + маршруты + xrefs + FAISS-индекс |
| **Точка входа скилла** | `skills/fpf/SKILL.md` | Логика маршрутизации по burden, читаемая Claude Code |
| **Команда агентов** | `agents/fpf-*.md` | Пять агентов: classifier, retriever, reasoner, reviewer, sync |

## Компоненты

| Компонент | Модуль | Роль |
|-----------|--------|------|
| Запуск конвейера | [rebuild_all.sh](build-pipeline.md) | Оркестрирует 8 шагов пересборки |
| Декомпозер | [split_spec](../modules/split_spec.md) | Делит монолит на файлы секций |
| Построитель индекса | [build_metadata](../modules/build_metadata.md) | Парсит оглавление в metadata.json |
| Обогащатель | [enrich_metadata](../modules/enrich_metadata.md) | Добавляет пользовательские запросы (EN+RU) |
| Глоссарий | [build_glossary](../modules/build_glossary.md) | Таблица топ-50 терминов |
| Лексические правила | [build_lexical](../modules/build_lexical.md) | Обязательные замены терминов |
| Маршруты | [build_routes](../modules/build_routes.md) | 10 подобранных цепочек под задачи |
| Перекрёстные ссылки | [build_xrefs](../modules/build_xrefs.md) | Инвертированный граф зависимостей по директориям |
| Эмбеддинги | [build_embeddings](../modules/build_embeddings.md) | FAISS + bge-m3 |
| CLI запроса | [semantic_search](../modules/semantic_search.md) | Семантический поиск во время выполнения |
| Classifier | [fpf-classifier](../agents/fpf-classifier.md) | Детекция burden |
| Retriever | [fpf-retriever](../agents/fpf-retriever.md) | Загрузка секций |
| Reasoner | [fpf-reasoner](../agents/fpf-reasoner.md) | Вывод на обычном языке |
| Reviewer | [fpf-reviewer](../agents/fpf-reviewer.md) | Контроль качества (Tier 2/3) |
| Sync | [fpf-sync](../agents/fpf-sync.md) | Сервисная синхронизация по расписанию |
| Хук changelog | [update_changelog](../modules/update_changelog.md) | PreToolUse бамп версии и changelog |

## Поток данных

```
FPF-Spec.md  ──split_spec──►  sections/*/**.md
                                     │
                                     ├──build_metadata──►  metadata.json
                                     │                          │
                                     │                    enrich_metadata
                                     │                          │
                                     ├──build_glossary──►  glossary-quick.md
                                     ├──build_lexical──►   lexical-rules.md
                                     ├──build_routes──►    routes/route-*.md
                                     ├──build_xrefs──►     */_xref.md
                                     └──build_embeddings──► embeddings/{faiss,meta,config}

Сообщение пользователя ──► fpf-classifier ──► fpf-retriever ──► fpf-reasoner ──► пользователь
                                                  │                │
                                                  ▼                ▼
                            (читают) routes / metadata / xrefs / semantic_search
                                                                   │
                                                                   ▼ (опционально, Tier 2/3)
                                                               fpf-reviewer
```

## Решения

- **Контракт обычного языка.** Терминология FPF никогда не попадает к пользователю. См. [plain-language-contract](plain-language-contract.md).
- **Трёхъярусная загрузка.** Маршруты как кэш, семантический поиск как откат, комбинация для пересекающих задач. См. [three-tier-retrieval](three-tier-retrieval.md).
- **Пересборка на стандартной библиотеке.** Все скрипты, кроме двух связанных с эмбеддингами, используют только стандартную библиотеку Python; скрипты эмбеддингов объявляют зависимости inline через PEP 723 и запускаются под `uv`.
- **Форк, дружественный upstream.** Спека синхронизируется с `ailev/FPF` через агента по расписанию. См. [sync-and-rebuild](sync-and-rebuild.md).

## Связанные статьи

- [skill-entry-point](skill-entry-point.md)
- [build-pipeline](build-pipeline.md)
- [agent-team](agent-team.md)
