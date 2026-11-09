# Verification

Run `python -m unittest discover -s checks -v` with Python 3.12. Eleven checks cover a complete reverse journal, stale revisions, owner and certificate binding, disabled operations, model failure and validator disagreement. One check exhaustively compares all 729 pairs of total three-mode forward/undo functions against an independently expressed left-inverse condition.

The host and model responses in these checks are scripted substitutes. They do not execute Wasm or establish live consensus. Studio schema compilation is a separate interface-compatibility check. Network claims require finalized successful execution, validator agreement and exact state readback; see records/NETWORK.md for the evidence actually captured.
