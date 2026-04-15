---
title: FPF-agent Wiki (Русский)
last_updated: 2026-04-15T00:00:00Z
tags:
  - index
---

# FPF-agent Wiki

Автоматически генерируемая документация по плагину **FPF-agent** для Claude Code — амплификатору мышления, применяющему паттерны First Principles Framework к координационным задачам пользователя так, чтобы терминология FPF никогда не попадала наружу.

## Устройство проекта

Репозиторий — форк `ailev/FPF` плюс скилл Claude Code и пять агентов, превращающих спецификацию FPF объёмом 5.5 МБ в нечто, чем может пользоваться обычный пользователь. Четыре подвижных части: монолит спеки, 240+ генерируемых файлов секций, точка входа скилла и команда агентов.

Ключевые архитектурные статьи:

- [Обзор](architecture/overview.md) — компоненты, поток данных, решения
- [Точка входа в Skill](architecture/skill-entry-point.md) — как Claude Code запускает агентов
- [Команда агентов](architecture/agent-team.md) — пять агентов и их контракт
- [Трёхъярусная загрузка](architecture/three-tier-retrieval.md) — маршруты как кэш, семантика как откат
- [Контракт обычного языка](architecture/plain-language-contract.md) — не подлежит обсуждению
- [Конвейер пересборки](architecture/build-pipeline.md) — 8 шагов
- [Синхронизация и пересборка](architecture/sync-and-rebuild.md) — merge upstream по расписанию

## Разделы

| Раздел | Статей | Описание |
|--------|--------|----------|
| [Модули](modules/) | 12 | Python-скрипты пересборки всех генерируемых артефактов |
| [Агенты](agents/) | 5 | Промпты агентов (classifier, retriever, reasoner, reviewer, sync) |
| [Маршруты](routes/) | 10 | Пользовательские маршруты burden → паттерны |
| [Архитектура](architecture/) | 7 | Системные виды |
| [Концепции](concepts/) | 5 | Внутренний словарь проекта (не термины FPF) |

## Модули

Двенадцать Python-скриптов, организующих конвейер пересборки и семантический поиск во время выполнения.

- [split_spec](modules/split_spec.md) — разбивает монолит 5.5 МБ на ~240 файлов секций
- [build_metadata](modules/build_metadata.md) — парсит оглавление в `metadata.json`
- [enrich_metadata](modules/enrich_metadata.md) — добавляет пользовательские запросы (EN+RU)
- [build_glossary](modules/build_glossary.md) — извлекает топ-50 терминов для резонера
- [build_lexical](modules/build_lexical.md) — правила замены из Part K
- [build_routes](modules/build_routes.md) — генерирует 10 файлов маршрутов
- [build_xrefs](modules/build_xrefs.md) — инвертированный граф перекрёстных ссылок
- [build_embeddings](modules/build_embeddings.md) — FAISS-индекс с bge-m3
- [semantic_search](modules/semantic_search.md) — CLI запроса во время выполнения
- [test_smoke](modules/test_smoke.md) — тесты целостности конвейера
- [smoke_codex](modules/smoke_codex.md) — тесты Codex-редакции скилла
- [update_changelog](modules/update_changelog.md) — PreToolUse-хук на коммитах

## Агенты

- [fpf-classifier](agents/fpf-classifier.md) — детекция burden и выбор тира
- [fpf-retriever](agents/fpf-retriever.md) — загрузка секций (маршрут или семантика)
- [fpf-reasoner](agents/fpf-reasoner.md) — вывод на обычном языке
- [fpf-reviewer](agents/fpf-reviewer.md) — страж жаргона + обоснованность + применимость
- [fpf-sync](agents/fpf-sync.md) — сервисная синхронизация по расписанию

## Маршруты

Десять маршрутов, каждый — подобранная цепочка секций под одну пользовательскую задачу.

- [Маршрут 1: Зоны ответственности](routes/route-1-project-alignment.md)
- [Маршрут 2: Язык и терминология](routes/route-2-language-discovery.md)
- [Маршрут 3: Разбор контракта](routes/route-3-boundary-unpacking.md)
- [Маршрут 4: Сравнение альтернатив](routes/route-4-comparison-selection.md)
- [Маршрут 5: Портфель подходов](routes/route-5-generator-portfolio.md)
- [Маршрут 6: Пересказ для аудитории](routes/route-6-rewrite-explanation.md)
- [Маршрут 7: Этический аудит](routes/route-7-ethical-assurance.md)
- [Маршрут 8: Доверие и обоснование](routes/route-8-trust-assurance.md)
- [Маршрут 9: Композиция и агрегация](routes/route-9-composition-aggregation.md)
- [Маршрут 10: Эволюция и обучение](routes/route-10-evolution-learning.md)

## Концепции

Внутренний словарь проекта. Это не термины предметной области FPF — это то, как мы говорим о внутреннем устройстве самого скилла.

- [Burden](concepts/burden.md)
- [Цепочка маршрута](concepts/route-chain.md)
- [Tier (ярус)](concepts/tier.md)
- [Глубина конвейера](concepts/pipeline-depth.md)
- [Рабочий процесс changelog](concepts/changelog-workflow.md)

## Глоссарий

Список всех терминов, встречающихся в статьях — см. [Глоссарий](glossary.md).

## На другом языке

[English wiki](../en/index.md) — documentation for code contributors.
