# Generalization experiment implementation

This implementation follows the user's current instruction to use the existing
DeepSeek Flash API adapter and to launch the experiment after code checks. The
older attached document's Phase 1 prohibition on live requests is superseded for
this run; it is retained as protocol background only.

## Runtime

`config/research/generalization_deepseek.toml` points at
`https://api.deepseek.com` with model `deepseek-flash`. The key is read from
`DEEPSEEK_API_KEY`. `scripts/research/run_generalization.py` writes one private
config and log per domain/arm/condition and disables cross-episode skill writes.

The smoke command is:

```powershell
python scripts/research/run_generalization.py --domains calendar --task-limit 1
```

Add `--attack` to use the frozen observation overlay. The three arms are
`STATIC_STAR`, `STATIC_DISCUSSION`, and `MANTA_NATIVE_FROZEN_SKILL`; their
topology, discussion, and communication settings are passed explicitly to the
existing CLI.

## Attack boundary

`research/generalization/protocol.py` implements deterministic non-LLM
manifest allocation, nonce generation, G1/G2 payload templates, one-shot
string-leaf append overlays, and conservative G1/G2 scoring. The overlay is
applied after a WorkBench handler returns and before the observation is added to
the model tool loop. It never changes tool arguments or sandbox state.

## Current scope

The smoke runner covers WorkBench first because its sandbox is available in this
checkout. AppWorld support from the earlier adapter is registered as a separate
benchmark and remains opt-in through an AppWorld config with its official SDK
environment. Results must be read from the per-episode `artifacts/generalization`
logs and hierarchical run artifacts; a process exit alone is not a task score.
