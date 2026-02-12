#!/usr/bin/env python
"""Quick test of Alligator detector."""
import sys
sys.path.insert(0, 'jgtagentic')

from alligator_regime import AlligatorDetector, AlligatorState
import pandas as pd
import numpy as np

# Create test data
np.random.seed(42)
uptrend = np.cumsum(np.random.randn(50) * 0.5 + 0.3) + 100
choppy = np.random.randn(50) * 0.2 + 110
prices = np.concatenate([uptrend, choppy])

df = pd.DataFrame({
    'High': prices + 0.2,
    'Low': prices - 0.2,
    'Close': prices
})

detector = AlligatorDetector(sleep_threshold=0.001)

print("=" * 60)
print("ALLIGATOR REGIME DETECTION TEST")
print("=" * 60)

# Test 1: Trending market (should be EATING)
df_trend = df.iloc[30:50]
result_trend = detector.detect(df_trend)
print("\n📈 TRENDING MARKET (bars 30-50):")
print(f"   State: {result_trend.state.value}")
print(f"   Direction: {result_trend.direction.value}")
print(f"   Tradeable: {'✅ YES' if result_trend.tradeable else '❌ NO'}")
print(f"   Spread: {result_trend.spread*100:.2f}%")

# Test 2: Ranging market (should be SLEEPING)
df_range = df.iloc[60:90]
result_range = detector.detect(df_range)
print("\n📊 RANGING MARKET (bars 60-90):")
print(f"   State: {result_range.state.value}")
print(f"   Direction: {result_range.direction.value}")
print(f"   Tradeable: {'✅ YES' if result_range.tradeable else '❌ NO'}")
print(f"   Spread: {result_range.spread*100:.2f}%")

# Test 3: Signal alignment
print("\n🎯 SIGNAL ALIGNMENT:")
print(f"   Trending + LONG: {'✅ ALIGNED' if detector.is_aligned('LONG', result_trend) else '❌ NOT ALIGNED'}")
print(f"   Ranging + LONG: {'✅ ALIGNED' if detector.is_aligned('LONG', result_range) else '❌ NOT ALIGNED'}")

print("\n" + "=" * 60)
if result_trend.state == AlligatorState.EATING and not result_range.tradeable:
    print("✅ ALL TESTS PASSED!")
    print("   - Trending market detected as EATING")
    print("   - Ranging market detected as SLEEPING/UNKNOWN")
    print("   - Alligator sleeping = NO TRADES (as Williams teaches)")
else:
    print("❌ TEST FAILED")
    
print("=" * 60)
