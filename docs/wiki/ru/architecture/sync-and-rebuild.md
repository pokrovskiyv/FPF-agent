---
title: Синхронизация и пересборка
sources:
  - CLAUDE.md
  - agents/fpf-sync.md
  - scripts/update_changelog.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Синхронизация и пересборка

## Компоненты

Синхронизация форка с upstream `ailev/FPF` идёт через единственный путь по расписанию. GitHub Action больше нет — проект упакован как плагин **сразу для двух** платформ: Claude Code (`.claude-plugin/`) и Codex CLI (`.codex-plugin/`), а весь цикл синхронизации выполняет один Claude Code remote routine.

| Компонент | Где | Роль |
|-----------|-----|------|
| Claude Code remote routine | `trig_01P7UzjrjgsgzLpMHn84bMoo` — управляется на [claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo](https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo) | Cron: 1-е и 15-е каждого месяца в 07:00 UTC (= 09:00 Europe/Belgrade). Запускает полный цикл из 8 шагов ниже, считывая [fpf-sync](../agents/fpf-sync.md) при каждом запуске. |
| Агент fpf-sync | [agents/fpf-sync.md](../agents/fpf-sync.md) | Runbook, который выполняет routine: проверка upstream, merge, пересборка, AI-обогащение, компиляция вики, changelog, коммит. Источник истины для каждого шага. |
| PreToolUse-хук changelog | `.claude/settings.json` → [scripts/update_changelog.py](../modules/update_changelog.md) | Срабатывает на каждом `git commit`. Парсит Conventional Commit, добавляет запись в changelog и автоматически бампит **только** `.claude-plugin/plugin.json`. |

Routine полностью заменяет старый GitHub Action (`.github/workflows/rebuild-sections.yml`), который стабильно падал и был удалён. Его больше не существует, ни один Action не активен — путь обновления единственный.

## Поток данных

Runbook fpf-sync состоит из **восьми** шагов. Шаги 2–5 пропускаются, когда upstream не изменился (Шаг 1 делает ранний выход), но Шаг 6 и далее всё равно выполняются — иначе локальные правки источников вики оставят её устаревшей.

```
 (1-е и 15-е каждого месяца, 07:00 UTC = 09:00 Europe/Belgrade)
 Claude Code remote routine  →  читает agents/fpf-sync.md
           │
           ▼
    runbook fpf-sync
           │
  Шаг 1 ──► git fetch upstream; сравнение хэша FPF-Spec.md
           │     (хэши совпали → пропуск Шагов 2–5, переход к Шагу 6)
           │
  Шаг 2 ──► git merge upstream/main --no-edit
           │     конфликт Readme.md ОЖИДАЕМ → git checkout --ours Readme.md && git add Readme.md
           │     ЛЮБОЙ другой конфликт → остановиться и сообщить (без force-resolve)
           │
  Шаг 3 ──► bash scripts/rebuild_all.sh
           │     (регенерирует sections/, metadata.json, глоссарий, лексические
           │      правила, routes, xrefs и FAISS-индекс эмбеддингов через uv)
           │
  Шаг 4 ──► AI-обогащение sections/**/_index.md
           │     (однопредложное описание на обычном языке для каждой секции, без жаргона FPF)
           │
  Шаг 5 ──► AI-обогащение sections/glossary-quick.md
           │     (колонка с простым определением для 50 терминов)
           │
  Шаг 6 ──► scanner.py check . → /wiki compile
           │     (двуязычно: регенерирует И docs/wiki/ru/, И docs/wiki/en/,
           │      обновляет docs/wiki/.state/manifest.json; проверка должна выйти с кодом 0)
           │
  Шаг 7 ──► раздел "What's New" в CHANGELOG.md (на обычном языке, для пользователя)
           │     + ручной бамп версии в ОБОИХ .claude-plugin/plugin.json
           │       И .codex-plugin/plugin.json (держим в lockstep)
           │
  Шаг 8 ──► git add sections/ docs/wiki/ CHANGELOG.md \
           │         .claude-plugin/plugin.json .codex-plugin/plugin.json
           └─► git commit -m "chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh"
               git push
```

Коммит на Шаге 8 дополнительно запускает PreToolUse-хук, который сам добавляет запись в changelog по Conventional Commit и бампит `.claude-plugin/plugin.json`. Текущая версия плагина — **0.6.0**.

## Решения

- **Один путь по расписанию.** Claude Code remote routine владеет всем циклом синхронизации. Предыдущий GitHub Action дублировал этот флоу, стабильно падал и был удалён — нет ни запасного Action, ни второго пути обновления.
- **Lockstep двух плагинов.** Проект поставляется как плагин и для Claude Code, и для Codex CLI, поэтому версию несут два манифеста. PreToolUse-хук знает только про `.claude-plugin/plugin.json`; поэтому Шаг 7 fpf-sync вручную бампит **оба** — `.claude-plugin/plugin.json` и `.codex-plugin/plugin.json`, чтобы они не разъехались.
- **AI-обогащение отдельно от механической пересборки.** `rebuild_all.sh` формирует сырые структуры только на stdlib; затем runbook fpf-sync переписывает описания `_index.md` и определения глоссария на обычном языке. Python-конвейер остаётся без внешних зависимостей, а описания получают качество LLM без жаргона.
- **Автоматический бамп одного манифеста при коммите.** PreToolUse-хук запускает `update_changelog.py`, который парсит Conventional Commits и бампит `.claude-plugin/plugin.json`: `feat:` → minor, `fix:` → patch, `feat!:` → major; `docs`/`test`/`chore`/`perf`/`ci`/`style`/`refactor` дают запись в changelog без бампа. Манифест Codex намеренно оставлен на routine.
- **Ожидаемый конфликт, скриптовое разрешение.** Plugin-ориентированный `Readme.md` форка всегда конфликтует со spec-ориентированным upstream. Этот единственный конфликт авторазрешается через `git checkout --ours Readme.md`; любой другой конфликт останавливает прогон, а не рискует плохим force-resolve.
- **Только merge, никакого rebase.** Runbook явно запрещает force-push и rebase, сохраняя upstream-downstream провенанс.

## Связанные статьи

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
