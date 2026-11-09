# RewindTable

An undo button is a claim. RewindTable checks the claim before a rehearsal can start.

A small workflow declares its modes and describes each operation together with its compensation. GenLayer independently translates both descriptions into finite partial functions. Contract code checks every enabled starting mode: applying an operation and then its compensation must return that exact original mode.

A many-to-one operation exposes the problem immediately. If both `idle` and `held` become `ready`, an undo rule that always returns to `idle` cannot restore a previous `held`. The contract records that counterexample and prevents the rehearsal from starting.

Stable Studionet contract: `0xaF85484be03e8119542A616804eE5886491d1ba2`. The production source matches the deployed bytes.

## Reservation example

The supplied case has two operations: `idle → held` and `held → ready`. Their compensations are `held → idle` and `ready → held`. Once independently agreed and checked, a signed rehearsal may execute both operations. Rewinding chooses the last operation automatically. The first rewind returns to held; the second returns to idle and closes the journal as RESTORED.

Only abstract state stored in this contract changes. There is no booking service integration, external command execution, asset transfer or real-world rollback guarantee.

## Using the contract

Deploy the complete `src/rewindtable.py` on Stable Studionet, chain 61999, RPC https://studio.genlayer.com/api. Constructor arguments are empty. Use full consensus, with zero attached value.

1. Call `register(tag, specification_json)` with the contents of `cases/reservation.json` as a string.
2. Call `verify(tag, 0)`. Read `book(owner, tag)` at finalized state.
3. Only READY may call `start(tag, 1, certificate, 0)`. The exact accepted certificate is required.
4. Call `step(tag, 2, 0)` and `step(tag, 3, 1)` to execute hold and prepare.
5. Call `rewind(tag, 4)` and `rewind(tag, 5)` to return to the initial mode.

Every write is owner-scoped. Revisions prevent stale calls. Tags and specifications cannot be replaced. A verified interpretation cannot be reevaluated; corrections use another tag. A book supports one bounded rehearsal. `finish` commits a nonempty forward journal terminally, while the first rewind permanently disables further forward execution. RESTORED and FINISHED cannot restart.

## Read the result

`report.roundtrips` contains every checked action/input pair. `report.counterexamples` identifies the input, forward output and incorrect or disabled restoration. `report.unknown` identifies unrepresentable cells. `maps` retains the complete independently accepted forward and undo tables. The certificate binds the owner, tag, exact specification, both maps and report.

[Finite-function rules](FUNCTIONS.md) · [Verification scope](CHECKS.md) · [Recorded transactions](records/NETWORK.md)

Evidence summary: [evidence.json](evidence.json). To inspect the existing deployment without signing, run `npm install` followed by `npm run read`. The command verifies source identity, finalized transaction outcomes, call parameters and stored books. It sends no writes.
