---
title: "Маршрут 8: Доверие и обоснование"
sources:
  - sections/routes/route-8-trust-assurance.md
  - scripts/build_routes.py
last_updated: 2026-07-01T07:00:00Z
tags:
  - spec
  - route
  - tier-1
  - trust-assurance
---

# Маршрут 8: Доверие и обоснование (Trust Assurance)

> Источник: `sections/routes/route-8-trust-assurance.md`

## Краткое описание

Маршрут 8 срабатывает, когда пользователь сомневается, можно ли доверять числу, оценке или системе: «можно ли доверять этой метрике?», «как агрегировать уверенность без завышенных утверждений?», «какова доказательная база за этим?». Он загружает расчёт доверия и обоснования, чтобы резонер построил профиль гарантий — формальность, область и надёжность по каждому компоненту — вместе с картой зависимостей и явным списком пробелов в доказательствах. Смысл — сделать слабые звенья видимыми, а не позволять одному уверенно выглядящему агрегату их прятать.

Это один из десяти практических входных маршрутов. Его цепочка секций задана как запись данных в `scripts/build_routes.py` (`ROUTES[7]`, `id: 8`, `slug: "trust-assurance"`) и рендерится в `sections/routes/route-8-trust-assurance.md` функцией `build_route_file`, которая резолвит каждый pattern ID по `sections/metadata.json`, подставляя заголовки и пути к файлам.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке; 3 помечены как core.
- **Core-секции (минимальная загрузка):** `B.3` (Trust & Assurance Calculus — F–G–R with congruence), `B.3.5` (Working-Model Relations & Grounding, CT2R-LOG), `B.1` (Holon Aggregation and Part-Whole Construction). Эти три отвечают на простую форму вопроса.
- **Полная цепочка добавляет:** `B.1.1` (Dependency Structure and Relation Grounding) и `A.6.B` (Boundary Norm Square — laws / admissibility / deontics / work); подтягиваются для сложных запросов, где важны зависимости агрегации и граничные обязательства.
- **Стратегия загрузки:** минимальная загрузка = первые 3 core-секции для простого запроса; полная = все 5 для сложного; при застое смотреть `_xref.md` секции за перекрёстными ссылками, а не расширять цепочку вслепую.
- **Генерируется, а не правится вручную:** файл маршрута пересоздаётся `build_routes.py` из таблицы `ROUTES`, поэтому цепочка остаётся синхронной с каноническими pattern ID и любыми изменениями заголовков/путей в `metadata.json`.

## Цепочка секций

| # | Паттерн | Заголовок | Core? |
|---|---------|-----------|-------|
| 1 | `B.3` | Trust & Assurance Calculus (F–G–R with Congruence) | да |
| 2 | `B.3.5` | Working-Model Relations & Grounding (CT2R-LOG) | да |
| 3 | `B.1` | Holon Aggregation and Part-Whole Construction | да |
| 4 | `B.1.1` | Dependency Structure and Relation Grounding | — |
| 5 | `A.6.B` | Boundary Norm Square (Laws / Admissibility / Deontics / Work) | — |

## Статус

Активен. Выбирается классификатором для задачи `trust_assurance` и потребляется ретривером, который сначала загружает три core-секции, а оставшиеся две подтягивает только для сложных запросов. Резонер выдаёт таблицу уверенности по компонентам → пробелы в доказательствах (где уверенность слабее всего) → рекомендации.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу `trust_assurance` и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку (3 core, затем полные 5)
- [fpf-reasoner](../agents/fpf-reasoner.md) — превращает цепочку в профиль гарантий и перечень пробелов
- [route-chain](../concepts/route-chain.md) — как маршруты кодируют упорядоченную цепочку секций
- [tier](../concepts/tier.md) — маршруты как кэш извлечения уровня Tier-1
