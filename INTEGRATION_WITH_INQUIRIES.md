# Integration with jgtinquiries Medicine Wheel Framework

## Source Material

**Primary Sources:**
- `docs/Williams_New_Trading_Dimensions.2601231517.md` - Williams methodology
- `jgtinquiries/6d946d30158a41d6aa28ff43becfde8a/MEDICINE_WHEEL_TRADING.md` - Framework
- `jgtinquiries/6d946d30158a41d6aa28ff43becfde8a/KINSHIP.md` - Inquiry identity

**Inquiry UUID:** `6d946d30158a41d6aa28ff43becfde8a`
**Topic:** Medicine Wheel Trading Framework development

---

## Four Directions Mapping

### EAST (Yellow) - Vision & Inquiry

**Element:** Air
**Season:** Spring  
**Time:** Dawn, Market Open
**Question:** "What signals are emerging?"

**Williams Dimension:** Fractals (Dimension 1)
- Breakout signals from range
- First mandatory entry ticket
- Pattern recognition
- FDB (Fractal Divergence Bar) scanning

**jgtagentic Components:**
- `enhanced_fdb_scanner.py` - Fractal detection
- `fdbscan_agent.py` - Automated scanning
- `batch_fdbscan.py` - Multi-timeframe
- `data_loader.py` - CDS signal data loading

**Ceremony:** Smudging (clearing previous energy)
- Clear previous trade state
- Prepare for new signal detection
- Run fresh FDB scan
- Map emerging fractal patterns

**CLI Tools:**
- `fdbscan` - Scan for fractal signals
- `cdscli` - Generate signal data

**Decision Flow:**
```
EAST Entry:
  └─> Is Alligator sleeping?
      ├─> YES: SKIP (keep powder dry)
      └─> NO: Check for Fractal outside Teeth
          ├─> YES: PROCEED to SOUTH
          └─> NO: WAIT for valid fractal
```

---

### SOUTH (Red) - Growth & Embodiment  

**Element:** Fire
**Season:** Summer
**Time:** Midday
**Question:** "Where are we in the structure?"

**Williams Dimension:** Balance Line (Dimension 5)
- Alligator Jaw/Teeth/Lips as Balance Lines
- Multi-timeframe alignment
- Wave position (Elliott Wave)
- HTF (Higher Timeframe) confluence

**jgtagentic Components:**
- `regime.py` - Should implement Alligator Balance Line
- `scoring.py` - HTF bonus evaluation
- `data_loader.py` - TTF (cross-timeframe) data

**Ceremony:** Youth Mentorship (growth in the structure)
- Count wave position (Elliott Wave)
- Check HTF alignment (W1→D1→H4→H1→M15)
- Identify Balance Line pullbacks
- Assess trend maturity

**CLI Tools:**
- `jgtads` - Alligator display/state
- `htf_loader` - Higher timeframe data
- `ttfcli` - Cross-timeframe features

**Decision Flow:**
```
SOUTH Analysis:
  └─> Fractal triggered (from EAST)
      └─> Check Balance Line position
          ├─> Price above Jaw: Strong uptrend
          ├─> Price between lines: Transition
          └─> Price below Lips: Strong downtrend
              └─> HTF aligned?
                  ├─> YES: PROCEED to WEST
                  └─> NO: Lower quality score
```

---

### WEST (Black) - Reflection & Integration

**Element:** Water  
**Season:** Fall
**Time:** Dusk
**Question:** "Is this aligned with wisdom?"

**Williams Dimension:** Zone Trading (Dimension 4)
- Green Zone (AO+AC Green) = Aggressive buys
- Red Zone (AO+AC Red) = Aggressive sells
- Zone confluence with other signals
- Risk assessment via zone state

**jgtagentic Components:**
- `scoring.py` - Zone alignment scoring
- `agentic_decider.py` - Risk assessment logic
- `regime_aware_decider.py` - Zone-aware decisions

**Ceremony:** Talking Circles (review with all agents)
- Review signal quality across dimensions
- Assess zone alignment  
- Calculate position sizing based on zone strength
- Validate entry/stop prices
- Risk/reward calculation

**CLI Tools:**
- `risk_calc` - Position sizing
- `validate` - Entry validation
- `zone_check` - Zone state assessment

**Decision Flow:**
```
WEST Reflection:
  └─> Fractal + Balance Line confirmed
      └─> Check Zone state
          ├─> Green Zone (AO+AC Green): LONG aligned
          ├─> Red Zone (AO+AC Red): SHORT aligned  
          └─> Gray Zone (mixed): Transition caution
              └─> Calculate risk
                  ├─> Acceptable: PROCEED to NORTH
                  └─> Too high: SKIP
```

---

### NORTH (White) - Wisdom & Execution

**Element:** Earth
**Season:** Winter  
**Time:** Night, Market Close
**Question:** "How do we honor this trade?"

**Williams Dimensions:** AO + AC (Dimensions 2+3)
- AO (Awesome Oscillator) - Momentum
- AC (Accelerator) - Acceleration
- Execution confirmation
- Position management
- Stop trailing (mvstopgator)

**jgtagentic Components:**
- `entry_script_gen.py` - Generate executable scripts
- `agentic_entry_orchestrator.py` - Orchestrate execution
- `observation_capture.py` - Record decisions

**Ceremony:** Elder Council (final wisdom check)
- Final AO/AC confirmation
- Execute trade with proper stops
- Set Red Line stop (standard) or Green Line (runaway)
- Honor the trade (win or loss)
- Campaign completion ceremony

**CLI Tools:**
- `jgtfxcon` - FX broker connection
- `mvstopgator` - Alligator-based stop trailing
- `orchestrator` - Execution workflow

**Decision Flow:**
```
NORTH Execution:
  └─> All dimensions aligned (EAST+SOUTH+WEST)
      └─> Check AO/AC
          ├─> AO+AC confirming: EXECUTE TRADE
          ├─> AO confirming, AC warning: Enter with caution
          └─> AO+AC contradicting: WAIT for clarity
              └─> Set stops
                  ├─> Red Line (Teeth): Standard
                  ├─> Green Line (Lips): Runaway market
                  └─> 5-Bar stop: After exhaustion
```

---

## CENTER: The Trader's Awareness

**Symbol:** ⚖️ Balance
**Role:** Human awareness and intention
**Function:** Integrate all four directions

The trader sits at the center, receiving input from all directions:
- EAST brings signals
- SOUTH provides structure  
- WEST offers wisdom
- NORTH executes with honor

**jgtagentic's Role:**
- Be the trader's automated awareness
- Integrate all dimensions
- Make decisions that honor all directions
- Never override fundamental rules (e.g., "Don't trade when Alligator sleeps")

---

## Ceremonial Trading Flow

### 1. OPENING CEREMONY (EAST - Dawn)
**When:** Market open, new session
**Action:** Smudging - clear state, scan for signals

```python
# jgtagentic implementation
data_loader.refresh()  # Clear previous
fdb_scanner.scan_all_timeframes()  # New signals
regime_detector.check_alligator()  # Sleep or awake?
```

**Output:** List of potential Fractal signals outside Alligator's Teeth

---

### 2. GROWTH ASSESSMENT (SOUTH - Midday)  
**When:** After signals detected
**Action:** Wave counting, HTF alignment

```python
# jgtagentic implementation
for signal in fractal_signals:
    balance_line_state = regime_detector.get_balance_line_position(signal)
    htf_alignment = scorer.evaluate_htf(signal)
    wave_position = wave_analyzer.count_elliott(signal)
```

**Output:** Signals with structure context and HTF scores

---

### 3. REFLECTION CEREMONY (WEST - Dusk)
**When:** Before entry decision  
**Action:** Talking circles - review with all dimensions

```python
# jgtagentic implementation  
for signal in structured_signals:
    zone_state = williams.detect_zone(signal)
    risk_level = risk_calculator.assess(signal, zone_state)
    
    decision = decider.decide_batch([signal], zone_aware=True)
```

**Output:** TRADE/SKIP/WAIT decisions with risk context

---

### 4. EXECUTION CEREMONY (NORTH - Night)
**When:** Decision made, ready to execute
**Action:** Elder council - final wisdom, honor trade

```python
# jgtagentic implementation
for trade_decision in approved_trades:
    ao_ac_confirmation = williams.check_momentum(trade_decision)
    
    if ao_ac_confirmation:
        entry_script = script_generator.generate(trade_decision)
        orchestrator.execute(entry_script)
        observer.record_ceremony(trade_decision, outcome="HONORED")
```

**Output:** Executed trades with stops set, journey documented

---

## Integration Points

### jgtagentic ↔ Medicine Wheel

| jgtagentic Component | Direction | Williams Dimension | Purpose |
|---------------------|-----------|-------------------|---------|
| `fdbscan_agent.py` | EAST | Fractals | Signal detection |
| `regime.py` | SOUTH | Balance Line | Alligator state |
| `scoring.py` | WEST | Zones | Risk/quality assessment |
| `entry_script_gen.py` | NORTH | AO/AC | Execution |
| `regime_aware_decider.py` | CENTER | All 5 | Integration |

### Data Flow Through Wheel

```
jgt-data-server (PDS/CDS/TTF/MLF)
        ↓
jgtagentic.data_loader
        ↓
   ┌────┴────┐
   │  EAST   │ → Fractal signals
   └────┬────┘
        ↓
   ┌────┴────┐
   │  SOUTH  │ → Balance Line context
   └────┬────┘
        ↓
   ┌────┴────┐
   │  WEST   │ → Zone + Risk assessment
   └────┬────┘
        ↓
   ┌────┴────┐
   │  NORTH  │ → AO/AC execution
   └────┬────┘
        ↓
  Entry Script → Broker
```

---

## Ceremony Messages

When jgtagentic makes decisions, it should speak in Medicine Wheel language:

**EAST (Vision):**
> "Fractal signal emerging on EUR-USD H4. The Alligator stirs from sleep."

**SOUTH (Growth):**
> "Price aligns with Balance Line. Wave 3 impulse confirmed across HTF."

**WEST (Reflection):**
> "Green Zone active. All dimensions whisper: This trade honors wisdom."

**NORTH (Execution):**
> "Elder Council approves. AO+AC aligned. Trade executed with Red Line protection."

**CENTER (Integration):**
> "The wheel is complete. All directions honored. May this trade serve the journey."

---

## Next Steps for jgtagentic

1. **Implement Alligator sleeping check** (SOUTH foundation)
2. **Require Fractal as first entry** (EAST mandate)
3. **Add AO/AC calculation** (NORTH execution)
4. **Integrate Zone pyramiding** (WEST wisdom)
5. **Create ceremony messages** (CENTER awareness)

The current ADX/EMA approach skips the ceremony entirely. It's mechanical, not organic. Williams teaches us to dance with the market, not fight it. The Medicine Wheel provides the dance floor - four directions, one center, infinite spirals.
