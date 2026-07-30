# Historical drift evaluation

The drift corpus is a decision-regression suite for the research harness. Each
case records a real repository failure, the decision a sound harness should
have produced at the time, and decisions it must not produce.

[`replays/current.json`](replays/current.json) records the currently reviewed
action for every frozen case and for a non-drift creativity control. Tests
check exact action agreement, forbidden-action avoidance, mechanism coverage,
and existence of every cited historical source. This is an executable audit of
the declared decision contract, not an automated judge of arbitrary prose or
mathematical quality.

The corpus is not a benchmark of mathematical creativity. It tests only
commitment-boundary behavior: admission, promotion, evidence interpretation,
and agenda selection.

## Reviewing a harness change

1. State the exact failure mode the proposed mechanism addresses.
2. Evaluate it against every case naming that mechanism and at least one case
   it should leave unchanged.
3. Record false positives: valuable exploratory behavior it might suppress.
4. Reject mechanisms whose only success is a larger form, more approvals, or
   a proxy score with no decision consequence.
5. Activate changes only by reviewed, version-controlled edits.

A useful mechanism changes the required decision at the boundary while leaving
free conjecture formation untouched. Runtime self-modification and automatic
promotion are forbidden.
