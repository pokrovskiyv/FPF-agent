---
title: "Маршрут 7: Этический аудит"
sources:
  - sections/routes/route-7-ethical-assurance.md
  - scripts/build_routes.py
last_updated: 2026-09-01T00:00:00Z
tags:
  - route
  - tier-1
  - ethical-assurance
---

# Маршрут 7: Этический аудит (Ethical Assurance)

> Источник: `sections/routes/route-7-ethical-assurance.md`

## Краткое описание

Срабатывает на вопросы о скрытых предубеждениях, этических допущениях или конфликтах ценностей между командами, работающими на разных масштабах ("как проверить наш процесс на предвзятость?", "у инженеров и операций конфликт ценностей — как его показать?"). На выходе пользователь получает реестр предубеждений, карту конфликтов по масштабам и чек-лист этического аудита. Это один из десяти входных маршрутов Tier-1; цепочка секций и её разбиение на core/full заданы декларативно в `scripts/build_routes.py` и разворачиваются в файл маршрута функцией `build_route_file()`.

## Ключевые решения

- **Длина цепочки:** 5 секций при полной загрузке, из них 3 отмечены как core.
- **Core-секции** (минимальная загрузка для простого запроса): `D.2` (Multilevel Ethics For System-Holon Work), `D.3` (Interlevel Ethical Conflict Structure), `D.5` (Bias Audit and Ethical Assurance).
- **Полная цепочка** (сложный запрос) добавляет: `D.1` (Ethical Value Plurality and FPF Boundary) и `D.4` (Ethical Mediation and Decision Use).
- **Порядок загрузки** фиксирован последовательностью цепочки; при обнаружении стагнации Retriever обращается к перекрёстным ссылкам в `_xref.md`.

## Цепочка секций

Цепочка загружается по порядку. Для простых запросов загружаются core-секции, для сложных — вся цепочка.

| # | Паттерн | Название | Core? |
|---|---------|----------|-------|
| 1 | D.1 | Ethical Value Plurality and FPF Boundary | |
| 2 | D.2 | Multilevel Ethics For System-Holon Work | YES |
| 3 | D.3 | Interlevel Ethical Conflict Structure | YES |
| 4 | D.4 | Ethical Mediation and Decision Use | |
| 5 | D.5 | Bias Audit and Ethical Assurance | YES |

Соответствие паттерн → файл разрешается против `sections/metadata.json` на этапе сборки; секции, путь к файлу которых ещё отсутствует в metadata, рендерятся с пустой колонкой файла, пока спецификация не будет пересобрана.

## Статус

Активен. Используется для задачи (burden) `ethical_assurance`, которую определяет Classifier. Шаблон резонера для этого маршрута: карта конфликтов по масштабам → реестр предубеждений (тип / место / риск / митигация) → чек-лист аудита. Определение маршрута находится в списке `ROUTES` в `scripts/build_routes.py`; редактирование цепочки или набора core там и повторный запуск скрипта регенерируют этот файл.

## Связанные статьи

- [fpf-classifier](../agents/fpf-classifier.md) — определяет задачу `ethical_assurance` и выбирает этот маршрут
- [fpf-retriever](../agents/fpf-retriever.md) — загружает цепочку секций (core или полную) и обращается к `_xref.md` при стагнации
- [fpf-reasoner](../agents/fpf-reasoner.md) — формирует реестр предубеждений, карту конфликтов и чек-лист аудита
- [route-chain](../concepts/route-chain.md) — объясняет, как устроены и используются цепочки маршрутов
