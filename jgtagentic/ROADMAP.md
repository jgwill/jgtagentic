# jgtagentic Roadmap

## Current State (v0.5.0)
- ✅ Autonomous from SANDBOX  
- ✅ Basic regime detection (ADX/EMA)
- ✅ Multi-factor scoring (MFI, zones, alligator, ADX, HTF)
- ✅ Data loader for jgt-data-server integration
- ✅ Decision engine (TRADE/SKIP/WAIT)

## Limitations
The current regime detection uses **ADX/EMA** which is NOT aligned with Williams methodology. This is a basic placeholder that misses the core trading philosophy.

## Williams 5 Dimensions Integration (Future)

Per *New Trading Dimensions* by Bill Williams and Medicine Wheel Trading Framework:

### 1. Alligator as Primary Regime Filter
**Replace ADX/EMA with Alligator (Jaw/Teeth/Lips)**
- Jaw (13-bar SMMA, offset +8): Balance Line for current timeframe
- Teeth (8-bar SMMA, offset +5): Balance Line for lower TF
- Lips (5-bar SMMA, offset +3): Balance Line for lowest TF

**States:**
- SLEEPING: Lines intertwined → NO TRADES (70-85% of time)
- EATING: Lines fanned out → ACTIVE TRADING (15-30% of time)
- SATED: Lines converging → EXIT SIGNALS

**Rule:** "Is the Alligator sleeping? If yes, wait."

### 2. The 5 Dimensions
**Dimension 1: Fractals** (EAST - Vision/Signal Detection)
- First entry signal - breakout from range
- Must occur OUTSIDE Alligator's Teeth (red line)
- Buy Stop 1 tick above Up Fractal / Sell Stop 1 tick below Down Fractal

**Dimension 2: Awesome Oscillator (AO)** (NORTH - Momentum)
- SMA(5) - SMA(34) of midpoint
- Saucer, Zero Cross, Twin Peaks signals
- Add to positions when momentum confirms

**Dimension 3: Accelerator (AC)** (NORTH - Acceleration)
- AO - SMA(AO, 5)
- Early warning system (changes before AO and price)
- Rule: Don't buy if AC is Red, don't sell if AC is Green

**Dimension 4: Zone Trading** (WEST - Aggressive Pyramiding)
- Green Zone: AO Green + AC Green → Add buys
- Red Zone: AO Red + AC Red → Add sells  
- Stop after 5 consecutive bars (exhaustion)

**Dimension 5: Balance Line** (SOUTH - Pullback Entries)
- Price vs Alligator lines
- Base bar + higher highs (buy) / lower lows (sell)
- Different confirmations based on price position vs Balance Line

### 3. Medicine Wheel Alignment

| Direction | Dimension | Function | Current Status |
|-----------|-----------|----------|----------------|
| EAST | Fractals | Signal detection | ❌ Need fractal detector |
| SOUTH | Balance Line | Wave/HTF analysis | ⚠️ Partial (alligator in scorer) |
| WEST | Zones | Risk/pyramiding | ⚠️ Partial (zone scoring) |
| NORTH | AO/AC | Execution momentum | ❌ Need AO/AC calculation |

### 4. Integration Strategy

**Phase 1: Alligator Regime**
- Replace `RegimeDetector.calculate_adx()` with `calculate_alligator()`
- Change regime states: TRENDING/RANGING → SLEEPING/EATING/SATED
- Update decision logic to reject all signals when Alligator sleeping

**Phase 2: Williams Indicators**
- Add `williams.py` module with:
  - `calculate_fractals(df)` → Up/Down fractals
  - `calculate_ao(df)` → Awesome Oscillator
  - `calculate_ac(df)` → Accelerator
  - `detect_zones(df)` → Green/Red/Gray zones
  - `find_balance_line_signals(df)` → Base bar + confirmations

**Phase 3: Integrated Scoring**
- Update `SignalScorer` to use Williams dimensions
- Weight by dimension alignment (all 5 aligned = highest score)
- Fractal REQUIRED as first entry (mandatory ticket)

**Phase 4: Decision Ceremony**
- Follow Williams checklist:
  1. Is Alligator sleeping? → SKIP
  2. Has Fractal triggered outside mouth? → First entry
  3. AO/AC signals → Add to position
  4. Zone alignment? → Aggressive pyramiding (max 5 bars)
  5. Balance Line pullback? → Re-entry
  6. Protection: Red Line stop (standard) / Green Line stop (runaway)

### 5. Data Requirements
**From jgt-data-server:**
- High, Low, Close columns (for Alligator midpoint calculations)
- Existing: jaw, teeth, lips columns (if pre-calculated in CDS)
- Existing: ao, ac columns (if pre-calculated in CDS)
- Existing: fh, fl columns (fractal high/low)

**Fallback:** Calculate on-the-fly if not in CDS

## Next Steps
1. Read Williams 5 Dimensions more carefully
2. Study existing jgtml CDS columns for Williams indicators
3. Design `williams.py` module API
4. Refactor `RegimeDetector` → `AlligatorRegime`
5. Test with backtest data from SANDBOX experiments
