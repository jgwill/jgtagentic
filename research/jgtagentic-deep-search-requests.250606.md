# JGTAgentic Deep-Search Requests (2025-06-06)

This document collects deep search requests to support integration of the Fractal Trading System (FTS) with the jgtagentic repository. Each section outlines an area where additional background research or code examples would assist future development.

## 1. Database Integration
- Clarify structure and fields of fractal pattern tables from `cleared_POE_Today_231114b.md`.
- Provide SQLAlchemy examples for representing fractal patterns and indicator values.
- Research best practices for migrating from existing prototypes to SQL-based storage.
- Explore dataset sources for initial fractal entries.

## 2. Reinforcement Learning Framework
- Gather sample reward functions aligning with trading outcomes.
- Provide pseudocode for RL agents evaluating sequential signals.
- Research techniques for parameter optimization across multiple indicators.
- Identify small open-source datasets suitable for RL experimentation.

## 3. Automated Use Cases
- Investigate cross-timeframe scanning strategies and how they feed into trade decisions.
- Review backtesting frameworks for Python-based trading bots.
- Provide example scripts for real-time market monitoring and alert generation.
- Explore risk management approaches that integrate with RL feedback.

## 4. Seven-Step Workflow
- Summarize data collection best practices for market data at multiple timeframes.
- Detail feature engineering methods for fractal extraction.
- Describe potential visualization techniques for step 5 "Action Material Generation".
- Review continuous learning pipelines that adapt trading models over time.

## 5. Documentation Strategy
- Collect references on building combined Jupyter Book and Sphinx documentation.
- Provide examples of CI workflows publishing docs to GitHub Pages.
- Research interactive visualization tools that integrate with Jupyter Book for trade analysis.

## 6. CLI and Orchestrator Patterns
- Investigate Python patterns for modular CLI tools with subcommands.
- Provide examples of orchestration flows coordinating multiple agents.
- Explore logging frameworks for capturing results from CLI-driven workflows.

---

Each deep-search result should return concise references and code snippets where possible. They will inform updates to the `.spec.md` files and guide the implementation of the FTS components.
