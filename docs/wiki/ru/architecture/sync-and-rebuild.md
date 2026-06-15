---
title: Синхронизация и пересборка
sources:
  - agents/fpf-sync.md
  - scripts/rebuild_all.sh
  - scripts/update_changelog.py
  - CLAUDE.md
last_updated: 2026-06-15T07:00:00Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Синхронизация и пересборка

## Компоненты

Поддержание репозитория в синхронизации с upstream `ailev/FPF` идёт через один слой автоматизации:

| Слой | Где | Что делает |
|------|-----|-----------|
| Claude Code remote routine | `trig_01P7UzjrjgsgzLpMHn84bMoo` — управляется на claude.ai/code/routines | 1-е и 15-е каждого месяца в 07:00 UTC. Получает изменения upstream, сравнивает хэш `FPF-Spec.md`, сливает при изменениях, пересобирает секции, AI-обогащает индексы и глоссарий, компилирует вики, обновляет changelog, публикует. |
| PreToolUse-хук | `.claude/settings.json` → `scripts/update_changelog.py` | Срабатывает на каждом `git commit`. Бампит версию в `plugin.json` и добавляет запись в changelog. |

Примечание: GitHub Action (`.github/workflows/rebuild-sections.yml`), который ранее покрывал тот же флоу, последовательно падал и был удалён. Remote routine его заменяет.

## Поток данных

```
 (1-е и 15-е каждого месяца, 07:00 UTC)
 Claude Code scheduled routine
           │
           ▼
    агент fpf-sync
           │
           ├──► 1. git fetch upstream; сравнение хэша FPF-Spec.md
           │       (выход, если совпадают)
           │
           ├──► 2. git merge upstream/main --no-edit
           │       (решаем ожидаемый конфликт Readme.md; при прочих — выход)
           │
           ├──► 3. bash scripts/rebuild_all.sh
           │       (8 шагов → sections/, metadata, routes, xrefs, embeddings)
           │
           ├──► 4. AI-обогащение sections/**/_index.md
           │       (однопредложное описание на обычном языке для каждой секции)
           │
           ├──► 5. AI-обогащение sections/glossary-quick.md
           │       (колонка с простым определением)
           │
           ├──► 6. /wiki compile
           │       (инкрементальное обновление docs/wiki/ru/ и docs/wiki/en/)
           │
           ├──► 7. Добавление раздела What's New в CHANGELOG.md; бамп версии при необходимости
           │
           └──► 8. git add sections/ docs/wiki/ CHANGELOG.md && git commit && git push
                   (PreToolUse-хук: бамп версии, запись в CHANGELOG)
```

## Решения

- **Один путь обновления по расписанию.** Claude Code remote routine владеет всем циклом синхронизации. Дублирования GitHub Action нет — предыдущий Action последовательно падал и был удалён.
- **AI-обогащение отдельно от механической пересборки.** `rebuild_all.sh` формирует сырые структуры; агент sync переписывает описания `_index.md` на обычный язык. Python-конвейер остаётся без внешних зависимостей, а качество описаний обеспечивает LLM.
- **Бамп версии автоматический.** PreToolUse-хук на `git commit` запускает `update_changelog.py`, который парсит Conventional Commits и бампит `plugin.json` соответственно — `feat:` → minor, `fix:` → patch, `feat!:` → major, остальные типы → запись в changelog без бампа.
- **Только merge, никакого rebase.** В списке "чего не делать" агента sync явно запрещены force-push и rebase. История остаётся почти линейной, а upstream-downstream провенанс сохраняется.

## Связанные статьи

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
