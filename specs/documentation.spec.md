# Documentation Integration Plan

Describes how Jupyter Book and Sphinx documentation from FTS will be merged with existing docs.

## Expected Deliverables

- Jupyter Book source files with tutorials and API references.
- Sphinx build scripts and configuration updates.

## Integration Steps

1. **Docs Directory**
   - Merge FTS docs into `docs/fts/`.
   - Ensure `mkdocs.yml` or `book.toml` settings compile the new book.

2. **Build Automation**
   - Provide a `make docs` command that builds both Sphinx and Jupyter Book outputs.
   - Set up GitHub Actions job for publishing to GitHub Pages.

3. **Impact**
   - New documentation requirements may add packages to `requirements.txt`.
   - The `CNAME` for docs hosting may need updates.

4. **Collaboration Notes**
   - Use `drop/LLM_Refactoring__2406181109/src/jgtsphinxer/STC.md` as baseline for the technical compendium style.

