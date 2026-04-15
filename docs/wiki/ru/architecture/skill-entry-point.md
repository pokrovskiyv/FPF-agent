---
title: Точка входа в Skill
sources:
  - skills/fpf/SKILL.md
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - skill
  - entry-point
---

# Точка входа в Skill

## Компоненты

Точка входа в навык FPF — это рукопожатие между Claude Code и командой агентов.

| Компонент | Файл | Роль |
|-----------|------|------|
| Дескриптор скилла | `skills/fpf/SKILL.md` | YAML-фронтматтер с описанием триггера + тело с логикой маршрутизации |
| Манифест плагина | `.claude-plugin/plugin.json` | Имя плагина, версия, ключевые слова — читается загрузчиком плагинов Claude Code |
| Манифест marketplace | `.claude-plugin/marketplace.json` | Объявляет плагин в marketplace Claude Code — пользователи ставят через `/plugin marketplace add pokrovskiyv/FPF-agent` |

## Поток данных

1. Пользователь пишет сообщение, подходящее под описание во фронтматтере скилла (координация / решение / аудит / сравнение).
2. Claude Code читает `skills/fpf/SKILL.md` и запускает [fpf-classifier](../agents/fpf-classifier.md) через Task.
3. Классификатор возвращает структурированное решение маршрутизации.
4. Скилл запускает [fpf-retriever](../agents/fpf-retriever.md) с этим решением.
5. Ретривер загружает секции; скилл запускает [fpf-reasoner](../agents/fpf-reasoner.md).
6. Для Tier 2/3 (семантический или пересекающий) скилл запускает [fpf-reviewer](../agents/fpf-reviewer.md).
7. Итоговый вывод показывается пользователю — терминологии FPF нигде не видно.

Тело скилла содержит таблицу burden, таблицу глубины конвейера и логику confidence gate. Все пути внутри — относительно `${CLAUDE_PLUGIN_ROOT}`.

## Решения

- **Широкое описание триггера.** YAML-фронтматтер намеренно покрывает координацию, принятие решений, аудит, сравнение и сольный анализ — не только командную координацию. Это не даёт упустить легитимные кейсы, а жёсткий negative-список (нет синтаксиса, нет файловых операций) блокирует ложные срабатывания.
- **Confidence gate.** Высокая уверенность (≥70%) — авто-диспатч; низкая — предложение "Похоже на координационную задачу. Помочь её структурировать?" перед запуском. Явное упоминание термина FPF (A.6, UTS, DRR) обходит гейт.
- **Две параллельные редакции.** `skills/fpf/SKILL.md` (Claude Code) и `.agents/skills/fpf/SKILL.md` (Codex). Их описания должны быть побитово идентичны — см. тест паритета в [smoke_codex](../modules/smoke_codex.md). В Codex нет `Task`-диспатча, поэтому оркестрация инлайн-прошита в скилл.

## Связанные статьи

- [agent-team](agent-team.md)
- [plain-language-contract](plain-language-contract.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [smoke_codex](../modules/smoke_codex.md)
