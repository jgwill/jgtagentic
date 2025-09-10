# Technical Integration Plan

This specification details the overarching technical modifications required to merge the FTS repository into `jgtagentic`.

## Expected Deliverables

- Refactored modules from `src/xpto231120v4.lua` translated into Python packages.
- Automated test suites for new components.
- CI/CD configurations for linting, testing, and deployment.

## Integration Steps

1. **Repository Layout**
   - Consolidate new packages under `src/fts/` (e.g., `ftsdb`, `ftsrl`, `ftsauto`, `ftsworkflow`).
   - Update `pyproject.toml` and `setup.py` to expose any new console scripts.

2. **Testing and CI**
   - Extend `pytest.ini` with coverage for FTS modules.
   - Add GitHub Actions workflows to run tests and docs builds.

3. **Coding Standards**
   - Follow existing linting rules and pre-commit hooks.
   - Ensure documentation builds without warnings.

4. **Collaboration Notes**
   - Coordinate with FTS developers to align naming conventions and packaging structure.
   - Provide migration guide from the Lua scripts if necessary.

