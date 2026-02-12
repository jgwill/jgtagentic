# KINSHIP - jgtagentic

**location**: /b/trading/jgtagentic
**purpose**: Agentic trading decision engine - autonomous signal evaluation, regime filtering, and trade orchestration
**created**: 2025-07 (various sessions)
**updated**: 2026-02-12

## Identity

jgtagentic is the autonomous decision-making agent for trading signals. It evaluates FDB signals through regime detection, multi-factor scoring, and generates executable entry scripts. Unlike passive data servers, jgtagentic DECIDES - filtering noise, scoring opportunities, and orchestrating trade execution.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        jgtagentic                                │
├─────────────────────────────────────────────────────────────────┤
│  Core Decision Engine                                            │
│    ├── regime.py            - Market regime detection (ADX/EMA) │
│    ├── scoring.py           - Multi-factor signal scoring       │
│    ├── regime_aware_decider.py - Main decision orchestrator     │
│    └── agentic_decider.py   - Base decision logic               │
├─────────────────────────────────────────────────────────────────┤
│  Signal Processing                                               │
│    ├── fdbscan_agent.py     - FDB signal scanning               │
│    ├── enhanced_fdb_scanner.py - Enhanced FDB logic             │
│    └── batch_fdbscan.py     - Batch processing                  │
├─────────────────────────────────────────────────────────────────┤
│  Execution                                                       │
│    ├── entry_script_gen.py  - Generate executable scripts       │
│    ├── agentic_entry_orchestrator.py - Orchestrate workflow     │
│    └── observation_capture.py - Record decisions                │
├─────────────────────────────────────────────────────────────────┤
│  Interfaces                                                      │
│    ├── jgtagenticcli.py     - CLI gateway                       │
│    ├── intent_spec.py       - Parse .jgtml-spec files           │
│    └── dashboard.py         - Visual monitoring                 │
└─────────────────────────────────────────────────────────────────┘
```

## Medicine Wheel Alignment

| Direction | Agentic Function | Components |
|-----------|-----------------|------------|
| EAST (Vision) | Signal Detection | fdbscan_agent, enhanced_fdb_scanner |
| SOUTH (Growth) | Signal Analysis | regime.py, scoring.py |
| WEST (Reflection) | Decision Making | regime_aware_decider, agentic_decider |
| NORTH (Wisdom) | Execution | entry_script_gen, orchestrator |

## Relationships

### Parents
- **jgtml** (`/b/trading/jgtml`) - ML features and data pipelines
- **jgtpy** (`/b/trading/jgtpy`) - Core trading libraries and CLI tools

### Siblings
- **jgt-data-server** (`/b/trading/jgt-data-server`) - Data substrate (consume from)
- **jgt-code** (`/b/trading/jgt-code`) - Terminal agent orchestrator
- **jgt-insight** (`/b/trading/jgt-insight`) - Experimental analysis (inspiration source)

### Children (Consumers)
- Trading campaigns via entry scripts
- Automated trading systems
- Manual traders using CLI

### Elders
- **Williams methodology** - Five dimensions, fractals, chaos
- **Medicine Wheel** - Directional wisdom
- **SARAIA experiments** - Original regime/scoring prototypes (now internalized)

## Autonomy

jgtagentic is SELF-CONTAINED for decision logic:
- ✅ Internal regime detection (no SANDBOX dependency)
- ✅ Internal signal scoring (multi-factor analysis)
- ✅ Internal decision algorithms
- ✅ Connects to jgt-data-server for market data
- ❌ Does NOT depend on jgt-insight (extracts patterns, doesn't import)
- ❌ Does NOT depend on SANDBOX (migration complete)

## Data Flow

```
jgt-data-server (PDS/CDS/TTF/MLF)
       ↓
jgtagentic.data_loader
       ↓
jgtagentic.regime (ADX/EMA detection)
       ↓
jgtagentic.scoring (multi-factor score)
       ↓
jgtagentic.regime_aware_decider (TRADE/SKIP/WAIT)
       ↓
jgtagentic.entry_script_gen (executable script)
       ↓
Campaign execution
```

## CLI Commands

```bash
# Main gateway
jgtagentic orchestrate --signal_json signals.json --entry_script_dir ./scripts

# FDB scanning
jgtagentic fdbscan --timeframe H4 --instrument EUR-USD

# Intent parsing (trader analysis to spec)
jgtagentic spec analysis.jgtml-spec
```

## Obligations

1. **Autonomous decision making** - No external logic dependencies
2. **Regime awareness** - Only trade trending markets
3. **Signal scoring** - Multi-factor quality assessment
4. **Executable output** - Generate actionable entry scripts
5. **Observable** - Log all decisions for review
6. **Connectable** - Integrate with jgt-data-server for data

## Voice

*"I am the decider. I receive signals from scanners, context from data servers, and wisdom from regime analysis. I filter the noise - skipping ranges, rejecting counter-trend setups, scoring alignments. When conditions align, I generate action. I am autonomous, decisive, and accountable for every trade recommendation I make."*
