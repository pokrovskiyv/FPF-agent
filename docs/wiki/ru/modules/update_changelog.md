---
title: update_changelog
sources:
  - scripts/update_changelog.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - hook
  - changelog
  - versioning
---

# update_changelog

> Источник: `scripts/update_changelog.py`

## Назначение

Скрипт PreToolUse-хука, запускающийся перед каждым `git commit`. Читает JSON хука из stdin, извлекает первую строку коммита, парсит её как Conventional Commit, автоматически бампит `version` в `.claude-plugin/plugin.json` (feat → minor, fix → patch, breaking → major) и добавляет оформленную запись в `CHANGELOG.md` под сегодняшней датой в подраздел "### All Changes". В конце стейджит оба файла, чтобы бамп и запись в changelog попали в тот же коммит.

Тихо пропускает, если сообщение коммита не Conventional или JSON хука не пришёл.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `extract_commit_message` | `(bash_command: str) -> str \| None` | Возвращает первую строку темы; поддерживает heredoc (`<<EOF ...`) и форму `-m "..."` / `-m '...'` |
| `parse_conventional_commit` | `(message: str) -> dict \| None` | Regex-парсер `type(scope)!: description`; None при несовпадении |
| `determine_bump` | `(parsed: dict) -> str` | Возвращает `major`, `minor`, `patch` или `none` по типу и флагу breaking |
| `bump_version` | `(current: str, bump_type: str) -> str` | Инкремент semver-строки; `none` оставляет без изменений |
| `update_plugin_json` | `(path: Path, new_version: str) -> None` | Иммутабельное чтение-запись `plugin.json` с обновлённой версией |
| `format_entry` | `(parsed: dict) -> str` | Форматирует строку (`- **feat(scope)**: description`) |
| `update_changelog` | `(path: Path, entry_line: str, date_str: str) -> None` | Вставляет под сегодняшнюю дату / "### All Changes"; идемпотентно (пропускает, если строка уже есть) |
| `stage_files` | `(*paths: Path) -> None` | Запускает `git add` по указанным путям |
| `main` | `() -> None` | Оркестрирует конвейер; печатает диагностику на каждом шаге |

## Алгоритм

1. Читаем JSON из stdin; тихо выходим, если пусто или невалидно.
2. Извлекаем bash-команду, затем первую строку сообщения коммита. Выходим, если что-то пусто.
3. Парсим как Conventional Commit; если не подходит — выход.
4. Определяем тип бампа. Если не `none`, читаем `plugin.json`, бампим версию, пишем обратно.
5. Формируем строку changelog и вызываем `update_changelog` с сегодняшней датой.
6. `git add` по изменённым файлам, чтобы они попали в текущий коммит.

Идемпотентность — внутри `update_changelog`: если ровно такая строка уже есть в файле, добавление пропускается.

## Зависимости

**Импорты:** `json`, `re`, `subprocess`, `sys`, `datetime.date`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** прописан в `.claude/settings.json` как PreToolUse-хук на `Bash` с условием `git commit*`.

## Связанные статьи

- [changelog-workflow](../concepts/changelog-workflow.md) — общая политика версионирования
- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- Раздел "Changelog & Versioning" в CLAUDE.md
