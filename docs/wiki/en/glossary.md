---
title: Glossary
last_updated: 2026-04-15T00:00:00Z
tags:
  - glossary
---

# Glossary

Project-internal vocabulary — terms that appear across this wiki and describe the skill's own machinery. For the FPF domain glossary (pattern terms), see `sections/glossary-quick.md` in the repo; those terms never appear in user output.

| Term | Definition | See also |
|------|------------|----------|
| **Agent team** | The five markdown-prompt agents under `agents/` that together form the pipeline | [agent-team](architecture/agent-team.md) |
| **Burden** | The classification label for a user's coordination problem. Determines route and output template | [burden](concepts/burden.md) |
| **Classifier** | First agent. Reads user message, emits routing decision with tier/burden/budget | [fpf-classifier](agents/fpf-classifier.md) |
| **Confidence gate** | Classifier rule: high confidence auto-dispatch; low confidence asks the user first | [skill-entry-point](architecture/skill-entry-point.md) |
| **Core section** | A section marked `YES` in a route's Core column — loaded for minimum-load queries | [route-chain](concepts/route-chain.md) |
| **Cross-reference (`_xref.md`)** | Per-directory index of patterns in OTHER parts that reference this directory | [build_xrefs](modules/build_xrefs.md) |
| **FAISS index** | Binary similarity index over embeddings; lookups ~1 ms | [build_embeddings](modules/build_embeddings.md) |
| **Jargon guard** | Reviewer check 1: scan output for FPF terminology, rewrite any found in plain language | [fpf-reviewer](agents/fpf-reviewer.md) |
| **Lexical rules** | Mandatory term substitutions from Part K of the spec, enforced internally by the Reasoner | [build_lexical](modules/build_lexical.md) |
| **Mode A / Mode B** | Retriever modes: A = route chain (Tier 1), B = semantic fallback (Tier 2/3) | [fpf-retriever](agents/fpf-retriever.md) |
| **Pattern ID** | Hierarchical identifier like `A.6.P` or `B.3.3`. Appears in metadata but never in user output | [plain-language-contract](architecture/plain-language-contract.md) |
| **Pipeline depth** | Number of agents engaged: Retriever→Reasoner (minimum) or +Reviewer (full) | [pipeline-depth](concepts/pipeline-depth.md) |
| **Plain language contract** | Non-negotiable: FPF terminology never leaks to the user | [plain-language-contract](architecture/plain-language-contract.md) |
| **Reasoner** | Third agent. Applies pattern structure, outputs in user's language | [fpf-reasoner](agents/fpf-reasoner.md) |
| **Retriever** | Second agent. Loads sections via Mode A or Mode B | [fpf-retriever](agents/fpf-retriever.md) |
| **Reviewer** | Fourth agent (Tier 2/3). Jargon guard + grounding + actionability | [fpf-reviewer](agents/fpf-reviewer.md) |
| **Route** | Curated section chain for one burden; 10 routes total | [route-chain](concepts/route-chain.md) |
| **Route chain** | Ordered list of pattern IDs making up one route | [route-chain](concepts/route-chain.md) |
| **Section** | One `.md` file under `sections/` corresponding to one H2 in `FPF-Spec.md` | [split_spec](modules/split_spec.md) |
| **Semantic fallback** | Tier 2 retrieval: keyword search + FAISS when no route matches | [three-tier-retrieval](architecture/three-tier-retrieval.md) |
| **Signal** | Classifier stage 1: "is this a problem FPF can help with?" | [fpf-classifier](agents/fpf-classifier.md) |
| **Stagnation detection** | Retriever safeguard: escalate or report when loading in circles | [fpf-retriever](agents/fpf-retriever.md) |
| **Sync agent** | `fpf-sync` scheduled agent: upstream merge + rebuild + AI enhancement | [fpf-sync](agents/fpf-sync.md) |
| **Tier** | Retrieval strategy level: 1 (route), 2 (semantic), 3 (combined) | [tier](concepts/tier.md) |
