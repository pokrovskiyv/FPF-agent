---
name: fpf
description: Apply FPF to complex coordination, responsibility, terminology, or decision problems, and explain FPF when explicitly requested. Skip routine coding, simple rewrites, and unrelated lookups.
---

# FPF Thinking Amplifier

## Plugin root

For this edition, `<FPF_PLUGIN_ROOT>` is `${CLAUDE_PLUGIN_ROOT}`. Resolve runtime paths against that plugin root, never against the user's current project.

## Choose the scope

Use the smallest analysis that answers the user's request. Do not run a fixed sequence of roles, repeat intermediate outputs, or request permission to use a method for an already requested analysis. Ask only when missing information materially changes the result and cannot be reasonably inferred.

## Retrieve only what is needed

- For an explicit FPF concept, use `sections/glossary-quick.md` or `sections/metadata.json` to locate the relevant section.
- For a coordination problem, inspect the relevant `sections/routes/route-*.md` guide or metadata queries. Read only sections needed for the question; a route is a guide, not a mandatory reading list.
- Use semantic search only when narrower retrieval leaves a material gap:
  `uv run <FPF_PLUGIN_ROOT>/scripts/semantic_search.py "query" --top-k 5 --json --index-dir <FPF_PLUGIN_ROOT>/sections/embeddings`.
  Results contain `rank`, `score`, `pattern_id`, `title` and a plugin-relative `file`. Read the relevant matches, not every result by default. Respect offline and package-install constraints; metadata and keyword lookup remain valid fallbacks.
- Do not read or edit the monolithic specification for ordinary analysis. Do not rebuild embeddings or generated sections merely to answer a question.

## Apply and verify

Use the retrieved ideas to answer the actual question. Choose a table, responsibility map, comparison, or prose only when it helps the reader. Preserve the user's wording, commitments and uncertainty.

In ordinary applied answers, use the user's language and keep framework jargon and internal workflow out of the response. When the user explicitly asks about FPF, its terminology, specification, or agent design, use and explain the necessary terms and references. `sections/lexical-rules.md` governs specification editing, not ordinary user vocabulary.

Check that FPF interpretations match the retrieved sections. Support project facts with project evidence and external claims with appropriate sources; distinguish inference and unknowns. The FPF specification is not evidence for unrelated real-world facts.

Review relevance, grounding and clarity before delivery. An independent reviewer is optional when complexity or risk justifies it; a self-review is not an independent or cold review. Correct concrete defects, then stop when the requested answer is complete. Repeat checks only after changes, failures, or new evidence.

## Optional supporting guidance

Read only the relevant part of these shared prompts if the task needs deeper guidance:
- `agents/fpf-classifier.md` — ambiguous routing.
- `agents/fpf-retriever.md` — retrieval methods.
- `agents/fpf-reasoner.md` — examples for a specific coordination problem.
- `agents/fpf-reviewer.md` — deeper grounding and language review.

These references do not mandate spawning agents or loading every role. For Codex, treat their `${CLAUDE_PLUGIN_ROOT}` token as `<FPF_PLUGIN_ROOT>`. `agents/fpf-sync.md` is repository maintenance, not part of answering a user.
