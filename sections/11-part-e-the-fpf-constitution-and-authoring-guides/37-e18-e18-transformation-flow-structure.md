## E.18 - Transformation Flow Structure

> **Tech-name:** **TransformationFlowStructure** (pattern label)
> **Plain-name:** Transformation flow structure
> **Type:** Structural/ontic-relation pattern (E)
> **Status:** Stable
> **Normativity:** Normative unless explicitly marked informative
> **Twin labels:** Tech / Plain per E.10; faces published through E.17 MVPK (no schemas in Part E).

### E.18:1 - Intent

Provide a notation-independent pattern for `TransformationFlowStructure`: a selected compound structure of atomic `U.Transformation` values and transformation-adjacent governed loci. The EntityOfConcern is the selected structure itself: loci for atomic transformations and adjacent governed values, one typed `U.Transfer` relation, and Eulerian/declarative valuations over paths or path slices inside the same selected structure. A locus may express, decompose, constrain, or locate a bounded transformation under `A.3.4`, or it may bind a signature, mechanism, work plan, performed work, check, structural reinterpretation, publication, evidence, result, or refresh locus that participates in or constrains transformations without becoming the transformation. Crossings appear at gates; publication faces appear through MVPK; comparable claims pin editions, reference planes, Bridge/CL notes, and refresh scope. Mathematical descriptions of this selected structure, including graph, algebra, category, tuple, path, slice, morphism, quotient, fold, refinement, factorization, or wiring expressions, are governed by `E.18.2` and `C.29` when lens adequacy matters.

**Use this when.** Use E.18 when project work needs one selected transformation-flow structure, path, path slice, crossing, gate, flow valuation, or refresh locus over `U.Transfer`; use neighboring patterns when the current EntityOfConcern is a work plan, performed work, method semantics, publication face, mathematical description, or wording-use cue rather than the selected structure.

**First useful move.** Name the selected transformation-flow structure, the locus kinds, the single `U.Transfer` relation, and the crossing, path, or path slice whose pins are required. For the ordinary case, this is enough: `TransformationFlowStructure`, current `PathId` or `PathSliceId` when a path or slice is the EntityOfConcern, locus kinds, one `U.Transfer`, and only the crossings or pins required by that application.

First-use slice:

```text
TransformationFlowStructure:
  selectedStructure: cooling-loop stabilization path for one reactor subsystem review.
  loci:
    L1: U.Transformation, cooling-loop operating-state stabilization.
    L2: U.Mechanism, control-law mechanism governing the stabilization.
    L3: U.WorkPlan, planned measurement and setting-change work.
    L4: U.Work, dated test run only after work occurs.
  transferRelationKind: U.Transfer.
  currentPathSlice: emergency-load-change review slice.
  crossingOrGate: safety-review gate only where context, edition, launch, or work boundary changes.
  mathematicalDescriptionRef?: E.18.2 only if a graph, algebra, or category expression is being used.
```

This slice names the selected structure and its governed loci first. Publication faces, TEVB viewpoint mapping, GateDecision records, and conformance rows are opened only when that use actually publishes, maps viewpoints, crosses a gate, or consumes assurance checks.

**Structure ontology.** E.18 keeps these distinctions primary:

| Construct | What it carries | Boundary |
|---|---|---|
| `TransformationFlowStructure` | the selected compound structure, positioned locus kinds, one `U.Transfer` relation, and structure-wide budgets or edition pins | not a work procedure, method sequence, mathematical graph expression, or one `U.Transformation` |
| transformation locus | an E.18 locus, path, path slice, substructure, or valuation used to express, decompose, constrain, or locate a bounded `U.Transformation` | governed by `A.3.4` for transformation identity and slots |
| functional behavior in a flow | a required behavior/functioning claim grounded as one bounded `U.Transformation` or as a compound `TransformationFlowStructure`, with any selected flow position, path, slice, crossing, or valuation named by value | not identical with `FunctionalElement@Context`, not the transformer system, not a module allocation, and not a method/work occurrence by itself |
| slot-filler locus | a structure-positioned signature, mechanism, work plan, performed work, check, structural reinterpretation, publication, evidence, result, refresh, or other governed value | not a transformation merely by structure membership |
| flow valuation | an Eulerian/declarative valuation over a path, path slice, state, guard, comparator, or budget over the selected structure | not a flowing thing, imperative route, second structure kind, or performed work |
| crossing or gate | a context, plane, edition, launch, or work-boundary change | not internal step validity or gate-decision publication by itself |
| MVPK face | publication of selected structure, path, or crossing material | not the structure semantics and not evidence by itself |
| refresh locus | the smallest path slice, crossing, edition pin, or publication face affected by change | not a whole-flow rewrite unless the whole flow is the changed locus |

When a sentence says that a system performs a functional transformation at one point in a flow, E.18 carries only the selected flow structure, locus, path, slice, crossing, valuation, and pins. The bounded transformation, transformer or candidate bearer, input/output or functional-port boundary, functioning relation, method/algorithm, mechanism, and performed work are recovered through `A.3.4`, `A.6.F`, `C.30.ASV`, `A.6.M`, `A.6.1`, and the A.15 family as applicable. A computational algorithm may fill `MethodRef?` or `MethodDescriptionRef?`; a physical-world way of transforming may fill `U.Method`; neither is inferred from E.18 structure membership.

**Not this pattern when.** Use `A.20` for internal step validity, `A.21` for gate-decision publication, `E.20` for mechanism-governing-definition placement, `A.3.4` for bounded transformation under conditions, `E.18.2` for mathematical descriptions of the selected structure, `C.27.TA` for temporal aspects, `C.27` for temporal-claim adequacy or supported-use claims, the A.15 family for work planning or performed work, `E.17` for publication faces, and `E.10` for wording-use repair when the current EntityOfConcern is not the selected structure, path, crossing, or flow valuation.

**What goes wrong if missed.** A practitioner may treat a reference flow, a wording-use cue such as `transition`, or a tool pipeline as a new graph kind or a hidden prescribed workflow, then lose comparability, crossing evidence, and slice-local refresh boundaries.

**What this buys.** E.18 keeps selected structure, publication pins, crossings, CV/GF separation, and refresh locality in one current structure pattern without turning every domain-specific path into its own flow doctrine or every mathematical graph description into the selected structure.

### E.18:2 - Problem frame

Teams can produce many **well-typed flow valuations** for transformations of the same context holon under `VP.Functional`, for example for a declared `U.Capability` or transformation claim. The holon is the described/context object; the E.18 `EntityOfConcern` remains the selected `TransformationFlowStructure` over transformations and adjacent governed loci. The P2W reference path is:
`U.Signature(profile=FormalSubstrate) -> U.PrincipleFrame -> U.Mechanism -> U.ContextNormalization (UNM) -> SelectionAndTuning locus (G.5/selector relation) <-> WorkPlanning locus (A.15.2 U.WorkPlan or plan-item relation) -> U.Work -> EvaluatingAndRefreshing locus (G.11/refresh relation)`
is one **path** among many possible domain-specific transformation-flow paths. Without a common **structure discipline**:

* flows look ad-hoc and **non-comparable**;
* cross‑Context **crossings** (plane/Context changes) are undocumented;
* MVPK faces carry **hidden arithmetic** or restate I/O;
* set‑returning selection is silently replaced by **single scores**;
* cycles lack **budget** discipline; refresh is **out‑of‑band**.

MVPK already fixes publication drift at the **single-arrow** scope; E.18 lifts those **publication and comparability laws** to the **selected transformation-flow structure as a whole**.

### E.18:3 - Problem

1. **Mathematical lens != selected structure.** A catalog of morphism-scoped, transformation-scoped, mechanism-scoped, work-scoped, or refresh-scoped patterns does not, by itself, explain **how the whole selected structure is built, constrained, and audited**.
2. **Flow proliferation.** Multiple “reference flows” can be declared; practitioners need **one structure discipline** that keeps their flow relations typed and comparable **without privileging any single flow**.
3. **Unsafe publication.** Faces re‑list I/O, hide scalarization, or omit edition/plane pins; cross‑Context reuse lacks **Bridge/CL** citation; **plane penalties** appear in F/G instead of R.
4. **Cycles without norms.** Selection↔Planning loops run without explicit **budget (Γ_time)**, **FreshnessRequest**, or **slice‑scoped** refresh; `FinalizeLaunchValues` (launch‑value slot filling) is performed too early (outside `U.Work` (`U.WorkEnactment`)).

### E.18:4 - Forces

| Force                                            | Tension                                                                                                                                                                    |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Universality vs specialization**               | One architecture covers supply chains, water networks, ML functionals, and the P2W first-principles-to-work path, **without** baking in any one morphism set. |
| **Publication neutrality vs auditability**       | Keep faces notation‑neutral and non‑mechanistic ↔ require **pins**, **ComparatorSet**, **Bridge/CL**, and **PublicationScope**.                                            |
| **Set-return discipline vs business pressure for totals** | Preserve **return sets and declared partial orders** ↔ stakeholders demand single numbers.                                                                                     |
| **Cross‑Context reuse vs safety**                | Enable reuse across `U.BoundedContext` ↔ require **Bridge/CL** with **R‑only penalties**.                                                                                  |
| **Agility vs reproducibility**                   | Permit evolving CG‑Spec/UNM/Comparator editions ↔ require **edition pins** and **re‑emission** on change.                                                                  |
| **Cycles vs convergence**                        | Allow Selection↔Planning iteration ↔ impose **budget** and **slice‑scoped** refresh to prevent thrash.                                                                     |

### E.18:5 - Solution - Transformation-flow structure model and relation disciplines
**Dominant Solution moves.** In ordinary E.18 use, keep five moves primary: name one selected transformation-flow structure; distinguish the selected structure from a flow valuation and from its mathematical descriptions; place gates only on crossings or the `U.WorkEnactment` boundary; preserve normalize-before-compare and set-return discipline; and keep cycles under budget plus `PathSlice` refresh. S12 viewpoint mapping remains conditional viewpoint-mapping input when engineering or publication viewpoint mapping is current.

#### E.18:5.1 - S1 - Selected Structure (conceptual)

Define a **typed, editioned transformation-flow structure**
`TransformationFlowStructure := (Loci, Transfer, tau_L, tau_Transfer, Gamma_time, Bridge, CL, TransportRegistry^Phi)`
with:

* **Loci:** structure-positioned loci or bindings to governed FPF values (open world). Common specialisations **include but are not limited to** the P2W illustrative set: bounded `U.Transformation`, `U.Signature(profile=FormalSubstrate)`, `U.PrincipleFrame`, `U.Mechanism`, `U.ContextNormalization (UNM)`, `SelectionAndTuning` locus governed by current selector/comparator patterns, `WorkPlanning` locus governed by `A.15.2 U.WorkPlan` or a plan-item relation, `U.Work`, and `EvaluatingAndRefreshing` locus governed by current refresh/evaluation patterns. This list is **illustrative**, not exhaustive. A locus may be expressed by a morphism, graph vertex, tuple position, or category-theoretic object under a mathematical lens when that lens is current, but E.18 does not make every locus a `U.Morphism`, graph vertex, or `U.Transformation`.
* **Transfer relation:** a **single relation kind `U.Transfer`** (typed) carrying carrier refs and token refs; all **plane/Context/edition** changes occur **only at loci via `OperationalGate(profile)`** with **Bridge + CL** annotations; penalties **-> R only**. Transport conversions pin **Phi-policies** and editions.
* **Scopes:** `Gamma_time` (budgets, horizons), `PublicationScope` for faces (E.17), and **slice ids** for refresh (G.11).

 **CtxState (PS‑projection; closed slots):** `CtxState = ⟨L, P, E⃗, D⟩` is the **projection of E.17 Publication Scope**.
 **Slot definitions (normative):**
  • `L := Locus` — an element of a partially ordered **ContextSlice** poset; addresses *where* claims apply (disciplinary / organizational / holonic slice).
  • `P := ReferencePlane` — the reference plane/units registry id; **no plane/unit declarations or translations** occur in CV; crossings remain gated (A.21).
  • `E⃗ := Edition vector` — a **partial map** `edition_key ↦ EditionId` over named families `{CG‑Spec, ComparatorSet, UNM.TransportRegistryΦ}` and optional `{DescriptorMapRef, DistanceDefRef, CharacteristicSpaceRef}` when cited.
  • `D := DesignRunTag` — `design(T^D)` or `run(T^R)`, used by **LaunchGate** and acceptance/telemetry duties.
 **Invariants.** Raw `U.Transfer` preserves `CtxState` (`⟨L,P,E⃗,D⟩`): it does **not** write/update any CtxState slot; any CtxState write/update (or entry to `U.WorkEnactment`) occurs at `OperationalGate(profile)`.
 **Extension discipline.** A conforming use registers any extra slot beyond ⟨L,P,E⃗,D⟩ in the **E.17/LEX “CtxState Extension Registry”** with slot‑id, intent, partial‑order law (neutral/absorbing), and SquareLaw compatibility; unregistered extensions are non‑conformant.
 **Data-shape location.** E.18 names the structure and valuation obligations for `PathId`, `PathSliceId`, Gamma pins, and lineage: flow is a valuation over `U.Transfer`, raw transfer preserves `CtxState`, and path or slice evidence is carried through this pattern plus `A.20`, with `G.6` or `G.11` for cases involving evidence-path visibility or refresh wiring. These are the current structure loci for path and slice currentness.

 * **Locus kinds:** `Transformation`, `Signature`, `Mechanism`, `WorkPlanning`, `Work`, `Check`, and `StructuralReinterpretation` are the current minimal structure-positioned locus baseline. Domain-specific species are open-world and non-exhaustive, but each species binds to one of the locus kinds or requires an explicit E.18 update. These are positioned loci in the selected structure, not a local taxonomy of new FPF kinds.
  **Exact identification (no local ontology):**
  — `Transformation` **≡** **A.3.4** `U.Transformation` when the structure locus, path, path slice, substructure, or flow valuation is being used as a bounded transformation under conditions.
  — `Signature` **≡** **A.6.0** `U.Signature` (universal, law-governed declaration).
  — `Mechanism` **≡** **A.6.1** `U.Mechanism` (law-governed application over a SubjectKind/BaseType), with placement and stabilization relations in `E.20` when current.
  — `WorkPlanning` **≡** **A.15.2** `U.WorkPlan` or its current plan-item relation when planning is the governed value.
  — `Work` **≡** **A.15.1** `U.Work` / `U.WorkEnactment` (dated world-contact; `FinalizeLaunchValues` only here).
  — `Check` **≡** `OperationalGate(profile)` (universal **gate**; `A.20` governs CV when internal step validity is current, and `A.21` governs gate profile, check aggregation, decision, and publication minima when gate fit or gate decision is current).
  — `StructuralReinterpretation` **≡** the E.18 placement of **A.6.4** `U.EpistemicRetargeting` as a structure-positioned locus; it is not a new retargeting kind. **All retargeting semantics** (slot-scoped discipline, `EntityOfConcernSlot`/`GroundingHolonSlot` behaviour, invariants, Bridges, witnesses) come from **C.2.1** and **A.6.2–A.6.5**; E.18 does **not** introduce a local variant of retargeting.

  `OperationalGate` is the E.18 check locus with DecisionLog aggregation. A check-locus label names only the current gate or check value that the selected structure positions: `A.20` governs internal constraint validity when that claim is current, `A.21` governs gate profile, aggregation, decision, and publication minima when gate fit or gate decision is current, and `A.3.4` governs the bounded transformation claim that the check constrains.
  The only extra discipline E.18 adds for `StructuralReinterpretation` is **structure-local**: CtxState and GateCrossing behaviour are governed by **CC-E18-06-EX** and **CC-E18-11** (projection-preserving w.r.t. `⟨L,P,E⃗,D⟩`, PathSlice-local, and "no plane/unit change without a gate"). `StructuralReinterpretation` is not a gate exception; it carries a recorded witness condition for saying no GateCrossing occurred. If any `CtxState` slot, plane/unit, edition, or design/run boundary changes, the case is a GateCrossing again.
> **MVPK integration (import).** Every locus with an external publication face is published via **MVPK** faces (`PlainView`, `TechCard`, `AssuranceLane`, `InteropCard`) under a declared **PublicationScope** (E.17). E.18 **reuses** MVPK's publication laws (pins, declared-order discipline, "no new numeric claims / no I/O re-listing") and only adds structure-scope constraints in S3 and **CC-E18-09/10**; it does **not** define a second, local publication semantics.

**GateCrossing (normative)**
**Definition.** A **GateCrossing** is the typed transition at a structure locus that writes/updates any of:
  (i) `U.BoundedContext` (**Context**), (ii) **ReferencePlane**, (iii) any member of the **Edition vector** `E⃗` (e.g., `CG‑Spec`, `ComparatorSet`, `UNM.TransportRegistryΦ`, `DescriptorMapRef`, `DistanceDefRef`, `CharacteristicSpaceRef`), (iv) **DesignRunTag** (`T^D↔T^R`), or (v) **Kind/EntityOfConcernRef** (only under `StructuralReinterpretation` subject to **CC-E18‑06‑EX**).
**Invariants.** Raw `U.Transfer` preserves `CtxState`; a GateCrossing occurs at exactly one `OperationalGate(profile)` (SquareLaw applies).
**Required pins (minimum).** `BridgeCard + UTS row`; `CL` for scope bridges; `CL^plane` for plane crossings; `CL^k` with `bridgeChannel=Kind` for kind transitions; `PublicationScopeId`; `PathSliceId`; Γ‑pins on compare/launch faces.
**Canonical reference.** `CrossingRef := ⟨GateId, channel, from, to, UTS.RowId, PathSliceId⟩`. Any DecisionLog entry whose rationale depends on a crossing cites `CrossingRef`.
**CrossingBundle (normative)**
**Definition.** A **CrossingBundle** is the published bundle that makes a GateCrossing **auditable and replayable** (crossing visibility). It includes:
* the canonical **`CrossingRef`**;
* the matching **UTS row** (**`UTS.RowId`**) for the crossing;
* the required pins **`PublicationScopeId`** and **`PathSliceId`**;
* where a Bridge is involved: the **BridgeCard** (F.9) and its disclosed fields (`BridgeId`, `bridgeChannel`, **CL** and loss notes; **`CL^k`** when `bridgeChannel=Kind`; **`ReferencePlane(src,tgt)`**);
* where planes differ: **`CL^plane`** and the active **`Φ_plane`** as a **`PolicyIdRef`** (policy-id + resolvable refs; F.8:8.1);
* the active penalty policy identifiers **`Φ(CL)`** (and **`Ψ(CL^k)`** if used) as **`PolicyIdRef`** bundles (policy-id + `PolicySpecRef` + `MintDecisionRef?`; F.8:8.1);
* any additional pins mandated by the active **GateProfile** / GateChecks (A.21) for this crossing.

**CrossingBundle rule.** Every **GateCrossing publishes its CrossingBundle**. Missing or non-conformant CrossingBundle is a **blocking** defect for downstream uses that rely on the crossing (selectors, acceptance, audits). A local descriptive graph with no downstream crossing consumption is not over-penalized by this CrossingBundle rule.

**Term separation.** **Transfer** denotes the sole relation kind `U.Transfer` in the selected structure. **Transport** denotes Phi-governed conversion **policies/registries** (**`TransportRegistry^Phi`** under UNM). Wording "reuse via Transport" refers to registries/policies, not to an additional transfer relation.

#### E.18:5.2 - S2 - Flows as valuations (paths + state + guards)
* A **Flow** is a **valuation** `nu` over `U.Transfer` relations and cut-sets, paired with an **admissible path** `p = v0 -> ... -> vk` in the selected structure. The valuation maps transfer relations or cut-sets to token/state values under `CtxState` and links publication-event records to a declared `PublicationScopeId`; it is not itself the performed work. The concrete pins and identifiers (`PathId`, `PathSliceId`, Gamma_time on compare and launch faces) are governed here as path and slice publication obligations and by `A.20` when CV witnesses are current; use `G.6` for evidence-path visibility and `G.11` for refresh wiring. This reflects the "selected structure != flow" norm (flow = valuation), with gates placed exactly on GateCrossings.
* **Multiple coupled flows.** One `TransformationFlowStructure` may contain several coupled flow valuations: a development-flow valuation over work that creates or repairs a specification, pattern, process description, mechanism description, method set, tool, or work plan; an application-flow valuation over use of that product for another `EntityOfConcern`; and an evaluation or refresh-flow valuation over evidence that identifies a problem and a repair return to the smallest affected development or application locus. The selected structure relates those flow valuations through `U.Transfer`, `PathSlice`, edition-change, refresh, return, or feedback relations, but it does not merge their governed objects, records, launch values, evidence, gates, or performed work. The same product may be a run result of one flow and a design-side input, tool, or contextual object for another flow; that flow-local relation-position change is recorded by the current flow relation and any current `DesignRunTag` crossing, not by silently changing the object kind.
* **Admissible path (definition).** A path `p` is **admissible** iff:
  (a) locus/transfer types match the declared `tau_L, tau_Transfer`;
  (b) any write/update to any member of `⟨L,P,E⃗,D⟩` (or kind‑retargeting under `StructuralReinterpretation`) appears at **exactly one** `OperationalGate(profile)`;
  (c) each GateCrossing on `p` has a **SquareLaw witness** (CC-E18‑23) and, where applicable, a **SquareLaw‑retargeting witness** (CC-E18‑06‑EX);
  (d) no hidden crossings occur across raw transfers;
  (e) Γ‑pins are present on compare/launch faces;
  (f) `T^D↔T^R` occurs **only** at `LaunchGate`.

* `U.Transfer` preserves `CtxState` (`⟨L,P,E⃗,D⟩`) and carries **Assurance‑operations** only (see S3b); any crossing of locus/plane/editions or `T^D↔T^R` is placed at `OperationalGate(profile)`.
* A **PathSlice** is a **slice‑scoped execution window** used for refresh/telemetry; faces pin `PathSliceId`; **re‑emission** happens when any pinned edition changes or `SliceRefresh` is triggered by sentinel rules.

> **Consequences.** The P2W reference flow is simply one `p` in `TransformationFlowStructure`. Other domains (supply chain, water network, NN functional) instantiate different `p` on the **same selected-structure pattern**.
>
**Why "flow = valuation" preserves the ordinary "something changes" intuition**
There are two complementary perspectives:
* **Lagrangian (intuitive):** track tokens or state changes through a physical, organizational, or computational network.
* **Eulerian (structural):** define a **function on transfer relations** ("how much/what is associated with each relation under a given regime"), with gate laws. E.18 deliberately fixes the **Eulerian semantics of flow** at the selected-structure scope: "flow (= valuation) + publication log", while change over time appears as **re-valuation** over a **PathSlice** (the execution/republishing window) under gate rules and the SquareLaw. This yields comparability, reproducibility, and slice-local refresh.

#### E.18:5.3 - S3 - Publication discipline (faces)

E.18 **imports E.17** wholesale **and associates MVPK faces with `PublicationScope` (USM)**.
**MVPK remains the normative source** for:
* the set of face kinds (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`),
* pin discipline and Publication Characteristics (PC),
* “no new numeric claims / no I/O re‑listing / no Γ‑semantics on faces”.

E.18 **does not re-specify** these laws; it only adds **structure-scope obligations** for faces published over transformation-flow paths:

1. **Crossings on faces.** When a face participates in a GateCrossing (S1.b/S9), it cites `BridgeId + UTS row + CL` and publishes **Φ(CL)/Φ_plane RuleId**; **penalties remain in R‑lane**.
2. **Gate requirement on cited editions.** Any face that references editions of `CG-Spec`, `ComparatorSet`, or `UNM.TransportRegistryPhi` includes **`BridgeCard + UTS row`**; faces without this are treated as **non-consumable downstream**. Bridge and terminology-synchronization checks are governed by `F.9`, `F.17`, `E.17`, and `E.18`; selection and comparator pressure stays with `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, or `G.11` for current selector or comparator cases.
3. **ComparatorSet & set returns (structure-scope).** Any `ComparatorSet` and `SetSemanticsRef` used along a transformation-flow path carries **edition identifiers**; affected faces are **re-emitted** on edition change; faces with comparison **return sets and declared partial orders** (no hidden scalarization), reusing MVPK's declared-order discipline.
4. **Gamma_time on compare and launch faces.** All compare and launch faces on E.18 paths pin `Gamma_time`; implicit *latest* is not admissible. `A.21` carries current GateProfile binding and minimum profile semantics; E.18 paths include the pin. **CHR avoids acceptance thresholds** (*NoThresholdsInCHR*); thresholding and launches are carried by `A.21`, Part G, and `U.Work` for current launch or thresholding cases. Unknowns remain tri-state (`pass|degrade|abstain`) and fold per the active GateProfile (`A.21`).

> **Reminder.** MVPK already bans "signature" on faces, I/O re-listing, arithmetic on faces, and unpinned numeric content (E.17 §5.4-5.5). E.18 **does not weaken or override** those rules; it only constrains how they are used along transformation-flow paths.

**Lean publish‑mode (AssuranceLane‑Lite).** Lean changes **publication faces only** (`PlainView`/`AssuranceLane` minimal), not checks; publication shows `GateProfile`, `GateCheckRef[]`, and `DecisionLogRef`; the underlying GateChecks list remains unchanged.

**Decision stability & idempotency (gate-local).** Gate decisions are stable under a declared equivalence relation over the pins used by `A.21`; the witness is recorded as `DecisionLog` or `EquivalenceWitnessRef`, with `G.6` or `G.11` used for cases involving evidence-path visibility or refresh implications. E.18 **does not** prescribe storage formats, key shapes, or hashing schemes.

**KindBridge admissibility (publication).**
Treat a step as a **EntityOfConcernRef/kind** transition (including `StructuralReinterpretation` under CC-E18‑06‑EX) **iff** the **UTS row**:
  — satisfies the minimal bridge and terminology-synchronization obligations of `F.9`, `F.17`, `E.17`, and `E.18` for the current crossing case (identity, `ReferencePlane`, `CL/CL^plane`, edition pins for `CG-Spec`, `ComparatorSet`, `UNM.TransportRegistryPhi`, `ComparatorSetRef`, `BridgeId`, and `Phi-RuleIds`), and
  — is additionally marked as a **KindBridge** per C.3 (`bridgeChannel=Kind`, `CL^k`, mapping or signature‑translation, order‑preservation claims, loss notes, definedness area, determinism).
Otherwise this KindBridge explanation does not apply (the step falls back to a gated crossing). When the crossing is gate-mediated, `CrossingRef` is cited and linked from the `DecisionLog`.

#### E.18:5.4 - S4 - Assurance‑operations on `U.Transfer` (counterfactual admissibility)
On `U.Transfer` relations, an operation is interpreted as a **declarative assurance-operation** **iff** it is one of
`ConstrainTo(rule)` - `CalibrateTo(calibrationReference)` - `CiteEvidence(evidenceRef)` - `AttributeTo(provenanceReference)`; otherwise this explanation does not apply.
Under this interpretation, `CtxState⟨L,P,E⃗,D⟩` is preserved.
If a claimed assurance operation would change plane or units, the assurance-operations explanation does not apply and the step is handled as a gated crossing (`OperationalGate(profile)+Bridge+UTS`).

If Φ assigns penalties, they appear in the R‑lane; otherwise no penalties appear here.

#### E.18:5.5 - S5 - Comparability & aggregation (normalize‑then‑compare; counterfactual form)

The comparison explanation applies under the following admissibility conditions:

* If a path segment intends to compare/aggregate, it is admissible as a comparison **only when** UNM precedes it; UNM is **method‑independent**, publishes **TransportRegistry^Phi** and **CG-Spec** references, and faces cite those editions; otherwise this comparison explanation does not apply.
* If the comparator defines a **declared partial order**, then returns are **sets/archives** (Pareto/Archive); if a **total order** is declared, it is the one provided by the comparator; otherwise set semantics apply and covert scalarization is out of scope here.
* If a claim is **ordinal‑only**, then only comparison results are published; arithmetic transforms (e.g., means/z‑scores) are out of scope of this explanation and belong to declared comparators or downstream policy.

**Edition-aware set/archive publication records (e.g., QD archives) pin `DescriptorMapRef.edition`, `DistanceDefRef.edition`, and `CharacteristicSpaceRef.edition` when applicable; refresh is slice-local. Comparator, archive, and refresh checks are governed by `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, `G.9`, and `G.11` for current archive or refresh cases.**

#### E.18:5.6 - S6 - Cycle discipline (Selection ↔ Planning)

* The selected structure may center a loop between the `SelectionAndTuning` locus governed by selector/comparator patterns and the `WorkPlanning` locus governed by `A.15.2 U.WorkPlan` or a plan-item relation.
* The Selection-Planning loop is represented under a local **budget / max_iter** in `Γ_time`; at expiry, the selector output includes the **current `CandidateSet`** and **`MethodTuning`** with a **partial-optimality** flag; further improvement is placed in the **next `PathSlice`**.
* **UNM occurs before the loop**; if measurements are missing or stale, UNM output includes a **FreshnessRequest** represented in `A.15.2 U.WorkPlan` or a plan-item relation and enacted only by dated work under `A.15.1 U.Work`. Transfers, units, and calibrations are published as `CalibrateTo(calibrationReference)` and pinned to `TransportRegistry^Φ` (**R-channel only** for penalties).
* **WorkEnactment is the only site for launch‑value slot filling** (`FinalizeLaunchValues / FinalizeLaunchValuesOnlyInWork`).
> **Refresh orchestration.** Telemetry from `U.WorkEnactment` and publications are **slice‑scoped**, editions re‑pinned, faces **re‑emitted**.

#### E.18:5.7 - S7 - Selector semantics (G.5) & parity harness (G.9)
E.18 keeps set-return, archive preservation, and comparator refs visible along the path. It does not define selector, archive, dominance, or comparator semantics; those remain with `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, `G.9`, and `G.11` for current selector or comparator cases.

* **Selectors return sets.** Default **DominanceRegime** is `ParetoOnly`; **IlluminationSummary** (telemetry summary) and any coverage/regret telemetry quantities are **report-only telemetry** (reported), excluded from dominance **unless** a CAL policy promotes them as declared dominance inputs (policy-id in SCR).

If `PortfolioMode=Archive`, a **QD archive** can be returned; when generation is in scope, pairs `{environment, method}` are managed under declared **EnvironmentValidityRegion** and **TransferRulesRef**; parity records and `PathSliceId` are pinned on publication. Comparator semantics and archive pinning are governed by `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, `G.9`, and `G.11` for current archive or comparator cases.

#### E.18:5.8 - S8 - Guard aggregation assignment and handling (USM §1.2)
* **USM.CompareGuard**/**USM.LaunchGuard** **publish `GuardOwnerGateId`**. Guard failures are **events** aggregated by the declared gate (not GateChecks).
* **Aggregation-assignment rules:** (i) `USM.LaunchGuard.aggregationGate = LaunchGateId(U.WorkEnactment)`; (ii) inside a Subflow, `USM.CompareGuard.aggregationGate = OperationalGate(InSentinel)`; join loci cannot be assigned as guard-pin aggregation gates.

**GateProfile data shape (cross-reference).** `A.21` carries the current GateProfile binding and minimum profile semantics. E.18 names the structure only where crossings need it; fuller profile-matrix material is not a separate current authority unless a current governing pattern explicitly admits it.

**Bridge-aware guards (cross-reference).** USM guards apply bridge-translation semantics (`translate(Bridge, Scope)`) with CL penalties in R-lane; guard vocabulary is governed by **A.2.6**, while gate aggregation remains in `A.21`.

**Error/timeout/unknown (profile-bound).** GateCheck errors/timeouts fold to **`degrade`** under `Lean\|Core` and to **`block`** under `SafetyCritical\|RegulatedX`; `unknown` follows the GateCheck's governing rule (safety-default: `degrade`). The `A.21` DecisionLog record and equivalence witness carry decision stability; E.18 does not define storage or key structures.

#### E.18:5.9 - S9 - Transport & crossings
* Cross-Context or cross-plane transfer relations appear as **GateCrossings** that include a **Bridge** with **CL** policy; **Phi(CL)/Phi_plane** are published; penalties appear **in R only**; **Scope membership** (USM) is unchanged by crossings. **SquareLaw is checked within a single `DesignRunTag`; a `T^D<->T^R` change is modelled as a pair of coordinated gates with `DesignRunTagFrom/To` and the selected `A.15` work or publication locus for the current case.**
* When *EntityOfConcernRef/kind* changes across a boundary, declare an explicit **KindBridge (`CL^k`)** in addition to plane/context CL; cross-context reuse of UNM uses `Transport`, with any `CL^plane` penalties published in **R-lane** only.

#### E.18:5.10 - S10 - Non‑mechanism boundary

* Publication is a **typed projection**, not execution. Any build/render/upload is **Work on carriers**; faces do **not** carry Γ-semantics.

#### E.18:5.11 - S11 - Coordination wording labels (when current)
Coordination wording may be published as **LexicalView** labels over a P2W carry-through flow valuation; it is orientation-only unless a bridge, crossing, work, or gate relation is current. It adds no current structure locus kind, checks, or mechanisms. Crossings with production flow use **Bridge+UTS** and the current bridge or crossing loci.

#### E.18:5.12 - S12 - Viewpoint Families To E.18 Constructs (neutral, holonic)
**S12 status.** S12 is secondary viewpoint-mapping input for a current viewpoint-family mapping claim. It is not the ordinary E.18 core for naming a selected structure, flow valuation, path slice, or crossing.

E.18 does not mint new viewpoint or view kinds. It **imports** the generic multi-view machinery of E.17.0 `U.MultiViewDescribing`, bundles from E.17.1, and the TEVB engineering bundle from E.17.2. S12 only describes how these existing `U.Viewpoint` / `U.ViewpointBundle` ids are *used* in transformation-flow structures and in `UTS.ViewpointMap`; intent/concern semantics are governed by E.17.0-E.17.2.

**Two-part use of TEVB and MVPK (ISO 42010 summary, no local re‑definition).**

* **Engineering viewpoints.** For engineering holons, E.18 assumes a TEVB bundle with `ViewFamilyId = VF.TEVB.ENG`. `EngineeringVPId` is one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`, and TEVB is the normative source for their semantics. E.18 does not refine these viewpoints.
* **Publication viewpoints.** Publication viewpoints come from MVPK (E.17); `PublicationVPId` is a `MVPK.ViewpointId` that governs faces under a `PublicationScope`.
* **Architecture relation.** E.18 can supply the selected transformation-flow structure used by an `ArchitectureOf@Context` claim when `DescriptionContext`, described holon, bounded context, and structure kind are explicit. It does not define architecture itself, and a transformation-flow structure is not the functional architecture by default. Use `C.30`, `C.30.ASV`, and the architecture transformation-flow relation pattern when the selected structure is used in an architecture-flow relation. Crossings and penalties follow E.18 gating rules (S9; CC-E18-11/23) but do not change viewpoint semantics.
* **Separation of roles.** `VP.*` from TEVB are **EngineeringVPId** values only; they are not publication faces. `PublicationVPId` values are defined in MVPK. The mapping between them is entirely via ISO-style correspondences and the `UTS.ViewpointMap`; E.18 does not define a second notion of viewpoint.

**Context object scope (summary).**

* **Engineering described object.** The engineering entity described by TEVB may be a holon (`U.System` or `U.Episteme`) per TEVB's `EntityOfConcernClassSpec`. That holon is the context object whose transformations, work, interfaces, or viewpoints may be structured. E.18 does not make that holon its own EoC unless the selected transformation-flow structure itself is under concern.
  Transformation, method, procedure/control, role-enactor structure, structural architecture, module, interface, and allocation terms are viewpoint concern/content about that holon unless a concrete E.18 use explicitly opens A.6.4 retargeting with `KindBridge (CL^k)`, retargeting witness, and the applicable species rule.
* **Publication described object.** MVPK can treat the *architecture description* itself as an EntityOfConcern; publication viewpoints for that AD are defined in MVPK, not here. E.18 only checks that such faces honor MVPK discipline and E.18 crossing rules when they publish selected transformation-flow material.

**Naming rules (aligned with E.17.0/E.17.1/E.17.2).**
* `ViewFamilyId` is the `U.ViewpointBundle.viewFamilyId` (e.g. `VF.TEVB.ENG` for TEVB); its lexical and ontological discipline is governed by E.17.1.
* `EngineeringVPId : ViewpointId` is always a `U.ViewpointId` drawn from some bundle (for TEVB, one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`). E.18 never defines new `VP.*` ids.
* `PublicationVPId : ViewpointId` is a `MVPK.ViewpointId` defined in E.17; TEVB viewpoints are **never** reused as publication viewpoints (per TEVB guard and MVPK).
* The unqualified field name `ViewpointId` is not valid in S12 rows. Use `EngineeringVPId` and/or `PublicationVPId` explicitly; any imported row with an unqualified `ViewpointId` is normalized to `PublicationVPId` before the row is used.

**Terminology guards (no local semantics).**
* Within S12, “viewpoint”, “view” and “correspondence” have exactly the meanings given in E.17.0; “publication face” means an MVPK face (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`) under some `PublicationVPId`.
* Faces are **carriers for views**: a face is part of a view only when linked via an ISO‑style `CorrespondenceRef` to an engineering `U.View` under some `EngineeringVPId`; S12 does not add extra conditions beyond E.17.0/E.17.2.
* Labels such as “Functional view”, “Procedural view”, “Role‑Enactor view”, “Module‑Interface view” in this section are lexical aliases for TEVB viewpoints; they are not interpreted as extra viewpoint kinds or as publication-face types.

**Purpose.** Provide a neutral (F.18) mapping from TEVB engineering viewpoint families - bundle `VF.TEVB.ENG` with `VP.Functional / VP.Procedural / VP.RoleEnactor / VP.ModuleInterface` - to E.18 constructs so that the same holon can be described through functional, procedural, role-enactor, or module-interface viewpoints while the E.18 construct scope remains explicit. S12 does not introduce new `U.Viewpoint` or `U.View` kinds, and it does not claim that all such views share one underlying transformation-flow structure unless the structure, EntityOfConcernRef, and correspondence refs are declared.

**Holon target.** The mapping applies to any holon, with the constraint that only `U.System` enacts `U.Work` (A.3/A.15). Supervisory and structural hierarchies remain distinct (B.2.5).

**Viewpoint family to primary E.18 constructs (TEVB-aligned)**
*All four families referenced below are TEVB engineering viewpoints; the "what ..." clauses are interpretive glosses for how they *use* E.18 constructs. Formal intent/concerns/allowed episteme kinds remain in TEVB (E.17.2).*
1) **Function-Oriented View (`EngineeringVPId = VP.Functional`, capability and transformation viewpoint)** - "what transformation is achieved under roles"
    * **Flow valuation example:** P2W carry-through flow valuation through loci `U.Signature(profile=FormalSubstrate) -> U.PrincipleFrame -> U.Mechanism -> U.ContextNormalization (UNM) -> SelectionAndTuning locus -> WorkPlanning locus -> U.Work -> EvaluatingAndRefreshing locus`, where each illustrative locus label names a governed value or relation rather than a new `U.*` kind.
    * **Publication:** MVPK publication faces per E.17; comparable claims pin to `CG‑Spec/ComparatorSet` editions; crossings are published through `Bridge+UTS` and `CL/CL^plane` (penalties → **R‑lane** only).
    * **Checks:** A.20 (CV) inside transformations; A.21 (GateFit) at gates; comparator, set-return, and No-Hidden-Scalarization discipline is carried through `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, `G.9`, and `G.11` for current selector or comparator cases.
    *  **Holonic note:** `U.Episteme` does not *act*; it is used by systems acting on carriers; `U.Work` appears only for `U.System`.
2) **Procedure‑Oriented View (`EngineeringVPId = VP.Procedural`, step/time storyboard)** — “what steps occur and when”
    * **FPF constructs:** `U.WorkPlan` (A.15.2) for intent/schedule; `U.WorkEnactment` for enactment.
    * **Boundary:** entry into `U.WorkEnactment` is via `OperationalGate(profile)` with `USM.LaunchGuard`; `DesignRunTag` separates design time from run time; `DesignRunTagFrom/To` appear only at gates.
    * **Holonic note:** Applies to any `U.System` scope (single holon or a supervised sub‑holon cluster); supervisory structure is handled by roles rather than structural mereology (B.2.5).
3) **Role‑Enactor / Device‑Structure View (`EngineeringVPId = VP.RoleEnactor`)** — “what carrier/ports/constraints exist; who typically enacts it”
    * **FPF constructs:** Module *interfaces* are `Signature` loci; module realizations are `Mechanism` loci; inter-module dependencies traverse `U.Transfer`, with gates on crossings.

    * **Publication:** MVPK faces are **typed projections**, not `U.Work` records or execution carriers; faces add **no new numeric claims** (E.17). Constraints and compatibility appear as CV checks (A.20).
    * **Holonic note:** Structural mereology (part/whole of the carrier) is modeled in Part A; E.18 ties interface/exposure semantics to mathematical-lens expressions and gates only when those are current.
    * **Device-view structural reinterpretation.** The same transformation-flow valuation can be described as a **device** that performs the transformation without changing the declared `TransformationFlowStructure`: model with `Signature` + `Mechanism` only; do **not** introduce extra transfer kinds. If EntityOfConcernRef retargets (function <-> element), use `StructuralReinterpretation` with a **`KindBridge (CL^k)`** on **UTS** and a **SquareLaw-Retargeting witness**; preserve `⟨L,P,E⃗,D⟩` and treat it as a non-crossing (**CC-E18-06-EX**; witness shape §4.7).
    * **Role‑label guard.** `TypicalEnactorRoleName` is **pedagogical only** and is not used as a GateFit role; GateFit uses `U.Role` (A.21).
4) **Module‑Interface View (`EngineeringVPId = VP.ModuleInterface`, physical/logical module structure)** — “what modules exist and how they specify commitments and constraints across interfaces”
    * **FPF constructs:** Module *interfaces* are `Signature` loci; module realizations are `Mechanism` loci; inter-module dependencies traverse `U.Transfer`, with gates on crossings.
    * **EntityOfConcernRef note:** Functional-view-to-element-structure reinterpretation follows the **Device‑View structural reinterpretation** rule above (Role‑Enactor family) and **CC-E18‑06‑EX**; see **§4.7** for the retargeting witness shape and CV witness linkage.
    * **Holonic note:** The same module can appear as a holon in multiple views; supervisory loops (B.2.5) remain orthogonal to structural composition.
This is an expandable list of viewpoint families; E.18 is intentionally viewpoint-neutral. Additional engineering bundles beyond TEVB (safety, mission, information, ...) are introduced as separate `U.ViewpointBundle` species via E.17.1/E.17.2; S12 does not define them.

**View-family label discipline for transformation-flow loci (recognition-only).**
*Scope.* When a viewpoint-family mapping claim is current, a pattern or domain profile may declare `LocusViewFamilyLabels[]` for transformation-flow locus labels so practitioners can recognize familiar engineering wording while the selected structure stays governed by E.18. Semantics come from the referenced `U.ViewpointBundle`, E.18 locus binding, and MVPK correspondences; labels are recognition aids, not loci, viewpoints, publication faces, checks, or work records.

*Norms.*
1. Each current transformation-flow locus label may publish `LocusViewFamilyLabels[]` records of the form `{ ViewFamilyId, EngineeringVPId?, Label : TechASCII }`.
   * If `ViewFamilyId = VF.TEVB.ENG`, then `EngineeringVPId` is one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}` (TEVB; CC-TEVB-1/6).
   * Other `ViewFamilyId` values denote `U.ViewpointBundle` instances defined elsewhere, not ad-hoc local families.
2. Labels are recognition-only: no arithmetic, no new claims, no check participation, no `CtxState` slot writes or updates, and no `DesignRunTag` change. They do not create MVPK faces.
3. Labels are not used as `PublicationVPId`; publication viewpoints remain in MVPK.
4. Twin registers are allowed as Tech and Plain labels per E.10; naming follows F.18 local-first discipline.
5. Do not name transformation-flow loci by operands or output states; an operation is not its operand or output state.
6. `TypicalEnactorRoleName` can be added for pedagogy; it is not used as a GateFit role because GateFit uses `U.Role` only.
7. Morphology: ASCII TitleCase; conjunctions use `And`; for composite actions use `XingAndYing` or `XAndYing` when grammar calls for it.
8. The P2W illustrative locus row (`U.Signature(profile=FormalSubstrate)` through `EvaluatingAndRefreshing` locus with functional or procedural labels and `TypicalEnactorRoleName`) is informative and does not change kind or viewpoint semantics.

**Conditional deliverable — `UTS.ViewpointMap` (TEVB-aligned when current).**

Publish a UTS block named `ViewpointMap` only when an engineering or publication viewpoint-family mapping claim is made or consumed. Ordinary E.18 use does not require `UTS.ViewpointMap` when the question under repair is only the selected structure, flow valuation, path slice, or crossing.

*Minimum row schema (per row, when `ViewpointMap` is current).*
* `ViewFamilyId` — `U.ViewpointBundle.viewFamilyId` (e.g. `VF.TEVB.ENG` for TEVB, or another bundle id).
* `EngineeringVPId : ViewpointId` — a viewpoint from that bundle (for TEVB, one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`).
* `PublicationVPId : ViewpointId?` — MVPK publication viewpoint id that governs faces implementing this engineering view (optional if not publishing).
* `TargetHolon ∈ {U.System, U.Episteme}` *(extended species can add `{U.PromiseContent|U.MethodFamily}`; if `TargetHolon ≠ U.System`, no `U.Work` enactment appears).*
* `PrimaryE18Constructs` - loci, transfer relations, and gates actually used for this `(ViewFamilyId, EngineeringVPId, TargetHolon)` (typically one of the four families above).
* `Crossings{BridgeId, CL/CL^plane?}` — crossings involved; penalties appear in R-lane only.
* `EditionPins{...}` whenever comparable claims appear (bind to CG-Spec/ComparatorSet editions; any face citing editions includes `BridgeCard + UTS` row per MVPK/UNM).
* `SenseCells[]` (at least two per row), each citing Context name + edition (F.17/E.10 discipline; UTS-wide coverage rules still apply).
* *(REQUIRED when publishing)* `CorrespondenceRef[]` — ISO 42010 correspondences linking published faces to the engineering view(s) they implement; can cross architecture descriptions.
* *Optional relation field* `ConcernsCovered[]` — ISO 42010 stakeholder concerns addressed by this row via GateProfiles/check catalogues.

**Conformance (S12-scoped, only when `ViewpointMap` is current).**
(i) `UTS.ViewpointMap` exists when a viewpoint-family mapping claim is made or consumed.
(ii) For each holon that claims TEVB alignment, there are at least four rows whose `{ViewFamilyId, EngineeringVPId}` cover `{VF.TEVB.ENG × {VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}}` (per CC-TEVB-1/6).
(iii) Rows that carry edition identifiers also include `BridgeCard + UTS` rows through `F.9`, `F.17`, `E.17`, and `E.18`; edition-bearing faces that lack such rows are not admissible for downstream consumption.
(iv) Each row has at least two `SenseCells` and the sheet meets global UTS coverage rules.
(v) Any `TargetHolon = U.System` that reaches `U.Work` shows `LaunchGate` with `DesignRunTag` consistency.
(vi) Crossings referenced in `ViewpointMap` follow CC-E18-11; comparability along the mapped paths follows CC-E18-10.
(vii) Rows do not use an unqualified `ViewpointId`; they use `EngineeringVPId` and/or `PublicationVPId` explicitly.
(viii) When faces are published, `CorrespondenceRef[]` is present and resolvable to `U.Viewpoint` ids.
(ix) Additional bundles (e.g. assurance, information, mission) can appear as extra `ViewFamilyId` values but are declared as `U.ViewpointBundle` species; they do not extend `VF.TEVB.ENG`.

### E.18:6 - Archetypal Grounding (Tell–Show–Show; concise)

*Tell (P2W reference path).* A first-principles-to-work path is one path through the selected transformation-flow structure, not the whole structure itself: `U.Signature(profile=FormalSubstrate)` declaration, principle frame, mechanism, normalization, selection, planning, work enactment, and refresh are represented as loci linked by one `U.Transfer` relation kind, with crossings pinned where context, plane, edition, or design/run state changes.

*Show-A (Supply chain).* Loci: procurement -> inbound QC (UNM) -> selection (supplier set; declared order) <-> planning (lotting/schedule; budget) -> execution (receipts; **WorkEnactment enacts world-contact**) -> refresh (quality telemetry; affected faces re-emitted). Crossings: vendor Context via **Bridge/CL**; penalties appear **in R only**; comparators pinned to CG-Spec edition.

*Show-B (Neural-net functional).* Loci: `U.Signature(profile=FormalSubstrate)` declaration (typed tensor-operation declaration) -> mechanism (combinator algebra) -> UNM (dataset normalization; **TransportRegistry^Phi**) -> selection (architecture/hyperparam set; Pareto set over accuracy@ratio and FLOPs@ratio) <-> planning (compute budget horizon) -> Work (training runs; Delta recorded) -> refresh (parity inserts; slice-scoped). Faces pin **DescriptorMapRef.edition** and **DistanceDefRef.edition** when QD telemetry values are shown; illumination remains **report-only telemetry** by default.

*Show-C (Developed product, then application).* One flow valuation represents development work that produces a specification, pattern, process description, mechanism description, method set, or tool through drafting, checks, projection, build, or publication. A later flow valuation represents use of that product in project work or analysis. A further flow valuation may represent another use of the result: a tool is made, then used to make a chair, then the chair supports a person writing a text. The selected structure can relate all these valuations through transfers and feedback, while each flow keeps its own governed object, `DesignRunTag`, flow-local relation position for the carried object, work occurrence, evidence, and reopened slice.

*Show-D (FPF pattern development and use).* A development-flow valuation represents pattern development work: creation, evaluation, projection, publication, and later repair of a pattern. A use-flow valuation represents application of that pattern to its own `EntityOfConcern`. An evaluation or use-found defect can select the smallest development slice for repair. E.18 keeps the common selected structure visible while separating the developed pattern, the use of the pattern, the evidence found during use, and the edition or slice that is reopened.

**Cross-pattern boundary slice (QD archive).** A QD selector returns an archive. Under `E.18`, this is one `PathSlice` in one `TransformationFlowStructure`; selection returns a set/archive, not a hidden scalar. Under `A.20`, the archive insertion or update step has a current CV class, `CV.Status`, and witness or refusal; no acceptance is inferred. Under `A.21`, a comparability gate or `LaunchGate` can publish a `GateDecision` only when that gate relation is current and consumes the relevant CV result. Under `E.20`, if a new selector mechanism-governing definition is introduced, the mechanism-governing definition is the locus for the meaning while suites and wiring only cite or bind it. These are four governed loci, not one prescribed work order.

> *Post-2015 SoTA echoes (illustrative):* **TAMP and MPC**, **MAP-Elites / QD (incl. CMA-ME)**, **refinement-typed stacks**, **profunctor optics**. Worked examples and Tell-Show-Show vignettes for P2W, comparator/archive, coupled development/application flows, and refresh specializations stay outside this selected-structure core unless a current pattern explicitly selects them.

### E.18:7 - Conformance — **Unified checklist (normative)**

**Conformance use.** This checklist is evidence for the selected-structure, flow-valuation, and crossing action guidance already stated in the Solution. It is not the first entry text for ordinary use and not a full audit regime by default; an item is applied only when its corresponding structure, crossing, publication, gate, refresh, or assurance move is current. Before applying any item, name the Solution move it tests; if no such practitioner move is current, treat the item as auxiliary-only or not applicable rather than expanding the applied assurance or conformance material.

**Conformance groups.** Ordinary E.18 use starts with selected structure, single transfer relation kind, locus typing, `CtxState` preservation, and flow valuation. Crossing/launch items apply only when a GateCrossing, `LaunchGate`, `StructuralReinterpretation`, or work-boundary crossing is current. Publication/assurance items apply only when MVPK faces, edition pins, evidence carriers, decision logs, or replay are current. Extension/change items apply only when locus-kind scope, budget/refresh behavior, or UNM/comparator editions are being changed or consumed downstream.

| ID | Requirement | Practical test |
|----|-------------|----------------|
| **CC-E18-01 — Single transfer relation kind** | The selected structure uses exactly one relation kind `U.Transfer`; all plane/Context/edition transitions occur only at loci via `OperationalGate(profile)`. | Model lint finds no auxiliary relation kinds for unit/plane changes; crossings sit on declared gates. |
| **CC-E18-02 — Locus kinds bind governed values** | Loci are structure-positioned bindings to governed values. The current minimal locus baseline is `{Transformation, Signature, Mechanism, WorkPlanning, Work, Check, StructuralReinterpretation}`. Domain-specific species are open-world and non-exhaustive; they bind to one of these locus kinds or require an explicit E.18 update. The baseline is **not** a local ontology: `Transformation -> A.3.4`, `Signature -> A.6.0`, `Mechanism -> A.6.1/E.20`, `WorkPlanning -> A.15.2`, `Work -> A.15.1`, `Check -> A.20 or A.21`, and `StructuralReinterpretation -> A.6.4 plus E.18/A.20` where CV is current. A morphism expression is a mathematical-lens view when current, not the FPF kind of every locus. | Type registry shows at least the listed locus kinds; additional species map to one of them; checks are realized as `OperationalGate` when a gate/check locus is present (see CC-E18-06-EX/11). **Lint:** registry/table exposes `{species -> {locusKind, governingPattern}}`; missing or mismatched governing pattern fails. |
| **CC-E18‑03 — Identity, composition, functorial faces** | Identities exist; path composition associative; publication is functorial: `Emit_s(t₂∘t₁)=Emit_s(t₂)∘Emit_s(t₁)`. | Pick two‑step path; MVPK faces commute (Square witness). |
| **CC-E18-04 — Structure spec** | Spec declares `tau_L`, `tau_Transfer`, `Gamma_time`, Transport/Bridge registries. | Spec file shows typed registries and Gamma policy. |
| **CC-E18‑05 — CtxState pins** | `CtxState=⟨L,P,E⃗,D⟩` is pinned on ports/tokens; raw `U.Transfer` does **not** write/update it. | Along a raw transfer, ⟨L,P,E⃗,D⟩ is preserved. |
| **CC-E18-06 — Operational gates only** | Any write/update to any member of `CtxState` or entry into `U.WorkEnactment` is mediated by `OperationalGate(profile)` with aggregated `DecisionLog`. | Diff CtxState across transfer relations; if any member differs, exactly one gate exists with DecisionLog. |
| **CC-E18-06-EX (strictly limited) — Projection retargeting without gate** | A locus of kind **`StructuralReinterpretation`** retargets the **published projection** without invoking `OperationalGate` **only if all hold**: **(a)** `CtxState` is preserved; **(b)** any **EntityOfConcernRef** change has a **KindBridge** (`CL^k`) entry on MVPK/**UTS**; **(c)** a **SquareLaw-retargeting witness** is present (on UTS); **(d)** the operation is **PathSlice-local** (`PathSliceId` pinned); **(e)** **no plane/unit change** occurs (plane/unit changes remain gated); **(f)** **CV.ReinterpretationEquivalence** (A.20) is `pass`; **(g)** **NoHiddenScalarization** - if the step concerns a comparable return shape, set/partial-order semantics are preserved and comparators remain ref-only (current comparator and set-return loci). | UTS row includes `bridgeChannel=Kind` and `CL^k`; SquareLaw-retargeting witness present; PathSliceId pinned; CV status recorded; no scalarization detected. |
| **CC-E18‑07 — CV⇒GF activation predicate** | Until **aggregated `ConstraintValidity` = `pass`**, all **GateFit** checks return `abstain`. | Simulate CV failure ⇒ GateFit `abstain`. |
| **CC-E18‑08 — LaunchGate discipline (incl. pre‑run barrier)** | Each `U.WorkEnactment` has exactly one `LaunchGate` assigned as the aggregator for `USM.LaunchGuard`; **mandatory** checks: `FreshnessUpToDate`, `DesignRunTagConsistency`. If preceding step’s CV ≠ `pass`, LaunchGate decision is `block` (cause logged). | Aggregation assignment `GuardOwnerGateId = LaunchGateId(U.WorkEnactment)`; CV≠pass ⇒ `block` with log. |
| **CC-E18-09 — MVPK publication discipline** | Every published locus uses MVPK; faces carry `PublicationScopeId`, presence pins, **edition ids**, Gamma pins; **no I/O duplication** or arithmetic; faces add no new numeric claims. | Cards show `PublicationScopeId`; pins present; no "signature"/math on faces. |
| **CC-E18‑10 — Normalize→Compare (CSLC)** | Any comparison cites **UNM/CG‑Spec** editions and **ComparatorSetRef**; ordinal claims are compare‑only; partial orders return sets; edition‑aware set/archive publication records (QD/archives) pin `{DescriptorMapRef, DistanceDefRef, CharacteristicSpaceRef?}.edition`; **any face citing editions includes `BridgeCard + UTS row`**. **NoHiddenScalarization — detection criteria:** (1) return shape is **set/poset**, not scalar; (2) `ComparatorSetRef` is present and edition‑pinned; (3) MVPK faces add **no new numeric claims**; (4) any summarisation is **order‑preserving & set‑valued**; otherwise conformance fails. | Faces show comparator pins; archive pins present; linter rejects edition cites without UTS; scalarisation checks pass. |
| **CC-E18‑11 — Crossings gated** | Cross-Context or cross-plane crossings publish **BridgeId + UTS + CL/CL^plane** and are mediated by `OperationalGate(profile)`; **Φ/Φ_plane penalties appear in R-lane only**; EntityOfConcernRef change publishes **KindBridge (CL^k)**. **Exception (StructuralReinterpretation):** a **projection‑only** EntityOfConcernRef retargeting is recorded **without** a gate **iff** **CC-E18‑06‑EX** holds; then the UTS row includes `bridgeChannel=Kind`, `CL^k`, and a **retargeting witness**; any plane/unit change falls back to a gated crossing; `PathSliceId` is pinned; UNM reuse cross‑context continues via `Transport`. | The crossing record shows Bridge/UTS/CL pins; penalty placement audited. |
| **CC-E18‑12 — Set‑returning selection** | The selection-and-tuning locus returns sets/archives under declared comparators (`ParetoOnly` by default) through the current selector/comparator governing pattern — no covert scalarization. | Selector output is a set/archive; policy id present if escalated. |
| **CC-E18‑13 — Budgeted Selection↔Planning loop** | The loop declares **budget / max_iter**; on expiry selector publishes partial‑optimal set + `MethodTuning`; next **PathSlice** scheduled. | Logs show budget stop and slice rollover. |
| **CC-E18‑14 — UNM before loop and FreshnessTicket state change** | UNM runs before selection; stale/missing inputs produce **FreshnessTicket/FreshnessRequest** planned in `WorkPlanning` and executed in `WorkEnactment`; calibrations appear as `CalibrateTo(calibrationReference)` with Φ pins. | Ticket state machine Issued→Planned→Executed→Closed; calibrations pinned. |
| **CC-E18‑15 — FinalizeLaunchValues only in WorkEnactment** | Only `U.WorkEnactment` performs `FinalizeLaunchValues` and fills launch‑value slots. | Any earlier attempt blocks at LaunchGate; a `FinalizeLaunchValues` witness is present in Work. |
| **CC-E18‑16 — Guard aggregation assignment & semantics** | `USM.CompareGuard`/`USM.LaunchGuard` publish the gate assigned to aggregate guard failures; guards are **events**, not GateChecks; failures are aggregated by that gate per profile. | Guard pins show the assigned gate; GuardFail recorded in that gate's DecisionLog. |
| **CC-E18‑17 — Assurance ops on Transfer** | On `U.Transfer` only `ConstrainTo/CalibrateTo/CiteEvidence/AttributeTo`; none write/update `⟨L,P,E⃗,D⟩`. | Edge audit shows ops; CtxState unchanged across the edge. |
| **CC-E18-17a — Assurance operation specifications (normative)** | **ConstrainTo(region/policy)**: tightens declared region/policy; **pre**: region subset current; **post**: `CtxState` unchanged; **idem.** and **monotone** under composition. **CalibrateTo(calibrationReference)**: attaches an **editioned** calibration reference, such as a map or standard, with Phi-policy id; admissible per cited `CG-Spec`; **post**: `CtxState` unchanged; **idem.** on same edition; penalties appear **in R only**. **CiteEvidence(evidenceRef)**: binds evidence references via **SCR/RSCR**; adds no numeric claims; **idem.**; missing carriers => **abstain**. **AttributeTo(provenanceReference)**: provenance only; decision algebra unaffected; **idem.** Hidden GateChecks, plane/unit changes, or edition writes on transfer relations are **forbidden**. | Operation specifications visible on transfer-relation audit; violations fail lint. |
| **CC-E18-18 — Flow = valuation, coupled-flow unity/separation, and slice-local refresh** | Each flow declares valuation `nu` over `U.Transfer` plus `PublicationScopeId` and `PathSliceId`; when several flows are coupled in one selected structure, development, application, evaluation, refresh, and repair flow valuations are related by transfer, feedback, return, or edition-change relations while keeping separate governed objects, records, evidence, gates, work occurrences, flow-local relation positions for carried objects, and `DesignRunTag` boundaries; refresh is bounded to the addressed slice; affected faces are re-emitted on edition change or selected refresh rule. | Flow publication shows `nu`; a coupled-flow case names which flow is being valued, which flow-local relation position the carried object fills, and which slice is reopened; refresh trigger causes slice-local recompute. |
| **CC-E18‑19 — Γ_time on compare/launch** | All compare/launch faces pin `Γ_time`; no implicit *latest*. | Face audit shows Γ pins; LaunchGate blocks on stale. |
| **CC-E18‑19a — Γ_time pin shape (normative)** | The `Γ_time` pin is one of: `snapshot(t)`, `interval[t1,t2]` (closed), or `policy(Γ_timeRuleId)` that resolves to either; CV computations record the **resolved time reference** in `DecisionLog` and do not widen Γ at publication time. | DecisionLog shows the resolved reference; linter rejects missing/implicit Γ. |
| **CC-E18‑20 — Lean publish‑mode ≠ weaken** | `AssuranceLane‑Lite` changes publication faces only; required GateChecks for the active profile remain intact. | Gate in Lean/Core shows minimal pins; GateChecks list unchanged. |
| **CC-E18-21 — Decision stability & idempotency witness** | Gate decisions are stable under the equivalence relation recorded by `A.21`; a **witness of equivalence** is present on the DecisionLog record; any change that breaks equivalence triggers re-aggregation. **Minimum lexeme (CV-relevant witness):** `EquivalenceWitness := { keys, E⃗, Γ_time(reference), PathSliceId?, ReturnShapeClass, ComparatorSetRef?, profile }`. | Modify any input outside the declared equivalence => re-aggregation; DecisionLog records the witness; lexeme present. |
| **CC-E18‑21a — Decision join (publication algebra)** | Aggregation over GateChecks is the **idempotent, commutative, associative join** on the lattice `abstain ≤ pass ≤ degrade ≤ block` with **neutral = `abstain`** and **absorbing = `block`**. The algebra is conceptual; publications carry only (i) the aggregated **GateDecision** and (ii) its **GateDecisionRationale** recorded in the **DecisionLog**. A **GateDecisionExplanation** is an optional human‑readable narrative derived from the GateDecisionRationale; it is **not** a decision and is not used as one. If aggregated `ConstraintValidity ≠ pass` or the active profile suppresses narratives, any GateFit‑oriented GateDecisionExplanation **does not apply**. | Review a gate with multiple GateChecks: the aggregated decision matches the lattice join; no per‑check arithmetic is introduced on faces. |
| **CC-E18‑22 — Errors/unknowns fold by profile** | Errors/timeouts fold to `degrade` under `Lean/Core` and to `block` under `SafetyCritical/RegulatedX`; `unknown` folds per GateCheck policy (safety‑default: `degrade`). | DecisionLog shows folds; profile switch changes fold behavior accordingly. |
| **CC-E18‑23 — SquareLaw on crossings** | For every GateCrossing, `gate_out ∘ transfer = transfer' ∘ gate_in`; LaunchGate case is mandatory. | MVPK shows commuting square; inconsistency yields `block/degrade` per profile. |
| **CC-E18‑24 — UNM declaration locus** | `CG‑Spec`, `ComparatorSet`, `UNM.TransportRegistryΦ` editions are declared only through the UNM governing locus (others ref‑only). | Declaration records show UNM as the governing locus; others have refs only. |
| **CC-E18‑25 — Evidence lanes & DecisionLogs** | AssuranceLane carries GateProfile, GateCheckRef list, edition pins, aggregated decision, `DecisionLogRef`; **evidence pins follow a two-part scheme**: **carriers** are pinned via **`SCR/RSCR`**, and **value annotations** are carried under **`VALATA (VA/LA/TA)`**. | Gate publication faces include these pins; logs retrievable. |
> **Coupling note.** `CC-E18‑07 (CV⇒GF)` and `CC-E18‑21a (Decision join)` together ensure that any GateFit‑scoped GateCheckRef **returns `abstain`** until the aggregated CV status equals `pass`; CV/GF separation remains intact.
> **Scope note (E.18 vs neighbor patterns):** Detailed mechanism-scoped checks and publication obligations are governed by the current neighbor patterns named in this pattern's Relations. E.18 fixes only selected-structure obligations: single `U.Transfer` relation kind, gate crossings, valuation, publication pins, CV/GF boundary, and slice-local refresh.

**Glossary (additions)**
* *Open-world species* - non-exhaustive domain-scoped locus specializations that map to the minimal locus baseline and name a governing pattern.
* *Signature locus* - structure-positioned use of **A.6.0** `U.Signature` (universal block). It is a governed value bound into the selected structure, not a local kind and not a `C.3.2 KindSignature`.
* *KindSignature (C.3.2)* - definition of a `U.Kind` by intent, extent, and formality; **unrelated** to E.18 locus kinds; never a `genus`.
* *Species (domain-scoped)* — typed specialisations `speciesOf(kind=...)` that declare `KindDefinition=<current governing pattern id>` (e.g., `kind=Mechanism; KindDefinition=A.6.1`).
* *KindBridge (`CL^k`)* — a compatibility note on UTS for EntityOfConcernRef/kind transitions; required by CC-E18‑06‑EX and crossings (CC-E18‑11).
* *Eulerian interpretation* - operational stance where a flow is treated as a valuation over `U.Transfer` and transfer relations perform assurance-only operations (no token-passing semantics).
* **GateCheckKind boundary.** `GateCheckKind` is a publication/check lexeme used inside `GateCheckRef`, not a structure locus kind. No `GateCheckKind` becomes an E.18 `Check` locus unless an `OperationalGate(profile)` locus is actually present.

* **GateCheckRef shape (publication lexeme governed by A.21).** Where publication faces over a selected structure carry GateChecks, a **GateCheckRef** is a record
  defined by `A.21`; E.18 constrains only where such faces carry those refs along transformation-flow paths.

`GateCheckRef := { aspect, kind, edition, scope }` with:
  `aspect ∈ {ConstraintValidity, GateFit}`, `kind ∈ GateCheckKind`, `edition ∈ Editions`, and `scope ∈ {lane | locus | subflow | profile}`.
* **GateDecision / GateDecisionRationale / GateDecisionExplanation (terminology).**
  — **GateDecision** — the aggregated lattice value produced by `OperationalGate(profile)` for a specific `{GateProfile, GateCheckRef[]}`.
  — **GateDecisionRationale** — the minimal structured rationale **for that GateDecision**: per‑check outcomes, profile‑bound folds, and published evidence or witness references on the DecisionLog; it records **why the GateDecision is admissible** under the active profile.
  — **GateDecisionExplanation** — an optional human‑readable narrative derived from the GateDecisionRationale; it **does not carry decision status**. While aggregated `ConstraintValidity ≠ pass`, GateFit‑scoped checks return `abstain`; any GateFit‑oriented GateDecisionExplanation **does not apply**.
> **Clarity note.** **GateDecision ≠ GateDecisionExplanation**; narratives are optional and derivative of GateDecisionRationale.

* **GateFit (aspect, not an entity).** GateFit names the **aspect** of checks that evaluate **profile‑fit**; there is no separate GateFit entity. “Gate decision under GateFit” means “the gate’s decision computed from GateChecks with `aspect=GateFit`”.

  This shape is publication-only; it introduces no new execution steps and no arithmetic on faces.  (Couples to A.20 or A.21 without duplicating their check catalogs.)
* *VALATA (VA/LA/TA)* — value-annotation scheme used on **AssuranceLane**; **carriers** are referenced via **SCR/RSCR**; detailed evidence obligations are governed by `A.10` and the named evidence, publication, or crossing pattern for the current case. Included here so evidence pins are self-describing in Part E texts.
* *Transfer vs Transport* - **Transfer** = the sole relation kind `U.Transfer` in the selected structure. **Transport** = Phi-policy/registry-defined conversions (`TransportRegistry^Phi`) referenced by UNM; "reuse via Transport" refers to the latter.
* *GateCrossing* - a typed locus transition that writes/updates a CtxState slot or the kind-channel; see **S1.b** for the normative list and required pins.
* *Admissible path* - a typed path obeying the GateCrossing discipline (no hidden crossings; witnesses present), Gamma-pinned on compare/launch, and `T^D<->T^R` only at `LaunchGate`; see **S2**.

### E.18:8 - Gating Profiles (applied to E.18)
This table is a selected-structure coverage table for E.18 crossings and path slices. It is not the source of `GateProfile` semantics. `A.21` governs gate decision semantics, folds, `DecisionLog` minima, and the GateFit check-catalog boundary.

> Gating is expressed as **publication-gating** per E.17 profiles. The structure model aligns with the **CC items** listed for the chosen profile; broader obligation profiles include all narrower-profile items.

| Profile                          | Required CC‑items                                         | Additional notes                                                                               |
| -------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Lean**                         | 01–06, 08–09, 11–12, 15, 19–21, 25                                                                                                           | Minimal MVPK presence; LaunchGate keeps `FreshnessUpToDate` & `DesignRunTagConsistency`. |
| **Core**                         | **Lean** + 07, 10, 13–14, 16–18, 22–23, 24                                                                                                  | Adds CV⇒GF order, CSLC pins, budgeted loop, guards, valuation/sentinel refresh, error folds, SquareLaw, and the UNM declaration locus. |
| **Safety‑Critical / RegulatedX** | **Core** + profile‑specific GateChecks (safety envelope, regulator id/editions) with stricter folds per **CC-E18‑22**; SquareLaw audits tightened | — |

**Recommended defaults (non-normative, tie-in to `A.21` and `G.11`).** Profiles inherit along a `PathSlice`; local overrides only **add** GateChecks; weakening uses a new `PathSlice` and refresh wiring through the current `G.11` locus when refresh wiring is current.

### E.18:9 - E.18 LEX Discipline (registration)
Register Tech tokens (ASCII) used by this pattern with twin-labels: `TransformationFlowStructure`, `TransformationFlowValuation`, `StructuralReinterpretation`, `OperationalGate`, `GateProfile`, `GateCheckRef`, **`GateCheckKind`**, `DecisionLog`, `USM.CompareGuard`, `USM.LaunchGuard`, `KindBridge`, `SubflowRef`, `FlowEmbed`, `SentinelId`, `PathSliceId`, `SliceRefresh`, `FinalizeLaunchValues`, `VALATA`. Add an ASCII alias **`CLKind`** <-> Plain `CL^k` (cf. `CLPlane` <-> `CL^plane`). Reference MVPK E.17 naming for faces.
**CtxState Extension Registry.** Register any extra CtxState slot beyond ⟨L,P,E⃗,D⟩ with: slot id, informal intent, partial‑order law (with neutral/absorbing), SquareLaw compatibility note, and the owning Gate profile(s) that may change it. Absence of registration ⇒ **non‑conformant**.

### E.18:10 - Consequences

**Benefits.**

1. **Universality with discipline:** one transfer relation kind and explicit gates eliminate second hidden work and method orders and make cross-domain flows (ML, supply-chain, TAMP and MPC, scientific work structures) uniformly analyzable and auditable.
2. **Comparability & replayability:** CSLC and edition‑pinned comparators prevent covert scalarization and enable declared set returns and reproducible decisions.
3. **Locality of change:** sentinel subflows restrict refresh to affected `PathSlice`s; large selected structures remain stable under frequent edition bumps.
4. **Clean DesignRunTag fold:** LaunchGate and `DesignRunTagConsistency` stop premature launch-value slot filling; acceptance and telemetry belong where they occur (`U.Work`).
5. **Assurance visibility:** MVPK makes GateProfile/DecisionLog records locally checkable and cacheable for the same `{PathSlice, GateChecks, Editions}`.

**Trade‑offs.**
a) **Higher upfront modeling cost:** explicit Bridge/UTS pins and GateProfiles demand care; mitigated by Lean profile and templates.
b) **Longer transfer face sets:** MVPK faces are verbose by design; lean face sets can be used for low-risk segments.
c) **Tooling alignment:** some incumbent DAG-only orchestrators conflict with budgeted cycles and set-return semantics; adapters project E.18 semantics to their interop boundary, while `E.18.2` carries the mathematical graph-description relation when that projection matters.

### E.18:11 - Rationale

E.18 states **strict separation of concerns** (selected-structure scope only); **specialized semantics are governed by the patterns named below for those current relations**:

* **What the selected structure is:** structure-positioned transformation and slot-filler loci plus the single relation kind `U.Transfer`; graph, morphism, tuple, category, or algebra language is used only when a current mathematical description or lens expresses the relation.
* **Where/when it crosses contexts:** **only** at `OperationalGate(profile)`, with Bridge+UTS, CL/CL^plane, and Φ published in R-lane.
* **How comparability works:** UNM is the single governing locus for unit, plane, and transport declarations, and selectors operate **only** on normalized, edition-pinned comparators, returning sets or archives rather than totals. Edition-aware pins and archive semantics are checked through `A.19.SelectorMechanism`, `C.18`, `C.19`, `G.5`, `G.9`, and `G.11` for current selector or archive cases.
* **How change propagates:** sentinel‑bounded `PathSlice` refresh; editions are monotone; LaunchGate is the only binder of launch‑values.

This arrangement gives checkable conditions for **functorial publication** (commuting squares on crossings) and **orthogonality** of inner technical validity (ConstraintValidity) to context fit (GateFit), which in turn keeps gate aggregation **order-independent** under the CV=>GF activation predicate.

### E.18:12 - SoTA‑Echoing (post‑2015, multi‑Tradition)

> Each row states the source idea, the FPF invariant E.18 adopts, the practitioner move it changes, and the shortcut it rejects. Vendor, tool, and literature tokens are informative; the invariant and practitioner move carry the pattern explanatory work.

| SoTA source idea | FPF invariant | Practitioner move | Rejected shortcut |
|---|---|---|---|
| **Applied category theory / compositional open systems** (Fong & Spivak, *Seven Sketches in Compositionality*, Cambridge University Press 2019; arXiv [`1803.05316`](https://arxiv.org/abs/1803.05316) source draft). | Use one `TransformationFlowStructure` whose loci are structure-positioned transformation and slot-filler values and whose links use the single relation kind `U.Transfer`; morphism language expresses composition only when the mathematical lens is current. | Name the selected structure, locus kinds, one `U.Transfer`, and any current path or crossing before treating a work or method sequence as structure semantics. | Treating category-theory prestige, tool pipelines, lineage packages, or work and method narratives as structure semantics. |
| **Operads, wiring diagrams, and hypergraph categories** (Spivak, *The operad of wiring diagrams*, arXiv [`1305.0297`](https://arxiv.org/abs/1305.0297); Baez & Fong, *A Compositional Framework for Passive Linear Networks*, arXiv [`1504.05625`](https://arxiv.org/abs/1504.05625)). | Typed ports and interface junctions motivate Bridge/CL/Phi pins at crossings; E.18 adapts the math by requiring publication pins that the math alone does not supply. | When an interface or boundary crossing matters, publish the Bridge, UTS row, CL/CL^plane, and R-lane penalty placement instead of leaving an unpinned junction. | Treating an interface diagram, wiring diagram, or decorated cospan as sufficient crossing evidence. |
| **Open-graph and string-diagram rewriting** (Bonchi, Gadducci, Kissinger, Sobocinski, Zanasi, *Rewriting modulo symmetric monoidal structure*, arXiv [`1602.06771`](https://arxiv.org/abs/1602.06771); Patterson, Spivak, Vagner, *Wiring diagrams as normal forms for computing in symmetric monoidal categories*, arXiv [`2101.12046`](https://arxiv.org/abs/2101.12046)). | Rewrites and subflow refactors are admissible only with edition bumps, sentinel scopes, and `PathSlice` locality sufficient for replay. | Localize the rewrite to the affected subflow or slice, pin editions, and re-emit affected faces. | Treating a global rewrite as replay-safe because the diagram still looks equivalent. |
| **Research-package portability / RO-Crate-style research packaging** (Soiland-Reyes et al., *Packaging research artefacts with RO-Crate*, arXiv [`2108.06503`](https://arxiv.org/abs/2108.06503); RO-Crate 1.2 as format lineage). | Portable package descriptions belong in MVPK faces and InteropCards; packages and lineage metadata do not define selected-structure semantics. | Publish package, provenance, and source refs as publication references while keeping structure meaning in the locus/gate definitions. | Treating a crate, package, file bundle, or lineage record as the semantic authority for the selected structure. |
| **Reproducibility and content addressability** (Di Cosmo, Gruenpeter, Zacchiroli, *Referencing Source Code Artifacts: a Separate Concern in Software Citation*, arXiv [`2001.08647`](https://arxiv.org/abs/2001.08647)). | Stable identifiers become edition pins and entries in `E⃗`; they make references checkable but do not decide locus, gate, or mechanism meaning. | Pin the exact editions of code, comparator, transport registry, descriptor map, or distance definition used by a face or path. | Treating an identifier, hash, or content-addressed source ref as semantic authority. |
| **TAMP and dynamic-planning/control practice** (Zhao et al., *A Survey of Optimization-based Task and Motion Planning*, arXiv [`2404.02817`](https://arxiv.org/abs/2404.02817); Shen et al., *Motion Planning in Dynamic Environments*, arXiv [`2606.02677`](https://arxiv.org/abs/2606.02677), as current dynamic-motion survey context). | Iteration is represented only as a budgeted Selection-Planning loop with freshness checks and launch values bound in dated `U.Work`. | Declare the loop budget, freshness/request boundary, next `PathSlice`, and Work-only launch-value filling. | Turning E.18 into an ordered work-method narrative, an unbounded loop, or pre-Work launch-value filling. |
| **Quality-Diversity / illumination search** (Mouret & Clune, *Illuminating search spaces by mapping elites*, arXiv [`1504.04909`](https://arxiv.org/abs/1504.04909), lineage; Chalumeau et al., *QDax*, arXiv [`2308.03665`](https://arxiv.org/abs/2308.03665); Ding et al., *QDHF*, arXiv [`2310.12103`](https://arxiv.org/abs/2310.12103); Bradley et al., *QDAIF*, arXiv [`2310.13032`](https://arxiv.org/abs/2310.13032) for feedback-guided cases). | Set and archive returns stay visible; E.18 treats covert scalarization to one winner as non-conformant while leaving selector, archive, dominance, and comparator semantics to neighboring loci. | Return the set/archive, pin comparator and descriptor/distance editions, and cite the selector/comparator loci for current cases. | Collapsing a partially ordered or archive-like result into a single best score. |
| **Profunctor optics / modular projection practice** (Pickering, Gibbons, Wu, *Profunctor Optics: Modular Data Accessors*, arXiv [`1703.10857`](https://arxiv.org/abs/1703.10857); Clarke et al., *Profunctor Optics, a Categorical Update*, arXiv [`2001.07488`](https://arxiv.org/abs/2001.07488), as later refinement). | MVPK faces are projections of selected-structure or mathematical-lens information; they carry views without adding new numeric or mechanism claims. | Publish views as MVPK faces with correspondence refs and pins, while leaving transformations and checks in their governing patterns. | Treating a view, projection, screen, or explanation as a transformation, evidence result, or gate decision. |

*Cross-tradition note.* Rows 1-3 (compositional graph practice), rows 4-5 (publication and reproducibility practice), row 6 (controls/robotics), row 7 (evolutionary search), and row 8 (PL/semantics) jointly position E.18 across multiple traditions per E.8, but each row is retained only because it changes a practitioner move or rejected overread.

### E.18:13 - Bias‑Annotation (per E.8 SG‑bias slot)

* **Acyclic-bias risk.** Tooling accustomed to DAGs may discourage admissible feedback loops; E.18 explicitly permits loops with budget/sentinel controls (CC-E18-13, -18).
* **Scalarization-bias risk.** Cultural defaults to single-score rankings can suppress Pareto/QD sets; E.18 keeps declared order relations and return sets visible (CC-E18-10, CC-E18-12).
* **Interop-dominance risk.** File/format ecosystems (CWL/RO-Crate/lineage) can be mistaken for semantic sources; E.18 places them in **InteropCard** and keeps governing semantics in loci/gates.
* **Over-formalization risk.** Category-theoretic formalisms can obscure operational guard-rails; E.18 grounds crossings in Bridge/UTS/CL/Phi pins and SquareLaw audits (CC-E18-11, -17).
* **Retrospective rewrite risk.** Global rewrites break replay; E.18 confines them to edition bumps and slice-local refresh (CC-E18-16).

**Mitigations.** Profile‑gated publication, audit of `DecisionLog`, mandatory edition pins, Lean‑to‑Core upgrade paths, and conformance tests tied to PathSlice replay.

### E.18:14 - Relations (explicit pattern-to-pattern relations)

> Relation rows are typed as **builds_on / constrains / coordinates / specializes / publishes_on / requires / provides_checks_for**.

**Foundations**
* **E.18 -> builds_on -> E.17 MVPK (for publications of selected structure material).** Faces, pins, lanes, functorial publication, Lean/Core/Regulated profiles.
* **E.18 -> builds_on -> A.6.0 U.Signature / A.6.1 U.Mechanism.** Locus kinds and governing-definition content boundaries.
* **E.18 -> builds_on -> A.7 Strict Distinction (EntityOfConcern, Description episteme, Description episteme admitted for specification use, and publication/carrier separation).** No new claims on faces; publication faces project selected structure, crossing, or flow-valuation information without becoming the governed selected structure, Description episteme, specification use, evidence, gate decision, work occurrence, or carrier.

**Flow semantics & checks**
* **E.18 -> coordinates -> A.20 U.Flow (ConstraintValidity scope).** CV checks apply inside transformations; no declaration/translation of planes/units in CV; **error/timeout/unknown folds** follow **CC-E18-22** as the **minimum default** (profiles can be stricter).
  **Terminology discipline (A.20 boundary).** In CV scope, publications use **status/witness** language; **GateDecisionRationale/GateDecisionExplanation** are reserved for gating and do not apply to CV.
* **E.18 -> coordinates -> A.21 GateProfilization (GateFit scope).** **GateFit-scoped GateChecks** are aggregated by `OperationalGate(profile)` with CV=>GF activation; the **enumeration and publication shape** of GateChecks are governed by **A.21**. **Equivalently:** a GateFit decision different from `abstain` appears only when aggregated `ConstraintValidity = pass`; otherwise the **GateDecisionExplanation (GateFit-oriented)** does not apply.
* **E.18 -> uses -> USM.CompareGuard and USM.LaunchGuard.** Guards publish scope and responsible gate; guard failures are handled by the declared gate.
* **E.18 -> constrains -> F.9/F.17 bridge and terminology-synchronization loci (Bridge+UTS, CL/CL^plane, Phi -> R).** A transition is treated as a **Crossing** iff `Bridge+UTS` and the appropriate `CL/CL^plane` are published; otherwise this crossing explanation does not apply. Where Phi defines penalties, they appear in the R-lane only.
* **Operational interpretation (default): Eulerian.** A flow is a **valuation** over `U.Transfer`; transfer relations carry **assurance-only operations** (see CC-E18-17); no token-passing semantics are assumed.

**UNM & comparability**
* **E.18 -> constrains -> UNM declaration and use loci.** `CG-Spec`, `ComparatorSet`, and `UNM.TransportRegistryPhi` declarations are governed by UNM; normalize-then-compare is mandatory.
* **E.18 -> constrains -> G.5 SelectionAndTuning.** Set-returning, comparator-pinned decisions, no hidden scalarization; `MethodTuning` without launch-value slot filling.
* **E.18 -> constrains -> G.11 EvaluatingAndRefreshing.** EditionBumpProposal, two-phase update through the UNM declaration locus, path-local refresh.

**Work boundary**
* **E.18 -> coordinates with -> A.15 U.WorkEnactment (`FinalizeLaunchValuesOnlyInWork`).** Single point of `FinalizeLaunchValues`; `FreshnessUpToDate` hard at LaunchGate; acceptance/telemetry published here.

**Structure & reuse**
* **E.18 -> provides selected-structure base for transformation-flow families.** Flow patterns such as P2W and EvaluatingAndRefreshing use E.18 for selected structure, valuation, crossings, guards, MVPK faces, and slice-local refresh. The current ontology is: `A.3.4` governs each bounded `U.Transformation`, E.18 governs the selected compound structure over transformations and adjacent governed loci, and neighbor patterns govern method, work, mechanism, evidence, publication, gate, decision, and refresh claims when those claims are current.
* **E.18 -> coordinates with -> architecture transformation-flow relation patterns.** When a selected transformation-flow structure is used in an architecture-flow relation, the architecture transformation-flow relation pattern records the relation between `TransformationFlowStructure` and `ArchitectureOf@Context`; E.18 keeps selected structure, crossing, and flow-valuation discipline.
* **E.18 -> publishes_on -> E.17 MVPK views** (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`) for every transfer/locus where publication occurs; Lean mode applies only as per profile.

### E.18:15 - Conformance Use Checks

1. **Model lint:** run static checks for CC-E18-01...25 (transfer relation kind, gates on crossings, CV=>GF, guard aggregation assignment, UNM declaration locus, SquareLaw).
2. **Publication audit:** sample a commuting square and a sentinel‑bounded subflow; verify pins and DecisionLog behavior on *block/degrade*.
3. **Replay test:** hold editions fixed; re‑run selection on a PathSlice; observe identical return‑sets; apply a bump; see only affected `PathSlice`s refresh.
4. **StructuralReinterpretation probe:** construct a minimal reinterpretation step; confirm `CL^k` with `bridgeChannel=Kind` on UTS, a SquareLaw‑retargeting witness on UTS, `PathSliceId` pinned, **CV.ReinterpretationEquivalence=pass**, and absence of hidden scalarization.

[20]: https://webstore.ansi.org/preview-pages/ISO/preview_ISO%2B23247-1-2021.pdf?srsltid=AfmBOooAUXpg38IpkTlUFtcCpaMVOjivkewJWDIUd1VemIJO91abNEkG "INTERNATIONAL STANDARD ISO 23247-1"

Relation boundary: `E.18` governs selected transformation-flow structures for structures of atomic `U.Transformation` values and their structure-positioned slot-filler loci. It does not define a second change ontology, a work sequence, a method, a mechanism, a mathematical graph expression, or a publication record. When a selected-structure use raises bounded-transformation, dynamics-episteme, temporal-aspect, temporal-claim adequacy, work planning, performed work, evidence, assurance, gate, decision, architecture, structural-view, mechanism, selector, comparison, refresh, publication, or wording-use claims, name the governing pattern for that relation before relying on the structure.

When a selected structure locus, selected path, path slice, substructure, or flow valuation expresses, decomposes, or constrains one bounded transformation relation, use `A.3.4` for the atomic `U.Transformation` claim and use `E.18` for the selected structure, containing locus, pins, locus kind, crossing, publication, comparability, and refresh discipline. E.18 locus kinds do not automatically fill neighboring slots: `Transformation` points to `A.3.4`, `Signature` points to `A.6.0`, `Mechanism` points to `A.6.1` and `E.20`, `WorkPlanning` and `Work` point to the A.15 work family, and `Check` points to `A.20` or `A.21` according to the current claim.

### E.18:15a - E.18.1 P2W Child-Pattern Relation

`E.18.1` is a child pattern for principles-to-work carry-through. It inherits this pattern's selected structure, path, flow-valuation, transfer, crossing, and gate minimum, then adds the local P2W relation from accepted problem-side output to the next FPF kind named by value, relation, record, or application. Pilot examples for one specialization belong in the selected child pattern that uses them; `E.18` keeps only the selected-structure law and this short child-pattern relation.

### E.18:End
