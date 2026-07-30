# Machine contracts

The structural JSON contracts are separated by boundary:

- `research_program.schema.json` — sustained mathematical commitment;
- `experiment.schema.json` — one reproducibly pinned computation;
- `promotion.schema.json` — candidate, theorem, method, or novelty promotion;
- `admission.schema.json` — human authorization of exact proposal bytes; and
- `run_result.schema.json` — supervisor-owned execution record.

All proposal variants share `research_proposal.schema.json`. The Python
validator implements the same field and discriminator contract and adds
repository-semantic checks that JSON Schema cannot supply: portfolio
membership, literature-catalog membership, path containment, file hashes,
admission hashes, Git state, and executable-version output. Provenance tests
pin the shared enums and nested required fields so the published schema cannot
silently lag the executable validator.
