# RewindTable

Undo cannot reconstruct information an operation has erased.

RewindTable is a reusable Intelligent Contract for checking compensation rules in small finite workflows. Each operation supplies independent forward and undo descriptions. GenLayer leader and validators interpret every input-mode cell separately; consensus compares the entire function tables. Deterministic code then checks the left-inverse equation for every enabled input and records concrete counterexamples.

Only a fully known reversible specification can open an owner-signed rehearsal. Each forward step is journaled. Rewind automatically compensates the most recent operation, recomputes the restored state from the accepted map, checks it against the original-state witness and pops the journal. Stale revisions, a different certificate or an uncertified specification cannot advance it.

The reservation example demonstrates two operations and two reverse steps. A separate erasure example maps two distinct inputs to one output and exposes exactly which original state its proposed compensation cannot restore. Network records identify the finalized transactions actually captured.

The result applies to a declared abstract finite system. It is not a guarantee that an external service, payment or physical action can be undone. No frontend, paid API or real asset transfer is part of the contract.
