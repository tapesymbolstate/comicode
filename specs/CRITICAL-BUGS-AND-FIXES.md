# 🔴 CRITICAL BUGS AND FIXES - 실제 버그 진단과 수정 방법

> **이 문서가 가장 중요합니다.** 다른 스펙들이 "모두 작동한다"고 해도, 이 문서가 실제 현실입니다.

## 현재 상황 (2026-01-18 업데이트)

- ✅ 코드는 에러 없이 실행됨
- ✅ 테스트는 통과 (1743 tests)
- ✅ **v0.1.62에서 주요 시각적 버그가 수정됨**

**수정된 사항:**
- 버그 1 (말풍선 겹침): Panel.add_content()에서 자동 충돌 회피 구현
- 버그 3 (좌표 변환): 잘못된 transform-based 좌표계 제거, 글로벌 좌표로 복귀

---

## 🔴 발견된 실제 버그들

### 버그 1: 말풍선 위치/겹침 문제

**증상**:
- 여러 캐릭터가 있을 때 말풍선이 겹침
- 말풍선이 캐릭터 위치와 무관하게 배치됨
- 말풍선 꼬리가 잘못된 방향을 가리킴

**재현 방법**:
```python
# 예제 03_group_scene.py의 경우
char1 = Stickman()
char1.move_to((200, 300))
bubble1 = char1.say("Text 1")

char2 = Stickman()
char2.move_to((400, 300))
bubble2 = char2.say("Text 2")

char3 = Stickman()
char3.move_to((600, 300))
bubble3 = char3.say("Text 3")

# 결과: 말풍선 3개가 겹쳐서 나올 수 있음
```

**원인 분석**:
1. `character.say()`가 말풍선을 생성할 때 자동 위치 지정
2. 하지만 다른 말풍선과의 충돌을 확인하지 않음
3. `auto_attach_to()`가 있지만 자동으로 호출되지 않음

**수정 방법**:

**Option A: character.say()에서 자동 충돌 회피** (권장)
```python
# comix/cobject/character/character.py

class Character(CObject):
    def say(self, text: str, avoid_bubbles=None, **bubble_kwargs) -> SpeechBubble:
        """Create speech bubble with automatic collision avoidance."""
        from ..bubble import SpeechBubble

        bubble = SpeechBubble(text, **bubble_kwargs)

        # 자동으로 충돌 회피 위치 찾기
        if avoid_bubbles:
            bubble.auto_attach_to(self, existing_bubbles=avoid_bubbles)
        else:
            bubble.attach_to(self)

        return bubble
```

**사용 예시**:
```python
bubbles = []
bubble1 = char1.say("Text 1")
bubbles.append(bubble1)

bubble2 = char2.say("Text 2", avoid_bubbles=bubbles)
bubbles.append(bubble2)

bubble3 = char3.say("Text 3", avoid_bubbles=bubbles)
```

**Option B: Panel에서 자동 배치** (더 쉬움)
```python
# comix/cobject/panel/panel.py

class Panel(CObject):
    def add_content(self, *cobjects: CObject) -> Self:
        """Add content with automatic bubble positioning."""
        # 캐릭터와 말풍선 분리
        characters = [obj for obj in cobjects if isinstance(obj, Character)]
        bubbles = [obj for obj in cobjects if isinstance(obj, Bubble)]

        # 말풍선 자동 배치
        if bubbles and characters:
            from ..bubble.bubble import auto_position_bubbles
            auto_position_bubbles(bubbles, characters)

        # 기존 로직
        for obj in cobjects:
            self._content.append(obj)
            self.add(obj)
        return self
```

**테스트 추가**:
```python
def test_bubble_collision_avoidance():
    """Test that multiple bubbles don't overlap."""
    panel = Panel(width=800, height=600)

    char1 = Stickman()
    char1.move_to((200, 300))
    bubble1 = char1.say("Text 1")

    char2 = Stickman()
    char2.move_to((250, 300))  # 가까이 배치
    bubble2 = char2.say("Text 2", avoid_bubbles=[bubble1])

    panel.add_content(char1, char2, bubble1, bubble2)

    # 말풍선이 겹치지 않는지 확인
    assert not bubble1.overlaps_with(bubble2), "Bubbles should not overlap"
```

---

### 버그 2: 캐릭터 표정/포즈 렌더링 불완전

**증상**:
- 일부 캐릭터 타입에서 표정이 렌더링 안됨
- 포즈 변경이 시각적으로 반영 안됨

**재현 방법**:
```python
char = Stickman()
char.set_expression("happy")
char.set_pose("waving")
# 렌더링해도 neutral + standing으로 보임
```

**원인 분석**:
- Expression/Pose 객체가 설정되지만 렌더링에 반영 안됨
- `generate_points()`가 expression/pose를 고려하지 않음

**수정 방법**:
```python
# comix/cobject/character/character.py

class Stickman(Character):
    def generate_points(self):
        """Generate points including expression and pose."""
        points = []

        # 1. 머리 (표정 포함)
        head_center = self._get_head_position()
        head_radius = self.height * 0.15

        # 표정에 따라 얼굴 특징 추가
        if self._expression.eyes == "happy":
            # ^_^ 눈 그리기
            pass
        elif self._expression.eyes == "sad":
            # T_T 눈 그리기
            pass

        # 2. 몸통 (포즈 포함)
        if self._pose.name == "waving":
            # 한쪽 팔 위로
            pass
        elif self._pose.name == "sitting":
            # 다리 접기
            pass

        self._points = points
```

---

### 버그 3: GridLayout 좌표 변환 문제

**증상**:
- 2x2, 3x2 등 그리드 레이아웃에서 콘텐츠 위치 이상
- 일부 패널에만 모든 콘텐츠가 몰림

**재현 방법**:
```python
page = Page()
page.set_layout(rows=2, cols=2)

for i in range(4):
    panel = Panel()
    char = Stickman()
    char.move_to((200, 200))  # 패널 중심 기준
    panel.add_content(char)
    page.add(panel)

page.auto_layout()
# 결과: 모든 캐릭터가 한 패널에 몰림
```

**원인 분석**:
- `auto_layout()`이 패널 위치는 계산하지만
- 패널 내부 콘텐츠의 좌표는 변환하지 않음
- 모든 객체가 전역 좌표계를 사용

**수정 방법**:

**Option 1: 패널별 좌표계 변환**
```python
# comix/layout/grid.py

class GridLayout:
    def apply_to_panels(self, panels):
        """Apply layout and transform panel content coordinates."""
        positions = self.calculate_positions(len(panels))

        for panel, pos in zip(panels, positions):
            # 패널 자체 위치
            panel.move_to(pos["center"])
            panel.width = pos["width"]
            panel.height = pos["height"]

            # 🔴 새로 추가: 패널 내부 콘텐츠 좌표 변환
            panel_offset = (pos["x"], pos["y"])
            for child in panel._content:
                # 자식 객체의 좌표를 패널 기준으로 변환
                child.position += panel_offset
```

**Option 2: 렌더러에서 좌표계 변환**
```python
# comix/renderer/svg_renderer.py

class SVGRenderer:
    def render_panel(self, panel):
        """Render panel with local coordinate system."""
        # 패널의 <g> 그룹 생성
        panel_group = self.dwg.g(
            transform=f"translate({panel.position[0]}, {panel.position[1]})"
        )

        # 패널 내부 콘텐츠는 (0,0) 기준 상대 좌표로 렌더링
        for child in panel._content:
            self.render_object(child, parent_group=panel_group)

        self.dwg.add(panel_group)
```

**테스트 추가**:
```python
def test_grid_layout_coordinate_transform():
    """Test that grid layout correctly positions content in each panel."""
    page = Page(width=800, height=800)
    page.set_layout(rows=2, cols=2)

    # 각 패널에 다른 색 원 추가
    colors = ["red", "green", "blue", "yellow"]
    for i, color in enumerate(colors):
        panel = Panel()
        circle = Circle(radius=50, fill_color=color)
        circle.move_to((200, 200))  # 패널 중심
        panel.add_content(circle)
        page.add(panel)

    page.auto_layout()

    # 렌더링 후 각 패널의 중심에 원이 있는지 확인
    # (시각적 검증 또는 SVG 파싱 필요)
```

---

## 🔧 우선순위 수정 작업

### P0: 즉시 수정 필요

1. **말풍선 겹침 방지** (버그 1)
   - 파일: `comix/cobject/panel/panel.py`
   - 예상 시간: 1-2시간
   - 검증: examples/03_group_scene.py 재실행 후 PNG 확인

2. **GridLayout 좌표 변환** (버그 3)
   - 파일: `comix/layout/grid.py` 또는 렌더러들
   - 예상 시간: 2-3시간
   - 검증: examples/07_custom_layout.py 재실행 후 PNG 확인

### P1: 중요하지만 긴급하지 않음

3. **표정/포즈 렌더링** (버그 2)
   - 파일: `comix/cobject/character/*.py`
   - 예상 시간: 3-4시간
   - 검증: examples/04_expressions.py 재실행 후 PNG 확인

---

## 🎯 Ralph Agent 작업 지침

**절대 규칙: 코드 수정 → 예제 실행 → PNG 확인 → 다시 수정**

### 단계별 워크플로우

#### 1단계: 버그 1 수정 (말풍선 겹침)

```bash
# 1. Panel.add_content() 수정
vim comix/cobject/panel/panel.py

# 2. 테스트 실행
uv run pytest tests/test_panel.py -k bubble

# 3. 예제 실행
uv run python examples/03_group_scene.py

# 4. PNG 확인 (CRITICAL!)
# Read tool로 examples/output/03_group_scene.png 열기
# 말풍선 3개가 겹치지 않는지 육안 확인

# 5. 여전히 겹치면?
# → 1번으로 돌아가 다시 수정
# → 완벽할 때까지 반복
```

#### 2단계: 버그 3 수정 (GridLayout)

```bash
# 1. GridLayout 또는 Renderer 수정
vim comix/layout/grid.py

# 2. 테스트 실행
uv run pytest tests/test_layout.py

# 3. 예제 실행 (여러 개)
uv run python examples/07_custom_layout.py
uv run python examples/04_expressions.py

# 4. PNG 확인
# 각 패널에 콘텐츠가 올바르게 배치되었는지 확인

# 5. 문제 있으면 1번으로
```

#### 3단계: 버그 2 수정 (표정/포즈)

```bash
# 1. Character generate_points() 수정
vim comix/cobject/character/character.py

# 2. 렌더러 수정 (필요시)
vim comix/renderer/svg_renderer.py
vim comix/renderer/cairo_renderer.py

# 3. 예제 실행
uv run python examples/04_expressions.py

# 4. PNG 확인
# 각 표정이 시각적으로 다르게 보이는지 확인
```

---

## 📊 진행 상황 추적

### 버그 수정 체크리스트

- [x] **버그 1: 말풍선 겹침** ✅ FIXED in v0.1.62
  - [x] `Panel.add_content()` 수정 - auto_position_bubbles 파라미터 추가
  - [x] `auto_attach_to()` 통합 - 충돌 회피 로직 사용
  - [x] examples/03_group_scene.py 확인
  - [x] PNG에서 말풍선 안 겹침 확인

- [x] **버그 3: GridLayout 좌표** ✅ FIXED in v0.1.62
  - [x] SVG/Cairo Renderer 수정 - 잘못된 translate transform 제거
  - [x] 글로벌 좌표계로 복귀 (panel-relative에서)
  - [x] examples/07_custom_layout.py 확인
  - [x] examples/04_expressions.py 확인
  - [x] PNG에서 각 패널에 콘텐츠 올바름 확인

- [x] **버그 2: 표정/포즈** ✅ ALREADY WORKING
  - [x] 표정이 이미 올바르게 렌더링됨 확인
  - [x] examples/04_expressions.py 확인
  - [x] examples/16_character_types.py 확인
  - [x] PNG에서 표정 차이 육안 확인

---

## 🚫 하지 말아야 할 것

- ❌ "테스트 통과했으니 됐다"고 생각하지 말 것
- ❌ PNG 확인 없이 다음 버그로 넘어가지 말 것
- ❌ "아마 작동할 것"이라고 가정하지 말 것
- ❌ 여러 버그를 동시에 수정하려 하지 말 것 (한 번에 하나씩)

## ✅ 반드시 해야 할 것

- ✅ 각 버그를 개별적으로 수정
- ✅ 수정 후 즉시 PNG 확인
- ✅ 완벽해질 때까지 반복
- ✅ 진행 상황을 이 문서에 기록

---

## 📝 수정 완료 기준

**각 버그는 다음이 모두 충족될 때만 "완료":**

1. ✅ 코드 수정됨
2. ✅ 관련 테스트 통과
3. ✅ 예제 실행됨 (에러 없음)
4. ✅ PNG 시각적 확인 완료
5. ✅ 의도한 대로 정확히 렌더링됨
6. ✅ 다른 예제들도 여전히 작동함 (회귀 테스트)

**모든 버그가 완료되면:**
- [ ] 전체 테스트 스위트 실행
- [ ] 모든 23개 예제 실행
- [ ] 모든 PNG/PDF 시각적 확인
- [ ] IMPLEMENTATION_PLAN.md 업데이트
- [ ] 이 문서를 "COMPLETED"로 표시

---

**이 문서는 살아있는 문서입니다. 버그 발견/수정할 때마다 업데이트하세요.**
