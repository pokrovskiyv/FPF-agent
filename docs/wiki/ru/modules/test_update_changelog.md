---
title: test_update_changelog
sources:
  - scripts/test_update_changelog.py
last_updated: 2026-06-16T07:21:51Z
tags:
  - module
  - testing
  - changelog
---

# test_update_changelog

> Источник: `scripts/test_update_changelog.py`

## Назначение

Регрессионные тесты для [update_changelog](update_changelog.md) — PreToolUse-хука changelog. Фиксируют исправление бага, когда тема коммита с апострофом внутри двойных кавычек `-m` (например `"docs: add What's New"`) обрезалась на апострофе и давала недописанный буллет (`- **docs**: What`). Тесты проверяют, что экстрактор сохраняет полное описание, а буллет, записанный в `CHANGELOG.md`, не обрезан.

Запуск перед правкой хука: `python3 scripts/test_update_changelog.py`.

## Интерфейс

Использует `unittest`. Два набора:

| Класс | Что проверяет |
|-------|--------------|
| `TestExtractCommitMessage` | `extract_commit_message` на: апострофе внутри двойных кавычек, экранированных двойных кавычках (`\"X\"`), обычных двойных / одинарных кавычках, извлечении темы из heredoc, многострочном сообщении (только тема), нескольких флагах `-m` (берётся первый) и отсутствии сообщения |
| `TestAppendedBullet` | Сквозной тест: parse → `format_entry` → `update_changelog` во временный файл, с проверкой, что полное описание присутствует, а старая обрезанная форма — нет |

## Зависимости

**Импорты:** `sys`, `tempfile`, `unittest`, `datetime.date`, `pathlib.Path` и тестируемые функции из `update_changelog` — только стандартная библиотека.

**Где используется:** запускается отдельно; как и прочие smoke-наборы, выполняется вручную перед коммитом, не подключён к автоматическому раннеру.

## Связанные статьи

- [update_changelog](update_changelog.md) — тестируемый модуль
- [test_smoke](test_smoke.md) — smoke-тесты целостности конвейера
- [changelog-workflow](../concepts/changelog-workflow.md)
