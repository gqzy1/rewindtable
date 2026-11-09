# Network observations

Stable Studionet, chain 61999. Contract: `0xaF85484be03e8119542A616804eE5886491d1ba2`.
Owner: `0x430472A4EcE92760B5468EC8FC46F7494B78FE55`.

Twelve transactions were sent, all with full consensus and zero attached value. The RPC reported zero gas price. Deployed source matched the complete production file byte for byte.

Eleven transactions are FINALIZED / MAJORITY_AGREE with successful leader execution: deployment, three registrations, verification of the reversible reservation case, start, two forward steps and two rewinds, and verification of the explicitly indexed lossy case. Each recorded three agree votes and two idle votes.

One transaction is a preserved failure, not a success: the first verification of the `broken` case is FINALIZED / MAJORITY_DISAGREE. Its leader execution returned SUCCESS, but that is the leader's local execution only. Three validators disagreed and one agreed, so the book stayed DRAFT at revision 0 and no certificate was stored. The leader's own payload shows the misreading: it interpreted the forward output as index 1, giving forward `[1,1,-1]` and counterexamples with restored `-1`, instead of the declared ready index 2. No Appeal was filed and the transaction was not resent.

The `lossy-explicit` verification was still ACCEPTED when work paused. It was re-read on 2026-11-10 with no new transaction sent, and is now FINALIZED / MAJORITY_AGREE / SUCCESS with three agree votes and two idle votes. Its stored book is BROKEN at revision 1: forward `[2,2,-1]`, undo `[-1,-1,0]`, counterexample action 0, before 1, after 2, restored 0, certificate `1085fc61a036e11c08501b898116004e2c429b3a32b0b9eb2fa2654e5ace14d8`. Both input modes map to ready, and the compensation returns only to idle, so the held state cannot be restored. The rehearsal cannot start from this book.

The reservation case completed its full rehearsal on chain. Its book is RESTORED at revision 6: current 0, initial 0, empty stack, with forward steps hold then prepare and rewinds in reverse order, returning through held to idle. Its certificate is `c18dc655e644dcd4d91eb2ca95a301404a9d98d05929921adcd58e17dbb1cc22`.

`records/transactions.json` contains explicitly selected receipt fields and hashes of the complete captured receipts; it is not a full raw receipt export. The complete receipts are retained off-repository and are identified by those hashes. `verification.json` binds each method and argument list to its transaction, lists the failed verification separately, and binds the three stored books to finalized readback. `npm install && npm run read` fetches the existing transactions, verifies exact deployed source, checks finality/agreement/execution and call bindings, confirms the preserved failure, and compares all three saved books with finalized state. It sends no writes.

Local scripted checks: 11 passed, including an exhaustive comparison of all 729 pairs of total three-mode forward/undo functions against an independently expressed left-inverse condition. Official genvm-linter 0.11.0 passed with only the I200 newer-runner advisory; the pinned runner compiled successfully in Stable Studio. These checks are separate from the real transactions above. No GitHub Actions run has been recorded for this repository yet.

Only abstract state stored in this contract changes. There is no booking service integration, external command execution, asset transfer or real-world rollback guarantee. Specifications and journals are public; no confidential information belongs in them.
