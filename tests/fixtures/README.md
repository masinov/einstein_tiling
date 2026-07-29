# Immutable fixtures

`polykites-n8.sqlite` is the checked-in control snapshot formerly stored as
`data/shapes.sqlite`.

- SHA-256: `6956f7c90f6bceae1b63678e8bb86d6df0cf90ce59b2f8db072188850d7c27b9`
- shapes: 1,264
- cell-count range: 1 through 8
- verdict rows: 2,391 (`A1-torus`, `A2-heesch`, `A3-patch`)

The fixture is read-only evidence for tests and known-system reproduction.  A
mutable funnel run continues to use the ignored path `data/shapes.sqlite`.
