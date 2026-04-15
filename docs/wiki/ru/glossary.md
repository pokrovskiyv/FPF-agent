---
title: Глоссарий
last_updated: 2026-04-15T00:00:00Z
tags:
  - glossary
---

# Глоссарий

Внутренний словарь проекта — термины, которые встречаются в статьях и описывают механику самого скилла. Для глоссария предметной области FPF (термины паттернов) см. `sections/glossary-quick.md` в репозитории; эти термины никогда не попадают в пользовательский вывод.

| Термин | Определение | См. также |
|--------|-------------|-----------|
| **Burden** | Классификационная метка координационной задачи пользователя. Определяет маршрут и шаблон ответа | [burden](concepts/burden.md) |
| **Classifier** | Первый агент. Читает сообщение пользователя, выдаёт решение маршрутизации (tier/burden/бюджет) | [fpf-classifier](agents/fpf-classifier.md) |
| **Confidence gate** | Правило классификатора: высокая уверенность — авто-диспатч, низкая — сначала спрашивает пользователя | [skill-entry-point](architecture/skill-entry-point.md) |
| **Core-секция** | Секция, отмеченная `YES` в колонке Core маршрута — грузится при минимальной загрузке | [route-chain](concepts/route-chain.md) |
| **FAISS-индекс** | Бинарный индекс подобия по эмбеддингам; поиск ~1 мс | [build_embeddings](modules/build_embeddings.md) |
| **Jargon guard (страж жаргона)** | Check 1 ревьюера: сканирует вывод на терминологию FPF, переписывает нарушения на обычный язык | [fpf-reviewer](agents/fpf-reviewer.md) |
| **Mode A / Mode B** | Режимы ретривера: A — цепочка маршрута (Tier 1), B — семантический откат (Tier 2/3) | [fpf-retriever](agents/fpf-retriever.md) |
| **Pattern ID** | Иерархический идентификатор вроде `A.6.P` или `B.3.3`. Есть в метаданных, но никогда в пользовательском выводе | [plain-language-contract](architecture/plain-language-contract.md) |
| **Pipeline depth (глубина конвейера)** | Число задействованных агентов: Retriever→Reasoner (минимум) или +Reviewer (полный) | [pipeline-depth](concepts/pipeline-depth.md) |
| **Plain language contract (контракт обычного языка)** | Не подлежит обсуждению: терминология FPF никогда не попадает к пользователю | [plain-language-contract](architecture/plain-language-contract.md) |
| **Reasoner** | Третий агент. Применяет структуру паттерна, пишет на языке пользователя | [fpf-reasoner](agents/fpf-reasoner.md) |
| **Retriever** | Второй агент. Грузит секции через Mode A или Mode B | [fpf-retriever](agents/fpf-retriever.md) |
| **Reviewer** | Четвёртый агент (Tier 2/3). Страж жаргона + обоснованность + применимость | [fpf-reviewer](agents/fpf-reviewer.md) |
| **Route (маршрут)** | Подобранная цепочка секций под один burden; всего 10 маршрутов | [route-chain](concepts/route-chain.md) |
| **Route chain (цепочка маршрута)** | Упорядоченный список pattern ID, составляющих маршрут | [route-chain](concepts/route-chain.md) |
| **Section (секция)** | Один `.md` в `sections/`, соответствующий одному H2 в `FPF-Spec.md` | [split_spec](modules/split_spec.md) |
| **Semantic fallback** | Загрузка Tier 2: keyword search + FAISS, когда маршрут не подходит | [three-tier-retrieval](architecture/three-tier-retrieval.md) |
| **Signal (сигнал)** | Стадия 1 классификатора: "это проблема, с которой FPF может помочь?" | [fpf-classifier](agents/fpf-classifier.md) |
| **Stagnation detection (детекция застревания)** | Предохранитель ретривера: эскалация или отчёт при зацикливании | [fpf-retriever](agents/fpf-retriever.md) |
| **Sync-агент** | `fpf-sync` по расписанию: merge upstream + пересборка + AI-обогащение | [fpf-sync](agents/fpf-sync.md) |
| **Tier (ярус)** | Уровень стратегии загрузки: 1 (маршрут), 2 (семантика), 3 (комбинация) | [tier](concepts/tier.md) |
| **Команда агентов** | Пять markdown-промпт агентов в `agents/`, составляющих конвейер | [agent-team](architecture/agent-team.md) |
| **Лексические правила** | Обязательные замены терминов из Part K спеки, применяемые резонером внутренне | [build_lexical](modules/build_lexical.md) |
| **Перекрёстная ссылка (`_xref.md`)** | Индекс паттернов из ДРУГИХ Part, ссылающихся на эту директорию | [build_xrefs](modules/build_xrefs.md) |
