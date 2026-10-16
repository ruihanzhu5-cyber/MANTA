# Pilot 03: identical contaminated-state topology counterfactual

## 1. Motivation

Separate attack exposure, model variation and communication structure with a genuine shared checkpoint.

## 2. Research Question

Does applying a legal topology mutation to the same contaminated state change subsequent actions?

## 3. Hypothesis

A controlled mutation can amplify, reduce or leave the downstream effect unchanged.

## 4. Threat Model

An already observed WorkBench email-body IPI, if a source episode exists; no new content is injected at continuation.

## 5. Experimental Setup

KEEP and MUTATE require identical sandbox, messages, artifacts, context, topology, controller state, tool deduplication, seed, model settings and prior injection count. The intervention is `CONTROLLED_TOPOLOGY_MUTATION`, separate from native MANTA adaptation.

## 6. Implementation Changes

Added an explicit checkpoint eligibility audit and an analysis path. No benchmark state, Auditor rule or model prompt was changed.

## 7. Real Execution Results

Status: `BLOCKED_BY_EXPERIMENTAL_PRECONDITION`. Eligible checkpoints: 0. KEEP runs: 0; MUTATE runs: 0; new model requests: 0. The absent outcomes are unknown, not zero-valued performance results.

## 8. Failure Cases

No Pilot 02 attack run exists

## 9. Interpretation

No repair-induced amplification, contaminated-handoff effect, safety–utility conflict or protective mutation can be estimated without equivalent state restoration.

## Does This Experiment Support Our Motivation?

`INCONCLUSIVE`: the causal intervention was not run because its state-equivalence prerequisite was unmet.

## 10. Limitations

Existing trace/metadata are observational records. They do not serialize WorkBench sandbox tables or the executor's exactly-once deduplication set for lossless continuation.

## 11. Next Experiments

Build and test a versioned checkpoint/restore path in a separate proposal, then pre-register a case with a genuine Planner mutation before any paid paired continuation.

## 12. Git Commit / Raw Evidence / Cost

Branch `research/pilot03-counterfactual-topology`; base `7d557dc793221906a46a1f83d4e5888fcc5c28d2`; Pilot 02 source `90bace138d7395833a5111acef7e05f28a13851f`; manifest SHA256 `c8765afd59432a7fba5b74e42d2f86aaa5520ca5c811170e3a6673f476f647d5`. No new API cost. Per-source paths and hashes are in checkpoint_manifest.json and summary.csv.
