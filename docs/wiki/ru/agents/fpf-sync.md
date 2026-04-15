---
title: fpf-sync
sources:
  - agents/fpf-sync.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - sync
  - scheduled
  - maintenance
---

# fpf-sync

> Источник: `agents/fpf-sync.md`

## Назначение

Сервисный агент по расписанию (раз в 2 недели, через remote trigger Claude Code — 1-го и 15-го числа каждого месяца). Синхронизирует локальный форк с upstream `ailev/FPF`, запускает полный Python-конвейер пересборки, затем делает AI-обогащение `_index.md` и `glossary-quick.md` — добавляет краткие описания на обычном языке. Коммитит и пушит все изменения.

В отличие от остальных агентов, fpf-sync никогда не общается с конечным пользователем — это чистое сопровождение проекта.

## Интерфейс

**Вход:** ничего (триггер по расписанию).

**Выход:** git-коммиты в main (`chore: sync upstream + AI-enhanced indexes`) и лог того, что было обогащено.

## Шесть шагов

1. **Проверка upstream.** `git fetch upstream main`, сравнение хэшей `FPF-Spec.md`. Совпадают → лог "No upstream changes" и остановка (экономия).
2. **Merge.** `git merge upstream/main --no-edit`. Конфликты → стоп и отчёт, никогда не форсим разрешение.
3. **Пересборка.** `bash scripts/rebuild_all.sh` — регенерирует `sections/`, `metadata.json`, `glossary-quick.md`, `lexical-rules.md`, маршруты, xrefs и FAISS-индекс. Для шага эмбеддингов нужен `uv`.
4. **AI-обогащение `_index.md`.** Для каждой директории с `_index.md` читаем первые 30 строк каждого упомянутого файла секции и переписываем индекс с однопредложными описаниями на обычном языке — фокус на то, какую проблему секция помогает решить, до 120 символов, без FPF-терминов.
5. **AI-обогащение `glossary-quick.md`.** Для каждого из 50 терминов читаем первые 20 строк исходной секции и добавляем колонку с простым определением (до 80 символов). Итоговая форма: `| Term | Primary Pattern | Plain Definition |`.
6. **Коммит и push.** `git add sections/ && git commit -m "chore: sync upstream + AI-enhanced indexes" && git push`.

## Явный запрет

В исходнике перечислены инварианты, которые агент не должен нарушать:

- Не менять `FPF-Spec.md` (источник истины от upstream)
- Не менять `scripts/`, `agents/`, `skills/` (ручное сопровождение)
- Никаких force-push и rebase — только merge
- Никакой FPF-терминологии в обогащённых описаниях
- Не запускаться, если в upstream нет изменений

## Триггеры

В CLAUDE.md описаны два слоя:

- **GitHub Action** (`.github/workflows/rebuild-sections.yml`) — на push в main и cron на 1-е и 15-е. Делает только Python-пересборку.
- **Claude Code Remote Trigger** — раз в 2 недели. Запускает полный цикл sync + rebuild + AI-enhance, описанный выше.

## Связанные статьи

- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- [build-pipeline](../architecture/build-pipeline.md)
- [agent-team](../architecture/agent-team.md)
- `.github/workflows/rebuild-sections.yml`
