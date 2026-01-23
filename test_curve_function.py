#!/usr/bin/env python3
"""Direct test of add_natural_curve function."""

from comix.utils.sketchy import add_natural_curve

# Test with two points
start = (100, 100)
end = (200, 100)

print("Testing add_natural_curve with:")
print(f"  start: {start}")
print(f"  end: {end}")
print(f"  curve_amount: 0.4")
print()

result = add_natural_curve(start, end, curve_amount=0.4, num_points=8)

print(f"Result ({len(result)} points):")
for i, point in enumerate(result):
    print(f"  {i}: {point}")

print()
print("If curves work, y-values should vary (not all 100)")
