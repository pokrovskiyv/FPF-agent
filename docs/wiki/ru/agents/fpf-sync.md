---
title: fpf-sync
sources:
  - agents/fpf-sync.md
last_updated: 2026-06-16T03:34:37Z
tags:
  - agent
  - sync
  - scheduled
  - maintenance
---

# fpf-sync

> Источник: `agents/fpf-sync.md`

## Назначение

Сервисный агент по расписанию. Синхронизирует локальный форк с upstream `ailev/FPF`, запускает полный Python-конвейер пересборки, делает AI-обогащение `_index.md` и `glossary-quick.md`, пересобирает двуязычную вики, обновляет changelog и поднимает версию в обоих манифестах плагина. Коммитит и пушит все изменения.

В отличие от остальных агентов, fpf-sync никогда не общается с конечным пользователем — это чистое сопровождение проекта.

## Интерфейс

**Вход:** ничего (триггер по расписанию).

**Выход:** один git-коммит в ветке main с сообщением `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh` и запушенный `main`. В индекс попадает строго такой набор:

```bash
git add sections/ docs/wiki/ CHANGELOG.md .claude-plugin/plugin.json .codex-plugin/plugin.json
```

## Восемь шагов

1. **Проверка upstream.** Добавить remote `upstream`, если его нет, `git fetch upstream main`, затем сравнить хэши `FPF-Spec.md` (`git rev-parse upstream/main:FPF-Spec.md` против `HEAD:FPF-Spec.md`). Совпадают → пропустить merge и пересборку (шаги 2–5) ради экономии, но **не останавливаться**: локальные правки источников вики (`CLAUDE.md`, `Readme.md`, `agents/*`, `sections/routes/*`, `skills/*`) могут оставить вики устаревшей, поэтому переходим к шагу 6.
2. **Merge.** `git merge upstream/main --no-edit`. Конфликт по `Readme.md` — **ожидаемый**: в форке README про плагин, в upstream — про спецификацию; он автоматически разрешается в пользу нашего: `git checkout --ours Readme.md && git add Readme.md`. При ЛЮБОМ другом конфликте агент останавливается и сообщает — никакого форсированного разрешения.
3. **Пересборка.** `bash scripts/rebuild_all.sh` — регенерирует `sections/`, `metadata.json`, `glossary-quick.md`, `lexical-rules.md`, маршруты, xrefs и FAISS-индекс. Для шага эмбеддингов нужен `uv` (sentence-transformers + faiss-cpu через inline-зависимости скрипта).
4. **AI-обогащение `_index.md`.** Для каждой директории с `_index.md` читаем первые 30 строк каждого упомянутого файла секции и переписываем индекс с однопредложными описаниями на обычном языке — фокус на то, какую проблему секция помогает решить, до 120 символов, без FPF-терминов. Формат ссылки: `- [Title](filename.md) — описание одним предложением`.
5. **AI-обогащение `glossary-quick.md`.** Для каждого из 50 терминов читаем первые 20 строк исходной секции и добавляем колонку с простым определением (до 80 символов). Итоговая форма: `| Term | Primary Pattern | Plain Definition |`.
6. **Компиляция двуязычной вики.** Сначала `python3 ~/.claude/skills/wiki/scanner.py check .`. Если вики устарела — запустить `/wiki compile` (LLM-driven, инкрементально): пересобирает каждую затронутую статью в ОБОИХ `docs/wiki/ru/` и `docs/wiki/en/` и обновляет `docs/wiki/.state/manifest.json`. Запасного варианта из командной строки нет: если скилл `/wiki` недоступен — СТОП и отчёт. Проверяем повторным `scanner.py check .` — он должен вернуть 0 до любого коммита.
7. **Обновление changelog и версии.** Добавить раздел "What's New" на обычном языке в `CHANGELOG.md` под сегодняшней датой, с точки зрения пользователя (не копировать сообщения коммитов). Если синхронизация добавила новые пользовательские паттерны — поднять версию в **обоих** `.claude-plugin/plugin.json` **и** `.codex-plugin/plugin.json` (minor-бамп), чтобы они шли синхронно; иначе оставить как есть.
8. **Коммит и push.** Застейджить набор выше, закоммитить с сообщением `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh`, затем `git push`.

## Почему оба plugin.json бампятся вручную

Проект поставляется как плагин для двух хостов — Claude Code (`.claude-plugin/`) и Codex CLI (`.codex-plugin/`, ставится через `scripts/install_codex_plugin.py`). PreToolUse-хук changelog (`scripts/update_changelog.py`) поднимает версию **только** в `.claude-plugin/plugin.json`. Поэтому рутина fpf-sync вручную бампит **оба** манифеста, чтобы их версии оставались синхронными. Сейчас оба на `0.6.1`.

## Явный запрет

В исходнике перечислены инварианты, которые агент не должен нарушать:

- Не менять `FPF-Spec.md` (источник истины от upstream)
- Не менять `scripts/`, `agents/`, `skills/` (ручное сопровождение)
- Не править `docs/wiki/` руками — только через `/wiki compile`
- Никаких force-push и rebase — только merge
- Никакой FPF-терминологии в обогащённых описаниях
- Не останавливаться рано, если вики устарела из-за локальных правок — шаг 6 всё равно выполняется, а обновление коммитится
- Не полагаться на автотриггер скилла — вызывать скиллы явно по имени (шаг 6 зовёт `/wiki compile`); в headless / неинтерактивных прогонах скиллы доступны только через `/name`, а не по совпадению описания ([#32184](https://github.com/anthropics/claude-code/issues/32184))

## Триггеры

Синхронизацию теперь запускает единственный механизм — **Claude Code Remote Routine** (триггер `trig_01P7UzjrjgsgzLpMHn84bMoo`), cron 1-го и 15-го числа каждого месяца в 07:00 UTC (= 09:00 Europe/Belgrade), управляется на <https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo>. На каждом запуске читает `agents/fpf-sync.md` и выполняет восемь шагов выше.

Прежний GitHub Action (`.github/workflows/rebuild-sections.yml`) делал то же самое, но стабильно падал и был **удалён** — remote routine полностью его заменяет. Активного GitHub Action больше нет, второго пути обновления тоже.

## Связанные статьи

- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- [build-pipeline](../architecture/build-pipeline.md)
- [agent-team](../architecture/agent-team.md)
