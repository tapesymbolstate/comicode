"""Parser DSL example - Create comics from markup text.

Demonstrates the markup parser for rapid comic creation without writing
Python code for every element. The DSL reads like a screenplay.
"""
# Status: ✅ Working (v0.1.108)

from comix.parser import parse_markup

# Example 1: Simple dialogue comic
simple_markup = """
[page 1x2]

# panel 1
Alice(left, happy): "Hello, how are you?"
Bob(right): "I'm doing great, thanks!"

# panel 2
Alice(left, surprised): "Really?"
Bob(right, happy): "Yes, really!"
"""

page1 = parse_markup(simple_markup)
page1.render("examples/output/12_parser_simple.png")
print("Created examples/output/12_parser_simple.png")


# Example 2: Four-panel comic (4koma style) with expressions
four_panel_markup = """
[page 4x1 400x1200]

# panel 1
Alice(center, neutral): "I have a question..."

# panel 2
Bob(center, confused): "What is it?"

# panel 3
Alice(center, excited): "Why did the programmer quit?"

# panel 4
Bob(center, surprised): "Because they didn't get arrays!"
sfx: BA DUM TSS
"""

page2 = parse_markup(four_panel_markup)
page2.render("examples/output/12_parser_4koma.png")
print("Created examples/output/12_parser_4koma.png")


# Example 3: Different bubble types
bubble_types_markup = """
[page 2x2]

# panel 1
Alice(center, neutral, speech): "This is a speech bubble."

# panel 2
Bob(center, confused, thought): "Hmm, what should I say?"

# panel 3
Alice(center, angry, shout): "LISTEN TO ME!"

# panel 4
Bob(center, scared, whisper): "okay... I'm listening..."
"""

page3 = parse_markup(bubble_types_markup)
page3.render("examples/output/12_parser_bubbles.png")
print("Created examples/output/12_parser_bubbles.png")


# Example 4: Korean dialogue (Unicode support)
korean_markup = """
[page 2x2]

# panel 1
철수(left, surprised): "뭐라고?!"
영희(right, smirk): "응, 진짜야"

# panel 2
철수(closeup, sad): "..."
sfx: 충격

# panel 3
narrator: "그날 이후..."

# panel 4
철수(center, happy): "그래도 괜찮아!"
"""

page4 = parse_markup(korean_markup)
page4.render("examples/output/12_parser_korean.png")
print("Created examples/output/12_parser_korean.png")


# Example 5: Multi-character scene with narrator
scene_markup = """
[page 1x3 800x900]

# panel 1
narrator: "In a meeting room far, far away..."
Boss(center, angry): "We need this done by Friday!"

# panel 2
Alice(left, scared): "But that's impossible!"
Bob(right, confused): "Wait, what project?"
Charlie(center, sleepy): "Zzz..."

# panel 3
Boss(center, surprised): "Did someone just fall asleep?!"
sfx: SNORE
"""

page5 = parse_markup(scene_markup)
page5.render("examples/output/12_parser_scene.png")
print("Created examples/output/12_parser_scene.png")


print("\nAll parser examples completed!")
print("The markup parser enables rapid comic creation with a screenplay-like syntax.")
