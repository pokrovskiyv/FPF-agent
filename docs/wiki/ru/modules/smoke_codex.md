---
title: smoke_codex
sources:
  - scripts/smoke_codex.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - module
  - testing
  - codex
  - smoke-tests
  - plugin
---

# smoke_codex

> Источник: `scripts/smoke_codex.py`

## Назначение

Дымовой сьют под Codex-редакцию навыка FPF (`.agents/skills/fpf/SKILL.md`) и под упаковку плагина для Codex CLI. Проверяет frontmatter скилла, что все упомянутые в теле скилла пути разрешаются, что описание скилла совпадает с Claude Code-редакцией (иначе среды будут срабатывать на разные формулировки пользователя), и что корень репозитория — корректно собранный плагин Codex с рабочим установщиком и метаданными маркетплейса.

Работает офлайн — Codex CLI не требуется, поведение LLM не проверяется. Также защищает от Codex-специфичных рисков: тело скилла не должно инструктировать Codex "Dispatch fpf-..." или использовать "Task tool", так как в Codex нет примитива Task-dispatch и команду агентов приходится оркестрировать инлайн.

## Интерфейс

Модуль на `unittest`. Автоматически обнаруживаемые классы тестов:

| Класс | Что проверяет |
|-------|--------------|
| `TestCodexSkillStructure` | frontmatter есть, `name: fpf`, описание содержательное (>50 символов) и идентично Claude Code-редакции (`skills/fpf/SKILL.md`) |
| `TestCodexSkillReferences` | ≥4 ссылки `agents/fpf-*.md` разрешаются; конкретные пути `sections/...` существуют; все `scripts/*.py` на месте; нет запрещённых токенов (`Dispatch fpf-`, `Task tool`) |
| `TestSemanticSearchCLI` | только при `--all`: подпроцесс `uv run scripts/semantic_search.py` успешно возвращает ожидаемую JSON-форму (`rank`, `score`, `pattern_id`, `title`, `file`, `keywords`) |
| `TestRootCodexPlugin` | корень репозитория — версионируемый плагин Codex: `.codex-plugin/plugin.json` объявляет `name: fpf`, `skills: ./.agents/skills/`, `license: MIT` и `interface` с `displayName: FPF` + `defaultPrompt`; все рантайм-файлы есть в корне плагина; нет дублирующего дерева `plugins/fpf`; скилл использует контракт `<FPF_PLUGIN_ROOT>`, и его ссылки разрешаются относительно этого корня |
| `TestCodexPluginInstaller` | `scripts/install_codex_plugin.py --home <tmp>` синхронизирует упакованный плагин в домашний (home-local) маркетплейс Codex, копирует все рантайм-файлы, пишет запись маркетплейса и не вкладывает дерево `plugins/fpf` |
| `TestRepoLocalMarketplace` | `.agents/plugins/marketplace.json` отдаёт единственную запись `fpf`, у которой `source` = `local`, `path` = `./.`, с политикой `AVAILABLE`/`ON_INSTALL` и категорией `Productivity` |

Хелперы: `split_frontmatter(text: str) -> tuple[str, str]` возвращает `(frontmatter_block, body)` (пустой frontmatter, если его нет), а `parse_minimal_yaml(fm: str) -> dict` — парсер YAML-подобного формата на стандартной библиотеке, достаточный для полей `name:` и `description:`, включая блочные скаляры `>`/`|`.

Константы уровня модуля фиксируют проверяемые пути: `CODEX_SKILL` (`.agents/skills/fpf/SKILL.md`), `CC_SKILL` (`skills/fpf/SKILL.md`), `PLUGIN_MANIFEST` (`.codex-plugin/plugin.json`), `DUPLICATED_PLUGIN_ROOT` (`plugins/fpf`, должен отсутствовать) и `REPO_MARKETPLACE` (`.agents/plugins/marketplace.json`). `RUN_ALL` равно `True`, если в `sys.argv` есть `--all`.

## Алгоритм

`setUp` в нужных классах читает и разбивает Codex SKILL.md. Тесты независимы:

1. **Структура** — парсинг frontmatter через `split_frontmatter` + `parse_minimal_yaml`, проверки `name == 'fpf'` и содержательного описания, затем чтение скилла Claude Code и проверка точного равенства описаний (дрейф описания = разное срабатывание между средами).
2. **Ссылки** — `_extract_paths(pattern)` дедуплицирует regex-совпадения; сьют проверяет `(PROJECT_ROOT / path).exists()` по каждому пути агента/секции/скрипта и использует простой `assertNotIn` по телу для защиты от Task-dispatch.
3. **Корень плагина** — загрузка `.codex-plugin/plugin.json` и проверка его полей; проверка наличия рантайм-файлов; утверждение, что `plugins/fpf` НЕ существует; утверждение, что тело скилла содержит `<FPF_PLUGIN_ROOT>`, фразу "plugin root" и `--index-dir <FPF_PLUGIN_ROOT>/sections/embeddings`, и НЕ содержит устаревшую формулировку `launched from the FPF-agent repo root`.
4. **Установщик** — запуск `install_codex_plugin.py` против home во временной директории (`tempfile.TemporaryDirectory()`), проверка кода возврата 0, затем проверка установленного манифеста, рантайм-файлов, отсутствия вложенного `plugins/fpf` и записи маркетплейса (`source.path == './plugins/fpf'`, `AVAILABLE`/`ON_INSTALL`, `Productivity`).
5. **Маркетплейс репозитория** — загрузка `.agents/plugins/marketplace.json` и проверка, что единственная запись `fpf` указывает на корень репозитория (`source.source == 'local'`, `source.path == './.'`).

Как и в `test_smoke.py`, флаг `--all` вычищается из `argv` перед `unittest.main`, чтобы раннер не жаловался на неизвестный флаг.

## Зависимости

**Импорты:** `json`, `re`, `subprocess`, `sys`, `tempfile`, `unittest`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** запускается отдельно после правок в `.agents/skills/fpf/SKILL.md`, `skills/fpf/SKILL.md`, `.codex-plugin/plugin.json`, `scripts/install_codex_plugin.py` или `.agents/plugins/marketplace.json`.

## Связанные статьи

- [test_smoke](test_smoke.md) — аналогичный сьют для Claude Code-редакции
- [skill-entry-point](../architecture/skill-entry-point.md)
- [semantic_search](semantic_search.md)
