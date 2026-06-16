---
title: Команда агентов
sources:
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - agents/fpf-sync.md
  - skills/fpf/SKILL.md
last_updated: 2026-06-16T03:34:37Z
tags:
  - architecture
  - agents
---

# Команда агентов

## Компоненты

Пять агентов, каждый — markdown-промпт в `agents/`. Четыре работают встроенно
на пользовательских запросах; пятый запускается вне конвейера, по расписанию.

| Агент | Модуль | Роль |
|-------|--------|------|
| **Classifier** | [fpf-classifier](../agents/fpf-classifier.md) | Решает, есть ли FPF-сигнал к обработке, выбирает тир и маршрут, выставляет бюджет токенов |
| **Retriever** | [fpf-retriever](../agents/fpf-retriever.md) | Загружает минимум секций — цепочка маршрута (Mode A) или keyword + FAISS семантический поиск (Mode B) |
| **Reasoner** | [fpf-reasoner](../agents/fpf-reasoner.md) | Применяет структуру паттерна к задаче пользователя, пишет на обычном языке (без FPF-жаргона) |
| **Reviewer** | [fpf-reviewer](../agents/fpf-reviewer.md) | Контроль качества: проверка жаргона, обоснованности, применимости (только Tier 2/3 и cross-cutting в Tier 1) |
| **Sync** | [fpf-sync](../agents/fpf-sync.md) | Сервисное сопровождение по расписанию: sync с upstream + пересборка + AI-обогащение индексов + обновление двуязычной вики |

## Поток данных

Четыре агента времени запроса складываются в адаптивный конвейер. Глубину
определяет Classifier; не каждый запрос доходит до Reviewer.

```
сообщение пользователя
     │
     ▼
┌──────────────┐
│ Classifier   │──► SIGNAL? TIER? BURDEN? ROUTE? BUDGET? SEARCH_QUERY?
└──────────────┘
     │
     ▼
┌──────────────┐        читает: routes/*.md, metadata.json,
│ Retriever    │───────►         _xref.md, semantic_search.py
└──────────────┘
     │
     ▼  содержимое загруженных секций
┌──────────────┐        читает (только внутри): glossary-quick.md,
│ Reasoner     │───────►                          lexical-rules.md
└──────────────┘
     │                    вывод на обычном языке
     │
     ├──► пользователь  (Tier 1 — простой маршрут)
     │
     ▼  (Tier 2/3 или Tier 1 cross-cutting)
┌──────────────┐
│ Reviewer     │──► STATUS: PASS | CORRECTED
└──────────────┘
     │
     ▼
пользователь


(отдельно, по расписанию, без взаимодействия — Claude Code Remote Routine)
┌──────────────┐
│ Sync         │──► цикл из 8 шагов: sync upstream + rebuild_all.sh
└──────────────┘     + AI-обогащение индексов + /wiki compile + коммит
```

Агенты общаются, передавая структурированный текст. Classifier выдаёт блок
`SIGNAL / TIER / BURDEN / ROUTE / BUDGET / SECTIONS / SEARCH_QUERY`; Retriever
возвращает содержимое загруженных секций со ссылками на источники; Reasoner
выдаёт результат на обычном языке; Reviewer возвращает `STATUS: PASS |
CORRECTED`. О том, как два режима Retriever сопоставлены с тирами, см.
[three-tier-retrieval](three-tier-retrieval.md).

### Sync: цикл сопровождения из 8 шагов

Агент Sync не входит в конвейер запросов. Он управляется **Claude Code Remote
Routine** (триггер `trig_01P7UzjrjgsgzLpMHn84bMoo`) по cron — 1-го и 15-го числа
каждого месяца в 07:00 UTC (= 09:00 Europe/Belgrade), управление —
<https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo>. Путь обновления
один: рутина при каждом запуске читает `agents/fpf-sync.md` и выполняет его
восемь шагов.

1. **Проверка upstream** — `git fetch upstream main`, сравнение хешей
   `FPF-Spec.md`. Если без изменений — шаги 2–5 пропускаются, но свежесть вики
   всё равно проверяется (шаг 6).
2. **Merge upstream** — `git merge upstream/main --no-edit`. Конфликт по
   `Readme.md` ожидаем (README нашего форка ориентирован на плагин) и
   автоматически разрешается через `git checkout --ours Readme.md && git add
   Readme.md`. ЛЮБОЙ другой конфликт останавливает запуск и идёт в отчёт.
3. **Пересборка** — `bash scripts/rebuild_all.sh` перегенерирует `sections/`,
   `metadata.json`, глоссарий, лексические правила, маршруты и индекс
   эмбеддингов FAISS.
4. **AI-обогащение `_index.md`** — для каждой секции в `_index.md` каждой
   директории пишется однострочное резюме на обычном языке.
5. **AI-обогащение `glossary-quick.md`** — для каждого из 50 терминов
   добавляется колонка с определением на обычном языке.
6. **Сборка двуязычной вики** — `python3 ~/.claude/skills/wiki/scanner.py
   check .`, затем `/wiki compile`, если вики устарела. Перегенерирует и
   `docs/wiki/ru/`, и `docs/wiki/en/`, обновляет `docs/wiki/.state/manifest.json`.
7. **Changelog + версия** — в `CHANGELOG.md` добавляется секция «What's New», и
   версия поднимается в ОБОИХ файлах — `.claude-plugin/plugin.json` и
   `.codex-plugin/plugin.json` (держатся синхронно).
8. **Коммит и пуш** — `git add sections/ docs/wiki/ CHANGELOG.md
   .claude-plugin/plugin.json .codex-plugin/plugin.json`, затем коммит с
   сообщением `chore: sync upstream + rebuild + AI-enhanced indexes + wiki
   refresh` и `git push`.

## Решения

- **Разделение ответственности, композиция конвейером.** У каждого агента
  времени запроса одна обязанность с чёткими входом и выходом — Classifier
  только решает, Retriever только грузит, Reasoner только пишет пользовательскую
  прозу, Reviewer только валидирует. Это держит промпты короткими и независимо
  тестируемыми.
- **Адаптивная глубина конвейера.** Простые запросы Tier 1: Retriever →
  Reasoner (~800 токенов). Маршрутные запросы Tier 1: ~1200–1500 токенов.
  Семантические Tier 2: добавляется Reviewer (~2000 токенов). Комбинированные
  Tier 3: все три (~2500 токенов). См.
  [pipeline-depth](../concepts/pipeline-depth.md).
- **Обычный язык — это контракт, а не пожелание.** Принцип #0 резонера и
  Check 1 ревьюера вместе обеспечивают полное отсутствие FPF-терминологии в
  выводе. См. [plain-language-contract](plain-language-contract.md).
- **Sync вне конвейера и с единственным путём.** Запускается только удалённой
  рутиной по расписанию, никогда — на запросах пользователя. Прежний GitHub
  Action (`.github/workflows/rebuild-sections.yml`) покрывал тот же процесс, но
  стабильно падал и был удалён — теперь удалённая рутина является единственным
  механизмом синхронизации.
- **Двойная упаковка плагина держится синхронно.** Проект поставляется как
  плагин для ОБОИХ окружений — Claude Code (`.claude-plugin/`) и Codex CLI
  (`.codex-plugin/` плюс `scripts/install_codex_plugin.py` и локальный
  маркетплейс в домашней директории). PreToolUse-хук changelog
  (`scripts/update_changelog.py`) поднимает версию только в
  `.claude-plugin/plugin.json`, поэтому шаг 7 Sync вручную поднимает оба файла
  `plugin.json`, чтобы версии оставались согласованными. Текущая версия: 0.6.1.

## Связанные статьи

- [skill-entry-point](skill-entry-point.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [plain-language-contract](plain-language-contract.md)
- [burden](../concepts/burden.md)
- [tier](../concepts/tier.md)
- [pipeline-depth](../concepts/pipeline-depth.md)
