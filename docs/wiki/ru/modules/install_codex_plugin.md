---
title: install_codex_plugin
sources:
  - scripts/install_codex_plugin.py
last_updated: 2026-06-16T07:21:51Z
tags:
  - module
  - codex
  - installer
  - marketplace
  - plugin
---

# install_codex_plugin

> Источник: `scripts/install_codex_plugin.py`

## Назначение

Устанавливает FPF как плагин Codex CLI в **домашний локальный marketplace**, благодаря чему навык работает из любой рабочей директории, а не только из корня репозитория FPF-agent. Установщик не копирует версионируемый дубликат пакета — он собирает минимальный плагин из корня репозитория, копируя только те runtime-файлы, которые реально нужны навыку, в `~/plugins/fpf` и регистрируя запись в `~/.agents/plugins/marketplace.json`.

Этот же скрипт обновляет плагин: после `git pull` повторный запуск пересобирает `~/plugins/fpf` из текущего состояния репозитория (старая целевая папка сначала удаляется) и идемпотентно обновляет запись в marketplace. Флаг `--home` перенаправляет корень установки — именно его используют смоук-тесты, чтобы ставить плагин во временную директорию.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `plugin_entry` | `() -> dict` | Собирает запись marketplace для `fpf`: `source` типа `local` указывает на `./plugins/fpf`, политика `installation: AVAILABLE` / `authentication: ON_INSTALL`, категория `Productivity` |
| `load_marketplace` | `(path: Path) -> dict` | Читает `marketplace.json` или возвращает свежий скелет `local`; бросает `ValueError` при невалидном JSON или корне не-объекте, и достраивает отсутствующие ключи `plugins` / `name` / `interface.displayName` |
| `update_marketplace` | `(path: Path) -> None` | Удаляет существующую запись `fpf`, добавляет свежую из `plugin_entry()`, создаёт родительскую папку и записывает форматированный JSON (`ensure_ascii=False`, indent 2) |
| `sync_plugin` | `(source: Path, target: Path) -> None` | Проверяет источник, удаляет старую цель и копирует в неё runtime-директории и файлы (пропуская `__pycache__`, `*.pyc`, `.DS_Store`) |
| `parse_args` | `(argv: list[str]) -> argparse.Namespace` | Разбирает `--home` (по умолчанию домашняя папка пользователя) и `--source` (по умолчанию корень проекта) |
| `main` | `(argv: list[str] \| None = None) -> int` | Резолвит home и source, выполняет `sync_plugin`, затем `update_marketplace`, печатает пути установки и marketplace, возвращает `0` |

Что именно копируется, задают константы модуля. `COPY_DIRECTORIES` копирует `.codex-plugin`, `.agents/skills/fpf`, `agents` и `sections`; `COPY_FILES` копирует `scripts/semantic_search.py` и `scripts/build_embeddings.py`. `PLUGIN_NAME` — `fpf`; `DEFAULT_PLUGIN_SOURCE` — корень репозитория, вычисленный из `__file__`.

## Алгоритм

1. `main` резолвит `--home` и `--source` (раскрывает `~` и приводит к абсолютным путям), затем выводит `target = home/plugins/fpf` и `marketplace_path = home/.agents/plugins/marketplace.json`.
2. `sync_plugin(source, target)` выполняет проверки: источник должен существовать, содержать `.codex-plugin/plugin.json` и не совпадать с целью. Затем проверяет, что существует каждый путь из `COPY_DIRECTORIES` и `COPY_FILES`, собирая все отсутствующие в один `FileNotFoundError`.
3. Если `target` уже есть, он удаляется через `shutil.rmtree` и создаётся заново. Каждая директория копируется через `shutil.copytree` (с фильтром-игнором), каждый файл — через `shutil.copy2` после создания родительской папки. Именно это делает повторный запуск установщика чистым обновлением, а не слиянием.
4. `update_marketplace(marketplace_path)` загружает (или инициализирует) marketplace, удаляет прежнюю запись `fpf`, чтобы повторные запуски её не дублировали, добавляет текущую `plugin_entry()` и записывает файл обратно.
5. `main` печатает `Installed plugin: <target>` и `Updated marketplace: <marketplace_path>` и возвращает `0`.

Таким образом, путь обновления единственный: `git pull`, чтобы обновить репозиторий, затем `python3 scripts/install_codex_plugin.py`, чтобы пересинхронизировать домашнюю копию. Отдельный шаг удаления не нужен — целевая папка пересобирается, а запись в marketplace заменяется на месте.

## Использование

```bash
# Первая установка (из корня репозитория)
python3 scripts/install_codex_plugin.py

# Обновление после подтягивания новой спеки/секций
git pull && python3 scripts/install_codex_plugin.py

# Установка в альтернативный home (используется тестами)
python3 scripts/install_codex_plugin.py --home /tmp/codex-home
```

После установки семантическому fallback нужно один раз построить FAISS-индекс из установленной копии: `cd ~/plugins/fpf && uv run scripts/build_embeddings.py`.

## Зависимости

**Импорты:** `argparse`, `json`, `shutil`, `sys`, `pathlib.Path` — только стандартная библиотека.

**Где используется:** запускается как скрипт. Упоминается в `Readme.md` и `CLAUDE.md` как команда локальной установки и числится в `CHANGELOG.md` как установщик Codex. Манифест `.codex-plugin/`, который он упаковывает, — это Codex-близнец `.claude-plugin/`; оба файла `plugin.json` держатся синхронно на версии `0.6.3`.

## Связанные статьи

- [smoke_codex](smoke_codex.md) — проверяет Codex-редакцию навыка, которую поставляет этот установщик
- [build_embeddings](build_embeddings.md) — строит FAISS-индекс, нужный установленному плагину для семантического fallback
- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — рутина, которая бампит и `.claude-plugin/plugin.json`, и `.codex-plugin/plugin.json`
- [changelog-workflow](../concepts/changelog-workflow.md)
