# Stickman Articulation - Joint and Limb Control

## What
Detailed control system for stickman character articulation, allowing precise manipulation of arm angles, elbow angles, leg angles, knee angles, and hand/finger options for creating custom poses and gestures.

## Why
While preset poses (standing, waving, sitting) are useful for common scenarios, users often need fine-grained control over character articulation to:
- Create custom poses not covered by presets
- Animate characters with specific joint movements
- Express subtle body language and gestures
- Point at specific objects or directions
- Show natural hand gestures (open palm, fist, pointing, etc.)

Without joint-level control, users are limited to preset poses and cannot create the exact character positions their comics require.

## Acceptance Criteria

### Must Have
- [x] Shoulder angle control for left and right arms independently ✅ v0.1.98
- [x] Elbow bend angle control for left and right arms independently ✅ v0.1.98
- [x] Hip angle control for left and right legs independently ✅ v0.1.98
- [x] Knee bend angle control for left and right legs independently ✅ v0.1.98
- [x] Basic hand options: none (line), fist, open, point ✅ v0.1.98
- [x] Angles specified in degrees (0-360) with intuitive defaults ✅ v0.1.98
- [x] Joint angles combine naturally (shoulder + elbow = full arm position) ✅ v0.1.98
- [x] All joint controls work with existing pose and expression systems ✅ v0.1.98

### Should Have
- [x] Preset arm poses: "down" (0°), "forward" (90°), "up" (180°), "back" (270°) ✅ v0.1.98 (via ArmController)
- [x] Preset leg poses: "standing" (0°), "bent" (45°), "sitting" (90°) ✅ v0.1.98 (via LegController)
- [x] Hand gesture presets: "relaxed", "fist", "point", "open", "peace", "thumbs_up" ✅ v0.1.98
- [x] Angle validation and clamping to prevent unnatural positions ✅ v0.1.98
- [x] Visual helper methods: `.point_at(x, y)` calculates arm angles automatically ✅ v0.1.98
- [ ] Smooth angle transitions for animation support (deferred - animation is optional feature)
- [x] Documentation with angle reference diagrams ✅ v0.1.98 (example 26)

### Won't Have (This Iteration)
- [ ] Wrist rotation angles (keep hands simple)
- [ ] Ankle/foot angles (stick figures typically have simple feet)
- [ ] Finger-by-finger control (hand gestures are sufficient)
- [ ] Spine/torso bending (keep torso as straight line)
- [ ] Neck angles (head position handled separately)
- [ ] Inverse kinematics (direct angle specification only)

## Context

### Angle Conventions

**Arm Angles** (measured from shoulder):
- 0° = arm hanging straight down (resting position)
- 90° = arm extending forward/horizontally
- 180° = arm raised straight up
- 270° = arm extending backward
- Positive angles = counterclockwise rotation
- Negative angles = clockwise rotation

**Elbow Angles** (bend amount):
- 0° = straight arm (no bend)
- 90° = right angle bend (forearm perpendicular to upper arm)
- 135° = natural relaxed bend
- 180° = fully bent (hand touches shoulder)
- Elbow always bends in anatomically natural direction

**Leg Angles** (measured from hip):
- 0° = leg hanging straight down (standing position)
- 45° = leg extended forward (walking)
- 90° = leg extended horizontally (sitting or high kick)
- -45° = leg extended backward (walking backward)

**Knee Angles** (bend amount):
- 0° = straight leg (standing, no bend)
- 45° = slight bend (relaxed standing)
- 90° = sitting position bend
- 135° = deep crouch/kneeling
- 180° = fully bent (heel touches buttocks)

### Hand/Finger Options

**Hand Representations** (for stick figure simplicity):
1. **none** (default): Hand is just endpoint of arm line (classic stick figure)
2. **fist**: Small circle at hand position (closed hand)
3. **open**: 5 short radiating lines from hand position (fingers spread)
4. **point**: Single extended line (index finger pointing)
5. **peace**: Two short lines (peace sign / victory)
6. **thumbs_up**: Vertical line with small perpendicular line (thumbs up gesture)
7. **relaxed**: 3-4 short parallel lines (relaxed fingers, not spread)

### User Flow

**Scenario 1: Custom Pose with Direct Angles**
```python
char = Stickman(height=150)
char.move_to((400, 300))

# Set precise joint angles
char.set_arm_angles(
    left_shoulder=45,   # Left arm forward-up
    left_elbow=90,      # Bent at right angle
    right_shoulder=0,   # Right arm hanging down
    right_elbow=0       # Straight
)
char.set_leg_angles(
    left_hip=0,         # Left leg standing
    left_knee=0,        # Straight
    right_hip=30,       # Right leg slightly forward
    right_knee=45       # Slightly bent
)
char.set_hands(left="open", right="fist")
```

**Scenario 2: Using Preset Helpers**
```python
char = Stickman(height=150)
char.move_to((400, 300))

# Convenient preset methods
char.left_arm.set_pose("waving")      # shoulder=180°, elbow=45°
char.right_arm.set_pose("pointing")   # shoulder=90°, elbow=0°, hand="point"
char.left_leg.set_pose("standing")    # hip=0°, knee=0°
char.right_leg.set_pose("walking")    # hip=30°, knee=15°
```

**Scenario 3: Point at Object**
```python
char = Stickman(height=150)
char.move_to((200, 300))

target = Rectangle(width=50, height=50)
target.move_to((500, 200))

# Automatically calculate arm angles to point at target
char.point_at(target, arm="right", hand="point")
# Calculates shoulder and elbow angles based on target position
```

### Edge Cases

- **Impossible angles**: Elbow bend > 180° should clamp to 180° (physically impossible)
- **Conflicting poses**: If user sets both `.set_pose("waving")` and `.set_arm_angles(...)`, direct angles should override preset
- **Angle wrap-around**: 370° should normalize to 10°, -90° should normalize to 270°
- **Very short limbs**: Hand gestures may not be visible if character height < 50px
- **Extreme leg angles**: Hip angles > 180° may cause legs to look unnatural (warn user)

### Technical Constraints

- Must maintain compatibility with existing Pose system
- Joint angles must be stored independently from preset poses
- Angles specified in degrees for user friendliness (convert to radians internally)
- Hand gestures rendered as additional geometry points after arm lines
- Elbow and knee positions calculated from segment lengths and bend angles

### Related Specs

- `stickman-reference-based.md` (character proportions and structure)
- `character-basics.md` (character system overview, poses)
- `getting-started.md` (basic usage examples)

## Examples

### Example 1: Waving with Custom Elbow Bend

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=150)
char.move_to((200, 250))

# Custom waving pose with specific elbow bend
char.set_arm_angles(
    left_shoulder=180,  # Left arm raised straight up
    left_elbow=30,      # Slight elbow bend (natural wave)
    right_shoulder=0,   # Right arm down
    right_elbow=0       # Straight
)
char.set_hands(left="open", right="none")

panel.add_content(char)
```

**Expected Visual**:
```
     O
    \|     ← Left arm waving (raised with slight bend)
     |     ← Right arm hanging
    / \
```

### Example 2: Pointing at Something

```python
from comix import Stickman, Panel

panel = Panel(width=600, height=400)

char = Stickman(height=120)
char.move_to((150, 300))

# Point right arm forward
char.set_arm_angles(
    left_shoulder=0,
    left_elbow=0,
    right_shoulder=90,   # Right arm extended horizontally
    right_elbow=0        # Straight (full extension)
)
char.set_hands(left="none", right="point")

panel.add_content(char)
```

**Expected Visual**:
```
     O
     |→    ← Right arm pointing (with finger extended)
     |
    / \
```

### Example 3: Walking Pose with Natural Leg Bends

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=150)
char.move_to((200, 280))

# Walking: left leg forward, right leg back
char.set_leg_angles(
    left_hip=30,      # Left leg forward
    left_knee=15,     # Slight knee bend
    right_hip=-20,    # Right leg back
    right_knee=10     # Slight knee bend
)

# Arms swing opposite to legs
char.set_arm_angles(
    left_shoulder=-15,   # Left arm back
    left_elbow=15,       # Natural swing bend
    right_shoulder=20,   # Right arm forward
    right_elbow=15       # Natural swing bend
)

panel.add_content(char)
```

**Expected Result**: Natural walking pose with coordinated limb movement.

### Example 4: Sitting with Bent Knees

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=120)
char.move_to((200, 300))

# Sitting pose
char.set_leg_angles(
    left_hip=90,      # Legs extended horizontally
    left_knee=90,     # Bent at right angle (sitting)
    right_hip=90,
    right_knee=90
)

# Resting arms
char.set_arm_angles(
    left_shoulder=0,
    left_elbow=90,    # Arms bent, hands in lap
    right_shoulder=0,
    right_elbow=90
)
char.set_hands(left="relaxed", right="relaxed")

panel.add_content(char)
```

**Expected Visual**:
```
     O
    /|\    ← Arms bent, hands near lap
     |
    ⌐⌐     ← Legs bent at knees (sitting position)
```

### Example 5: Automatic Point-At Calculation

```python
from comix import Stickman, Panel, Circle

panel = Panel(width=600, height=400)

char = Stickman(height=120)
char.move_to((150, 300))

target = Circle(radius=20, color="red")
target.move_to((500, 150))

# Automatically calculate angles to point at target
char.point_at(target, arm="right", hand="point")

panel.add_content(char, target)
```

**Expected Result**: Character's right arm automatically angled to point directly at the red circle.

### Example 6: Expressive Hand Gestures

```python
from comix import Stickman, Panel

panel = Panel(width=800, height=300)
panel.set_layout(rows=1, cols=4)

# Show different hand gestures
gestures = ["open", "fist", "point", "peace"]

for i, gesture in enumerate(gestures):
    p = Panel()
    char = Stickman(height=100)
    char.move_to((100, 180))

    # Both arms raised to show hands clearly
    char.set_arm_angles(
        left_shoulder=135,
        left_elbow=45,
        right_shoulder=135,
        right_elbow=45
    )
    char.set_hands(left=gesture, right=gesture)

    p.add_content(char)
    panel.add(p)
```

**Expected Result**: Four panels showing stickman with different hand gestures (open, fist, point, peace).

## Implementation Notes

### Joint Angle Storage

```python
class Stickman(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Joint angles (degrees)
        self._left_shoulder_angle = 0.0
        self._left_elbow_angle = 0.0
        self._right_shoulder_angle = 0.0
        self._right_elbow_angle = 0.0
        self._left_hip_angle = 0.0
        self._left_knee_angle = 0.0
        self._right_hip_angle = 0.0
        self._right_knee_angle = 0.0

        # Hand options
        self._left_hand = "none"
        self._right_hand = "none"

    def set_arm_angles(
        self,
        left_shoulder: float | None = None,
        left_elbow: float | None = None,
        right_shoulder: float | None = None,
        right_elbow: float | None = None
    ):
        """Set arm joint angles in degrees."""
        if left_shoulder is not None:
            self._left_shoulder_angle = self._normalize_angle(left_shoulder)
        if left_elbow is not None:
            self._left_elbow_angle = self._clamp_elbow(left_elbow)
        if right_shoulder is not None:
            self._right_shoulder_angle = self._normalize_angle(right_shoulder)
        if right_elbow is not None:
            self._right_elbow_angle = self._clamp_elbow(right_elbow)

        self.generate_points()  # Regenerate geometry
        return self

    def set_leg_angles(
        self,
        left_hip: float | None = None,
        left_knee: float | None = None,
        right_hip: float | None = None,
        right_knee: float | None = None
    ):
        """Set leg joint angles in degrees."""
        if left_hip is not None:
            self._left_hip_angle = self._normalize_angle(left_hip)
        if left_knee is not None:
            self._left_knee_angle = self._clamp_knee(left_knee)
        if right_hip is not None:
            self._right_hip_angle = self._normalize_angle(right_hip)
        if right_knee is not None:
            self._right_knee_angle = self._clamp_knee(right_knee)

        self.generate_points()
        return self

    def set_hands(
        self,
        left: str | None = None,
        right: str | None = None
    ):
        """Set hand gesture options.

        Options: "none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"
        """
        valid_hands = ["none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"]

        if left is not None:
            if left not in valid_hands:
                raise ValueError(f"Invalid hand option: {left}. Must be one of {valid_hands}")
            self._left_hand = left

        if right is not None:
            if right not in valid_hands:
                raise ValueError(f"Invalid hand option: {right}. Must be one of {valid_hands}")
            self._right_hand = right

        self.generate_points()
        return self

    def point_at(
        self,
        target: CObject | tuple[float, float],
        arm: str = "right",
        hand: str = "point",
        elbow_bend: float = 0.0
    ):
        """Automatically calculate arm angles to point at target.

        Args:
            target: Object to point at, or (x, y) coordinates
            arm: "left" or "right"
            hand: Hand gesture to use (default: "point")
            elbow_bend: Amount of elbow bend in degrees (0 = straight)
        """
        # Get target position
        if isinstance(target, tuple):
            target_x, target_y = target
        else:
            target_x, target_y = target.get_center()

        # Get shoulder position
        shoulder_x, shoulder_y = self._get_shoulder_position(arm)

        # Calculate angle from shoulder to target
        dx = target_x - shoulder_x
        dy = target_y - shoulder_y
        angle_to_target = np.degrees(np.arctan2(dy, dx))

        # Set arm angles
        if arm == "left":
            self.set_arm_angles(
                left_shoulder=angle_to_target,
                left_elbow=elbow_bend
            )
            self.set_hands(left=hand)
        else:
            self.set_arm_angles(
                right_shoulder=angle_to_target,
                right_elbow=elbow_bend
            )
            self.set_hands(right=hand)

        return self

    @staticmethod
    def _normalize_angle(angle: float) -> float:
        """Normalize angle to 0-360 range."""
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    @staticmethod
    def _clamp_elbow(angle: float) -> float:
        """Clamp elbow bend to physically possible range."""
        return max(0, min(180, angle))

    @staticmethod
    def _clamp_knee(angle: float) -> float:
        """Clamp knee bend to physically possible range."""
        return max(0, min(180, angle))
```

### Point Generation with Joint Angles

```python
def generate_points(self) -> None:
    """Generate stickman geometry with joint angles."""
    h = self.character_height

    # ... (head and torso generation same as before)

    # Arms with shoulder and elbow angles
    arm_length = h * self.arm_ratio
    upper_arm_length = arm_length * 0.5
    forearm_length = arm_length * 0.5

    # Left arm
    shoulder_x, shoulder_y = 0, arm_y  # Shoulder position

    # Upper arm endpoint (elbow)
    left_shoulder_rad = np.radians(self._left_shoulder_angle)
    elbow_left_x = shoulder_x + upper_arm_length * np.cos(left_shoulder_rad)
    elbow_left_y = shoulder_y + upper_arm_length * np.sin(left_shoulder_rad)

    # Forearm endpoint (hand) - elbow bend applied
    # Elbow angle rotates forearm relative to upper arm direction
    forearm_angle = left_shoulder_rad + np.radians(self._left_elbow_angle)
    hand_left_x = elbow_left_x + forearm_length * np.cos(forearm_angle)
    hand_left_y = elbow_left_y + forearm_length * np.sin(forearm_angle)

    # Add arm segments
    points.append([shoulder_x, shoulder_y])
    points.append([elbow_left_x, elbow_left_y])
    points.append([elbow_left_x, elbow_left_y])
    points.append([hand_left_x, hand_left_y])

    # Add hand gesture geometry if needed
    if self._left_hand != "none":
        hand_points = self._generate_hand_gesture(
            hand_left_x, hand_left_y,
            forearm_angle,
            self._left_hand
        )
        points.extend(hand_points)

    # Right arm (similar logic)
    # ...

    # Legs with hip and knee angles (similar two-segment approach)
    # ...

    self._points = np.array(points, dtype=np.float64)

def _generate_hand_gesture(
    self,
    hand_x: float,
    hand_y: float,
    arm_angle: float,
    gesture: str
) -> list:
    """Generate geometry points for hand gesture."""
    points = []
    finger_length = self.character_height * 0.05  # Proportional finger size

    if gesture == "fist":
        # Small circle at hand position
        for angle in np.linspace(0, 2 * np.pi, 8):
            radius = finger_length * 0.5
            points.append([
                hand_x + radius * np.cos(angle),
                hand_y + radius * np.sin(angle)
            ])

    elif gesture == "open":
        # 5 radiating lines (spread fingers)
        for i, finger_angle in enumerate([-45, -22.5, 0, 22.5, 45]):
            angle = arm_angle + np.radians(finger_angle)
            points.append([hand_x, hand_y])
            points.append([
                hand_x + finger_length * np.cos(angle),
                hand_y + finger_length * np.sin(angle)
            ])

    elif gesture == "point":
        # Single extended line (index finger)
        points.append([hand_x, hand_y])
        points.append([
            hand_x + finger_length * 1.5 * np.cos(arm_angle),
            hand_y + finger_length * 1.5 * np.sin(arm_angle)
        ])

    elif gesture == "peace":
        # Two lines (V sign)
        for finger_angle in [-15, 15]:
            angle = arm_angle + np.radians(finger_angle)
            points.append([hand_x, hand_y])
            points.append([
                hand_x + finger_length * np.cos(angle),
                hand_y + finger_length * np.sin(angle)
            ])

    elif gesture == "thumbs_up":
        # Vertical line with perpendicular thumb
        points.append([hand_x, hand_y])
        points.append([hand_x, hand_y - finger_length])
        points.append([hand_x, hand_y - finger_length * 0.5])
        points.append([hand_x + finger_length * 0.5, hand_y - finger_length * 0.5])

    elif gesture == "relaxed":
        # 3-4 parallel short lines (relaxed fingers)
        for i in range(4):
            offset = (i - 1.5) * finger_length * 0.3
            perp_angle = arm_angle + np.pi / 2
            base_x = hand_x + offset * np.cos(perp_angle)
            base_y = hand_y + offset * np.sin(perp_angle)
            points.append([base_x, base_y])
            points.append([
                base_x + finger_length * 0.7 * np.cos(arm_angle),
                base_y + finger_length * 0.7 * np.sin(arm_angle)
            ])

    return points
```

### Convenience Methods

```python
class ArmController:
    """Helper class for arm control (accessed via char.left_arm or char.right_arm)."""

    ARM_PRESETS = {
        "down": {"shoulder": 0, "elbow": 0},
        "forward": {"shoulder": 90, "elbow": 0},
        "up": {"shoulder": 180, "elbow": 0},
        "waving": {"shoulder": 180, "elbow": 30},
        "pointing": {"shoulder": 90, "elbow": 0, "hand": "point"},
        "relaxed": {"shoulder": 0, "elbow": 15},
        "thinking": {"shoulder": 120, "elbow": 90, "hand": "fist"},
    }

    def __init__(self, character: Stickman, side: str):
        self.character = character
        self.side = side  # "left" or "right"

    def set_pose(self, preset: str):
        """Apply preset arm pose."""
        if preset not in self.ARM_PRESETS:
            raise ValueError(f"Unknown arm preset: {preset}")

        config = self.ARM_PRESETS[preset]

        if self.side == "left":
            self.character.set_arm_angles(
                left_shoulder=config["shoulder"],
                left_elbow=config.get("elbow", 0)
            )
            if "hand" in config:
                self.character.set_hands(left=config["hand"])
        else:
            self.character.set_arm_angles(
                right_shoulder=config["shoulder"],
                right_elbow=config.get("elbow", 0)
            )
            if "hand" in config:
                self.character.set_hands(right=config["hand"])

class LegController:
    """Helper class for leg control."""

    LEG_PRESETS = {
        "standing": {"hip": 0, "knee": 0},
        "walking": {"hip": 30, "knee": 15},
        "sitting": {"hip": 90, "knee": 90},
        "kneeling": {"hip": 135, "knee": 135},
        "bent": {"hip": 0, "knee": 45},
    }

    # Similar implementation to ArmController
```

### Integration with Existing Pose System

The joint angle system should work alongside the existing pose system:
- If user calls `.set_pose("waving")`, it applies preset joint angles
- If user then calls `.set_arm_angles(...)`, it overrides the preset
- Pose presets are implemented as combinations of joint angles
- This maintains backward compatibility while adding fine control

## Open Questions

- [ ] Should elbow/knee bend angles use 0° = straight or 180° = straight? **Needs decision**
  - Option A: 0° = straight (bend angle measures deviation from straight)
  - Option B: 180° = straight (bend angle measures interior angle)
  - **Recommendation**: 0° = straight (more intuitive: "0 bend = no bend")

- [ ] Should we support negative elbow/knee angles for hyperextension? **Needs decision**
  - May be useful for stylized poses
  - Could look unnatural/broken

- [ ] How detailed should hand gestures be? **Needs decision**
  - Current plan: Simple geometric representations
  - Alternative: More detailed finger positions

- [ ] Should `.point_at()` adjust body position or just arm? **Needs decision**
  - Current plan: Only arm angles
  - Alternative: Could also rotate torso or face direction

- [ ] Do we need forearm rotation (wrist twist)? **Defer to future**
  - Adds complexity
  - May not be visible in stick figure style

## Test Requirements

1. **Angle setting and retrieval**:
   - Test: `.set_arm_angles(left_shoulder=90)` sets angle correctly
   - Test: Angles normalize correctly (370° → 10°, -90° → 270°)
   - Test: Elbow angles clamp to 0-180° range
   - Test: Knee angles clamp to 0-180° range

2. **Geometry generation**:
   - Test: Shoulder angle 0° positions arm straight down
   - Test: Shoulder angle 90° positions arm horizontally
   - Test: Elbow bend 90° creates right angle at elbow joint
   - Test: Hand position calculated correctly from shoulder + elbow angles

3. **Hand gestures**:
   - Test: "fist" renders small circle at hand position
   - Test: "open" renders 5 radiating finger lines
   - Test: "point" renders single extended finger line
   - Test: Invalid hand option raises ValueError

4. **Point-at functionality**:
   - Test: `.point_at((x, y))` calculates correct arm angle
   - Test: Pointing at object to the right sets positive angle
   - Test: Pointing at object above sets ~90° angle
   - Test: Elbow bend parameter affects forearm position

5. **Preset compatibility**:
   - Test: Existing `.set_pose("waving")` still works
   - Test: Direct angle setting overrides pose preset
   - Test: Arm and leg presets apply correct joint angles

6. **Visual rendering**:
   - Test: SVG output contains correct arm/leg segments
   - Test: Hand gesture geometry renders in both SVG and Cairo
   - Test: Extreme angles don't cause rendering errors

## Success Metrics

**This spec is successful when:**
1. Users can create any custom stickman pose using joint angles
2. Joint angle controls are intuitive (degrees, clear naming)
3. Hand gestures enhance expressiveness without over-complicating
4. `.point_at()` helper method saves users from manual angle calculations
5. System works seamlessly with existing pose and expression features
6. Documentation includes clear angle reference diagrams
7. Users report "I can finally create the exact pose I need"

## References

- [Human Joint Ranges of Motion](https://en.wikipedia.org/wiki/Range_of_motion) - Anatomical constraints
- [Character Rigging Basics](https://docs.blender.org/manual/en/latest/animation/armatures/) - Joint angle systems
- [Stick Figure Animation Tutorials](https://www.stickpage.com/sfa/) - Common stick figure poses
