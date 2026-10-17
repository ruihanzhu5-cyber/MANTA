# AppWorld handoff method notes

The code renders packets only after ContextPolicy filtering. `NATIVE_PACKET` deep-copies the native packet, `SUMMARY_ONLY` keeps packet identity and the native summary, and `EVIDENCE_REFERENCED` adds stable artifact/record handles and structural field paths without copying tool-result values.

B0 was intentionally run before any handoff-arm comparison. Both official tasks failed in both baseline arms, so the documented stop rule `NO_VALID_CLEAN_CASE` applies. No attack recipient, injection payload, or hidden verifier was used.

Raw traces and ledger files are local ignored artifacts. Only this sanitized report and the source/configuration are intended for version control.
