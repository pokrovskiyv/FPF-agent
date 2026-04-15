---
title: build_embeddings
sources:
  - scripts/build_embeddings.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - embeddings
  - faiss
---

# build_embeddings

> Источник: `scripts/build_embeddings.py`

## Назначение

Строит FAISS-индекс (flat inner-product) по всем секциям из `metadata.json`, используя мультиязычную модель эмбеддингов `BAAI/bge-m3` (1024 измерения). Индекс обеспечивает семантический откат (Tier 2): когда задача пользователя не совпадает ни с одним из 10 курируемых маршрутов, ретривер запрашивает индекс для поиска ближайших по смыслу секций.

В отличие от других скриптов конвейера, требует внешние зависимости (`sentence-transformers`, `faiss-cpu`, `numpy`), управляемые через inline `# /// script` (PEP 723); запускается через `uv run scripts/build_embeddings.py` — `uv` ставит зависимости по требованию.

## Интерфейс

| Функция | Сигнатура | Что делает |
|---------|-----------|-----------|
| `load_sections` | `(metadata_path: Path) -> list[dict]` | Обходит метаданные, читает каждый найденный файл секции, собирает сводный текст (`Pattern P: title \n Keywords: ... \n Questions: ... \n content[:2000]`), пропускает секции короче 50 символов |
| `build_index` | `(sections: list[dict], model_name: str) -> tuple[IndexFlatIP, ndarray]` | Загружает модель sentence-transformers, кодирует батчами по 8 с L2-нормализацией, строит FAISS IP-индекс (эквивалент косинусного сходства на нормализованных векторах) |
| `main` | `() -> None` | Точка входа argparse (`--metadata`, `--model`, `--output`); пишет `faiss.index`, `metadata.json` (соответствие id → секция) и `config.json` (имя модели, размерность, префикс запроса) |

## Алгоритм

1. Загружаем `sections/metadata.json`.
2. Для каждой записи с найденным `file` читаем файл; пропускаем, если меньше 50 символов контента.
3. Строим составной текст: pattern ID + название + до 10 ключевых слов + до 5 пользовательских вопросов + до 2000 символов тела. Это даёт эмбеддеру несколько якорей: заголовки для точных совпадений, вопросы для поиска на обычном языке, тело для тематических совпадений.
4. Кодируем все тексты за один батч-вызов с `normalize_embeddings=True`. Храним как float32.
5. Строим `faiss.IndexFlatIP` (inner-product индекс, эквивалентный косинусной близости на нормализованных векторах) и добавляем все эмбеддинги.
6. Сериализуем три файла: `faiss.index`, параллельный `metadata.json` (ключи — индексы в списке) и небольшой `config.json` с именем модели (нужно при запросе) и `query_prefix: "query: "`.

## Зависимости

**Импорты:** `argparse`, `json`, `sys`, `pathlib.Path`, `faiss`, `numpy`, `sentence_transformers.SentenceTransformer`.

**Требование к среде:** `uv` (автоматически ставит sentence-transformers, faiss-cpu, numpy). Модель (~2 ГБ) скачивается при первом запуске.

**Где используется:** вызывается из `scripts/rebuild_all.sh` (шаг 8). Результат читает [semantic_search](semantic_search.md) при запросе.

## Связанные статьи

- [semantic_search](semantic_search.md) — парный модуль со стороны запроса
- [build_metadata](build_metadata.md) / [enrich_metadata](enrich_metadata.md) — формируют вход
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [fpf-retriever](../agents/fpf-retriever.md) — вызывает semantic_search как подпроцесс
