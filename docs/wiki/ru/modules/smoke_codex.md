---
title: smoke_codex
sources:
  - scripts/smoke_codex.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - testing
  - codex
  - smoke-tests
---

# smoke_codex

> Источник: `scripts/smoke_codex.py`

## Назначение

Дымовой сьют под Codex-редакцию навыка FPF (`.agents/skills/fpf/SKILL.md`). Проверяет frontmatter, что все пути в теле скилла разрешаются, и что описание скилла совпадает с Claude Code-редакцией — иначе окружения будут срабатывать на разные формулировки пользователя.

Также защищает от Codex-специфичных рисков: тело скилла не должно инструктировать Codex "Dispatch fpf-...", так как в Codex нет примитива Task-dispatch.

## Интерфейс

Модуль на `unittest`. Автоматически обнаруживаемые классы тестов:

| Класс | Что проверяет |
|-------|--------------|
| `TestCodexSkillStructure` | frontmatter есть, `name: fpf`, описание содержательное (>50 символов) и идентично Claude Code-редакции |
| `TestCodexSkillReferences` | ≥4 ссылки `agents/fpf-*.md` разрешаются; конкретные пути `sections/...` существуют; все `scripts/*.py` на месте; нет запрещённых токенов (`Dispatch fpf-`, `Task tool`) |
| `TestSemanticSearchCLI` | только при `--all`: подпроцесс `uv run scripts/semantic_search.py` успешно возвращает ожидаемую JSON-форму |

Хелперы: `split_frontmatter(text) -> (fm, body)` и `parse_minimal_yaml(fm) -> dict` — парсер YAML-подобного формата на стандартной библиотеке, достаточный для полей `name:` и `description:`.

## Алгоритм

setUp в каждом классе читает и разбивает Codex SKILL.md. Тесты независимы:
- Тесты ссылок используют `_extract_paths(pattern)` для дедупликации regex-совпадений и проверяют `(PROJECT_ROOT / path).exists()` по каждому пути.
- Тест совпадения описаний читает и скилл Claude Code, требует точного равенства строк — дрейф описания = разное срабатывание между средами.
- Защита от Task-dispatch — простой `assertNotIn` по телу.

Как и в `test_smoke.py`, флаг `--all` вычищается из `argv` перед `unittest.main`, чтобы раннер не жаловался.

## Зависимости

**Импорты:** `json`, `re`, `subprocess`, `sys`, `unittest`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** запускается отдельно после правок в `.agents/skills/fpf/SKILL.md` или `skills/fpf/SKILL.md`.

## Связанные статьи

- [test_smoke](test_smoke.md) — аналогичный сьют для Claude Code-редакции
- [skill-entry-point](../architecture/skill-entry-point.md)
- [semantic_search](semantic_search.md)
