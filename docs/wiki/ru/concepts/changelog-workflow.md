---
title: Рабочий процесс changelog
sources:
  - scripts/update_changelog.py
  - CHANGELOG.md
  - CLAUDE.md
  - .claude/settings.json
  - .claude-plugin/plugin.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - workflow
  - changelog
  - versioning
---

# Рабочий процесс changelog

## Определение

**Рабочий процесс changelog** — автоматическая + ручная пара шагов, которая держит `CHANGELOG.md` и поле `version` в `plugin.json` в синхронизации с каждым коммитом. Использует парсинг Conventional Commits: `feat:` → minor-бамп, `fix:` → patch-бамп, `feat!:` → major-бамп, остальные типы (`docs`, `test`, `chore`, `perf`, `ci`, `style`, `refactor`) → запись в changelog без бампа.

Состоит из автоматической половины (PreToolUse-хук) и ручной (пишется раздел "Что нового" для человека).

## Как это работает в системе

### Автоматическая половина

Описана в `.claude/settings.json` как PreToolUse-хук на `Bash` с условием `git commit*`. Хук запускает [update_changelog](../modules/update_changelog.md), который:

1. Читает JSON хука из stdin.
2. Извлекает первую строку сообщения коммита (heredoc или `-m`).
3. Парсит как Conventional Commit — тихо выходит, если не подходит.
4. Бампит версию `plugin.json`, если тип `feat` / `fix` / с `!`.
5. Добавляет bullet в `CHANGELOG.md` под сегодняшнюю дату / "### All Changes".
6. `git add`-ит изменённые файлы, чтобы они попали в тот же коммит.

Идемпотентен — повторный коммит с той же темой не дублирует записи.

### Ручная половина

Для изменений, видимых пользователю (`feat:` или значимый `fix:`), Claude или разработчик также пишут строку в подраздел "### What's New" в `CHANGELOG.md` под сегодняшней датой. Это — обычный язык с точки зрения пользователя, не сообщение коммита.

CLAUDE.md явно уточняет: "Пишите на обычном языке с позиции пользователя, не копируйте commit-сообщения. Группируйте связанные изменения в один пункт."

## Почему автомат и ручка разделены

- Автомат фиксирует ЧТО (историю коммитов) — детерминированно, полно.
- Ручка фиксирует ЗАЧЕМ на уровне продукта — то, что пользователь реально читает.

Смешение дало бы либо пункты "### What's New — `chore(agents): bump description`" (бессмысленные), либо потребовало бы вызывать LLM в хуке (медленно, нестабильно).

## Связанные статьи

- [update_changelog](../modules/update_changelog.md)
- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- Раздел "Changelog & Versioning" в CLAUDE.md
- `CHANGELOG.md` — сам управляемый файл
