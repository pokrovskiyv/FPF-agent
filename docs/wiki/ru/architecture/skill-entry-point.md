---
title: Точка входа в Skill
sources:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - skills/fpf/SKILL.md
last_updated: 2026-07-15T17:17:20Z
tags:
  - architecture
  - skill
  - entry-point
---

# Точка входа в Skill

## Компоненты

Точка входа в навык FPF — это рукопожатие между хостом (Claude Code или Codex CLI) и командой агентов. Один и тот же навык поставляется как плагин для **двух** рантаймов.

| Компонент | Файл | Роль |
|-----------|------|------|
| Дескриптор скилла | `skills/fpf/SKILL.md` | YAML-фронтматтер с описанием триггера + тело с логикой маршрутизации |
| Манифест плагина | `.claude-plugin/plugin.json` | Имя плагина, `version` (`0.6.3`), ключевые слова — читается загрузчиком плагинов Claude Code |
| Манифест marketplace | `.claude-plugin/marketplace.json` | Объявляет плагин `fpf` (source `./`, репозиторий `pokrovskiyv/FPF-agent`) — пользователи ставят через `/plugin marketplace add pokrovskiyv/FPF-agent` |
| Манифест плагина Codex | `.codex-plugin/plugin.json` | Зеркальный манифест для редакции Codex CLI; версия держится синхронно с `.claude-plugin/plugin.json` |
| Установщик Codex | `scripts/install_codex_plugin.py` | Ставит плагин FPF в Codex CLI через локальный (в домашней директории) marketplace |

Плагин представляется как *«Coordination patterns for specialists, teams, and AI agents»* с `category: workflow` и ключевыми словами `coordination`, `structured-thinking`, `decision-making`, `comparison`, `audit`.

## Поток данных

1. Пользователь пишет сообщение, подходящее под описание во фронтматтере скилла (координация / решение / аудит / сравнение или явный термин FPF).
2. Хост (Claude Code или Codex CLI) читает `skills/fpf/SKILL.md` и запускает [fpf-classifier](../agents/fpf-classifier.md).
3. Классификатор возвращает структурированное решение маршрутизации (burden, tier, route).
4. Скилл запускает [fpf-retriever](../agents/fpf-retriever.md) с этим решением.
5. Ретривер загружает максимально узкие релевантные секции; скилл запускает [fpf-reasoner](../agents/fpf-reasoner.md).
6. Для Tier 2/3 (семантический фолбэк или пересекающий запрос) скилл запускает [fpf-reviewer](../agents/fpf-reviewer.md) для проверки обоснованности и контроля жаргона.
7. Итоговый вывод показывается пользователю — терминологии FPF нигде не видно.

Тело скилла содержит таблицу burden, таблицу глубины конвейера и логику confidence gate. Все пути внутри — относительно `${CLAUDE_PLUGIN_ROOT}`.

## Решения

- **Широкое описание триггера.** YAML-фронтматтер намеренно покрывает координацию, принятие решений, аудит, сравнение и сольный анализ — не только командную координацию. Это не даёт упустить легитимные кейсы, а жёсткий negative-список (нет обычного кодинга, нет простых багфиксов, нет вопросов по синтаксису) блокирует ложные срабатывания.
- **Confidence gate.** Высокая уверенность (≥70%) — авто-диспатч; низкая — предложение *«Похоже на координационную задачу. Помочь её структурировать?»* перед запуском. Явное упоминание термина FPF (holon, UTS, DRR) обходит гейт.
- **Упаковка под два рантайма.** Проект упакован как плагин **сразу для двух** хостов: Claude Code (`.claude-plugin/`) и Codex CLI (`.codex-plugin/` + `scripts/install_codex_plugin.py` + локальный marketplace в домашней директории). Это не Claude-Code-only артефакт. Оба манифеста несут одну и ту же версию (`0.6.3`); как они держатся синхронно — см. [Версионирование](#версионирование).
- **Контракт простого языка.** FPF — невидимая инфраструктура: тело скилла запрещает любую терминологию FPF в выводе. Паттерны применяются внутренне Reasoner-ом и контролируются Reviewer-ом. См. [plain-language-contract](plain-language-contract.md).

## Версионирование

Поле `version` живёт в двух манифестах и должно двигаться синхронно:

- PreToolUse-хук обновления чейнджлога (`scripts/update_changelog.py`) запускается перед каждым `git commit` и авто-бампит **только** `.claude-plugin/plugin.json` (`feat` → minor, `fix` → patch, `feat!` → major).
- Рутина [fpf-sync](../agents/fpf-sync.md) (Step 7) вручную бампит **оба** файла — `.claude-plugin/plugin.json` и `.codex-plugin/plugin.json` — чтобы обе редакции оставались в lockstep.

Единственный путь обновления спецификации и сгенерированных артефактов — **Claude Code Remote Routine** (триггер `trig_01P7UzjrjgsgzLpMHn84bMoo`, cron 1-го и 15-го числа каждого месяца в 07:00 UTC = 09:00 Europe/Belgrade). Прежний GitHub Action `.github/workflows/rebuild-sections.yml` больше не существует; второго механизма синхронизации нет. Восьмишаговый конвейер — см. [fpf-sync](../agents/fpf-sync.md).

## Связанные статьи

- [agent-team](agent-team.md)
- [plain-language-contract](plain-language-contract.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-sync](../agents/fpf-sync.md)
