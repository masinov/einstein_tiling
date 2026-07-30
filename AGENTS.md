# Repository research instructions

Read and follow `CLAUDE.md`; its research-governance rules apply to every
agent, regardless of agent brand or interface.

In particular, do not write or launch a nontrivial experiment until its ready
proposal has a separate hash-pinned human admission record and passes
`scripts/check_experiment_gate.py`. Launch the exact frozen command through
`scripts/run_research.py`. User-supplied prior-art facts are halt conditions
until recorded and resolved against primary sources.
