# Finite-function rules

There are 2–6 distinct named modes and 1–3 distinct actions. Each action has a forward and undo description of at most 1000 characters. A table position is an input mode; its value is an output index, -1 for explicitly disabled, or -2 for unknown. Identity means the same index, not -1.

The leader and each validator independently interpret every forward and undo cell from the original descriptions. Equivalence requires equality of the entire normalized function tables. Agreement only on the overall reversibility label is insufficient. No stored state is mutated inside nondeterministic execution. Model failure or disagreement leaves the book DRAFT.

Undo may depend only on the current mode. Hidden history, backups, external state and action arguments are unavailable. A description needing them becomes unknown. The model must not repair a bad compensation to make the operation reversible.

For each action f with compensation g, deterministic code checks g(f(x)) = x for every enabled x. A known failure produces BROKEN, even if another cell is unknown. Otherwise any unknown cell produces UNCERTAIN. A fully known nonempty collection of successful roundtrips produces REVERSIBLE and phase READY. If every forward operation is disabled, INERT prevents a vacuous certificate.

Only left inversion on the enabled forward domain is required. Compensation outside a forward image may be disabled. Different actions need not commute. Reverse journal order is essential and enforced.

The stored pre-state is a consistency witness, never the source of the restored value. Rewind computes the compensation from the current mode, checks that it equals the journal witness, then pops the operation. At most twelve forward steps and twelve reverse steps are possible.

## Boundaries

These are declarations about an abstract finite system, not observations of an implementation. Hidden modes, external side effects, concurrent mutation and misleading text are outside the model. Independent model agreement can be wrong. No financial, physical or legal effect is undone. Specifications and journals are public; never include confidential information.

Each address may register twelve books. This bounds ordinary use per address, not Sybil activity. The parser rejects duplicate JSON keys, Boolean indices, out-of-range targets and malformed tables. Prompt text is untrusted data, but prompt-injection resistance is not an absolute guarantee.
