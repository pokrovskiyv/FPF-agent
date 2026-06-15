## A.15.4 - Work-Relevant Source Restoration

> **Type:** Architectural (A)
> **Status:** Stable
> **Normativity:** Normative unless marked informative

**At a glance.** Use `A.15.4` when an encountered source candidate is about to guide work or reliance before the claim-carrying source has been recovered. The source candidate may be a dashboard tile, credential view, copied approval, generated explanation, provenance mark, schema wording, API wording, publication face, or composed source chain.

**Use this when.** Use this pattern when the acting user is ready to proceed because something looks approved, current, safe, evidenced, delegated, released, or ready, but the work claim or reliance claim still needs its governing project source named by value.

**First output.** One compact source-restoration note:

```text
SourceRestorationNote:
  EncounteredSourceCandidate:
  WorkOrRelianceClaimUnderRepair:
  ClaimOrEffectNeeded:
  GoverningSourceNeeded:
  RelationGovernedMoveNow:
  BlockedOverread:
  StopOrReopenCondition:
```

**First move in practice.** Name what the encountered source candidate may safely do now: orient the user, help find a source, allow a bounded reversible probe under `U.WorkPlan`, proceed inside a recovered relation, or block only the unsupported work or reliance claim.

**What goes wrong if missed.** A dashboard, credential view, copied approval, generated explanation, provenance mark, schema wording, API wording, publication, display, or cue starts acting as the work or reliance source relation. Work then proceeds or stops while the gate decision, evidence path, speech act, commitment, role assignment, status record, work occurrence, source episteme, or source publication that would carry the claim is missing, stale, revoked, or contradicted.

**Primary EntityOfConcern in plain terms.** One source-restoration relation for one work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair. The relation connects the encountered source candidate, the needed claim or effect, the source that must carry that claim, the next relation-governed move, and the blocked overread.

**First restoration checks.**
1. Name the encountered source-candidate kind and publication position without treating its appearance as the source relation itself.
2. Name the work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair.
3. Name the claim or effect that would be carried: gate passage, release reliance, evidence relation, assurance claim, speech act, commitment, role relation, status currentness, work occurrence, source currentness, boundary claim, or another claim named by value.
4. Recover the source that must carry that claim: the governing FPF pattern plus the reference named by value.
5. Choose the lightest relation-governed disposition now: proceed inside the recovered relation, narrow the move, run a bounded reversible probe under `U.WorkPlan`, reopen or refresh the source, ask the accountable role assignment to expose or repair it, or block only the unsupported claim or effect.

**Not this pattern when.** Stay in A.15 when the question under repair is only `U.Role`, `U.Method`, `U.MethodDescription`, `U.WorkPlan`, and `U.Work` separation. Stay in E.17 when the question under repair is only publication-face exposure or multi-view publication. Stay in A.10, B.3, A.20, A.21, A.2.8, A.2.9, A.6, or A.15.1 when evidence, currentness, engineering justification, gate-passage claim, `ConstraintValidity` status, commitment, speech act, boundary claim, or work occurrence already governs the claim or effect directly.

**What this buys.** The acting engineer-manager can keep work moving without trusting appearances: use the source candidate for orientation or source-finding when that is all it can carry, proceed only inside the recovered relation when that relation exists, and turn repeated ambiguity into source-system repair work rather than repeated manual reconstruction.

### A.15.4:1 - Problem Frame

Dashboards, credential views, generated explanations, copied approvals, provenance labels, green tiles, schema wording, API wording, and composed source chains often look ready for action before the source that carries the claim is visible. The practical problem is to decide what an engineer-manager may do now without turning appearance into approval, gate passage, evidence, assurance, performed work, role currentness, status currentness, or release permission.

**Plain recognition line.** Let the visible cue point to a relation named by value, source episteme, source publication, evidence path, gate decision, role record, status record, work occurrence, or assurance claim. Do not let the cue become the relation that permits work or reliance.

**Source wording discipline.** In this pattern, `source` is not a generic kind. `Governing source` means the project-side value, named by FPF kind and reference, that carries the claim or effect under repair: source `U.Episteme`, source `U.EpistemePublication`, evidence path, gate decision, speech act, commitment, credential record, status record, role assignment, work-occurrence record, register entry, source relation, or another named project-side value. Source-finding cues, publication faces, publication carriers, renderings, dashboards, copied wording, and generated explanations remain source candidates unless they expose that governing source. If no governing source can be named, keep the encountered source candidate at cue-only orientation or source-finding use.

### A.15.4:2 - Cluster Boundary

A.15 remains the kernel for separating `U.Role`, holder and context, `U.Method`, `U.MethodDescription`, `U.WorkPlan`, and dated `U.Work`. A.15.4 starts only when an encountered source candidate begins to justify a work claim or reliance claim and the team must recover the source that carries that claim, effect, or relation. If the governing pattern and project-side reference are already known, use them directly and keep A.15.4 as the bounded restoration step.

### A.15.4:3 - Work-Relevant Source Restoration

##### Core stress-case rule

**Ordinary source-restoration note.** In ordinary use, do not build a source dossier. The first useful note is:

`encounteredSourceCandidate; work or reliance claim under repair; claim or effect needed; governing source needed; relation-governed move now; blocked overread; stop or reopen condition`

The encountered source candidate may be a tile, credential view, approval-looking memo, generated explanation, copied review, provenance mark, API wording, functional-description publication, or composed source chain. The pattern asks whether the requested claim is currently carried by a project-side source named by value, not whether the source candidate is impressive, fluent, easy to inspect, or visually salient.

**Conditional source-relation field set.** Use the fuller fields below only when release, safety, compliance, role, status, gate, assurance, contested source, external reliance, cross-context reuse, currentness, revocation, generated source relation, or copied source relation is being relied on for the claim under repair. These fields are local restoration aids, not a new record kind.

| Field | Working question |
| --- | --- |
| subject or actor | Who or what would perform the work, rely on the source candidate, hold the status, or be affected by the claim? |
| role | Which `U.RoleAssignment` or role-context claim is being made? |
| guided action or work target | Which selected method, method of work, `U.WorkPlan`, planned work, dated `U.Work`, work result, release move, reliance move, source status, or effect is being guided? |
| affected resource or claim | Which resource, claim, gate, credential, status, evidence, approval, or source finding with authority-reference relation is supposedly affected? |
| context | Which bounded context, environment, project slice, interface setting, protocol setting, or relying situation makes the claim applicable? |
| policy or gate version | Which policy, gate profile, constraint version, method version, or register edition is supposed to govern the claim? |
| time window | During which window is the claim, effect, source relation, or recovered-use boundary claimed to hold? |
| currentness or revocation field | Is the source relation current, stale, revoked, superseded, expired, contradicted, or unknown? |
| issuer or source | Which issuer, governing source, register source, source-status record, speech act, gate decision, evidence path, or work-occurrence record carries the claim, effect, source relation, or recovered-use boundary? |
| verifier or relying context | Who is checking or relying on the claim, and in which context? |
| evidence or attestation path | Which `A.10` evidence, provenance, or attestation path, if any, justifies the claim without itself becoming approval, gate passage, assurance, or work occurrence? |
| sourceRelationClass | Which `E.17:5.1b` source-relation class or claim-use class applies to the encountered source candidate and required claim or use? |
| unsupported effect | Which requested work claim, reliance claim, or downstream effect remains unsupported and must be narrowed, repaired, reopened, probed, or blocked? |

Start with the A.15.4 first restoration checks above when the encountered source candidate is about to guide a work move, reliance move, or work-relevant claim. If the issue under repair is only evidence, currentness, gate-passage claim, `ConstraintValidity` status, engineering justification, commitment, speech act, boundary wording, use-boundary wording, credential proof, source-status proof, explanation, comparison, or publication-carrier or front-end behavior, use the pattern governing that issue directly. Use A.15.4 only when the source must be restored before role, method, plan, work, work result, result measurement, or another work move or reliance move can proceed.

**Authority-looking source-backed work or reliance case.** Use A.15.4 when an approval-, permission-, gate-, command-, credential-, delegation-, revocation-, status-, provenance-, dashboard-, copied-review-, generated-explanation-, schema-, API-, or composed-chain case is about to be used as a work cue, reliance claim source, release-reliance claim source, performed-work evidence source, approval-claim source, approval-effect source, role-claim source, status-claim source, or next work-relevant move. The recognition moment is that an encountered publication, display, credential view, wording, or explanation looks like permission, prohibition, readiness, or evidence for starting work. The repair question remains: which work or reliance claim is being made, and which source must carry it?

Here "authority-looking case" is only a recognition phrase for the encountered situation. The governing source that permits, forbids, records, or carries the work-relevant claim may instead be a `GateDecision`, `SpeechAct`, `U.Commitment`, `RoleAssignment`, credential record, status record, `A.6.B`-claim being made, `A.10` evidence path, or `B.3` assurance claim. Use `E.17:5.1c` for the shared meanings of `orientation use`, `reliance use`, work claim, reliance claim, operative claim, unsupported downstream use, and `reopen trigger`; use `E.17:5.1d` when the primary question under repair belongs to another governing pattern.

The central behaviour is: name the work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair; name the source that carries the needed claim or effect; keep the `U.Episteme` or `U.EpistemePublication` distinct from publication form, MVPK face, publication carrier, rendering, and source-finding cue; choose the minimum sufficient next move; and do not raise the claim beyond the recovered relation, source relation, or recovered use boundary. If the named project record states the governing FPF relation, use that recorded relation directly rather than inferring it from wording.

**Positive repaired disposition.** An encountered `U.Episteme` publication, publication form, MVPK face, publication carrier, rendering, or source-finding cue may guide work or reliance only to the claim or effect carried by the recovered source, actor or role, work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair, affected work target, context, window, and source-recoverable claim or effect. The repaired outcome is the smallest relation-governed work or reliance statement plus the unsupported work claim or reliance claim still blocked.

Reliance dispositions by recovered source relation:

| Work or reliance disposition | Use when | Minimum useful record |
| --- | --- | --- |
| Orientation or source-finding note | The encountered source candidate is only a publication face, publication carrier, rendering, cue, search handle, learning aid, or reversible local probe trigger. | `encounteredSourceCandidate; required claim or effect not yet carried by a recovered source; source to reopen; stop condition`. |
| Routine reliance note | The team needs ordinary bounded reliance without release, safety, compliance, delegated role or status claim, contested source, or cross-context reuse. | Work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair; required claim or effect; actor or role; affected work target, context, effective window; source reference exposed by the encountered source candidate; and reopen condition. |
| High-impact reliance disposition | The required claim or effect is external-impact, irreversible, release-bearing, gate-bearing, compliance-bearing, safety-bearing, delegated, revoked, status-claim-bearing, generated-source-mediated, copied-source-mediated, provenance-mediated, contested, or cross-context. | Governing source with the `A.10`, `A.6`, `B.3`, `A.2.9`, `A.2.8`, `A.21`, `A.20`, or `A.15.1` fields needed for that claim or effect. |

A small A.15.4 restoration note is enough for the first disposition:

| Field | Value |
| --- | --- |
| work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair | Name the claim or P2W chain position by value: method-family selection, selected method, method of work, work plan, planned work, dated `U.Work` occurrence, work result, result-measurement, release reliance decision, or non-work reliance claim. A planned baseline remains a `U.WorkPlan` or `U.WorkPlanning` plan record; performed work becomes `U.Work` only after it occurs and is recorded under `A.15.1`; work-result measurement belongs with the evidence or result-measurement source. This row is a local restoration label unless it cites an existing FPF kind or governing FPF relation. |
| governing source needed | Approval, permission, gate passage, role or status currentness, work occurrence, evidence relation, assurance claim, boundary claim, or other claim named by value or effect needed before that work claim, reliance claim, or P2W chain-position claim can be treated as carried by a recovered source. The governing relation must be carried by the named FPF pattern and recovered project-side reference, not by a new `A.15.4` kind. |
| actor or role | Who would act or rely. |
| affected work target, context, and window | Release, service, person, role holder, work target, claim, tenant, environment, physical batch, construction element, machine state, or effective window affected by that class or claim. |
| claim-bearing episteme or episteme publication | The claim-bearing FPF kind is `U.Episteme` or a species such as `U.EpistemePublication`; if the encountered source candidate is only a publication form, MVPK face, publication carrier, rendering, `PublicationUnit`, dashboard tile, copied text, credential view, generated explanation, API wording, or cue, name that kind named by value separately. |
| source needed or safe next move | Source `U.Episteme`, source `U.EpistemePublication`, register entry, governing source, source status to refresh, reversible probe, role assignment accountable for exposing or repairing the missing source, or narrower relation-governed use. |
| stop or reopen condition | What blocks the work claim or reliance claim and what would reopen it. |

**Borrowed episteme and publication discipline.** A.15.4 borrows the `C.2.1`, `E.17`, and `A.16.0` distinction rather than minting a new generic `U.*` kind. The claim-bearing FPF kind here is `U.Episteme`; `U.EpistemePublication` is used only when that episteme is available as a published episteme with MVPK-face references. Publication forms, MVPK faces, publication carriers, renderings, `PublicationUnit` instances, and source-finding cues are separate kinds or relation positions in the case. A planned baseline remains a `U.WorkPlan` or `U.WorkPlanning` plan record such as `SlotFillingsPlanItem`; launch values and finalization values remain their own project records, decision logs remain gate or decision records, performed-work evidence remains evidence, and dated work occurrences remain `A.15.1` or `U.Work` matters.

When the required source is incomplete, choose one relation-governed source-restoration disposition after naming the work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair and the source that must carry that claim or effect; pick the lightest move that preserves practical work and source recoverability:

1. Use the encountered source candidate only for orientation or source-finding.
2. Reopen the required source `U.Episteme`, source `U.EpistemePublication`, register entry, or governing source, or refresh status or currentness.
3. Narrow actor or role, requested operation or work class, affected work target, affected resource, affected claim, context, and effective window until the recovered source really covers the move.
4. Run a bounded reversible probe under an explicit `U.WorkPlan` when no external-impact reliance is being made.
5. Ask the role assignment accountable for the issuer, gate decision, evidence path, role record, status record, or boundary claim set to expose or repair the missing source.
6. Repair the `U.WorkPlan`, `U.MethodDescription`, dashboard label, source link, or boundary wording that made the overread plausible.
7. Proceed only inside the recovered scope and window.
8. Block only the work claim or reliance claim that lacks source relation.

##### Repair assignment rule

**Broken-source repair assignment.** If the required governing source is unavailable to the acting user, assign only prospective repair work, request work, decision work, work-plan work, or source-gap work to the role assignment accountable for the missing source relation. The acting user records the blocked work claim or reliance claim, the missing source relation, and the safe narrowed move now.

**Source-candidate kind check.** First name the kind of the encountered source candidate: actual `U.Episteme`, actual `U.EpistemePublication`, publication form, MVPK face, publication carrier, rendering, `PublicationUnit`, dashboard tile, credential view, generated wording, copied wording, or source-finding cue. If the source candidate exposes the governing source, use that exposed source directly. If only the display face, publication carrier, wording, or cue is named, the A.15.4 disposition is orientation, source-finding, bounded reversible probe, source-repair request, or blocked unsupported reliance until the source relation named by value is recovered.

**Pressure guard.** Release pressure, delegated pressure, compliance pressure, color, salience, copied wording, or generated wording does not replace the source relation named by value. A dashboard tile may guide release only as a current view of the relevant `GateDecision` plus evidence path, currentness path, scope, and window.

##### Governing-source lookup table

Governing sources by required claim or effect kind:

- cue-only orientation: use only for attention, learning, source-finding, or a reversible local probe trigger; stay with `A.16`, `A.16.1`, or `A.6.A` when those claims are being made.
- issuing, approval, authorization, delegation, or revocation act: cite `A.2.9` `U.SpeechAct` or `SpeechActRef`, including act type, actor, role, affected work target or claim, judgement context, window, publication-carrier reference, evidence reference when currentness matters, and instituted effects if claimed. Because `U.SpeechAct <: U.Work`, it can evidence only that communicative act.
- deontic permission, obligation, prohibition, or recommendation-as-duty: cite `A.2.8` `U.Commitment` and the instituting `SpeechActRef` when provenance matters. If the word instead names claimed use boundary, gate passage, authorization act, role effect, status effect, credential status, cue, or advice, use the pattern that carries that kind named by value.
- role or status reliance: cite `A.2.1`, `U.RoleAssignment`, a status-changing `U.SpeechAct`, a governing context-state record, a credential proof or status result under `A.10`, or an `A.21` `GateDecision` when the status is gate-governed.
- boundary, policy, API, schema, "allowed", "authorized", "approved", "recommended", or "guaranteed" wording: split the statement through `A.6` or `A.6.B`; use `A.6.C`, `A.2.3`, `A.2.8`, and `A.2.9` for agreement-like guarantee, SLA, or promise wording before work use or reliance use.
- gate decision or gate passage: cite `A.21` `OperationalGate(profile)`, `GateDecision`, `GateDecisionRationale`, `DecisionLogRef`, gate profile, gate version, check set, scope, window, and replay or freshness pins.
- `U.Flow.ConstraintValidity` witness: cite `A.20` `ConstraintValidity` status, witness, `GateCheckRef.aspect = ConstraintValidity`, `PathId` or `PathSliceId` when applicable, window, sentinel, and pins when those fields are needed for the claim.
- release, deployment, repair, inspection, or rollback work occurrence: cite `A.15.1` dated `U.Work` occurrence and the `A.10` evidence or provenance relation when reliance on occurrence is needed.
- evidence, provenance, authenticity, currentness, copied-source, or generated-source relation: apply `A.10` and name the claim-bound evidence path, currentness path, and relation-governed or blocked use.
- assurance, readiness, safety, compliance, trust, release confidence, or `R`, `F`, `G`, or `CL` increase: apply `B.3` and name the typed assurance claim plus its limitations and reopen condition.
- generated explanation: use `E.17.EFP` for explanation faithfulness or source-finding relation, then require `A.10` claim-bound source relation for every operative claim that will be relied on.
- ambiguous approval, permission, or authorization wording: choose among the rows above named by value by asking what effect is claimed now: speech act, commitment, claimed use boundary, gate passage, role or status change, credential status, evidence relation, assurance claim, or work occurrence.

Recovered source outputs for A.15.4 closure:
| Governing source relation used | Recovered output for this A.15.4 restoration | A.15.4-local use |
| --- | --- | --- |
| `A.6` or `A.6.B` | Typed claim IDs (`L-*`, `A-*`, `D-*`, and `E-*`) plus the pattern that governs the claim being made or effect and the governing source for that claim or effect. | Use for wording, boundary, API, schema, or use-boundary recovery before work or reliance use. |
| `A.10` | Claim-bound evidence path, freshness field, currentness field, and relation-governed or blocked use for the attempted claim. | Use for evidence, provenance, authenticity, credential-currentness, copied-source, or generated-source recovery. |
| `B.3` | Typed assurance claim, no-assurance-use disposition, or rejected or downgraded assurance claim. | Use only when the project move under repair relies on a typed assurance claim. |
| `A.21` | `OperationalGate(profile)`, `GateDecision`, `DecisionLogRef`, gate profile, gate version, scope, window, and replay or freshness pins. | Use for gate-passage reliance in the named scope and window. |
| `A.20` | `ConstraintValidity` status, witness, `PathId` or `PathSliceId` when applicable, window, sentinel, and pins when those fields are needed for the claim. | Use for `U.Flow.ConstraintValidity` reliance. |
| `A.2.9` | `SpeechActRef` with act type, actor, role, affected work target or claim, judgement context, window, and instituted effects if claimed. | Use for issued acts and, where needed, dated occurrence of that communicative act. |
| `A.2.8` | `U.Commitment` deontic relation with accountable role, agent, referents, modality, scope, effective window, and instituting source when needed. | Use for deontic permission, obligation, prohibition, or recommendation-as-duty. |
| `A.15.1` | Dated `U.Work` occurrence plus `A.10` evidence or provenance relation when relied on. | Use for reliance on performed work. |
| `E.17.EFP` | Explanation class, source-finding relation, and faithfulness relation over the source `U.Episteme` or source `U.EpistemePublication`. | Use for generated-explanation faithfulness and source-finding before operative reliance. |

High-impact work or reliance - especially external-impact, irreversible, release-bearing, role-bearing, status-claim-bearing, gate-bearing, compliance-bearing, safety-bearing, delegated, contested, or assurance-bearing claim or effect - may guide work only for the actor, role, work or reliance claim under repair, work-relevant P2W claim under repair, P2W chain position under repair, affected work target or claim, audience, scope, environment, version, policy context, operational mode, and time window for which the required FPF-governed project source, relation, evidence path, gate decision, or assurance claim is recoverable. Cue-only, source-finding, learning, and bounded reversible probes stay lightweight and do not require a full source dossier.
Quick dispositions:

| Encountered case | First `A.15.4` disposition |
| --- | --- |
| Source-backed release dashboard tile | If the tile is a current dashboard view of `A.21` `GateDecision` or `DecisionLogRef` plus release scope or work target, environment, scope, window, gate profile, gate version, and `A.10` evidence path, it may carry gate-passage reliance for that release and environment. |
| Unsourced or stale release dashboard tile | Display or source-finding only until the current `GateDecision` or `DecisionLogRef`, release scope or work target, scope, window, gate profile, gate version, and `A.10` evidence path are recoverable; use `B.3` only if an assurance claim is being made. |
| Copied review summary or copied approval | Copied wording and copied-currentness cue at most; approval, authorization, permission, commitment, or work occurrence needs the original `A.2.9` `SpeechActRef`, `A.21` decision, `A.2.8` commitment, or `A.15.1` work source plus `A.10` evidence. |
| Delegation chain with forwarded approval | Each link names delegator, delegatee, delegated operation or work class, affected work target, affected resource, affected claim, scope, window, source permitting delegation, subdelegation allowance if any, revocation source, currentness source or currentness path, and evidence path. A forwarded approval is not delegated authority by copy alone. |
| Role, revocation, or status display | Resolve to role assignment, status-changing speech act, context-state record, credential proof or status result, or gate decision with freshness field, revocation source, or revocation record; visual status cannot defeat a higher-priority revocation or supersession source. |
| Conflicting sources | Do not resolve by color, visual salience, copied wording, or apparent recency. Name source order, governing decision source, freshness policy, and supersession rule; the work claim, reliance claim, or effect is contested until resolved, while source-finding and bounded reversible probes remain available. |
| Credential badge or register-backed status view | Use the display as a publication of a credential source or status source, not the source itself. Find the governing status register or issuer, trust root, holder binding or subject binding, verifier context, relying context, proof or status result, revocation, freshness, and effective window. If the governing register entry itself creates or changes role, status, permission, duty, or gate effect in the bounded context, cite that register or status-source entry named by value and the `A.2.1`, `A.2.8`, `A.2.9`, `A.6.B`, or `A.21` source it depends on. Otherwise rely only on credential-currentness for that holder and context. |
| Rollback command-like cue | Treat as cue or `A.6.A`-governed invitation unless command record, authorization, work occurrence, performed-work result, or gate decision is recoverable. |
| Generated explanation says "authorized" | Explanation may help find sources; it does not issue, approve, revoke, commit, authorize, pass a gate, provide evidence for performed work, or raise assurance. A citation or source mention inside the explanation guides work use or reliance use only when the cited publication carrier carries that relied-on claim named by value in the relying context under `A.10`. |
| Extracted source, rewrite, representation shift, explanation, then gate or release claim | Reopen the governing source at the first lossy or non-commutative transform step; the gate claim or release claim waits for the required transform record, evidence path, explanation relation, gate decision, or assurance claim. |
| Repeated green-tile failures without recoverable source relation | Treat recurrence as upstream source-system repair work: expose decision refs, fix dashboard semantics, add source links and currentness, revise boundary wording, or add review cues so the acting user is not repeatedly forced to reconstruct missing source relation. |

##### Worked dashboard and approval examples

Worked dashboard and approval slice:

A release dashboard shows a green approval-looking tile for `Release-2026.05.08-prod`. If the tile is a current view of the relevant `GateDecisionRef` plus evidence path and currentness path, it may carry bounded gate-passage reliance for that release scope and window. A claim that deployment happened still requires an `A.15.1` work-occurrence source. If the gate source is missing or stale, treat the tile as orientation and source-finding until the team can name the release-work claim under repair, release-work position under repair, governing pattern for the claim or effect, and governing source for the gate decision, evidence path, and currentness path.

| Step | Required move |
| --- | --- |
| Required project claim or effect kind | Release reliance, gate passage, compliance proof, assurance increase, evidence relation, or currentness relation. |
| Gate decision source | Cite the current `A.21` `GateDecision` or `DecisionLogRef`, gate profile, gate version, release scope or work target, scope, window, and replay or freshness pins. Without that source, the tile is not release permission or gate passage. |
| `U.Flow.ConstraintValidity` source | Cite `A.20` `ConstraintValidity` status or witness only when the claim is about `U.Flow.ConstraintValidity`, not about the gate decision itself. |
| Evidence and currentness source | Use `A.10` for the dashboard query, publication-carrier integrity, evidence refs, time, window, freshness field, revocation source or revocation record, verifier context, relying context, and rival explanation such as stale display or copied status. |
| Assurance source | Use `B.3` only if the tile is being used to raise readiness, compliance, trust, safety, release confidence, `R`, `F`, `G`, or `CL`; otherwise no assurance tuple is being claimed. |
| Repaired gate-use reliance | With the decision and evidence path recovered, rely on gate passage only for the named release scope or work target, environment, gate profile, gate version, time, and window; a claim that deployment happened still needs an `A.15.1` work-occurrence source. |
| Blocked overreads | The dashboard color does not create approval, permission, compliance proof, rollback success, work occurrence, or assurance by display. |

Approval memo green-tile case:

An approval memo may carry an approval claim when it exposes the `A.2.9` `SpeechActRef`, actor, role, affected release scope or work target, judgement context, time, window, publication-carrier refs, evidence refs, and instituted effect being claimed. That carries the bounded approval claim or effect only. It does not prove that release, deployment, rollback, or other work occurred; that performed-work claim still needs the dated `A.15.1` work-occurrence source plus any `A.10` evidence path required for the relying context.

Credential and status green-tile case:

A credential or status response may carry holder reliance, status reliance, or currentness reliance only inside the issuer or governing status register, holder binding or subject binding, verifier context, relying context, proof result or status result, revocation source or revocation record, freshness field, and effective window that it exposes. It does not by itself carry release, work occurrence, gate passage, engineering justification, evidence for underlying operational facts, or contextual permission; those uses require the governing source for the claim or effect.

Role prompts:

| Role in the situation | Prompt |
| --- | --- |
| Acting user | What can I safely do next without turning the encountered episteme or episteme publication into unsupported work or reliance justification? |
| Release engineer | Which `A.21` gate decision, decision log, release scope, work target, and `A.15.1` work occurrence are separate here? |
| Issuer, gate, evidence, or role source | What source, status, decision ref, or evidence path must be exposed or repaired? |
| Audit or peer-review role | Which evidence path, decision ref, speech-act ref, commitment, work occurrence, or assurance claim must be recoverable? |
| Boundary claimant | Which words need typed claim IDs before they can guide work or reliance? |
| Manager | Is repeated ambiguity source-system repair work rather than another manual check for the acting user? |
| LLM user or tool user | Which governing source does the explanation help find, and which operative claims still need an `A.10` claim-bound source relation? |
| Security or compliance source | Which revocation, currentness, proof, status, source order, or supersession source must be exposed? |
| Model or data source | Which intended use, evaluation condition, version, window, limitation, and evidence path bound the model or data documentation? |
| Assurance role | Which named claim actually has a `B.3` assurance claim, with what assurance tuple, evidence path, limitations, and reopen condition? |
Search aliases for A.15.4 include: approval, approval-looking display, authorization, authorization-looking display, permission, permission display, allowed wording, green dashboard, release tile, release readiness, model card, datasheet, data card, provenance, provenance mark, attestation, attestation label, credential, credential badge, generated explanation, copied review, copied approval, review summary, compliance-looking mark, delegation, delegation display, revocation, revocation status, gate passed, gate passage, rollback successful, rollback cue, and assurance label. These are search handles only; decide the governing source and governing pattern or source relation from the work or reliance question under repair, not from the displayed word, publication-carrier name, or source name.

Work and reliance disposition table for authority-looking cases:

| Question under repair | Start in | First useful output |
| --- | --- | --- |
| Can this encountered episteme publication, publication face, publication carrier, rendering, or cue guide work or reliance? | `A.15.4` | Candidate next `U.WorkPlanning`, `U.Work`, or reliance move; governing pattern for the claim or effect; governing source; minimum relation-governed next move. |
| Is the problem boundary, policy, API, schema, or connector wording? | `A.6` or `A.6.B` | Typed `L-*`, `A-*`, `D-*`, and `E-*` claims before the work claim or reliance claim is used. |
| Is the problem evidence, currentness, provenance, credential status, generated-source relation, copied-source relation, or source-chain recovery? | `A.10` | Claim-bound evidence path, currentness path, and relation-governed or blocked use. |
| Is the problem assurance, readiness, safety, compliance, trust, release confidence, or change in `R`, `F`, `G`, or `CL`? | `B.3` | Typed assurance claim, no-assurance-use disposition, or downgraded or rejected assurance use. |

Display guidance for bounded status: a visible status meant to guide work should expose source type, reference or link named by value, freshness, window, scope, unsupported work claim, unsupported reliance claim, and unsupported effect. For example, prefer `Gate check passed; GateDecisionRef; release scope; environment; window; not compliance proof, rollback success, or assurance increase` over a bare approval-looking label.

Incident-learning fields for authority-looking overread: encountered episteme or episteme publication, work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair, governing pattern and governing source for the claim or effect, actor, role, affected work target or claim, context, window, missing or stale source `U.Episteme`, source `U.EpistemePublication`, register entry, or governing source; governing FPF relation or role assignment accountable for exposing or repairing that missing source, plausible overread, safe disposition used now, and upstream repair work for the source, dashboard, explanation, credential view, boundary wording, publication face, or publication carrier.

Contestability and redress relation: when an authority-looking case affects person or team status, access, assignment, responsibility, release blockage, compliance claim, or safety-impacting work, name the review relation or redress relation before the work claim or reliance claim hardens. The relation should name the disputed source or claim, the role assignment accountable for refreshing or correcting that source, the evidence relation or status-currentness relation to reopen, the safe interim disposition, and the time and window for review.

Lintable overread cues:

| Lint signal | Governing relation named by value |

| --- | --- |
| `approved`, `authorized`, `allowed`, `recommended`, or `guaranteed` in boundary, API, schema, or policy wording | Split through `A.6` or `A.6.B` into `L-*`, `A-*`, `D-*`, and `E-*`; use `A.6.C`, `A.2.8`, and `A.2.9` for agreement-like wording when agreement, commitment, or speech-act claims are being made. |
| Dashboard tile, status color, or release tile used as release evidence or gate passage | Require `A.21` `GateDecision` or `DecisionLogRef` plus `A.10` evidence path and currentness path. |
| Credential screenshot or badge used as permission, authorization, role relation, or status relation | Require `A.10` issuer, holder, verifier, status, currentness, and relying-context fields, then the `A.2.8`, `A.2.9`, `A.2.1`, `A.6.B`, or `A.21` source named by value for the required permission, authorization, role, status, gate claim, or gate effect. |
| Generated explanation uses `authorized`, `approved`, or similar wording | Use `E.17.EFP` for explanation relation and source-finding relation and `A.10` claim-bound source relation; issue, approval, gate, and commitment claims still need `A.2.9`, `A.21`, or `A.2.8`. |
| Model card, datasheet, label, or note cited as readiness, safety, compliance, or release confidence | Require a typed `B.3` assurance claim, intended-use match, evaluation condition, limitations, and `A.10` evidence path. |
| Provenance or attestation label cited as truth, safety, release, or permission | Require `A.10` bounded provenance claim or process claim plus separate evidence for truth, safety, release, permission, or assurance. |
| Evidence, assurance, gate, or work-occurrence words without the governing source that carries that claim or effect | Recover the `A.10` evidence relation, `B.3` assurance claim, `A.21` gate decision, or `A.15.1` work-occurrence record respectively before the work claim or reliance claim is used. |

Stress cases for practice:

| Case | Expected A.15.4 disposition |
| --- | --- |
| Green release dashboard tile with no `GateDecisionRef`. | Source-finding only; recover `A.21` decision or decision log plus `A.10` evidence before gate-passage reliance. |
| Copied approval from last month. | Recover original `A.2.9` `SpeechActRef`, currentness, freshness, and any `A.2.8` commitment or `A.21` gate source needed for the claim. |
| Credential badge screenshot after revocation. | Treat as contested credential-currentness; use `A.10` issuer, holder, verifier, source-status, and revocation relation and do not infer permission. |
| Generated explanation says `authorized by policy`. | Use `E.17.EFP` for explanation and source-finding and `A.10` claim-bound source relation; issuing, gate, and commitment claims still need their own sources. |
| Boundary wording says `guaranteed approved for production`. | Split through `A.6` or `A.6.B`; if agreement-like or promise-bearing, unpack through `A.6.C`, `A.2.8`, and `A.2.9`. |
| Dashboard says green while decision log says blocked. | Treat as conflicting sources; name source order, governing decision source, freshness policy, and supersession rule before the work claim or reliance claim is used. |
| CRISPR lab dashboard says the guide edit is ready. | Treat the dashboard as orientation or source-finding until the protocol, approval record or gate record, role authorization, evidence path, current lab source, and `U.WorkPlan` for the intended edit are recoverable. A ranked guide row or readiness tile does not create biological-intervention permission, safety, or performed work. |

##### High-impact source-restoration slice

A lab manager sees a green tile for `CRISPR-guide-G42 ready` and a copied message saying the edit is approved. `A.15.4` does not ask the manager to decide whether the tile is a good UI. It asks what work or reliance claim is about to be made.

```text
SourceRestorationNote:
  EncounteredSourceCandidate: green guide-readiness tile plus copied approval-looking message
  WorkOrRelianceClaimUnderRepair: proceed with the planned gene-editing work for sample batch B-17
  ClaimOrEffectNeeded: authorization for intervention, current protocol, role authority, evidence path, and lab work plan
  GoverningSourceNeeded: current protocol publication; approval record or gate record when required; role assignment; A.10 evidence relation and currentness relation; A.15.2 work plan
  RelationGovernedMoveNow: source-finding and source refresh; no intervention until the needed sources are named
  BlockedOverread: tile color and copied message do not authorize biological work or prove safety
  StopOrReopenCondition: reopen when the protocol, approval source or gate source, evidence path, role assignment, and work plan are current for batch B-17
```

### A.15.4:4 - Conformance Checklist

| ID | Requirement (Normative Predicate) | Purpose and Rationale |
| :--- | :--- | :--- |
| **CC-A15.4-1 (Work-relevant source restoration)** | Before an authority-looking case guides work or reliance, a conforming `A.15.4` use SHALL produce the ordinary source-restoration note: encountered source candidate, work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair, governing pattern for the claim or effect, governing source needed, relation-governed next project move now, and blocked overread. It SHALL name the pattern and governing source that carry the requested claim or effect; if that source is absent or stale, it SHALL lower only the unsupported reliance to orientation, source-finding, contested use, source repair, bounded reversible probe, or blocked unsupported claim. | Prevents appearance-based reliance while keeping ordinary use cheap. |
| **CC-A15.4-2 (P2W publication use boundary)** | A principle scheme, functional diagram, scenario, screen, or explanation that exposes a P2W chain may guide only the named `A.15` work or planning kind named by the project use: method-family selection, selected method, `U.WorkPlan`, dated `U.Work`, work-result record, or result measurement. Claims outside that named use require their own governing source. | Keeps P2W publication use tied to the work move under repair instead of turning publication form into project authority. |
| **CC-A15.4-3 (Lowering and refresh)** | When the governing pattern, governing source, source-currentness relation, revocation relation, affected work target, relying context, or time window cannot be recovered, the work or reliance claim SHALL be lowered to orientation, source-finding, contested use, bounded reversible probe, source-repair request, or blocked unsupported claim. Refresh is required when source currentness, revocation, governing decision, evidence path, status register, copied-source relation, generated-source relation, or publication relation changes. | Keeps A.15.4 useful without admitting a new source kind. |

### A.15.4:5 - Common Anti-Patterns and How to Avoid Them

- **Appearance as source relation.** A dashboard tile, credential display, copied approval, generated explanation, provenance label, command-like cue, or composed source chain is used as if presentation itself carried the work-relevant source relation. First name the work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair, then recover the governing pattern and governing source for the requested claim or effect. If that source is missing, lower only the unsupported reliance.

### A.15.4:5a - Consequences

| Consequence | Trade-off and cost | Mitigation |
| --- | --- | --- |
| Work can continue at the lightest relation-governed level instead of stopping on every suspicious display. | The practitioner must name the claim being made and governing source reference before relying on the source. | Use the ordinary six-field source-restoration note first; use fuller fields only for high-impact or contested reliance. |
| Appearance-based approval, evidence, assurance, gate, and work-occurrence overreads are blocked. | Some convenient dashboard or copied-text shortcuts become unusable until source currentness is recovered. | Keep orientation, source-finding, and bounded reversible probes available when no external-impact reliance is being made. |
| Repeated ambiguity becomes source-system repair work rather than repeated manual heroics. | The repair may reveal missing register entries, stale source publications, or underspecified gate and evidence paths. | Assign only prospective repair work or source-gap work; do not backdate evidence, gate passage, work occurrence, or assurance. |

### A.15.4:5b - Rationale

A.15.4 exists because work often meets sources through displays, publication faces, generated explanations, copied statements, credential views, dashboard tiles, schema wording, API wording, or composed source chains before the governing source is visible. The pattern protects work momentum and source recoverability together: it lets the practitioner use the encountered source candidate for orientation or bounded source-finding, while preventing the source candidate from becoming approval, evidence, assurance, gate passage, performed work, release permission, role currentness, or status currentness by appearance.

The pattern is deliberately a restoration relation, not a new authority source. Once the evidence, gate, assurance, speech-act, commitment, role, status, work-occurrence, publication, or boundary claim named by value is recovered, the pattern that governs that claim carries it directly.

### A.15.4:6 - SoTA Alignment

**SoTA alignment rule.** Interpret each row here as source idea -> local FPF invariant -> practical local test -> popular shortcut rejected. A source citation governs nothing by reputation; it counts only when the cited idea is translated into the Solution, conformance checks, boundary rules, worked slices, and relations of this pattern.

| Claim need | Source idea and current source | Current source reference | Local FPF invariant and practical local test | Adopted invariant, adapted invariant, and rejected shortcut |
| --- | --- | --- | --- | --- |
| Dynamic authorization or policy-response displays need requested operation named by value, affected resource or work target, context, and window relation. | Dynamic authorization practice separates subject, requested operation, affected resource or work target, context, and window before a relying move is allowed. | NIST Zero Trust and dynamic authorization practice; Cedar policy language; Zanzibar-style relation authorization; source maturity = current standards, specifications, and widely used technical practice. | The restoration note names the work or reliance claim under repair, work-relevant P2W claim under repair, or P2W chain position under repair, the affected resource or work target, affected claim when one is being made, policy version, context, and time window before treating a visible allow response, deny response, or policy response as a relation-governed work or reliance source. | **Adopt, adapt, reject.** Adopt bounded currentness, source-relation, and relation-governed-use invariants; adapt them through FPF project records named by value; reject treating policy-looking output as permission or work-relevant source relation by display. |
| Credential or register-backed status needs issuer, holder, verifier, status, currentness, and relying-context fields. | Credential and status practice separates issuer, holder binding or subject binding, verifier context, relying context, proof result or status result, governing register entry, revocation, freshness, and effective window. | W3C Verifiable Credentials and digital identity or register-backed status practice; source maturity = current specifications and technical practice. | A credential view or status tile can carry only the holder claim, status claim, or currentness claim whose issuer, register, proof result or status result, revocation, freshness, and relying context are recoverable. | **Adopt, adapt, reject.** Adopt status-currentness separation; reject treating a badge, screenshot, or register excerpt as role, status, permission, gate passage, or work reliance without the governing source for that claim or effect. |
| Provenance and attestation marks need source relation and process-trace relation without becoming truth, release, or work evidence. | Provenance and attestation practice separates origin relation, process traceability relation, build claim, supply-chain claim, and verification metadata from truth of downstream claims or release permission. | C2PA content provenance; SLSA and in-toto attestations; source maturity = current standards, specifications, and widely used practice. | A provenance or attestation mark remains source relation or process-trace relation until `A.10`, `B.3`, `A.20`, `A.21`, `A.15.1`, or another source relation named by value carries the downstream claim. | **Adopt, adapt, reject.** Adopt source traceability and process traceability; reject provenance-mark-as-truth, release permission, gate passage, assurance, or work occurrence. |
| Change, gate, release, and approval displays need decision, schedule, and performed-work separation. | Release and change practice separates approval acts, authorization acts, gate decisions, planned schedules, and performed work. | ITIL 4 Change Enablement and current release or change practice; source maturity = current practitioner guidance plus mature service practice. | A dashboard or approval-looking display must expose the `GateDecision`, `SpeechAct`, `Commitment`, `U.WorkPlan`, or `A.15.1` work-occurrence source that carries the claim named by value or effect. | **Adopt, adapt, reject.** Adopt decision, schedule, and performed-work separation; reject a green tile, copied approval, or generated explanation as rollout, release, or work reliance by appearance. |

**Digital-identity and provenance boundary.** The W3C Verifiable Credentials, C2PA, SLSA, in-toto, Cedar-style, Zanzibar-style, NIST, and ITIL sources are used for currentness, status, provenance, authorization-source fields, and change-practice fields. They do not turn a visible credential, provenance label, attestation, policy response, register excerpt, or dashboard display into work occurrence, gate passage, permission, assurance, release, or project claim relation without the governing source required by `A.15.4`, `A.15`, `A.10`, `B.3`, `A.20`, or `A.21`.

The nearest recovery references are the worked dashboard and approval examples, `CC-A15.4-1`, `CC-A15.4-2`, `A.10`, `B.3`, `A.20`, `A.21`, `A.2.8`, `A.2.9`, and `A.15.1`. If a SoTA row cannot be recovered through those local checks, do not let the source citation stand in for the local `A.15.4` rule.

### A.15.4:7 - Relations

* **Cluster relation:** `A.15.4` is a cluster member under `A.15` for work-relevant source restoration; it does not replace the A.15 role, method, plan, and work kernel.
* **Uses:** `E.17:5.1b` and `E.17:5.1c` source-relation and use-boundary vocabulary, `E.17.EFP` for generated-explanation faithfulness and source-finding, `A.6`, `A.6.B`, and `A.6.C` for boundary, policy, API, and schema wording, `A.10` for evidence, currentness, provenance, and credential status, `B.3` for engineering justification claims, `A.20` for `U.Flow.ConstraintValidity`, `A.21` for gate decisions, `A.2.8` for commitments, `A.2.9` for speech acts, and `A.15.1` for dated `U.Work` occurrences.
* **E.10.ARCH relation-selection rule:** When `E.10` encounters source-relation, authority, permission, approval, status, green-tile, generated-explanation, copied-review, credential, provenance, or dashboard wording that is about to guide work or reliance, `E.10.ARCH` selects `A.15.4` only after excluding or assigning direct evidence (`A.10`), assurance (`B.3`), gate (`A.21`), constraint (`A.20`), boundary or use-boundary wording (`A.6` and `A.6.B`), speech act (`A.2.9`), commitment (`A.2.8`), work occurrence (`A.15.1`), and publication-face or explanation questions (`E.17` and `E.17.EFP`). `A.15.4` records the work-relevant source-restoration relation named by value; it does not replace those governing patterns.
* **A.15 boundary relation:** use `A.15` directly when the remaining question under repair is role, method, plan, and work alignment rather than source restoration.

### A.15.4:7a - C.29 mathematical-lens use relation

> If a mathematical lens appears in work-relevant source restoration, use `C.29` only to state why the lens helps expose or bound an encountered source candidate such as generated wording, dashboard cue, copied phrase, publication form, MVPK face, publication carrier, rendering, `PublicationUnit`, or source-finding cue. `A.15.4` still governs the source candidate, source relation named by value, restoration or reopen condition, reliance relation, and whether that candidate can guide work under a recovered source relation. Method choice, plans, and performed work remain governed by `A.15` and `A.15.1` when those claims are being made; a `C.29` lens-use result does not turn a cue, rendering, or diagnostic phrase into source relation.

### A.15.4:7b - P2W Result-Related Source Boundary

When a P2W use under `E.18.1` produces result wording, use this pattern only when an encountered source candidate such as publication, dashboard, generated explanation, copied statement, provenance mark, schema wording, API wording, or composed source chain is about to justify a work-result or reliance claim by appearance. No generic `WorkResult` kind is admitted.

Recover the governing source before relying on any result-related cue: result artifact, resource ledger, launch-values-bound record, substitution record, telemetry, acceptance record, quality-evaluation record, done-state update, feedback pin, result measurement, evidence path, assurance claim, parity relation, refresh relation, or role-enactability claim. If the governing pattern or relation is missing, use the encountered source candidate only for orientation or source-finding and block only the unsupported result or reliance claim.

### A.15.4:7c - Lowering, Repair, and Refresh Conditions

Lower an `A.15.4` use when the work or reliance claim under repair, work-relevant P2W claim under repair, P2W chain position under repair, governing pattern, governing source, relying context, time window, source-currentness relation, revocation relation, evidence path, gate decision, assurance claim, speech-act ref, commitment, role assignment, status record, or work-occurrence source cannot be named for the intended use. The lowered use is orientation, source-finding, contested use, bounded reversible probe, source-repair request, or blocked unsupported claim.

Repair the source-restoration note when source currentness, revocation, source order, governing decision source, evidence path, copied-source relation, generated-source relation, dashboard publication, credential view, status register, boundary wording, or work-result cue changes. Repair the governing source through the evidence, assurance, gate, constraint, speech-act, commitment, role, status, work-occurrence, publication, or boundary-wording pattern governing the recovered claim when that recovered claim belongs outside A.15.4.

Refresh before allowing the encountered source candidate to guide release, safety, compliance, delegated role or status, contested source, cross-context reuse, work-result reliance, external-impact reliance, or irreversible work. Stop the refresh at the smallest changed source-restoration value: encountered source candidate, source episteme, source publication, governing source, source-currentness relation, status or revocation record, gate relation, evidence relation, assurance relation, copied-source relation, generated-source relation, or work-governed relation.

### A.15.4:End
