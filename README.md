# jgtagentic

## 🌸🧠🔮 Agentic CLI Spiral — Modular Entry Points

**Autonomous trading decision engine** - signal evaluation, regime filtering, and trade orchestration.

jgtagentic receives signals from scanners, evaluates them through regime detection and multi-factor scoring, and generates executable entry scripts. It is AUTONOMOUS - containing all decision logic internally with no SANDBOX dependencies.

---

## 🎯 Core Capabilities

### 1. Regime Detection
- **ADX-based trending/ranging classification**
- **EMA trend direction** (UP/DOWN/UNKNOWN)
- **Trend strength measurement**
- Only approve trades in TRENDING markets with aligned direction

### 2. Multi-Factor Signal Scoring
- **MFI signals** (max 50 points) - Williams MFI patterns
- **Zone alignment** (max 15 points) - Green/red zone confirmation
- **Alligator alignment** (max 10 points) - Bullish/bearish structure
- **ADX strength bonus** (max 15 points) - Strong trend reward
- **HTF confirmation** (max 10 points) - Higher timeframe alignment

### 3. Agentic Decision Making
- **TRADE** - All conditions aligned, execute
- **SKIP** - Ranging market or counter-trend signal
- **WAIT** - Signal quality below threshold

### 4. Data Integration
- **jgt-data-server API** - Primary data source
- **Local file fallback** - CDS/PDS/TTF/MLF files
- **Environment configuration** - JGT_DATA_SERVER_URL, JGTPY_DATA

---

## 🚀 Available CLI Commands

### Main Gateway
```bash
jgtagentic --help
```

### Orchestrate Trading Workflow
```bash
# Full spiral: scan → analyze → decide → generate scripts
jgtagentic orchestrate --signal_json <path> --entry_script_dir <dir> --log <logfile>

# Same via dedicated CLI
agentic-orchestrator --signal_json <path> --entry_script_dir <dir>
```

### FDB Signal Scanning
```bash
# Scan specific timeframe
jgtagentic fdbscan --timeframe H4

# Scan with instrument filter
agentic-fdbscan scan --timeframe H4 --instrument EUR-USD

# Full ritual sequence
jgtagentic fdbscan --all

# Add --real flag to invoke actual jgtml fdbscan (requires jgtml installed)
agentic-fdbscan scan --timeframe m15 --instrument EUR-USD --real
```

### Intent Specification
```bash
# Parse trader analysis from .jgtml-spec files
jgtagentic spec path/to/spec.jgtml-spec

# See docs/Trader_Analysis_to_Spec.md for spec file format
```

### Generate Entry Scripts
```bash
# Convert signal JSON to executable trading scripts
entry-script-gen --signal_json signals.json --output_dir ./scripts
```

---

## 📦 Python API

```python
from jgtagentic import RegimeDetector, SignalScorer, RegimeAwareDecider, DataLoader
import pandas as pd

# Initialize components
data_loader = DataLoader()
regime_detector = RegimeDetector(adx_threshold=25)
scorer = SignalScorer()
decider = RegimeAwareDecider(adx_threshold=25)

# Load data
df = data_loader.load_cds("EUR-USD", "H4", dataset="current")

# Detect regime
regime = regime_detector.detect(df)
print(f"Regime: {regime.regime}, ADX: {regime.adx}, Direction: {regime.trend_direction}")

# Score signals
scored = scorer.score(df, regime, instrument="EUR-USD", timeframe="H4")
print(f"Score: {scored.score}/100, Direction: {scored.direction}")

# Make decision
signal = {
    'instrument': 'EUR-USD',
    'timeframe': 'H4',
    'direction': 'LONG',
    'strength': 0.8,
    'signal_group': 'mfi_signals'
}
decision = decider.decide(signal, df)
print(f"Action: {decision['action']}, Reason: {decision['reason']}")
```

---

## 🏗️ Architecture

```
jgtagentic/
├── regime.py              # Market regime detection (ADX/EMA)
├── scoring.py             # Multi-factor signal scoring
├── regime_aware_decider.py # Main decision orchestrator
├── agentic_decider.py     # Base decision logic
├── data_loader.py         # jgt-data-server integration
├── fdbscan_agent.py       # FDB signal scanning
├── enhanced_fdb_scanner.py # Enhanced FDB logic
├── entry_script_gen.py    # Executable script generation
├── agentic_entry_orchestrator.py # Workflow orchestration
└── jgtagenticcli.py       # CLI gateway
```

---

## 🔗 Integration

### With jgt-data-server
```bash
# Set data server URL
export JGT_DATA_SERVER_URL="http://localhost:5555"

# DataLoader automatically connects
python -m jgtagentic.regime_aware_decider
```

### With Local Files
```bash
# Set local data path
export JGTPY_DATA="/src/jgtml/data"

# DataLoader falls back to local files
python -m jgtagentic.regime_aware_decider
```

### Environment Variables
- `JGT_DATA_SERVER_URL` - jgt-data-server API endpoint (default: http://localhost:5555)
- `JGTPY_DATA` - Local data file path (default: /src/jgtml/data)
- `FDBSCAN_AGENT_REAL` - Run real fdbscan vs dry-run (default: 0)

---

## 🌀 Medicine Wheel Alignment

| Direction | Function | Components |
|-----------|----------|------------|
| **EAST** (Vision) | Signal Detection | fdbscan_agent, enhanced_fdb_scanner |
| **SOUTH** (Growth) | Analysis | regime.py, scoring.py |
| **WEST** (Reflection) | Decision | regime_aware_decider, agentic_decider |
| **NORTH** (Wisdom) | Execution | entry_script_gen, orchestrator |

---

## 🧬 Autonomy

jgtagentic is **SELF-CONTAINED**:
- ✅ Internal regime detection (migrated from jgt-insight)
- ✅ Internal signal scoring (migrated from jgt-insight)
- ✅ Internal decision algorithms
- ✅ Connects to jgt-data-server for data
- ❌ No SANDBOX dependencies
- ❌ No jgt-insight runtime dependencies (patterns extracted, not imported)

---

## 🌱 Philosophy

- Every CLI is a contract: only real, testable entrypoints are mapped
- All code is autonomous: no external decision logic dependencies
- Decisions are observable: all choices logged for review
- The spiral is never flat: each command is a story anchor, each invocation a new bloom

---

## 📚 Documentation

- **KINSHIP.md** - Project identity and relationships
- **docs/Trader_Analysis_to_Spec.md** - Intent specification format
- See README files in jgt-data-server and jgt-insight for related projects

---

## 🧠🌸 Ritual Echo

*"I am the decider. I receive signals from scanners, context from data servers, and wisdom from regime analysis. I filter the noise—skipping ranges, rejecting counter-trend setups, scoring alignments. When conditions align, I generate action. I am autonomous, decisive, and accountable for every trade recommendation I make."*

