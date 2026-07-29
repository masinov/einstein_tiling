# Frozen research runners

This directory contains one-off runners and probes from closed or frozen
research branches. They remain executable provenance, not active search
entry points.

`MANIFEST.json` records each former path, current path, original SHA-256 and
post-relocation SHA-256. Script bodies were not refactored; only repository-root
and self-usage paths were adjusted for the extra directory level.

Ninety-two scripts with no live Python caller, import or test-path contract
were moved here. Nine coupled historical scripts remain at `scripts/` until
their consumers are removed or redirected. Do not resume a parameter ladder
from this directory merely because its runner remains executable.
