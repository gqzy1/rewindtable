# Reproducing the checks

Run `python -m unittest discover -s checks -v` with Python 3.12. Eleven checks passed locally. The suite loads the production source with an explicit scripted host. It invokes the actual leader/validator callbacks with independent responses and checks a complete reverse journal, stale revisions, owner and certificate binding, disabled operations, model failure and validator disagreement. One check exhaustively compares all 729 pairs of total three-mode forward/undo functions against an independently expressed left-inverse condition.

These are local model fixtures. They do not execute GenVM Wasm or call an actual LLM. Official genvm-linter 0.11.0 passed; Stable Studio compiled the exact pinned production source. Twelve separate real transactions and finalized state readback are documented in [records/NETWORK.md](records/NETWORK.md).
