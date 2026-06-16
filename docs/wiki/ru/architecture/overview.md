---
title: Обзор
sources:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - CLAUDE.md
  - Readme.md
last_updated: 2026-06-16T03:34:37Z
tags:
  - architecture
  - overview
  - packaging
---

# Обзор

## Что это за репозиторий

Спецификация **First Principles Framework (FPF)** (~61 000 строк) плюс **навык**, применяющий паттерны FPF к координационным задачам пользователя, при этом сама терминология FPF никогда не попадает наружу.

Проект **упакован сразу для двух сред**: один и тот же репозиторий — это плагин и для **Claude Code** (через `.claude-plugin/`), и для **Codex CLI** (через `.codex-plugin/` плюс локальный marketplace в домашней директории). Текущая версия: **0.6.1** (держится синхронной в обоих манифестах).

Подвижные части на диске:

| Слой | Где лежит | Что содержит |
|------|-----------|--------------|
| **Монолит спеки** | `FPF-Spec.md` | Источник истины от upstream; напрямую не редактируется |
| **Декомпозированные секции** | `sections/` | ~240 генерируемых файлов + metadata.json + маршруты + xrefs + FAISS-индекс |
| **Точка входа навыка (Claude Code)** | `skills/fpf/SKILL.md` | Логика маршрутизации по burden, читаемая Claude Code |
| **Точка входа навыка (Codex CLI)** | `.agents/skills/fpf/SKILL.md` | Тот же навык, доступный из Codex |
| **Команда агентов** | `agents/fpf-*.md` | Пять агентов: classifier, retriever, reasoner, reviewer, sync |
| **Манифест Claude Code** | `.claude-plugin/` | `plugin.json` + `marketplace.json` |
| **Манифест Codex CLI** | `.codex-plugin/` | `plugin.json`, указывающий на навык в `.agents/skills/` |
| **Установщик Codex** | `scripts/install_codex_plugin.py` | Собирает локальный пакет в `~/plugins/fpf` и регистрирует его в `~/.agents/plugins/marketplace.json` |

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
| Установщик Codex | [install_codex_plugin](../modules/install_codex_plugin.md) | Локальный пакет Codex + запись в marketplace |
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

### Два пути установки

Обе среды используют один и тот же репозиторий; различается только входной манифест.

```
Claude Code:  /plugin marketplace add pokrovskiyv/FPF-agent
              └─ читает .claude-plugin/marketplace.json → ставит плагин "fpf"
              └─ обновления подтягиваются автоматически при пушах в main

Codex CLI:    codex plugin marketplace add pokrovskiyv/FPF-agent
              └─ корень репозитория и есть Codex-плагин: .codex-plugin/plugin.json
              └─ навык берётся из .agents/skills/fpf/

Codex (локально, без marketplace UI):
              python3 scripts/install_codex_plugin.py
              └─ собирает ~/plugins/fpf из корня репозитория
              └─ регистрирует его в ~/.agents/plugins/marketplace.json
              └─ обновление: git pull && python3 scripts/install_codex_plugin.py
```

## Решения

- **Двойная упаковка.** Один репозиторий поставляется и как плагин Claude Code (`.claude-plugin/`), и как плагин Codex CLI (`.codex-plugin/` + `scripts/install_codex_plugin.py`). Форка нет: навык для Codex берётся из `.agents/skills/fpf/`, а оба файла `plugin.json` несут одну и ту же версию.
- **Контракт обычного языка.** Терминология FPF никогда не попадает к пользователю. См. [plain-language-contract](plain-language-contract.md).
- **Трёхъярусная загрузка.** Маршруты как кэш, семантический поиск как откат, комбинация для пересекающих задач. См. [three-tier-retrieval](three-tier-retrieval.md).
- **Пересборка на стандартной библиотеке.** Все скрипты, кроме двух связанных с эмбеддингами, используют только стандартную библиотеку Python; скрипты эмбеддингов объявляют зависимости inline через PEP 723 и запускаются под `uv`.
- **Синхронность версий.** PreToolUse-хук changelog (`scripts/update_changelog.py`) автоматически бампит версию только в `.claude-plugin/plugin.json`. Сервисная рутина синхронизации вручную бампит **оба** файла — `.claude-plugin/plugin.json` и `.codex-plugin/plugin.json`, чтобы они не разъезжались.
- **Единственный путь обновления.** Синхронизация с upstream идёт только через один механизм — Claude Code Remote Routine (`trig_01P7UzjrjgsgzLpMHn84bMoo`, cron 1-го и 15-го числа в 07:00 UTC). Прежнего GitHub Action больше нет. См. [sync-and-rebuild](sync-and-rebuild.md).

## Связанные статьи

- [skill-entry-point](skill-entry-point.md)
- [build-pipeline](build-pipeline.md)
- [agent-team](agent-team.md)
- [sync-and-rebuild](sync-and-rebuild.md)
