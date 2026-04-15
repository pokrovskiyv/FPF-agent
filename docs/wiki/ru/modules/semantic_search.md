---
title: semantic_search
sources:
  - scripts/semantic_search.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - query-time
  - embeddings
  - faiss
---

# semantic_search

> Источник: `scripts/semantic_search.py`

## Назначение

CLI для запросов к FAISS-индексу, созданному [build_embeddings](build_embeddings.md). Кодирует запрос на естественном языке (любом — английском, русском и т.д. благодаря мультиязычной модели `bge-m3`) той же моделью, что строила индекс, запускает top-K поиск по внутреннему произведению и печатает или возвращает JSON с найденными секциями.

Ретривер вызывает модуль как подпроцесс (`uv run scripts/semantic_search.py ... --json`) при семантическом откате (Tier 2) и комбинированном режиме (Tier 3).

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `load_model` | `(model_name: str) -> SentenceTransformer` | Ленивая загрузка модели с кэшем на уровне модуля — повторные вызовы в одном процессе не переинициализируют |
| `search` | `(query, index_dir=DEFAULT_INDEX_DIR, top_k=5) -> list[dict]` | Читает config/index/mapping, кодирует запрос с `query_prefix`, нормализует, вызывает `index.search`, возвращает ранжированный список `{rank, score, pattern_id, title, file, keywords}` |
| `main` | `() -> None` | Точка входа argparse (`query`, `--top-k`, `--index-dir`, `--json`, `--threshold`); печатает результаты как таблицу или JSON |

## Алгоритм

1. Загружаем `sections/embeddings/config.json` для имени модели и префикса запроса, `metadata.json` для соответствия id → секция и `faiss.index`.
2. Кодируем `query_prefix + query` с `normalize_embeddings=True` (совпадает с тем, как строился индекс).
3. Вызываем `index.search(vec, top_k)` — FAISS возвращает скоры (скалярные произведения) и индексы.
4. Зиппируем результаты с mapping, формируем итоговый список.
5. Опциональный фильтр по порогу: отбрасываем результаты с `score < threshold` (по умолчанию 0.0 = оставляем все).
6. Вывод: читаемая таблица (по умолчанию) или JSON (`--json`).

`_model_cache` на уровне модуля держит модель загруженной между вызовами в одном процессе — это важно, когда тесты или пакетные запросы вызывают `search()` многократно.

## Зависимости

**Импорты:** `argparse`, `json`, `sys`, `pathlib.Path`, `faiss`, `numpy`, `sentence_transformers.SentenceTransformer`.

**Требование к среде:** `uv` и готовый FAISS-индекс от `build_embeddings`. Модель (~2 ГБ) скачивается при первом запуске.

**Где используется:** вызывается как подпроцесс из [fpf-retriever](../agents/fpf-retriever.md) в семантическом режиме. Проверяется тестами [test_smoke](test_smoke.md) и [smoke_codex](smoke_codex.md).

## Связанные статьи

- [build_embeddings](build_embeddings.md) — строит индекс, по которому идёт поиск
- [fpf-retriever](../agents/fpf-retriever.md) — основной потребитель
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
