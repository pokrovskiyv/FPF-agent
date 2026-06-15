## E.10.D2 - EntityOfConcern, Description Episteme, and Specification-Use Discipline

*Definitional pattern - normative, notation-agnostic*

> **One-sentence summary.** For any `EntityOfConcern` in FPF, keep the entity under concern distinct from the `Description` episteme that describes it in a bounded context and viewpoint, and admit `...Spec` wording only for a Description episteme whose specification use is made checkable by explicit conditions. Specification is not a third peer ontology class beside the entity and its Description episteme.

**Status.** Definitional pattern.
**Builds on:** A.7 **Strict Distinction (Clarity Lattice)**; E.10.D1 **D.CTX (Context is U.BoundedContext)**; C.2.1 **U.EpistemeSlotRelation**; C.2.3 **Unified Formality Characteristic (F)**; F.15 **SCR/RSCR Harness**.
**Coordinates with.** F.4 **Role Description**; F.5 **Naming Discipline**; F.12 **Service Acceptance Binding**; F.9 **Alignment & Bridge across Contexts**; F.9.1 **Bridge Stance Overlay**; F.10 **Status Families Mapping**.
**Non-goals.** This pattern does not define editors, workflows, registries, storage formats, or publication carriers. It gives the boundary discipline that other FPF patterns use when they name an entity, its Description episteme, and any specification-use admission.

### E.10.D2:1 - Problem frame

Use this pattern when FPF-governed wording names something under concern and also names a description, view, specification, publication, file, card, diagram, dashboard, work record, evidence item, assurance result, gate result, or decision around it.

The first useful move is to ask five questions:

1. What is the `EntityOfConcern`?
2. Which Description episteme describes it, if describing is live?
3. Which `DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>` bounds that description?
4. Is specification use admitted by explicit checkability, acceptance, validation, formality, or harness conditions, or is this only a Description episteme?
5. Which neighboring FPF pattern carries any publication, carrier, evidence, assurance, gate, decision, commitment, promise, work, view, bridge, retargeting, or state-family claim?

Not this pattern when the question under repair is already an evidence path named by value, assurance claim, gate decision, commitment, work occurrence, bridge, representation transition, source relation, or state-family field. Use the neighboring pattern governing that claim for that claim and use E.10.D2 only to keep the EntityOfConcern, Description episteme, and specification-use boundary readable.

FPF frequently has to say that some item is being described: a role, method, system, work occurrence, promise content, characteristic, architecture, episteme, view, or another FPF entity. The old short memory of "thing / words / rules" remains useful, but it becomes harmful when it is taught as three peer kinds.

The working distinction is sharper:

* the **EntityOfConcern** is the item under concern;
* the **Description episteme** is the claim-bearing episteme that describes that item under one bounded context and viewpoint;
* **specification use** is an admitted use or refinement of a Description episteme, not a separate peer class;
* publication faces, publication forms, carriers, renderings, work occurrences, gate decisions, evidence relations, and assurance claims remain outside this boundary unless a neighboring pattern makes one of them the EntityOfConcern.

This matters whenever wording such as `RoleDescription`, `ArchitectureDescription`, `MethodSpec`, `ServiceSpec`, "the diagram is the architecture", "the card authorizes work", or "the file is the method" could make readers confuse the item under concern with a description, a publication, a carrier, a work occurrence, or a granted use.

What goes wrong if E.10.D2 is missed: specification-looking words become authority, a publication becomes the thing described, a file becomes the method, an approval state over an episteme becomes a runtime state, or two descriptions with the same label are treated as the same EntityOfConcern across contexts.

What E.10.D2 buys in practice: the practitioner can name the item under concern, keep the Description episteme inspectable, admit specification use only when checkability exists, and send every other claim being made to the governing FPF pattern that carries it.
### E.10.D2:2 - Problem

1. **Entity-description collapse.** A text treats the `EntityOfConcern` as if it were identical to the Description episteme, the diagram, the card, the file, or the work record.
2. **Specification inflation.** A text calls any detailed write-up a `...Spec` although no checkability, acceptance condition, or harness relation is present.
3. **Publication or carrier substitution.** A publication face, document, dashboard, schema file, or generated view is treated as the described entity or as the authority for work.
4. **Context and viewpoint loss.** A Description episteme is read as global even though FPF descriptions are bounded by `DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>`.
5. **Status and state leakage.** Epistemic or deontic statuses over epistemes are used as if they were role states, system states, or runtime facts about the EntityOfConcern.

### E.10.D2:3 - Solution

For any sentence that names an entity and also names description, specification, view, publication, carrier, evidence, evaluation, or work:

1. **Name the EntityOfConcern.** State what item is under concern: for example `U.Role`, `U.Method`, `U.System`, `U.Work`, `U.PromiseContent`, `U.Characteristic`, `U.ArchitectureOf@Context`, or `U.Episteme`.
2. **Name the Description episteme when describing is live.** A `...Description` is a `U.Episteme` that describes the EntityOfConcern under `DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>`.
3. **Admit specification use only by conditions.** A `...Spec` is a Description episteme admitted for specification use when checkability conditions are present. The conditions must name formal checkability or declared formality, checkable invariants or acceptance criteria, a validation or acceptance harness, and the same DescriptionContext.
4. **Keep publication and carrier relations separate.** A card, document, dashboard, diagram, file, rendering, or API surface may publish, encode, render, or expose a Description episteme; it is not thereby the EntityOfConcern and it does not by itself create permission, evidence, gate, assurance, decision, commitment, or work.
5. **Exit to the neighboring pattern when another claim becomes live.** Evidence goes to evidence patterns; assurance to assurance patterns; gate decisions to gate patterns; commitments and promises to F.18 and related patterns; work to work and P2W patterns; publication and view mechanics to E.17/A.6.3/C.2.P; retargeting to A.6.4.

Ordinary minimum: write one line that names the EntityOfConcern, the Description episteme or `not live`, the DescriptionContext or missing-context blocker, the specification-use admission value, and the neighboring FPF pattern governing that claim for any live non-description claim.

```text
E10D2BoundaryLine:
  entityOfConcernRef:
  descriptionEpistemeRef or notLive:
  descriptionContext or missingContextBlocker:
  specificationUseAdmission: admitted | notAdmitted | candidateOnly
  neighboringPatternApplicationRefs for non-description claims:
  admissibleUse:
  nonAdmissibleUse:
```

Stop at the boundary line when it makes the next admissible move clear. Open heavier episteme, publication, source, bridge, evidence, assurance, gate, decision, work, or state-family records only when those claims are being made.
### E.10.D2:4 - Core field discipline

#### E.10.D2:4.1 - EntityOfConcern

`EntityOfConcern` means the item under concern in the current claim. It is not a universal "object" bucket and not an authoring target. It may be a system-side entity, an episteme, a relation, a characteristic, a work occurrence, a pattern, or another FPF kind named by value.

When the EntityOfConcern is itself an episteme, the same distinction still holds. The episteme under concern is not automatically identical to a Description episteme about that episteme, and a publication of that episteme is still a publication relation.

#### E.10.D2:4.2 - Description episteme

A Description episteme is a `U.Episteme` whose `subjectRef` is interpreted through:

```
DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>
```

It may carry labels, glosses, characterizations, state graphs, structural views, criteria, diagrams, examples, or other claim-bearing content about the EntityOfConcern. Those parts remain episteme content. They do not become parts of the EntityOfConcern unless a separate FPF pattern establishes that relation.

#### E.10.D2:4.3 - Specification-use admission

Use a `...Spec` name only when the Description episteme is admitted for specification use under all applicable conditions:

1. **Checkability.** The claimed invariants or acceptance conditions are checkable.
2. **Declared formality or equivalent discipline.** The text states the formal mode, notation discipline, measurement criterion, comparator, or other exact basis that makes checking possible.
3. **Harness or validation relation.** The text names the acceptance harness, SCR/RSCR check, validation method, measurement procedure, or neighboring FPF relation that will check the specification use.
4. **Same DescriptionContext.** The specification-use episteme preserves or explicitly updates `EntityOfConcernRef`, `BoundedContextRef`, and `ViewpointRef`.

If any condition is absent, use `...Description` and state the live criteria informatively or as candidates without claiming specification use.

#### E.10.D2:4.4 - Publication, carrier, and work boundary

`U.Carrier` encodes an episteme. A publication face/form/unit makes an episteme available. A rendering or UI surface displays it. A work occurrence uses it or acts under it. None of those relations changes the EntityOfConcern or upgrades a Description episteme to specification use by itself.

### E.10.D2:5 - Naming discipline

**Default suffix.** Use `...Description` for a Description episteme unless specification-use admission is explicit.

**Reserved suffix.** Use `...Spec` only for a Description episteme admitted for specification use. Do not use `Spec` as a synonym for "detailed", "important", "official-looking", "formal-looking", or "stored in a schema".

**Entity names.** Use the bare FPF kind named by value for the EntityOfConcern: `Role`, `Method`, `System`, `Architecture`, `Characteristic`, `PromiseContent`, `Work`, `Episteme`, or another kind named by value. Do not append `Description`, `Spec`, `Card`, `View`, or `Carrier` unless the episteme, view, publication, or carrier is the actual EntityOfConcern.

**DescriptionContext names.** Use `EntityOfConcernRef`, `BoundedContextRef`, and `ViewpointRef` for Description episteme addressing. Do not revive `DescribedEntityRef`, `EntityOfInterest`, or peer-layer I-D-S wording.

### E.10.D2:6 - Invariants

**D2-1 (Entity-description distinction).** The EntityOfConcern and the Description episteme about it are distinct even when the EntityOfConcern is itself an episteme.

**D2-2 (Specification is admitted use).** Specification is not a peer class beside EntityOfConcern and Description episteme. A `...Spec` is a Description episteme admitted for specification use.

**D2-3 (DescriptionContext).** A Description episteme names or recovers `DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>`.

**D2-4 (Publication and carrier separation).** Publication faces, publication forms, publication units, carriers, renderings, files, dashboards, and UI surfaces do not become the EntityOfConcern and do not grant specification use by appearance.

**D2-5 (Work separation).** A plan, checklist, or specification-use Description episteme does not execute work. Work occurrences and work results remain under work and P2W patterns.

**D2-6 (Status-state separation).** Epistemic and deontic statuses over epistemes are not role states, system states, or runtime facts unless the exact state pattern grants that interpretation.

**D2-7 (No label-only cross-context sameness).** Identical labels in two bounded contexts or viewpoints do not establish sameness. Use F.9 bridges, A.6.3 views, or A.6.4 retargeting as appropriate.

**D2-8 (ReferencePlane reservation).** Do not call this distinction a plane. Use `ReferencePlane` only where CHR or another governing pattern defines that field.

### E.10.D2:7 - Reasoning primitives

**Description link.**

```
EntityOfConcernRef(T), BoundedContextRef(C), ViewpointRef(Vp)
  |- isDescriptionOf(TDesc, T, C, Vp)
```

`TDesc` is the Description episteme about EntityOfConcern `T` in bounded context `C` under viewpoint `Vp`.

**Specification-use admission.**

```
isDescriptionOf(TDesc, T, C, Vp)
  and checkableInvariants(TSpec)
  and validationOrAcceptanceHarness(TSpec)
  and sameDescriptionContext(TSpec, TDesc)
  |- admittedForSpecificationUse(TSpec, T, C, Vp)
```

Only under those conditions may the episteme be named `TSpec`.

**Characterization relation.**

```
isDescriptionOf(RoleDesc, U.Role, C, Vp)
  and characterizes(RoleDesc, U.RCS)
  and characterizes(RoleDesc, U.RSG)
  |- RoleDesc characterizes U.Role by those structures @C,Vp
```

The role is characterized through the Description episteme. The structures are not silently parts of the role.

**Evaluation relation.**

```
evidence E satisfies criteria K within window W
  |- attestation(subject has state/status/result S @C within W)
```

Evaluation produces an attestation in a window. It does not mutate the EntityOfConcern.

### E.10.D2:8 - Anti-patterns and repairs

| Anti-pattern | Symptom | Repair |
|---|---|---|
| **Entity-description collapse** | "The method is the document"; "the architecture is the diagram"; "the role contains the checklist". | Name the EntityOfConcern, then name the Description episteme or publication relation separately. |
| **Spec by name** | Any detailed write-up is called `...Spec`. | Use `...Description` unless specification-use admission conditions are present. |
| **Publication as authority** | A card, dashboard, schema, generated view, or file is treated as permission, evidence, gate, assurance, decision, or work. | Send that claim being made to the neighboring pattern governing that claim; keep the publication relation separate. |
| **Carrier identity** | The file path or repository entry is treated as the episteme or EntityOfConcern. | Say the carrier encodes or renders the episteme. |
| **Context erasure** | A context-local Description episteme is read as a global definition. | Restore `BoundedContextRef` and `ViewpointRef`, or use F.9/A.6.3/A.6.4 for cross-context relations. |
| **Status-state leakage** | Evidence, requirement, approval, or standard status becomes a role-state node. | Keep statuses over epistemes distinct from state graphs and runtime state attestations. |

### E.10.D2:9 - Worked examples

#### E.10.D2:9.1 - Role

`U.Role :: ChangeAuthority` is the EntityOfConcern. `ChangeAuthorityRoleDescription@ITIL4` is a Description episteme with `DescriptionContext = <EntityOfConcernRef(ChangeAuthority), BoundedContextRef(ITIL4), ViewpointRef(RoleViewpoint)>`.

The Description episteme may characterize the role by credential level, mandate window, separation-of-duty criteria, and a role-state graph. The role does not contain the graph or the checklist. If testable invariants and an acceptance harness are declared, a `ChangeAuthorityRoleSpec@ITIL4` may be admitted for specification use.

#### E.10.D2:9.2 - Method

`U.Method :: BacklogRefinement` is the EntityOfConcern. A team note, practice card, or pseudo-code sketch is a `BacklogRefinementMethodDescription@EssenceContext` when it describes the method. It becomes `BacklogRefinementMethodSpec@EssenceContext` only when checkable method constraints and an acceptance or validation harness are present.

Calendar sessions, chat threads, and tickets are work occurrences or work records. They may use the method description, but they are not the method and not the Description episteme.

#### E.10.D2:9.3 - Architecture

`ArchitectureOf@Context(Holon)` is the EntityOfConcern. An architecture description, structural view, graph, ADR, or dashboard is a Description episteme, view, publication, or carrier about that architecture. The diagram does not become the architecture, and an ADR does not by itself create permission or assurance.

If a structural view uses a mathematical lens, C.29 carries the declared mathematical-lens use question. If an architecture description is used to guide work, A.15.4 and P2W-related patterns carry the work-relevance relation.

#### E.10.D2:9.4 - Episteme as EntityOfConcern

A safety case, DRR, pattern, or source bundle can itself be the EntityOfConcern. A review note describing that DRR is then a Description episteme about an episteme. A published PDF of the DRR is a carrier or publication relation. This prevents the common slide from "talking about a description" into "talking only about descriptions of descriptions".

### E.10.D2:9.5 - Source-use and SoTA-echoing

| Source or practice line | FPF use | Boundary |
| --- | --- | --- |
| ISO/IEC/IEEE 42010-style architecture-description practice separates described architecture, stakeholder concern, viewpoint, view, model kind, correspondence, and architecture-description publication. | Adapt the separation as pressure for `DescriptionContext`, viewpoint, view, and correspondence discipline beyond architecture-only cases. | Does not make every Description episteme an architecture description and does not grant evidence, assurance, gate, decision, or work authority. |
| Requirements and specification practice treats specifications as checkable descriptions used for acceptance, verification, validation, or conformance. | Use `...Spec` only when the Description episteme has explicit checkability, formality, criteria, comparator, harness, or neighboring-pattern gate. | A detailed or official-looking document is not specification use by name alone. |
| FPF episteme, publication, view, carrier, and source-use machinery (`C.2.1`, `E.17`, `E.17.0`, `A.6.3`, `C.2.P`) supplies the ontology named by value. | Reuse existing episteme slots, DescriptionContext, views, publication faces/forms/units, carrier separation, source relation, bridge, and retargeting exits. | E.10.D2 does not mint a rival description ontology and does not replace source, evidence, bridge, work, or state-family patterns. |
| Andrey Rodin-style near-sameness and postulate-theory concerns motivate explicit same-EntityOfConcern and bridge checks across descriptions. | Same label, similar description, or shared formal substrate is not enough; use F.9, A.6.3, A.6.4, or same-EntityOfConcern recovery by value. | E.10.D2 names the boundary; it does not decide all cross-context sameness or mathematical-substrate adequacy. |
### E.10.D2:10 - Relations

**Builds on:**

* **A.7 - Strict Distinction (Clarity Lattice).** Supplies the general distinction between an EntityOfConcern and the epistemes, publications, carriers, work, decisions, evidence, and assurance claims around it.
* **C.2.1 - U.EpistemeSlotRelation.** Supplies `DescriptionContext`, `subjectRef`, and episteme slot discipline.
* **C.2.3 - Unified Formality Characteristic.** Supplies formality levels used by specification-use admission.
* **F.15 - SCR/RSCR Harness.** Supplies check and regression-check harness discipline.

**Coordinates with:**

* **A.6.2/A.6.3/A.6.4.** Description epistemes can be transformed, viewed, or retargeted only under their episteme-morphism laws.
* **E.17 and E.17.0.** Publication, view, face, form, unit, and carrier relations remain separate from the EntityOfConcern and Description episteme.
* **F.9.** Cross-context relation or near-sameness requires a bridge, not label reuse.
* **F.4/F.5/F.8/F.10.** Role, service, naming, acceptance, and evaluation patterns consume this boundary when they name descriptions and specifications.

### E.10.D2:11 - Current repair moves

Use these repairs when live FPF prose violates this pattern:

1. Replace old `DescribedEntity*`, `EntityOfInterest`, `EoI`, and `EoIClass` wording with `EntityOfConcern`, `EntityOfConcernRef`, `EntityOfConcernClass`, or the local FPF kind named by value. Retain old spellings only as source-side trigger wording.
2. Replace peer-layer I-D-S wording with EntityOfConcern / Description episteme / specification-use admission wording.
3. Replace "contains RCS/RSG/checklist" with "is characterized through the Description episteme by RCS/RSG/checklist".
4. Replace carrier identity with "carrier encodes" or "publication exposes" wording.
5. Replace generic "object under description" talk with the EntityOfConcern named by value and its `DescriptionContext`.

6. Replace `...Spec` names that lack specification-use admission with `...Description`.
7. Send permission, evidence, assurance, gate, decision, promise, commitment, work, publication, view, bridge, or retargeting claims to the neighboring pattern governing that claim instead of keeping them as local semio guard prose.

### E.10.D2:12 - Conformance checklist

| ID | Check |
|---|---|
| **CC-D2-1** | The text names or recovers the EntityOfConcern and does not hide it behind generic `object`, `target`, `subject`, source-side wording, or carrier wording. |
| **CC-D2-2** | Every Description episteme recovers `DescriptionContext = <EntityOfConcernRef, BoundedContextRef, ViewpointRef>` when the description relation is live. |
| **CC-D2-3** | Every `...Spec` wording has explicit specification-use admission: checkable invariants or criteria, check method or harness, and preserved or declared DescriptionContext. |
| **CC-D2-4** | Publication faces/forms/units, carriers, renderings, views, and work records are not treated as the EntityOfConcern. |
| **CC-D2-5** | Evidence, assurance, gate, decision, promise, commitment, and work claims exit to the neighboring pattern governing that claim when they are being made. |
| **CC-D2-6** | The text does not use old I-D-S peer-class wording, `intensional object`, `DescribedEntity*`, `EntityOfInterest`, `EoI`, or `EoIClass` as accepted vocabulary for current FPF prose. |
| **CC-D2-7** | The word `plane` is not used for this distinction; only governing patterns such as CHR may define `ReferencePlane`. |

### E.10.D2:13 - Phrasebook

| Avoid | Use |
|---|---|
| "The role contains the state graph." | "The RoleDescription characterizes the role by a state graph." |
| "The diagram is the architecture." | "The diagram publishes or renders an architecture Description episteme or structural view." |
| "MethodSpec draft." | "MethodDescription draft; specification use not admitted until checkability and harness conditions are present." |
| "The PDF is the method." | "The PDF is a carrier that encodes the MethodDescription." |
| "Same label, same thing." | "Same label requires a bridge, view, retargeting relation, or explicit same-EntityOfConcern claim." |
| "Evidence status is a role state." | "Evidence status classifies an episteme; role states belong to the relevant role-state graph." |

### E.10.D2:14 - Didactic memory

Use the short memory **entity / description / admitted specification use**:

1. **Entity.** What item is under concern?
2. **Description.** Which episteme describes it, in which bounded context and viewpoint?
3. **Admitted specification use.** What makes a `...Spec` checkable here?
4. **Publication and carrier.** What only exposes, renders, stores, or transports the episteme?
5. **Neighboring claims.** Which evidence, assurance, gate, decision, commitment, work, bridge, view, or retargeting pattern carries any additional claim being made?

### E.10.D2:End
