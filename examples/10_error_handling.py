"""Error handling and fallbacks.

This example demonstrates graceful error handling:
- Checking for optional dependencies (pycairo)
- Validating parameters with helpful error messages
- Fallback rendering options when features unavailable
- Safe file operations
"""
# Status: ✅ Working (v0.1.108)

import importlib.util
import os

from comix import Page, Panel, Stickman

# Ensure output directory exists
output_dir = "examples/output"
os.makedirs(output_dir, exist_ok=True)

# Create a simple comic page
page = Page(width=600, height=400)
page.set_layout(rows=1, cols=2)

panel1 = Panel()
char1 = Stickman(height=80)
char1.move_to((150, 200))
char1.set_expression("happy")
bubble1 = char1.say("Error handling!")
panel1.add_content(char1, bubble1)

panel2 = Panel()
char2 = Stickman(height=80)
char2.move_to((150, 200))
char2.set_expression("neutral")
bubble2 = char2.say("Be defensive!")
panel2.add_content(char2, bubble2)

page.add(panel1, panel2)
page.auto_layout()

# Example 1: Check for Cairo availability before PDF rendering
print("Example 1: Checking for Cairo...")
if importlib.util.find_spec("cairo") is not None:
    print("  Cairo is available - PNG/PDF rendering supported")
    has_cairo = True
else:
    print("  Cairo not available - using SVG fallback")
    has_cairo = False

# Example 2: Render with format fallback
output_base = f"{output_dir}/10_error_handling"
if has_cairo:
    # Preferred: PNG with Cairo
    page.render(f"{output_base}.png")
    print(f"  Created {output_base}.png (PNG via Cairo)")
else:
    # Fallback: SVG always available
    page.render(f"{output_base}.svg")
    print(f"  Created {output_base}.svg (SVG fallback)")

# Example 3: Validate character height
print("\nExample 3: Parameter validation...")
try:
    invalid_char = Stickman(height=-10)  # Invalid height
except ValueError as e:
    print(f"  Caught expected error: {e}")

try:
    invalid_char = Stickman(height=0)  # Zero height
except ValueError as e:
    print(f"  Caught expected error: {e}")

# Valid height works fine
valid_char = Stickman(height=50)
print(f"  Valid character created with height={valid_char.character_height}")

# Example 4: Safe file path handling
print("\nExample 4: Safe file operations...")
test_output = f"{output_dir}/10_test_output.svg"

# Always use SVG as it's guaranteed to work
page.render(test_output)

if os.path.exists(test_output):
    file_size = os.path.getsize(test_output)
    print(f"  File created: {test_output} ({file_size} bytes)")
    # Clean up test file
    os.remove(test_output)
    print("  Test file cleaned up")

# Example 5: Quality setting validation
print("\nExample 5: Quality settings...")
valid_qualities = ["low", "medium", "high"]
for quality in valid_qualities:
    print(f"  Quality '{quality}' is valid (DPI: {72 if quality == 'low' else 150 if quality == 'medium' else 300})")

print("\nAll error handling examples completed successfully!")
