"""Claim taxonomy for Receipts.

Every atomic claim gets exactly one type, which decides its verification path:

- tech: a technology, tool, architecture, or implementation fact that could in
  principle be checked against code evidence (repos, dependency files, READMEs).
  Only these proceed to retrieval + NLI.
- quantitative: contains a number, percentage, or measured outcome (e.g.
  "reduced response times by 62%"). Code evidence almost never proves these,
  so they are auto-flagged "unverifiable" — an honest verdict, not a failure.
- soft: leadership, collaboration, communication, process (e.g. "led a 3-person
  team", "authored documentation for non-technical staff"). Unverifiable from
  code by definition.

A claim that mixes types is split by the decomposer; if a single atom still
mixes a number with a tech fact ("built a 15-route REST API"), it is typed
quantitative when the number is the load-bearing assertion, tech when the
number is incidental scale.
"""

TECH = "tech"
QUANTITATIVE = "quantitative"
SOFT = "soft"

CLAIM_TYPES = (TECH, QUANTITATIVE, SOFT)
