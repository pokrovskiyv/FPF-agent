---
title: "Маршрут 6: Пересказ для аудитории"
sources:
  - sections/routes/route-6-rewrite-explanation.md
  - scripts/build_routes.py
last_updated: 2026-07-01T07:00:00Z
tags:
  - route
  - tier-1
  - rewrite-explanation
---

# Маршрут 6: Пересказ для аудитории (Rewrite Explanation)

> Источник: `sections/routes/route-6-rewrite-explanation.md`

## Краткое описание

Срабатывает на запросы вида "перепиши, не меняя смысл", "объясни для другой аудитории", "сравни две версии на верность смыслу". На выходе — переписанный текст с заметками о том, что сохранено и что изменено, плюс профиль верности смыслу. Цель — чтобы пересказ не превратился в молчаливый перевод, который незаметно теряет или искажает смысл. Это самый короткий маршрут Tier 1 (всего 5 секций, 3 из них core). Файл маршрута генерируется скриптом `scripts/build_routes.py` из записи `ROUTES[5]`: заголовки и пути файлов для каждого паттерна подставляются из `sections/metadata.json`.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке (самый короткий маршрут Tier 1), 3 из них core.
- **Core-секции:** `A.6.3.CR` (conservative retextualization — с сохранением объекта-предмета), `A.6.3.RT` (representation-scheme transition с сохранением EntityOfConcern), `E.17.EFP` (ExplanationFaithfulnessProfile — дисциплина использования объяснений).
- **Полная цепочка добавляет:** `E.17.ID.CR` (ComparativeReviewUnit — ограниченное сравнение по единицам сравнительного обзора) и `E.17.AUD.LHR` (PublicationUnit Stability Discipline and Local Head Restoration).
- **Резолвинг `A.6.3.CR`:** стоит первым в цепочке (и является core), резолвится в `sections/06-cluster-aiva-signature-stack-boundary-discipline-a6/10-a63cr-a63cr-conservativeretextualization-entityofconcern-preservin.md`.

## Статус

Активен. Используется для задачи `rewrite_explanation`. Шаблон вывода резонера: "Переписанный текст → Что сохранено → Что изменено (с обоснованием)". Файл маршрута пересобирается командой `python3 scripts/build_routes.py` (часть `./scripts/rebuild_all.sh`) при каждом изменении метаданных — цепочка и ссылки на паттерны синхронизируются с источником автоматически.

## Стратегия загрузки

- **Минимальная загрузка** (простой запрос): первые 3 core-секции.
- **Полная загрузка** (сложный запрос): все 5 секций цепочки.
- **При застое:** проверить соответствующий `_xref.md` на перекрёстные ссылки.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — выбирает этот маршрут по задаче
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций
- [fpf-reasoner](../agents/fpf-reasoner.md) — формирует пересказ и заметки о верности смыслу
- [route-chain](../concepts/route-chain.md) — описывает механизм цепочек маршрутов
