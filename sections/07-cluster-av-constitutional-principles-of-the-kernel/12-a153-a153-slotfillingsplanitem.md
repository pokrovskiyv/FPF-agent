## A.15.3 - SlotFillingsPlanItem

> **Tech-name:** `SlotFillingsPlanItem`
> **Plain-name:** planned slot-fillings baseline item (planned baseline)
> **Type:** Architectural (A)
> **Status:** Stable
> **Normativity:** Normative (unless explicitly marked informative)
> **Placement:** Part A → A.15 (Work & WorkPlanning)
> **Builds on:** `U.WorkPlan` (A.15.2), performed-work occurrence discipline (A.15.1 and E.18), Context discipline (E.10.D1), `MechSuiteDescription` (A.6.7), and publication/view discipline (E.17; views are projections, not places of meaning)
> **Used by:** planned-baseline requirements from suites or kits; P2W (selection -> WorkPlanning -> WorkEnactment); Part G universalization
> **Purpose (one line):** provide a universal, context-explicit **planned baseline** that maps a slot-bearing description's `SlotKind`s to **planned fillers**, to be consumed by Work enactment where launch values are finalized.

**At a glance.** Use `SlotFillingsPlanItem` when a `U.WorkPlan` needs a planned baseline saying which planned fillers will occupy which `SlotKind`s of one slot-bearing description before work is enacted.

**Use this when.** Use this pattern when planned references, policies, spec pins, method-description references, evidence pin refs, or crossing-policy pins must be fixed for a P2W work-planning slice, and the plan must stay distinct from launch values, gate decisions, evidence, and performed work.

**First output.** One `SlotFillingsPlanItem` with exactly one `target_slot_bearing_description_ref`, explicit `bounded_context_ref`, EntityOfConcern ref, time selector or time rule, authoritative planned-filling rows, and any expected guard, evidence, edition, or crossing pins needed before work enactment.

**Working action path.**
1. Name the slot-bearing description whose `SlotKind` set is being filled.
2. Name the EntityOfConcern and grounding holon or reference plane when needed.
3. Name context, time selector or time rule, and any P2W slice or publication scope needed for reproducibility.
4. Fill the authoritative rows by `SlotKind`, using ByValue or ByRef with concrete RefKinds and edition pins when needed.
5. Keep derived indices, views, guard pins, evidence pins, and crossing pins as projections or expectations; do not turn them into execution, gate, evidence, or launch-value claims.

**Ordinary use.** For a minimal baseline, context, time selector, target slot-bearing description, EntityOfConcern ref, and planned-filling rows are enough.

**Reliance-bearing use.** Use the fuller record when reproducibility, launch guard preparation, crossing expectations, suite or kit reuse, Part G universalization, or P2W carry-through depends on the baseline.

**Stop condition.** Stop once planned fillers are explicit enough for the intended WorkPlanning move, or lower the claim to a plan cue, source-gap note, relation governed by another FPF pattern, or blocked kind-definition gap without claiming a conforming planned baseline.

**Not this pattern when.** Not this pattern when the live object is the slot-bearing description itself, a mechanism definition, a performed-work occurrence, a gate decision, a launch-value witness, evidence, assurance, or a publication view. Use the corresponding governing pattern and return here only for the planned slot-filling baseline.

**Name and reference discipline (informative)**
* **Kind reuse:** This pattern uses the kind name `SlotFillingsPlanItem`. It reuses existing Core terms and disciplines (e.g., `U.WorkPlan.PlanItem`, SlotKind, ValueKind, RefKind, and refMode discipline, edition pinning, `U.BoundedContext`, and the P2W split between WorkPlanning and WorkEnactment).
* **`SlotFillingsPlanItem` (kind name):** keep the suffix `PlanItem` to preserve the WorkPlanning placement. Do not mint aliases like *SlotBinding…* (conflicts with the A.6.5 binding discipline) or *SlotValue…* (ambiguous slot-bearing description or context).
* **Anchor names:** if a §4.2 anchor is materialized as a formal field name, keep `…_ref` only for fields whose values are concrete RefKind handles, and keep `…_id` only for identifiers. Avoid introducing generic placeholders such as `SpecRef`, `PolicyRef`, or `GateRef` inside this pattern; use existing concrete ref kinds. When no concrete ref kind exists, the planned-baseline claim is blocked until a governing FPF pattern defines the kind.
* **Row vocabulary:** treat `SlotFillingRow` and `PlannedFiller` as internal names of this pattern. Do not treat them as shared tokens outside this pattern unless a governing FPF pattern defines them.

### A.15.3:1 - Problem frame

FPF frequently needs to make **reproducible, reviewable choices** about *what fills which conceptual slot* (specification references, policy references, mechanism-instance references, time selectors, evidence hooks, etc.) **before** any Work is enacted. These choices must be visible as a planned baseline for a concrete P2W slice (CG-frame, path slice, or publication scope), and must remain distinct from run-time “actuals” and gate decisions.

However, absent a universal WorkPlanning plan item for architecture-by-planned-slot-filling, practitioners tend to hide these choices inside mechanism prose, CG-Spec and CN-Spec descriptions, local cards, or informal checklists—making Part G patterns difficult to universalize and making Work audit trails ambiguous.

`SlotFillingsPlanItem` addresses this by defining a **WorkPlan PlanItem kind** whose job is to state, in one place and with explicit context, a mapping:

> *(Target slot-bearing description, slot kind) → planned filler (ByValue | ByRef(<concrete RefKind>), with edition pins when needed)*

and to do so in a form that can be cited by Work enactment and by suite or kit spec pins, without collapsing into “execution” or “decision logging”.

### A.15.3:2 - Problem (what breaks without it)

Without an explicit `SlotFillingsPlanItem` baseline, at least six failure modes recur:

1. **Hidden slot-bearing-description reference and meaning drift:** a planned filler is stated without making explicit *whose* slot set is being filled, allowing silent reinterpretation of `SlotKind`s across kits or suites.

2. **Planning and enactment collapse:** plan documents get “backfilled” with run-time values, so there is no stable planned baseline and no clean variance trail. WorkPlan explicitly warns against this.

3. **Implicit time (“latest”) and implicit recency:** planned claims about comparability or launch readiness omit an explicit `Γ_time`, which violates the time discipline (“no implicit recency”).

4. **Edition ambiguity:** references to method, policy, and specification references are not edition-pinned where reproducibility requires it, or the plan mutates the edition vector instead of citing pinned editions (edition changes are crossings, not “plan edits”).
   A particularly harmful subtype is **edition-key backfill**: retroactively editing a previously used baseline so that an edition-key change looks like an innocent PlanItem edit (hiding the required GateCrossing witness and breaking audit traceability).

5. **Crossing invisibility:** cross-context or cross-plane expectations (Bridge + policy ids) are not stated at plan time, so downstream gate crossings appear as “magic” rather than traceable expected constraints.

6. **G-pattern fragmentation:** each Part G pattern invents its own place to stash planned refs (method pick, comparator pick, QD archive config, etc.), blocking a clean “G.Core” universal layer and making modular reuse brittle.

### A.15.3:3 - Forces (what we must balance)

* **Strict distinction:** planned baseline is not a run-time witness; launch values are finalized only in Work enactment.
* **Context must be explicit:** every normative claim or rule is context-bound; the PlanItem must carry its context rather than relying on file location or prose.
* **Time must be explicit:** no implicit “latest”; any plan that will be cited by comparability or launch-readiness checks needs an explicit `Γ_time` selector or rule.
* **SlotKind meaning is stable:** the plan may choose fillers, but must not reinterpret SlotKinds or smuggle new semantics into indices.
* **Derived indices must not become “places of meaning”:** projections like “planned spec refs” are useful, but must remain derivable from the authoritative rows.
* **Conceptual, not procedural:** no solver steps, no lints, no “data governance”; this is an epistemic object used by humans in review.
* **Supports universalization:** one PlanItem pattern must be usable across the whole of Part G, not just G.5.
* **Integrates with suites or kits:** suites may require a planned-baseline ref and may act as slot-bearing descriptions.

| Force | Tension |
| --- | --- |
| Planning and enactment split | Plan must be citeable without containing run-time values. |
| Slot meaning stability | SlotKinds must not drift by implicit slot-bearing-description changes. |
| Edition honesty | Baselines must pin editions where meaning changes; avoid “latest”. |
| Suite and kit modularity | Suite descriptions define slot interfaces and obligations; baselines choose fillers for a plan instance. |
| Auditability | A practitioner or auditor must reconstruct “what was planned” without chasing hidden defaults. |
| Extensibility | Allow suite-specialized variants without breaking universal core. |

### A.15.3:4 - Solution

#### A.15.3:4.1 Definition

A `SlotFillingsPlanItem` is a **kind of `U.WorkPlan.PlanItem`** whose content is a **planned slot-fillings ledger** for a *single* slot-bearing description, within an explicit P2W context.

It is a **WorkPlanning baseline**, intended to be:

* produced and accepted in WorkPlanning,
* **cited** by downstream Work enactment (as planned baseline),
* compared against actual fillings (variance recorded in Work, not by rewriting the plan).

**Normative note (EntityOfConcern, Description episteme, specification use, and views):** A `SlotFillingsPlanItem` is a Description episteme for planning (a PlanItem). It MAY be projected into `U.View` (e.g., `TechCard(SlotFillingsPlanItemRef)`), but any view is strictly a projection and MUST NOT introduce additional claims or “shadow defaults”.

#### A.15.3:4.2 Core conceptual descriptors (not a data schema)

A conformant `SlotFillingsPlanItem` SHALL provide the following description (names are indicative; the semantics are normative):

1. **PlanItem core (from A.15.2)**
   The PlanItem MUST remain a WorkPlanning plan item: it may include assumptions, dependencies, constraints, expected publications or records, and notes; it MUST NOT contain run-time logs or actual fillings.

2. **Target slot-bearing description**

   * `target_slot_bearing_description_ref : <concrete …DescriptionRef>` (required)
     Identifies the **Description episteme whose SlotKind set is being filled** (e.g., a kit description or a suite description).
     The slot-bearing description MUST be referenced as an **edition-addressable Description episteme** (a concrete `…DescriptionRef` such as `MechSuiteDescriptionRef`, `…KitDescriptionRef`, etc.),
     and MUST NOT target a `MechanismDefinitionRef`. If a standalone mechanism baseline is needed, introduce an explicit Description-scoped slot-bearing description wrapper, such as a mech kit or suite-of-one, and target that.
     A `MechSuiteDescription` MAY serve as a slot-bearing description for this purpose.
     If the slot-bearing description’s SlotKind interface is edition-sensitive (or expected to evolve), the reference MUST be edition-pinned (e.g., `target_slot_bearing_description_ref.edition`) whenever the PlanItem is used as a reproducibility baseline.

3. **EntityOfConcern and grounding (for the measurement or selected filler under planning)**

   * `described_entity_ref : <concrete RefKind>` (required)
     The referent is the *EntityOfConcern* (C.2.3 role): the thing the planned baseline is **about**.
     It MUST NOT be silently conflated with a holon. (Example: a baseline can be about a width measurement while the grounding holon is a stool with that width.)
     Use a concrete RefKind of the EntityOfConcern (e.g., `U.HolonRef`, `U.MeasureRef`, …). Do **not** mint a new generic `EntityRef` token inside this pattern.
   * `grounding_holon_ref? : U.HolonRef` (optional; required when the EntityOfConcern is not itself a holon and a grounding holon is needed for reference-plane anchoring)
   * `reference_plane? : ReferencePlane` (optional; required when not unambiguously derivable from cited context publications or records such as CG-frame and specification pins)

4. **Explicit planning context** (no hidden context)

   * `bounded_context_ref : U.BoundedContextRef` (required)
   * `cg_frame_ref? : CGFrameRef` (recommended when the fillings feed CG legality and selection)
   * `path_slice_id? : PathSliceId` (recommended for P2W reproducibility)
   * `publication_scope_id? : PublicationScopeId` (recommended if the plan will be surfaced in publication-facing views)
     These anchors exist because FPF claim discipline requires explicit context for claims or rules.

5. **Explicit time selector** (no implicit recency)

   * exactly one of:

     * `Γ_time_selector : Γ_timeSelector` (ByValue), or
     * `Γ_time_rule_ref : Γ_timeRuleRef` (RefKind)
       This MUST be present whenever the plan is intended to serve comparability or launch-readiness downstream checks.

6. **Expected guard pins** (references and expectations only; no gate decisions)

   * `expected_usm_guard_pins : [USM.CompareGuard | USM.LaunchGuard]` (ByValue; subset of `{USM.CompareGuard, USM.LaunchGuard}`)
     These lexemes are reserved for `USM.Guards` **pins** (gate-level surfaces), not for mechanism operator names.
     If `USM.LaunchGuard` is expected, the plan MUST include enough pins and references to make that guard executable downstream (explicit `Γ_time_selector` or `Γ_time_rule_ref`, pinned editions where needed, and evidence pin anchors).
     The PlanItem MUST NOT include outcomes for these guards and MUST NOT emulate gate decisions; it only records *expectations* and *required anchors*.

   * `guard_owner_gate_ref? : <concrete OperationalGateRefKind>` (refs only; required when `expected_usm_guard_pins` is non-empty unless unambiguously derivable)
     Identifies the gate that aggregates `GuardFail` outcomes (via the `GuardOwnerGateSlot` discipline). This remains an expectation pin, not a decision log.
     (Use the concrete RefKind that addresses `OperationalGate(profile)` in A.21. If such a RefKind does not exist, do not claim a conforming guard-owner gate reference.)

7. **Planned evidence anchors (pin refs only)**

   * `planned_evidence_pin_refs? : [<concrete …PinRef>…]`
     These are anchors to *where* evidence will be placed or cited (typically SCR pins or RSCR pins; optionally other pin kinds explicitly allowed by the downstream guard regime),
     not the evidence itself.

8. **The planned slot-fillings ledger (authoritative rows)**

   * `planned_fillings : [SlotFillingRow+]` where:

     `SlotFillingRow := ⟨ slot_kind, planned_filler, edition_pin? ⟩`

     * `slot_kind : SlotKind`
       A SlotKind provided by the `target_slot_bearing_description_ref` (the PlanItem MUST NOT reinterpret SlotKind meaning).
       Unless the slot-bearing description explicitly declares the slot as multi-valued, each `slot_kind` SHALL appear **at most once** in `planned_fillings`.
     * `planned_filler : PlannedFiller` where:
       `PlannedFiller := ByValue(value) | ByRef(ref : <concrete RefKind>)`
       In `ByRef(…)`, the `ref` MUST be of a **concrete RefKind** (e.g., `…SpecRef`, `…PolicyRef`, `…MethodDescriptionRef`);
       the PlanItem MUST NOT use an untyped generic `Ref` or `RefKind` placeholder.
       The chosen filler MUST conform to the SlotSpec discipline of the slot-bearing description (A.6.5-style: `refMode ∈ {ByValue | <concrete RefKind>}`).
       Changes to planned fillers are described using the A.6.5 verb discipline: ByValue content change uses `fill`, `assign`, or `update`; ref retargeting uses `retarget`; ref resolution uses `resolve`; never describe the change by “renaming the slot”.
     * `edition_pin? : EditionId`
       Required only when reproducibility depends on an edition **and** the planned filler cannot carry an edition pin directly (preferred: `…DescriptionRef.edition` on the ref itself).
       If both the planned filler ref and the row provide edition pinning, they MUST agree (mismatch ⇒ nonconformant).
       ByValue rows SHOULD NOT carry edition pins unless the pinned edition is explicitly tied to a cited external publication or record (e.g., a referenced rule, policy, or method description).

9. **Derived indices (optional; never a second canonical source)**

   * `planned_spec_ref_index? : [<concrete …SpecRef>…]`
   * `planned_policy_ref_index? : [<concrete …PolicyRef>…]`
   * `planned_mechanism_instance_ref_index? : [<concrete …MechanismInstanceRef>…]`
     If any of these are present, they MUST be **derivable projections** of `planned_fillings`; any mismatch is nonconformant.
     (These are *categories* of refs extracted from the authoritative rows, not an invitation to introduce new generic `SpecRef` or `PolicyRef` token-kinds.)

10. **Expected crossing policy pins (refs only; no crossing witnesses)**

   * `expected_crossing_policy_refs? : [⟨bridge_card_ref, phi_policy_id, psi_policy_id?, phi_plane_policy_id?, reference_plane(src,tgt)⟩ …]`
     These communicate what the plan expects will be needed for crossings, without claiming that a crossing has occurred.
     `bridge_card_ref` is expected to pin a Bridge identity and channel (BridgeId + channel) and to be auditable via downstream CrossingBundle and UTS rows.
     This section states **Bridge-only** expectations; it MUST NOT introduce non-Bridge crossing mechanisms, and it MUST NOT embed CL, Φ, Ψ, or Φ_plane tables (references, policy identifiers, and pins only).

   * `expected_crossing_bundle_refs? : [CrossingBundleRef…]` (optional)
     Permitted only when the plan is explicitly citing already-published CrossingBundle baselines (e.g., “fixed context constants”); otherwise, the PlanItem SHALL state only expected policy pins and allow the crossing witness to appear at the gate-level or work-level.

11. **Notes (didactic, non-normative)**

* `planned_filling_notes?`
  Helpful narrative for practitioners or auditors; must not embed new claims that contradict the rows.

#### A.15.3:4.2.1 Canonical skeleton (Show)

The following compact pseudo-record illustrates the intended *canonical minimum*: explicit context + explicit time + a few authoritative rows.

```
SlotFillingsPlanItem := ⟨
  kind = SlotFillingsPlanItem,
  target_slot_bearing_description_ref = CHRMechanismSuiteDescriptionRef@edition(E_suite),
  described_entity_ref = U.HolonRef(H:EntityOfConcern), // or another concrete RefKind per C.2.3
  grounding_holon_ref = U.HolonRef(H:grounding-holon)?,  // when the EntityOfConcern is not itself a holon
  bounded_context_ref = U.BoundedContextRef(BC:context),
  cg_frame_ref = CGFrameRef(CG:frame),              // optional but typical for G.* legality and selection
  path_slice_id = PathSliceId(P2W:slice),           // optional but typical for reproducibility
  Γ_time_selector = point(t0),                      // no implicit “latest”
  expected_usm_guard_pins = {USM.CompareGuard, USM.LaunchGuard},
  planned_evidence_pin_refs = [RSCR.PinRef(RSCR:evidence-anchor)],
  planned_fillings = [
    ⟨ slot_kind = CNSpecSlot, planned_filler = ByRef(CNSpecRef(CN:…@edition(E_cn))) ⟩,
    ⟨ slot_kind = CGSpecSlot, planned_filler = ByRef(CGSpecRef(CG:…@edition(E_cg))) ⟩,
    ⟨ slot_kind = ScoringMethodDescriptionSlot,
      planned_filler = ByRef(ScoringMethodDescriptionRef(M:…@edition(E_m))) ⟩
  ]
⟩
```

#### A.15.3:4.3 Relation to Work enactment (planned baseline vs actuals)

* A `SlotFillingsPlanItem` is **not** a witness of `FinalizeLaunchValues`.
  Launch values (actuals) occur only in Work enactment, and their witness belongs in Work and audit surfaces, not in this PlanItem.

* Deviation at execution time is allowed, but it must be recorded as **variance in Work**, and the plan must not be rewritten to match the execution.
  When a Work enactment claims to follow a planned baseline, the Work MUST cite the `SlotFillingsPlanItem` in its Audit as the planned baseline reference, and MUST record any variance against it (rather than “backfilling” the plan).
  The baseline citation SHOULD be edition-addressable (i.e., the Work cites a stable PlanItem edition), so that subsequent PlanItem revisions cannot erase what was actually planned.
  If the baseline needs to change (including any edition-pinned ref changes), create a **new PlanItem edition** (or a new PlanItem) and treat the difference as a planning change—not as a retroactive edit of the previously cited baseline.

#### A.15.3:4.4 Relation to suites or kits

* Any suite or kit that requires a “planned baseline” may require and cite a reference to a `SlotFillingsPlanItem` via its spec pins; `MechSuiteDescription` explicitly provides a place for such a requirement.

#### A.15.3:4.5 - Variants

1. **Suite-specialized PlanItem (Refinement)**
   A suite may define `XSuiteSlotFillingsPlanItem ⊑ SlotFillingsPlanItem` with:

   * fixed `target_slot_bearing_description_ref = XSuiteDescriptionRef`,
   * additional required rows (e.g., mandatory pinned `CGSpecRef`, `CNSpecRef`, suite-required mechanism instance refs),
   * additional required expected pins (guards, crossing policies).

2. **Minimal vs crossing-aware variants**

   * *Minimal:* includes only context + planned rows + time selector.
   * *Crossing-aware:* adds `expected_crossing_policy_ref[]` and explicit `reference_plane`.

3. **Evidence-gated variant**
   For workflows where `USM.LaunchGuard` is expected, require `planned_evidence_pin_refs[]` and explicitly pin the relevant edition set needed for the downstream guard.

#### A.15.3:4.6 - Local boundaries

`SlotFillingsPlanItem` is a planned-baseline item. It records planned fillers for one slot-bearing description before work enactment. Keep these nearby boundaries local:

| Source pressure | Local boundary |
|---|---|
| mechanism or operator wording | Do not use this item as a mechanism or operator signature; cite the mechanism or signature pattern when that relation is live. |
| spec, suite, kit, or acceptance-harness wording | The item may cite a slot-bearing description, but it does not replace CN-Spec, CG-Spec, suite description, kit description, policy, or acceptance record. |
| threshold-like or eligibility wording | Pin the acceptance, policy, comparator, or guard relation explicitly; do not hide it as an anonymous ByValue filler. |
| gate, decision, or crossing wording | The item may state expected policy refs; it does not contain `GateDecision`, `DecisionLog`, or a claim that a crossing occurred. |
| actuals or launch values | The item is not a run-time witness and does not contain `FinalizeLaunchValues` actuals. |
| publication view | A view may project the item, but the view introduces no new planned rows, defaults, or semantics beyond the item. |

#### A.15.3:4.7 - When to use

Use `SlotFillingsPlanItem` whenever:

* a P2W-selected work-planning slice needs a **planned baseline** for what fills a suite or kit slot set before work is enacted;
* you must pin edition and time policies explicitly (e.g., legality gates, comparator sets, transport registries);
* you are using or revising Part G patterns and want a uniform place to record selected references, policies, and mechanism instances;
* you expect a LaunchGate or any guard-based eligibility check to be meaningful and traceable.

#### A.15.3:4.8 - Implementation notes

**Informative use guidance (conceptual):**

1. Choose one `target_slot_bearing_description_ref` per PlanItem. If multiple slot-bearing descriptions are involved, create multiple `SlotFillingsPlanItem`s (one per slot-bearing description) to keep slot meaning unambiguous.
2. Fill rows by SlotKind, not by positional arguments or “index numbers”.
3. If any downstream reasoning may hinge on “now vs then”, supply `Γ_time_selector` or `Γ_time_rule_ref` explicitly.
4. Prefer edition-pinned references when the downstream step is intended to be reproducible across review cycles.
5. Use derived indices only as projections for practitioner navigation; never maintain them independently.
6. If a PlanItem has been cited as a baseline by a Work, do not “edit it in place” to match reality. Create a new PlanItem edition and let Work record variance and, when needed, the required crossing witnesses.

### A.15.3:5 - Archetypal Grounding (Tell–Show–Show; System / Episteme)

#### A.15.3:5.1 - Archetype 1: CHR suite planned baseline for lawful characterization

**Tell.** A team plans a characterization workflow over a CG-frame that uses a CHR mechanism suite. The suite requires an explicit planned baseline reference.

**Show (failure without `SlotFillingsPlanItem`).** The “plan” is implicit: it says “use the latest CG-Spec and the current best comparator; compute scores and launch” without an explicit `Γ_time`, without edition pins, and without a stable mapping from SlotKinds to chosen fillers. Subsequent review cannot distinguish: (i) what was planned, (ii) what was executed, and (iii) what changed via a crossing or edition-key shift.

**Show (repair with `SlotFillingsPlanItem`).** A conformant `SlotFillingsPlanItem`:
* targets `CHRMechanismSuiteDescriptionRef` as the slot-bearing description (and pins its edition if used as a reproducibility baseline),
* pins `CNSpecRef` and `CGSpecRef` (editions pinned where reproducibility requires),
* pins a `ScoringMethodDescriptionRef.edition` (e.g., a monotone scoring family) and, when needed, a set-valued method family (e.g., conformal-style set predictions),
* declares `Γ_time_selector = point(t0)` (no implicit “latest”),
* declares `expected_usm_guard_pins = {USM.CompareGuard, USM.LaunchGuard}`,
* includes evidence pin refs that will be populated or used in Work enactment.

The resulting Work enactment cites this PlanItem as the planned baseline; any substitution (e.g., retargeting a method description ref) appears as Work variance (and, when relevant, as a crossing witness), not as a retroactive plan rewrite.

#### A.15.3:5.2 - Archetype 2: Archive and QD selection with edition-sensitive descriptors

**Tell.** A workflow plans to return an **archive** (quality-diversity style) rather than a single winner. The selection pipeline depends on descriptor maps and distance definitions that are edition-sensitive.

**Show (failure without `SlotFillingsPlanItem`).** Descriptor-map and distance-definition drift is discovered only after the fact: an "archive" is produced, but practitioners or auditors cannot reconstruct which descriptor edition and distance definition were assumed at planning time, and the published view or card becomes the de facto mutable canonical source.

**Show (repair with `SlotFillingsPlanItem`).** A conformant `SlotFillingsPlanItem`:
* targets an archive-selection kit or suite as `target_slot_bearing_description_ref`,
* pins `DescriptorMapDescriptionRef.edition` and `DistanceDefDescriptionRef.edition` (or their kit equivalents),
* states `expected_usm_guard_pins = {USM.CompareGuard}` (if no LaunchGate is expected yet),
* records expected crossing policy pins if descriptors are reused cross-context.

This prevents “silent” descriptor drift across iterations and makes Part G’s archive-related extensions composable rather than embedded in selector prose.

### A.15.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Ontology and episteme**, **Prag**, **Did**. Scope: **Universal**.

| Lens | Bias / limitation introduced by the pattern | Mitigation |
| --- | --- | --- |
| Gov | Baseline immutability and variance recording can be misread as bureaucracy rather than epistemic hygiene. | Keep the baseline minimal; use suite-specialized refinements only when a suite description truly requires them. |
| Arch | Enforces a clean P2W seam and discourages “configuration hidden in mechanisms”. This can expose underspecified slot-maintenance assignments earlier. | Treat that friction as an architectural signal; refine the slot-maintenance interface rather than hiding choices in prose. |
| Ontology and episteme | Biases toward explicit context, time, and edition pinning; exploratory reasoning may feel constrained. | Use minimal variants (context + rows + time selector) for exploration; graduate to pinned editions only when reproducibility is required. |
| Prag | Increases upfront explicit-writing cost (explicit context, time, edition pins). | Use derived indices as projections for practitioner navigation; avoid duplicating content on views or cards. |
| Did | Biases against “one true card” habits by treating views as projections; may clash with existing documentation culture. | Provide a TechCard and PlainView projection explicitly, but keep the PlanItem as the governing work-plan record. |

### A.15.3:7 - Conformance Checklist

| ID          | Check (normative)                                                                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CC-A15.3-01 | The object is a `U.WorkPlan.PlanItem` with `kind = SlotFillingsPlanItem`, and obeys WorkPlan guardrails (no logs or actual fillings, no step logic).                                                                           |
| CC-A15.3-02 | `target_slot_bearing_description_ref` is present and identifies a real slot-bearing description (kit or suite); SlotKinds in rows are interpreted only within that slot-bearing description.                                                                      |
| CC-A15.3-02a | If the PlanItem is used as a reproducibility baseline and the slot-bearing description is edition-addressable, `target_slot_bearing_description_ref` is edition-pinned (e.g., `…DescriptionRef.edition`).                                      |
| CC-A15.3-02b | `target_slot_bearing_description_ref` is a **Description-scoped** ref (e.g., `MechSuiteDescriptionRef`, `…KitDescriptionRef`) and MUST NOT target `MechanismDefinitionRef`. |
| CC‑A15.3‑02c (single slot-bearing description) | A `SlotFillingsPlanItem` targets exactly one slot-bearing description via `target_slot_bearing_description_ref`. If multiple slot-bearing descriptions are involved, they MUST be represented by multiple PlanItems (one per slot-bearing description). |
| CC-A15.3-03 | `described_entity_ref` is present. If `grounding_holon_ref` or `reference_plane` is omitted, the omission must be unambiguously derivable from cited context publications or records (e.g., the pinned CG-frame and specification context). |
| CC-A15.3-03a | `described_entity_ref` is a concrete RefKind (no generic “EntityRef” placeholder is introduced by this pattern). |
| CC-A15.3-04 | Context anchors are explicit at least to `bounded_context_ref`; if the fillings serve legality or selection, then CG-frame and path-slice anchors are present.                                                           |
| CC-A15.3-05 | Time is explicit: the item includes `Γ_time_selector` or `Γ_time_rule_ref`; “latest” or “current” without explicit `Γ_time` is nonconformant.                                                                             |
| CC-A15.3-05a | Exactly one of `Γ_time_selector` and `Γ_time_rule_ref` is present (XOR); both-present or both-absent is nonconformant. |
| CC-A15.3-06 | `planned_fillings` is the authoritative source: each row is `⟨slot_kind, planned_filler, edition_pin?⟩`; each planned filler is explicit `ByValue` vs `ByRef(ref-of-concrete-RefKind)` and conforms to the slot-bearing description’s SlotSpec discipline (no silent slot-meaning changes). |
| CC-A15.3-06a | Unless the slot-bearing description declares a slot as multi-valued, `planned_fillings` contains **no duplicate** `slot_kind` rows (duplicate keys ⇒ nonconformant). |
| CC-A15.3-06b | If both a row and its `ByRef(…)` filler carry edition pinning, they MUST agree; mismatch ⇒ nonconformant. |
| CC-A15.3-07 | Any present “indices” (`planned_*_ref_index`) are derivable projections of `planned_fillings` and are not independently maintained; mismatch ⇒ nonconformant.                                                         |
| CC-A15.3-08 | The PlanItem contains no `GateDecision` or `DecisionLog`, and makes no claim that a crossing occurred; only expected policy pins may be stated.                                                                      |
| CC-A15.3-09 | The PlanItem contains no `FinalizeLaunchValues` witness and no launch-time actuals; launch values are finalized only in Work enactment.                                                                             |
| CC-A15.3-10 | If `expected_usm_guard_pins` includes `USM.LaunchGuard`, the PlanItem contains sufficient pins and references (explicit `Γ_time_selector` or `Γ_time_rule_ref`, pinned editions, evidence pin anchors, and `guard_owner_gate_ref` or an unambiguous derivation) to make downstream guard execution possible.     |
| CC-A15.3-10a | In this pattern, “evidence anchors” are expressed as pin refs (e.g., SCR pins or RSCR pins). Do not introduce a generic `EvidenceHookRef` token here; use concrete pin refs. |
| CC-A15.3-11 | The PlanItem does not claim to set or mutate the edition vector (`editions{…}` or `edition_key`). It may pin editions and may state *expected* edition-sensitive crossings, but edition changes themselves are crossings (gate-level or work-level witnesses). |
| CC-A15.3-12 | When used as a baseline for enactment, execution-time deviations are recorded as Work variance and the baseline PlanItem is not rewritten (“no backfill”); the Work Audit cites the PlanItem (preferably by edition-addressable ref) as the planned baseline reference.  |
| CC-A15.3-12a | Any change to edition-pinned refs that would alter the effective edition-key for legality or selection MUST NOT be retroactively applied to the already-cited baseline PlanItem. Treat it as (i) a new PlanItem edition for subsequent enactments and (ii) variance or required crossing witnesses for the enactment that deviated. |
| CC-A15.3-13 | If `expected_crossing_policy_refs` is present, it contains references and policy identifiers only (BridgeCardRef + policy-id refs + plane ids); it MUST NOT embed CL, Φ, Ψ, or Φ_plane tables or introduce non-Bridge transport edges. |
| CC‑A15.3‑13a (crossing bundles are not witnesses) | `expected_crossing_bundle_refs` (if present) is used only to cite already‑published, context‑constant CrossingBundle baselines; it MUST NOT be used to claim that a crossing occurred for this enactment, nor to substitute for gate-level or work-level crossing witnesses. |
| CC‑A15.3‑14 (view projection discipline) | Any `U.View` projection of a `SlotFillingsPlanItem` (e.g., `TechCard(PlanItemRef)`, `PlainView(PlanItemRef)`) MUST be an explicit projection that introduces no additional claims, defaults, or rows beyond the PlanItem; any additional semantics on the view is nonconformant. |
| CC-A15.3-15 | Lower, repair, and refresh conditions are explicit: missing target description, SlotKind interface, EntityOfConcern, context, time, concrete RefKind, edition pin, guard pin, evidence pin, crossing policy, or cited-baseline variance lowers or reopens the planned-baseline claim rather than widening it. |

### A.15.3:8 - Common Anti‑Patterns and How to Avoid Them

#### A.15.3:8.1 - Plan-as-execution

A plan document says: “Use the latest CG-Spec and the current best comparator; compute scores and launch.”
This is nonconformant because it omits explicit `Γ_time`, omits edition pins, collapses planning into execution, and provides no stable baseline for variance and audit.

#### A.15.3:8.2 - Anti-example: Edition-key change disguised as a plan edit (backfill)

A team executes Work while actually using `CGSpecRef@edition(E2)` (or `ComparatorSetRef@edition(E2)`), but the previously approved baseline PlanItem had pinned `@edition(E1)`.
Later, instead of recording variance and the required GateCrossing witness for the **edition-key change**, someone edits the baseline PlanItem “in place” to replace `E1 → E2`,
and then claims “no variance; we followed the plan”.

This is nonconformant because it:
* collapses planning into execution (retroactive baseline editing),
* hides an edition-key change that is crossing-relevant,
* destroys reproducibility and breaks Work and audit traceability.

Correct handling: keep the old baseline intact; record variance in Work and, where applicable, require the gate-level or work-level crossing witness (UTS and CrossingBundle with policy-id pins),
or produce a new PlanItem edition as the new planned baseline for subsequent enactments.

### A.15.3:9 - Consequences

| Benefit | Trade-off and cost | Notes and mitigation |
| --- | --- | --- |
| Improved modularity | Requires an explicit baseline plan item | Keep baselines minimal; specialise only when a suite truly needs it. |
| Audit clarity | More up-front specification work | The explicit-writing workload is intentional: it buys attributable variance and prevents “mystery defaults”. |
| Edition honesty | Forces practitioners to declare editions and time | Use editioned refs and time selectors by ref; keep actual `Γ_time` in Work evidence. |
| Controlled specialisation | Multiple PlanItem kinds may exist (core + suite‑specialised) | Create a suite-specific refinement only when the suite description requires it; keep the universal core stable. |

### A.15.3:10 - Rationale

This pattern exists to give WorkPlanning an explicit, citeable place to commit to “which planned values or references will fill which slots” without collapsing into run-time state.

Keeping the baseline bound to exactly one slot-bearing description makes SlotKind semantics checkable and prevents accidental cross-slot-bearing-description drift.

Treating indices as derived projections preserves the canonical row source while still enabling human-friendly navigation or tooling acceleration.

Finally, by disallowing run-time witnesses (launch values, observed values, concrete `Γ_time`) the pattern enforces the planning and enactment split and keeps audit variance attributable to an explicit baseline rather than to shifting defaults.

### A.15.3:11 - SoTA‑Echoing (informative)

This pattern aligns with post‑2015 practice in multiple traditions while deliberately staying notationally and tool independent.

* **ISO/IEC/IEEE 12207:2017** — **Adopt** the separation between planning documents, execution records, and baseline and change-control concepts; **Adapt** them into a lightweight, citeable PlanItem kind; **Reject** treating one process-tooling arrangement as normative inside FPF.
* **ISO 26262:2018** — **Adopt** the emphasis on traceability, change impact visibility, and preventing retroactive “paper compliance”; **Adapt** it into baseline immutability + variance reporting; **Reject** treating safety certification structure as a required envelope for all contexts.
* **NIST SP 800-128 Rev.1 (2020)** — **Adopt** baseline management and deviation recording as an audit primitive; **Adapt** by expressing baselines as epistemic, context-bound references rather than machine configuration states; **Reject** security-tooling prescriptions as a dependency of the conceptual model.
* **Forsgren, Humble, Kim (2018), _Accelerate_** — **Adopt** the empirical lesson that explicit change tracking and small, attributable deltas improve reliability; **Adapt** by making the baseline the anchor for fulfilment and variance; **Reject** any “one true pipeline” or vendor-specific operational recipe.
* **Morris (2021), _Infrastructure as Code_ (2nd ed.)** — **Adopt** the desired-state vs observed-state distinction and the discipline of explicit declarations; **Adapt** by keeping declarations as plan-level epistemes rather than deployment manifests; **Reject** binding the model to any specific IaC syntax or platform.

### A.15.3:12 - Relations

* **Builds on and is governed by:**
  * **A.15.2 `U.WorkPlan`** — container + PlanItem discipline; baseline citeability.
  * **A.6.5 slot discipline** — SlotKind and RefKind hygiene and binding-time separation.
  * **E.10.D1 Context discipline** — explicit context and edition; no implicit “latest”.
  * **E.18 and E.18.1** — keeps `FinalizeLaunchValues` strictly in WorkEnactment; pin and guard discipline.
* **E.17 publication discipline** — views are projections; no new semantics on cards.
* **Interacts with and complements:**
  * **A.6.7 `MechSuiteDescription`** — suites may require the presence of a planned-baseline reference or pin without embedding planned fillers or launch values.
  * **A.15.1 Work and WorkEnactment discipline** — fulfilment and variance are recorded downstream against this baseline.
  * **C3.2-S-02 Time discipline** — time selection policy may be pinned by ref; run-time `Γ_time` stays in Work evidence.

### A.15.3:12a - P2W Planned-Baseline Use Relation

When `E.18.1` reaches a planned-baseline question, `SlotFillingsPlanItem` records the planned mapping from a slot-bearing description and `SlotKind`s to planned fillers. It may include evidence-reference hooks, edition pins, assumptions, dependencies, and freshness requests needed before work is enacted.

If the same phrase also carries launch-value, run-time actual, evidence, gate, or result meaning, the carry-through record names that separate relation before the PlanItem is used downstream.

### A.15.3:12b - Planned-Baseline To Performed-Work Boundary

A performed `U.Work` occurrence may cite a `SlotFillingsPlanItem` as the planned baseline for slot fillers. The performed-work record states variance, substitution, and launch-value finalization under the current gate relation and work-governing patterns.

This preserves the P2W split: WorkPlanning places the baseline, while performed work records what happened.

### A.15.3:12c - Lowering, Repair, and Refresh Conditions

Lower a `SlotFillingsPlanItem` claim when the item cannot name exactly one Description-scoped slot-bearing description, concrete `SlotKind`s from that description, `described_entity_ref`, `bounded_context_ref`, time selector or time rule, authoritative planned-filling rows, concrete RefKinds for ByRef fillers, or required edition pins. Do not repair the missing detail by widening the planned-baseline claim; lower it to a plan cue, source-gap note, relation governed by another FPF pattern, or blocked kind-definition gap.

Repair the PlanItem when a source-currentness change alters the slot-bearing description edition, SlotKind interface, planned filler, concrete RefKind, edition pin, context anchor, time rule, evidence pin, guard pin, crossing-policy reference, or expected gate relation. If a performed `U.Work` occurrence already cited the PlanItem as a baseline, preserve the cited baseline and record variance or crossing witnesses in the work-governed relation rather than rewriting the cited baseline to match what happened.

Refresh before the PlanItem is used for work enactment, launch guard preparation, cross-context comparison, suite or kit reuse, Part G universalization, publication-view projection, evidence-reference use, or P2W carry-through. Stop the refresh at the smallest changed object: the plan item, its target slot-bearing description, a concrete RefKind, the cited source edition, the performed-work variance record, or the related gate, evidence, bridge, or publication relation.

### A.15.3:End
