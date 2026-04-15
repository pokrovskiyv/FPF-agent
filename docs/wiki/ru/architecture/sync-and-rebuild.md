---
title: Синхронизация и пересборка
sources:
  - agents/fpf-sync.md
  - scripts/rebuild_all.sh
  - scripts/update_changelog.py
  - CLAUDE.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Синхронизация и пересборка

## Компоненты

Поддержание репозитория в синхронизации с upstream `ailev/FPF` идёт через двухслойную автоматизацию:

| Слой | Где | Что делает |
|------|-----|-----------|
| GitHub Action | `.github/workflows/rebuild-sections.yml` | Запускает `scripts/rebuild_all.sh` на push в main при изменении `FPF-Spec.md`. Также по cron (1-е и 15-е каждого месяца, 09:00 UTC) для автосинхронизации форка. |
| Claude Code remote trigger | Управляется на claude.ai/code/scheduled | Раз в 2 недели запускает [fpf-sync](../agents/fpf-sync.md). Та же пересборка плюс AI-обогащение `_index.md` и `glossary-quick.md`. |
| PreToolUse-хук | `.claude/settings.json` → `scripts/update_changelog.py` | Срабатывает на каждом `git commit`. Бампит версию в `plugin.json` и добавляет запись в changelog. |

## Поток данных

```
 (раз в 2 недели)
 Claude Code scheduled trigger
           │
           ▼
    агент fpf-sync
           │
           ├──► 1. git fetch upstream; сравнение хэша FPF-Spec.md
           │       (выход, если совпадают)
           │
           ├──► 2. git merge upstream/main --no-edit
           │       (выход при конфликте)
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
           └──► 6. git add sections/ && git commit && git push
                   (PreToolUse-хук: бамп версии, запись в CHANGELOG)


 (ортогонально, на каждом push)
 GitHub Action
           │
           ├──► rebuild-sections.yml запускает rebuild_all.sh
           │       (шаги 1–7; шаг 8 пропускается в CI — нет uv)
           │
           └──► коммитит перегенерированный sections/ в main при изменениях
```

## Решения

- **Два независимых пути обновления.** GitHub Action занимается push-триггерами; Claude Code-агент — синхронизацией с upstream по расписанию. Они не мешают друг другу, так как обе ветви коммитят в main, а агент sync идемпотентен.
- **AI-обогащение отдельно от механической пересборки.** `rebuild_all.sh` формирует сырые структуры; агент sync переписывает описания `_index.md` на обычный язык. Python-конвейер остаётся без внешних зависимостей, а качество описаний обеспечивает LLM.
- **Бамп версии автоматический.** PreToolUse-хук на `git commit` запускает `update_changelog.py`, который парсит Conventional Commits и бампит `plugin.json` соответственно — `feat:` → minor, `fix:` → patch, `feat!:` → major, остальные типы → запись в changelog без бампа.
- **Только merge, никакого rebase.** В списке "чего не делать" агента sync явно запрещены force-push и rebase. История остаётся почти линейной, а upstream-downstream провенанс сохраняется.

## Связанные статьи

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
