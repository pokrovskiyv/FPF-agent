---
title: Конвейер пересборки
sources:
  - scripts/rebuild_all.sh
  - scripts/split_spec.py
  - scripts/build_metadata.py
  - scripts/enrich_metadata.py
  - scripts/build_glossary.py
  - scripts/build_lexical.py
  - scripts/build_routes.py
  - scripts/build_xrefs.py
  - scripts/build_embeddings.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - pipeline
  - rebuild
---

# Конвейер пересборки

## Компоненты

Конвейер управляется `scripts/rebuild_all.sh` — 8-шаговым shell-скриптом, пересобирающим все генерируемые артефакты из `FPF-Spec.md`. Шаги 1–7 — Python только на стандартной библиотеке; шаг 8 требует `uv` и модель `bge-m3`.

| Шаг | Скрипт | Что создаёт |
|-----|--------|-------------|
| 1 | [split_spec](../modules/split_spec.md) | `sections/**/*.md` (~240 файлов + `_index.md` в каждой директории) |
| 2 | [build_metadata](../modules/build_metadata.md) | `sections/metadata.json` |
| 3 | [enrich_metadata](../modules/enrich_metadata.md) | `sections/metadata.json` (на месте) |
| 4 | [build_glossary](../modules/build_glossary.md) | `sections/glossary-quick.md` |
| 5 | [build_lexical](../modules/build_lexical.md) | `sections/lexical-rules.md` |
| 6 | [build_routes](../modules/build_routes.md) | `sections/routes/route-*.md` |
| 7 | [build_xrefs](../modules/build_xrefs.md) | `sections/*/_xref.md` |
| 8 | [build_embeddings](../modules/build_embeddings.md) | `sections/embeddings/{faiss.index, metadata.json, config.json}` |

## Поток данных

```
FPF-Spec.md  (5.5 МБ, ~1.3 млн токенов)
     │
     ▼  шаг 1  rm -rf sections/; python3 scripts/split_spec.py
sections/**/*.md  +  sections/*/_index.md
     │
     ▼  шаг 2  python3 scripts/build_metadata.py
sections/metadata.json           (≈242 записи, пути к файлам разрешены)
     │
     ▼  шаг 3  python3 scripts/enrich_metadata.py
sections/metadata.json           (обогащён пользовательскими запросами, идемпотентно)
     │
     ├──► шаг 4  build_glossary   → glossary-quick.md
     ├──► шаг 5  build_lexical     → lexical-rules.md      (читает FPF-Spec Part K)
     ├──► шаг 6  build_routes      → routes/route-*.md
     ├──► шаг 7  build_xrefs       → */_xref.md
     └──► шаг 8  uv run build_embeddings → embeddings/
```

Каждый шаг идемпотентен: повторный запуск даёт те же артефакты, если источник не менялся. Шаг 1 перед работой удаляет `sections/`, чтобы устаревшие файлы не копились.

## Решения

- **Только стандартная библиотека для 7 из 8 шагов.** Пересборка запускается везде, где есть Python 3. Единственный шаг с тяжёлыми ML-зависимостями (`build_embeddings`) использует PEP 723 inline-metadata и `uv`, который автоматически ставит всё при первом запуске.
- **`set -euo pipefail` в начале.** Любая ошибка останавливает пересборку; shell падает, вместо того чтобы оставлять частичные артефакты.
- **В конце печатается статистика.** Скрипт считает директории, файлы секций, записи metadata и маршруты — быстрый sanity-check после каждой пересборки.
- **Шаг эмбеддингов только при пересборке.** Занимает ~90 секунд, после первого запуска ничего не докачивает, но именно этот шаг чаще всего падает на свежей машине (скачивание модели). Запускайте `./scripts/rebuild_all.sh` локально после синхронизации спеки; CI-путь пропускает шаг 8.

## Связанные статьи

- [overview](overview.md)
- [sync-and-rebuild](sync-and-rebuild.md)
- Отдельные статьи модулей (ссылки в таблице шагов выше)
