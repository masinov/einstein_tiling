# Human admission records

Admission is separate from proposal authorship. An agent may prepare a
proposal and mark it `ready`; it may not authorize its own proposal.

After explicit human approval, add one record named `<proposal-id>.json` from
[`TEMPLATE.json`](TEMPLATE.json). The record pins the exact proposal bytes and
states the authorized scope and the human authorization reference. The gates
reject a missing, revoked, moved, edited, or mismatched record.

Admission does not establish truth, novelty, or a result. It only authorizes
the bounded commitment described by those exact proposal bytes.
