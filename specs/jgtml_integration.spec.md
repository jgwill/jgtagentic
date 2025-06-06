# jgtml Integration Recommendations

This spec outlines how jgtagentic should depend on the `jgwill/jgtml` package and
what enhancements are expected as the Fractal Trading System evolves.

## Recommended Version
- Use **jgtml >=0.0.304** which includes the latest fractal detection utilities.

## Integration Notes
- Import scanning functions via `from jgtml import fdb_scanner_2408` as outlined in `.github/instructions/jgtAgenticPyDev.instructions.md`.
- jgtml should provide GPU-accelerated scanning when available; integration code
  should allow optional CuPy/PolarsGPU backends as described in the FTS Enhancement Blueprint.
- Ensure jgtml exports helpers for QuestDB and Pinecone so that scan results can
  be persisted according to `fractal-database.spec.md`.

## Future Considerations
- Monitor jgtml releases for reinforcement-learning hooks that expose signal
  validity metrics. These should map into the RL modules defined in
  `reinforcement-learning.spec.md`.
- Provide CLI flags or config options to toggle high-performance modes so FTS can
  maintain sub-100ms latency targets.
