---
title: check_wiki_gate
sources:
  - scripts/check_wiki_gate.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - module
  - hook
  - wiki
  - gate
---

# check_wiki_gate

> Источник: `scripts/check_wiki_gate.py`

## Назначение

Детерминированный PreToolUse-хук (прописан на `git commit` в `.claude/settings.json`), который блокирует коммит, *заявляющий* обновление вики, если вики на самом деле устарела. Реальный сбой, который он предотвращает: рутина `fpf-sync` коммитит "… + wiki refresh", но `/wiki compile` тихо ничего не сделал (манифест не сдвинулся) — и заявление попало в историю без реальных изменений. Хук читает сообщение коммита; если его тема говорит об обновлении вики, а `scanner.py check` сообщает, что вики устарела, коммит отклоняется (exit 2) с пояснением. Коммиты, не заявляющие обновление вики, не затрагиваются никогда, а любая инфраструктурная ошибка приводит к fail-open (коммит проходит).

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `extract_commit_message` | `(bash_command: str) -> str \| None` | Достаёт сообщение коммита из bash-команды; поддерживает heredoc (`<<EOF … EOF`) и формы `-m "…"` / `-m '…'`; возвращает `None`, если ничего не совпало |
| `wiki_is_stale` | `() -> bool \| None` | Запускает `scanner.py check <корень проекта>`; `True` = устарела (exit 1), `False` = свежая (exit 0), `None` = определить не удалось (нет сканера, ошибка subprocess или неожиданный код выхода → fail-open) |
| `main` | `() -> None` | Читает JSON хука из stdin, решает, нужен ли гейт, и вызывает `sys.exit(2)` для отказа, если заявление не подтверждено |

Константы модуля: `PROJECT_ROOT` (корень репозитория, на два уровня выше скрипта), `SCANNER` (`~/.claude/skills/wiki/scanner.py`) и `CLAIM_RE` (`wiki\s+(refresh|compile|rebuild)`, без учёта регистра).

## Алгоритм

1. Читаем payload хука как JSON из stdin. При `JSONDecodeError` / `EOFError` тихо выходим (коммит разрешён).
2. Читаем `tool_input.command`. Если в нём нет `git commit` — выходим (нас не касается).
3. Извлекаем сообщение коммита через `extract_commit_message`. Если оно не совпадает с `CLAIM_RE` — то есть не заявляет refresh/compile/rebuild вики — выходим (разрешаем).
4. Вызываем `wiki_is_stale()`. Только когда возвращается ровно `True`, хук отказывает: пишет в stderr подсказку по исправлению (запустить `/wiki compile`, убедиться, что `docs/wiki/.state/manifest.json` сдвинулся, перепроверить через `scanner.py check .`) и вызывает `sys.exit(2)`, чтобы заблокировать вызов инструмента.
5. Любой другой путь — нет заявления, вики свежая или неопределённый результат сканера (`None`) — проваливается дальше, и коммит проходит. Гейт намеренно fail-open: он блокирует только при *положительном* сигнале устаревания против *положительного* заявления.

## Зависимости

**Импорты:** `json`, `re`, `subprocess`, `sys`, `pathlib.Path` — только стандартная библиотека.

**Внешний инструмент:** `~/.claude/skills/wiki/scanner.py` (проверка свежести вики), запускается через `sys.executable`.

**Где используется:** `.claude/settings.json` как PreToolUse-хук на `Bash` с условием `git commit`.

## Связанные статьи

- [update_changelog](update_changelog.md) — другой PreToolUse-хук на `git commit`
- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — рутина `fpf-sync`, чьё заявление об обновлении вики страхует этот гейт
- Раздел "Wiki" в CLAUDE.md — `/wiki compile`, `scanner.py check` и манифест
