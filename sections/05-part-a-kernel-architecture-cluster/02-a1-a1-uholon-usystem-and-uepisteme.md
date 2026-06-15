## A.1 - U.Holon, U.System, and U.Episteme

> **Type:** Part A architectural ontology pattern
> **Status:** Stable
> **Normativity:** Normative unless a section is explicitly informative

### A.1:0 - Use This When

Use this pattern when a project must say what kind of thing is under concern before it can discuss parts, boundaries, interactions, roles, work, architecture, or descriptions.

Typical moments:

- a team calls everything a "system" and then tries to ask physical questions about theories, documents, models, or descriptions;
- an episteme is treated as an acting agent that performs work or makes decisions;
- a group, organization, model, document set, machine, neural-network architecture, or research program must be treated as a whole with parts;
- a set of items is expected to act, but no boundary, part-whole relation, or acting system has been named;
- architecture or structure claims need a grounding holon before selected structures can be described.

**First useful move.** Decide whether the subject is only a `U.Entity`, a `U.Holon`, a `U.System` holon, or a `U.Episteme` holon in the current bounded context.

**What goes wrong if missed.** A theory gets ports, a document edits itself, a list becomes an acting organization, and architecture is discussed without naming the holon whose structure is being selected.

**What this buys.** FPF gets one compact root for composition: identity starts at `U.Entity`; part-whole composition starts at `U.Holon`; acting work attaches to `U.System`; claim-bearing knowledge is carried by `U.Episteme` without making it an agent.

**Not this pattern when.**

- If the current question is local vocabulary, role assignment, or meaning inside one semantic frame, use `A.1.1` and the role-governing patterns.
- If the current question is the episteme slot relation, use `C.2.1`.
- If the current question is selected structure over a holon, use `A.22`.
- If the current question is architecture of a holon in context, use `C.30`.
- If the current question is work, method, or role-method-work alignment, use `A.15` and its dependent patterns.

### A.1:1 - Problem Frame

FPF cannot use `system` as its universal root. A pump, a theory, a software product, a legal code, a dashboard, a research program, and a team can all be objects under concern, but they do not all act, exchange matter, have physical ports, or execute methods.

The root distinction is:

- `U.Entity`: something that can be individuated and referenced;
- `U.Holon`: an entity that is usable as a whole with parts and as a part within larger wholes;
- `U.System`: an acting physical or operational holon;
- `U.Episteme`: a claim-bearing, non-agentive holon.

A.1 governs this holonic ontology. It lets FPF talk about composition and boundaries across systems and epistemes without building a second ontology from the words "object", "system", "document", "model", "theory", or "architecture".

### A.1:2 - Problem

Without A.1:

1. **System-bias spreads.** Physical assumptions are projected onto epistemes, descriptions, theories, and documents.
2. **Epistemes become agents.** A document, theory, model, or pattern is said to decide, perform, authorize, promise, or edit itself.
3. **Collections become collectives by wording.** A set of people, services, files, or claims is treated as an acting whole without a boundary and role assignment.
4. **Architecture loses its grounding holon.** A structure or architecture claim floats free of the holon whose structure is being selected.
5. **Part-whole reasoning is applied too early.** A bare entity is given parts, components, and aggregation before it is modeled as a holon.

### A.1:3 - Forces

| Force | Tension |
| --- | --- |
| Universal root vs domain comfort | Practitioners know words such as system, theory, model, product, and organization; FPF needs a cross-domain root that does not import one domain's assumptions. |
| Identity vs composition | A thing can be individuated before FPF knows whether it has parts or belongs to a larger whole. |
| Acting vs claim-bearing | Systems can enact roles, methods, plans, and work; epistemes can be described, revised, published, and used, but they do not act by themselves. |
| Boundary clarity vs modeling burden | A holon needs a boundary; not every first mention needs a full decomposition. |
| Collection vs collective | A set can be useful without being an acting system; an acting group needs a boundary and systemhood. |

### A.1:4 - Solution

Use the A.1 holon stack:

```text
U.Entity
  U.Holon
    U.System
    U.Episteme
```

This is not a publication hierarchy. It is the root ontology for cross-domain composition in FPF.

#### A.1:4.1 - U.Entity

`U.Entity` is anything that can be individuated and referenced under a bounded context. It carries no part-whole assumption by itself.

Use `U.Entity` when the current move only needs to point to a thing: a number, a claim, a named product, a material batch, a data value, a legal clause, a role value, a source reference, or another object under concern.

Do not apply holon aggregation, membership tests, or acting-system roles to a bare `U.Entity` unless the current pattern also models it as a `U.Holon` or a subtype of `U.Holon`.

#### A.1:4.2 - U.Holon

`U.Holon` is a `U.Entity` treated as a whole with parts and as a participant in larger wholes under a bounded context.

The A.1 holon slot relation is:

```text
HolonSlotRelation:
  holonIdentity:
  boundedContextRef:
  boundaryRef:
  partRelationSet:
  containingWholeRef?
  interactionSet?
  subtypeKind?: U.System | U.Episteme | other accepted subtype
  selectedStructureRef?
```

The boundary is current for the bounded context. A holon may have several possible boundary descriptions across contexts or viewpoints, but one current holon use must say which boundary governs the claim being made.

`partRelationSet` names the part-whole relations current for the use. Under open-world discipline, an omitted part list means "not recovered or not current for this claim", not "there are no parts."

#### A.1:4.3 - Boundary and Interaction

`U.Boundary` delimits the holon from its environment in the current bounded context.

`U.Interaction` names what crosses that boundary when such crossing is current: matter, energy, information, control signal, material flow, document transfer, claim update, or another governed crossing kind.

Do not call every boundary an interface. Use interface language only when a governing module, signature, mechanism, architecture, or boundary pattern makes interface meaning current.

#### A.1:4.4 - Holon Membership Test

When a candidate part is contested, use the holon membership test:

1. **Dependency:** removing the candidate breaks a core invariant of the holon.
2. **Internal interaction:** the candidate participates in interactions within the holon boundary that matter for the current claim.
3. **Emergence:** the candidate contributes to a collective property that justifies treating the whole as one holon.

Passing one or more tests can justify part membership for the current claim. Failing all three keeps the candidate outside the holon boundary for that claim.

#### A.1:4.5 - U.System

`U.System` is a holon that can act physically or operationally. It can bear roles, enact methods, perform work, participate in mechanisms, maintain state, transform other entities, and produce effects.

Use `U.System` when the current claim needs acting-system eligibility:

- role assignment to a system in a bounded context;
- method enactment or work occurrence;
- physical or operational boundary crossing;
- system architecture or selected structure;
- mechanism realization or transformer participation.

A collective system is not the same as a set. If a group of people, machines, services, or agents is expected to act, model the acting whole as a `U.System` with a boundary and role assignments. If no acting whole is claimed, keep it as a set or collection under the governing relation.

#### A.1:4.6 - U.Episteme

`U.Episteme` is a holon whose parts are claim-bearing and interpretation-bearing values: claims, definitions, reference schemes, viewpoints, evidence relations, argument structures, model content, or other episteme components governed by `C.2.1`.

`U.Episteme` is non-agentive. It does not decide, promise, authorize, perform work, or revise itself. A system in role may write, revise, publish, compare, transform, or use an episteme. The episteme remains the claim-bearing holon under the `C.2.1` slot relation.

An episteme can be an `EntityOfConcern`. This does not make it an acting system. It means the current description, evaluation, architecture claim, or transformation claim is about that episteme as the subject under concern.

#### A.1:4.7 - Cross-Level Use

The same project object can appear at different levels without changing kind by wording:

- a system can fill `GroundingHolonSlot` in an episteme description;
- an episteme can be the `EntityOfConcern` of another episteme;
- a system can publish or transform an episteme;
- a selected structure can be about a system, episteme, organization, document set, model, or research program when that object is treated as a holon.

Slot position does not create a new kind. A system filling a role-assignment holder slot remains a system. An episteme filling an EntityOfConcern slot remains an episteme. A holon whose structure is described does not become the description of that structure.

### A.1:5 - Archetypal Grounding

#### A.1:5.1 - Water Pump as U.System

Pump #37 is a `U.System` holon in a maintenance bounded context.

```text
HolonSlotRelation:
  holonIdentity: Pump #37
  boundedContextRef: plant maintenance context
  boundaryRef: casing plus inlet and outlet flanges
  partRelationSet: motor, impeller, seals, housing
  containingWholeRef: cooling-water subsystem
  interactionSet: water flow, electrical energy, control signal
  subtypeKind: U.System
```

The pump can bear a maintenance role, enact a repair method, perform work through technicians and tools, and have selected structures such as transformation-flow, control, or module-interface structure.

#### A.1:5.2 - Scientific Theory as U.Episteme

Newtonian gravitation as taught in one edition is a `U.Episteme` holon in a physics-education bounded context.

```text
HolonSlotRelation:
  holonIdentity: Newtonian gravitation in the selected edition
  boundedContextRef: physics education context
  boundaryRef: selected axioms, vocabulary, reference scheme, and admissible claim set
  partRelationSet: definitions, laws, derivations, examples, evidence relations
  containingWholeRef: mechanics curriculum episteme
  interactionSet: citation, teaching, model-use, revision, publication
  subtypeKind: U.Episteme
```

The theory does not teach itself or revise itself. A teacher, author, student, reviewer, or software system in role may publish, explain, compare, or modify an episteme. The episteme carries claims and relations; the acting system performs the work.

#### A.1:5.3 - Team as Collection or Collective System

A list of named engineers is a collection. It becomes a `U.System` only when the project claims an acting whole: boundary, membership rule, coordination structure, role assignments, decision method, and work occurrences are current.

If the project says "the team approved the architecture", A.1 asks whether there is a collective system and whether a decision pattern or governance pattern makes that claim admissible. If not, name the specific system-in-role or decision relation that actually carries the claim.

### A.1:6 - Bias-Annotation

Lenses tested: **Onto**, **Arch**, **Epist**, **Prag**, **Gov**, **Did**.

This pattern intentionally resists:

- **system-bias:** treating all objects as acting physical systems;
- **episteme-agent bias:** assigning work, authority, or decision to claim-bearing epistemes;
- **collection-bias:** treating any set as an acting collective;
- **boundary-bias:** choosing boundaries for convenience or politics without a membership test;
- **publication-form bias:** treating a document, diagram, or model publication as the holon it describes.

### A.1:7 - Conformance Checklist

| Check | Requirement |
| --- | --- |
| `CC-A1-1` | A modeled object is first typed as `U.Entity`, `U.Holon`, `U.System`, `U.Episteme`, or another accepted subtype before part-whole, role, work, or architecture claims rely on it. |
| `CC-A1-2` | Part-whole and aggregation claims apply only to holons or accepted holon subtypes. |
| `CC-A1-3` | A current holon use names the bounded context and governing boundary for the claim. |
| `CC-A1-4` | Contested holon membership uses dependency, internal interaction, and emergence tests. |
| `CC-A1-5` | Acting roles, method enactment, and work occurrence claims attach to `U.System` or an accepted acting-system subtype, not to `U.Episteme`. |
| `CC-A1-6` | A set or collection is not treated as an acting collective unless modeled as a `U.System` with boundary and role assignments. |
| `CC-A1-7` | `U.Episteme` is non-agentive; systems may transform, publish, or use epistemes, but the episteme does not act by itself. |
| `CC-A1-8` | Slot positions such as EntityOfConcern, grounding holon, role holder, transformed entity, or described holon do not create new kinds for their fillers. |
| `CC-A1-9` | Publication forms and descriptions of holons are kept distinct from the holons they describe. |

### A.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Symptom | Repair |
| --- | --- | --- |
| System as universal root | A theory, document, or model receives physical system properties. | Re-type as `U.Episteme` or another holon subtype, then use the governing pattern for the claim. |
| Document edited itself | A model, theory, or document is said to perform a revision. | Name the `U.System` in role that performed the work and the `U.Episteme` that was changed. |
| Collection as actor | A list or set is said to decide or perform work. | Model a collective `U.System` or name the actual acting system-in-role. |
| Boundary by section heading | A document section, org chart box, or folder is treated as a holon boundary by appearance. | Name the bounded context and boundary relation; apply membership tests. |
| Architecture without holon | A selected structure is discussed without the holon whose structure is selected. | Use A.1 to name the holon, then `A.22` and `C.30` for selected structure and architecture. |

### A.1:9 - Consequences

Positive consequences:

- FPF can talk about physical systems, organizations, documents, theories, models, and research programs under one composition root without making them all systems.
- Acting work stays attached to systems in roles.
- Epistemes can be described, compared, published, and transformed without becoming agents.
- Architecture and selected-structure claims gain a grounding holon.

Costs:

- Authors must stop using "system" for every object under concern.
- A holon boundary must be named when part-whole or architecture claims rely on it.
- Some familiar sentences need repair: "the document decided" becomes a claim about a system in role, a decision relation, and an episteme or publication.

### A.1:10 - Rationale

The A.1 stack prevents category errors by separating individuation, composition, acting eligibility, and claim-bearing. `U.Entity` gives the minimal "something under concern" without part assumptions. `U.Holon` adds composition and boundary. `U.System` adds acting eligibility. `U.Episteme` adds claim-bearing structure without agentivity.

This also prevents ontology duplication. A theory under concern, a theory description, a publication of that description, and the system that edits the publication can all be named without turning each slot position into a new kind. The same discipline is needed by architecture: architecture is selected structure of a holon in context, not a diagram and not a floating root kind.

The older phrase "entity to holon to system or episteme" remains useful only when read as this typed stack. It is not a process sequence and not a rule that every entity must become a holon.

### A.1:11 - SoTA-Echoing

| Source family | Current lesson for A.1 | FPF decision |
| --- | --- | --- |
| Compositional open systems and boundary-based modeling. | Composable objects need explicit boundaries and typed interaction with environments. | `U.Holon` requires a current boundary and part-whole relation before aggregation or architecture claims rely on it. |
| Domain-driven bounded-context practice. | Meaning and role assignments are local to a context; one word does not carry the same ontology everywhere. | A.1 pairs holon identity with `U.BoundedContext`; A.1.1 governs the semantic frame. |
| FAIR, provenance, and knowledge-representation practice. | Claim-bearing knowledge objects and their publications must be separated from physical systems and publication forms. | `U.Episteme` is a non-agentive holon governed by `C.2.1`; systems in role create, publish, or use epistemes. |
| Systems engineering and digital-twin practice. | Design and run descriptions need boundary-consistent grounding objects. | Architecture and structure patterns name the grounding holon before treating selected structure or description as current. |

Source role and currentness: the compositional open-systems and systems-engineering rows are current support for boundary-consistent grounding; bounded-context practice is carried through `A.1.1`; FAIR, provenance, and knowledge-representation practice support the separation among claim-bearing epistemes, publications, and acting systems. Older named traditions under these families are lineage or background unless a governing pattern cites them by value. Reopen A.1 when accepted FPF work or current systems, KR, provenance, or digital-twin practice changes the root split among `U.Entity`, `U.Holon`, `U.System`, `U.Episteme`, boundary, or publication-form separation; do not reopen it for a new tool, notation, or diagram style that does not change that root ontology.

### A.1:12 - Relations

- **Builds on:** `E.24` for ontic introduction discipline and `A.6.5` for slot relation discipline.
- **Coordinates with:** `A.1.1` for bounded context, `A.22` for selected structure, `C.30` for architecture, `C.2.1` for episteme slot relation, `A.15` for role-method-work alignment, `E.24.PUB` for holon-description publication boundary, and `E.10.ARCH` for wording-use restoration.
- **Used by:** patterns that need a grounding holon, acting system, non-agentive episteme, part-whole relation, or collection-versus-collective distinction.

### A.1:13 - Footer Marker

### A.1:End
