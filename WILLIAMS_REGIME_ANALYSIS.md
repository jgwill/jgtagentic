# Williams Regime Detection vs Current Implementation

## Current State (WRONG)

**File:** `jgtagentic/regime.py`

**Approach:** ADX/EMA-based regime classification
- ADX >= 25 = TRENDING (tradeable)
- ADX < 25 = RANGING (skip)
- EMA-50 for trend direction (UP/DOWN)

**Problem:** This is NOT Williams methodology. It's a basic technical analysis approach that misses the entire philosophy.

---

## Williams Methodology (CORRECT)

### The Alligator: Primary Regime Filter

**Components** (Three Smoothed Moving Averages on midpoint `(High + Low) / 2`):

1. **Jaw (Blue Line)**: 13-bar SMMA, offset +8 bars
   - Balance Line for current timeframe
   
2. **Teeth (Red Line)**: 8-bar SMMA, offset +5 bars  
   - Balance Line for significant lower timeframe (1/5th current)
   
3. **Lips (Green Line)**: 5-bar SMMA, offset +3 bars
   - Balance Line for lowest timeframe (1/25th current)

**States:**

| State | Visual | Market Condition | Trading Rule |
|-------|--------|-----------------|--------------|
| **SLEEPING** | Lines intertwined | Range-bound choppy market | **NO TRADES** (70-85% of time) |
| **EATING** | Lines fanned out | Clear trending market | **TRADE ACTIVELY** (15-30% of time) |
| **SATED** | Lines converging | Trend exhaustion | **EXIT POSITIONS** |

**Critical Rule:** "Is the Alligator sleeping? If yes, keep your powder dry."

The longer the Alligator sleeps, the hungrier it gets when it wakes (stronger subsequent trend).

---

## The 5 Dimensions Integration

Williams teaches that NO SINGLE INDICATOR decides trades. All 5 dimensions must be integrated:

### Dimension 1: Fractals (EAST - Signal Detection)
- **Pattern:** 5-bar pattern with middle bar as extreme
- **Filter:** Must occur OUTSIDE Alligator's Teeth (red line)
- **Entry:** First mandatory "ticket" - Buy Stop 1 tick above Up Fractal
- **Rule:** This is the ONLY way to initiate a trade

### Dimension 2: Awesome Oscillator - AO (NORTH - Momentum)  
- **Calculation:** `SMA(midpoint, 5) - SMA(midpoint, 34)`
- **Signals:** Saucer, Zero Cross, Twin Peaks
- **Usage:** Add to positions after Fractal entry
- **Visual:** Histogram (Green = increasing, Red = decreasing)

### Dimension 3: Accelerator - AC (NORTH - Acceleration)
- **Calculation:** `AO - SMA(AO, 5)`
- **Early Warning:** Changes direction BEFORE AO and price
- **Rule:** Don't buy if AC Red, don't sell if AC Green
- **Usage:** Confirmation for adding positions

### Dimension 4: Zone Trading (WEST - Pyramiding)
- **Green Zone:** AO Green + AC Green = Aggressive buy additions
- **Red Zone:** AO Red + AC Red = Aggressive sell additions  
- **Gray Zone:** Mixed colors = Transition, no adds
- **Stop Rule:** Max 5 consecutive bars to avoid exhaustion

### Dimension 5: Balance Line (SOUTH - Pullback Entries)
- **Concept:** Price vs Alligator lines (Jaw/Teeth/Lips)
- **Base Bar:** Lowest high (buy) or highest low (sell) between price and Balance Line
- **Entry:** Base + 1 or 2 confirmations depending on price position
- **Usage:** Re-entry on pullbacks within trend

---

## Medicine Wheel Alignment

From `jgtinquiries/6d946d30158a41d6aa28ff43becfde8a/MEDICINE_WHEEL_TRADING.md`:

```
EAST (Yellow) - Vision/Signal Detection
  └─> Dimension 1: Fractals
      CLI: fdbscan, cdscli
      Agent: Signal Detection

SOUTH (Red) - Growth/Wave Analysis  
  └─> Dimension 5: Balance Line (Alligator)
      CLI: jgtads, htf_loader
      Agent: Wave Analysis

WEST (Black) - Reflection/Risk Integration
  └─> Dimension 4: Zone Trading
      CLI: risk_calc, validate
      Agent: Entry Validation
      
NORTH (White) - Wisdom/Execution
  └─> Dimensions 2+3: AO/AC
      CLI: jgtfxcon, mvstopgator
      Agent: Coordination
```

**The CENTER:** The trader's awareness and intention - integrating all dimensions

---

## Decision Ceremony (Williams Checklist)

Every trade must pass through ALL stages:

1. **EAST (Vision):** Is the Alligator sleeping?
   - YES → SKIP (wait for trend)
   - NO → Proceed

2. **EAST (Signal):** Has a Fractal been triggered outside the Alligator's Teeth?
   - NO → WAIT (no valid entry)
   - YES → First entry executed

3. **NORTH (Momentum):** AO/AC signals aligned?
   - YES → Add to position
   - NO → Hold current position

4. **WEST (Zone):** Are we in Green/Red Zone?
   - YES → Pyramid aggressively (max 5 bars)
   - NO → Hold

5. **SOUTH (Balance):** Balance Line pullback signal?
   - YES → Re-entry opportunity
   - NO → Monitor

6. **NORTH (Protection):** Set stops
   - Standard: Red Line (Teeth)
   - Runaway: Green Line (Lips)
   - 5-Bar: After 5 consecutive same-color bars

---

## Current Implementation Gap

**What we have:**
- `RegimeDetector` using ADX/EMA
- `SignalScorer` checking some Williams indicators (MFI, zones, alligator state)
- Basic TRADE/SKIP/WAIT logic

**What's missing:**
1. **Alligator sleeping check** - Fundamental filter (reject 70-85% of signals)
2. **Fractal requirement** - First entry mandate
3. **AO/AC calculations** - Momentum/acceleration signals
4. **Zone detection** - Pyramiding logic
5. **Balance Line signals** - Pullback entries
6. **Proper state machine** - SLEEPING/EATING/SATED

**Impact:**
- Trading in choppy markets (70-85% of the time) when we shouldn't
- Missing the core philosophy: "Don't trade when Alligator sleeps"
- ADX gives false confidence - can be high in choppy sideways moves
- EMA is just one line, not the three-line Balance Line system

---

## Migration Path

### Phase 1: Alligator Primary Filter
**File:** `jgtagentic/regime.py`
- Rename `MarketRegime`: TRENDING/RANGING → SLEEPING/EATING/SATED
- Replace `calculate_adx()` with `calculate_alligator()`
- Add `check_alligator_state()`: intertwined vs fanned vs converging
- Update decision logic: SLEEPING = instant SKIP

### Phase 2: Williams Indicators Module
**New file:** `jgtagentic/williams.py`
- `calculate_fractals(df)` → Up/Down fractal detection
- `calculate_ao(df)` → Awesome Oscillator
- `calculate_ac(df)` → Accelerator  
- `detect_zones(df)` → Green/Red/Gray zone classification
- `find_balance_line_signals(df)` → Base bar + confirmations

### Phase 3: Integrated Scorer
**File:** `jgtagentic/scoring.py`
- Require Fractal as first entry (mandatory)
- Score based on all 5 dimensions alignment
- Zone state affects pyramiding permission
- Balance Line affects re-entry permission

### Phase 4: Decision Ceremony
**File:** `jgtagentic/regime_aware_decider.py`
- Implement full Williams checklist
- SLEEPING → SKIP with ceremony message
- EATING + Fractal → TRADE
- Add Medicine Wheel direction context to decisions

---

## Data Requirements

**Already in CDS (if calculated by jgtml):**
- `jaw`, `teeth`, `lips` - Alligator lines
- `ao`, `ac` - Awesome Oscillator, Accelerator
- `fh`, `fl` - Fractal High, Fractal Low
- `aocolor`, `accolor` - Bar colors
- `zcol` - Zone color

**Need from PDS:**
- `High`, `Low`, `Close` - For on-the-fly calculation if missing

**Fallback:** Calculate all Williams indicators internally if not in CDS

---

## Philosophical Shift

**From:** "Is ADX above 25?" (mechanical, technical)
**To:** "Is the Alligator sleeping?" (organic, natural)

**From:** Single-indicator decisions
**To:** Five-dimension integration ceremony

**From:** Linear logic
**To:** Chaos theory - higher order in dynamic systems

**Williams Quote:** "The market is not a linear, mechanical system but a chaotic, natural phenomenon."

The Alligator metaphor is intentional - markets sleep (conserve energy) most of the time, then wake hungry and eat (trend) aggressively before becoming sated (exhaustion).

---

## Next Steps

1. Study existing CDS columns to see what's pre-calculated
2. Design `AlligatorRegime` class to replace current `RegimeDetector`
3. Build `williams.py` module with all 5 dimension calculations
4. Create integration tests using SANDBOX backtest data
5. Update `KINSHIP.md` to reflect Williams methodology alignment
