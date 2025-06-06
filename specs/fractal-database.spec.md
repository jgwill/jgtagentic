# Fractal Database Integration Plan

This specification describes how the upcoming Fractal Trading System (FTS) repository will supply database schemas and how those assets should integrate with the `jgtagentic` codebase.

## Expected Deliverables

- SQL or ORM schema definitions for fractal patterns, indicator values and signals.
- Data access modules or services for querying and persisting fractal data.
- Example datasets for initial testing.

## Integration Steps

1. **Directory Placement**
   - Database schemas will live under `src/ftsdb/` within this repository.
   - Data access utilities will form a Python package `ftsdb` for reuse by agents.

2. **Dependencies**
   - If an ORM is supplied (e.g., SQLAlchemy), add it to `requirements.txt` and update `pyproject.toml`.
   - Provide migration scripts if needed using `alembic` or similar.

3. **Impact**
   - New modules will expand the Python package layout.
   - Tests under `tests/ftsdb/` will validate schema integrity and query logic.

4. **Collaboration Notes**
   - The FTS repository should provide schema diagrams and field descriptions matching the draft in `src/ftsds/data/export-FTSKnower23/cleared_POE_Today_231114b.md`.
   - Each table or model will be documented with examples in the Jupyter Book docs.

