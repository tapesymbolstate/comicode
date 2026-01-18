# Visual Validation Requirements - 시각적 검증 필수 사항

> This document contains **mandatory process guidelines** for all development work.
>
> **Status (v0.1.110)**: All visual bugs have been fixed. All 26 examples produce correct visual output.

## What
모든 구현 작업은 반드시 실제 렌더링 결과물을 육안으로 확인하고 검증해야 한다.

## Why
**코드가 에러 없이 실행되고 테스트가 통과해도 실제 결과물이 엉망일 수 있다.**

현재 상황 (v0.1.110):
- ✅ 2107개 테스트 통과 (+ 30 skipped = 2137 collected)
- ✅ 코드 에러 없음
- ✅ **시각적 버그 수정 완료 (v0.1.85)**

**이것이 이 문서의 프로세스를 따라야 하는 이유다. 테스트만으로는 충분하지 않다. 눈으로 직접 확인해야 한다.**

## CRITICAL: Ralph Agent 작업 방식

### 절대 규칙: 구현 → 렌더링 → 검증 → 수정 루프

```
1. 기능 구현
   ↓
2. 예제 실행하여 PNG 생성
   ↓
3. PNG 파일을 Read tool로 확인 ← 🔴 필수!
   ↓
4. 시각적 문제 발견 시:
   - 문제 정확히 진단
   - 원인 코드 수정
   - 다시 2번으로
   ↓
5. 시각적으로 올바를 때만 다음 작업
```

**절대 하지 말 것:**
- ❌ 예제만 작성하고 결과물 확인 안 함
- ❌ "테스트 통과했으니 OK" 가정
- ❌ 다음 기능으로 넘어가기 전에 검증 안 함
- ❌ "아마 작동할 것" 추측

**반드시 해야 할 것:**
- ✅ 매번 PNG를 Read tool로 열어서 확인
- ✅ 예상 결과와 실제 결과 비교
- ✅ 문제 발견 즉시 수정
- ✅ 완벽할 때까지 반복

## Acceptance Criteria

### Must Have - 모든 구현 작업에 적용

- [ ] **구현 후 즉시 검증**: 코드 작성 직후 반드시 실제 렌더링 결과 확인
- [ ] **PNG 파일 직접 확인**: Read tool로 생성된 PNG를 열어서 육안 검증
- [ ] **예상 vs 실제 비교**: 스펙에 명시된 예상 결과와 실제 출력 비교
- [ ] **문제 발견 시 즉시 수정**: 시각적 문제 발견하면 바로 원인 찾아 수정
- [ ] **재검증**: 수정 후 다시 렌더링하고 확인
- [ ] **완벽할 때만 완료**: 시각적으로 100% 올바를 때만 다음 단계로

### Visual Validation Checklist

렌더링 결과를 확인할 때 반드시 체크:

#### 레이아웃 검증
- [ ] 모든 패널이 올바른 위치에 배치되었는가?
- [ ] 패널 크기가 균등한가? (2x2 그리드면 4개 패널 크기 같아야)
- [ ] 패널 간격(gutter)이 일정한가?
- [ ] 내용이 한 패널에 몰리지 않았는가?
- [ ] 패널 경계가 페이지 밖으로 나가지 않았는가?

#### 캐릭터 검증
- [ ] 캐릭터가 **완전히** 렌더링되었는가? (머리만이 아니라 몸통, 팔, 다리 모두)
- [ ] 캐릭터 위치가 의도한 곳인가?
- [ ] 여러 캐릭터가 겹치지 않았는가?
- [ ] 캐릭터 크기가 적절한가? (너무 크거나 작지 않은가)
- [ ] 표정이 올바르게 렌더링되었는가?

#### 말풍선 검증
- [ ] 말풍선 **테두리**가 보이는가? (텍스트만 있으면 안됨)
- [ ] 말풍선이 캐릭터를 가리키는 **꼬리**가 있는가?
- [ ] 텍스트가 말풍선 안에 깔끔하게 들어가는가?
- [ ] 여러 말풍선의 텍스트가 겹치지 않았는가?
- [ ] 말풍선이 패널 밖으로 나가지 않았는가?
- [ ] 말풍선 크기가 텍스트에 맞게 조절되었는가?

#### 텍스트 검증
- [ ] 텍스트가 읽을 수 있는가? (겹치거나 깨지지 않음)
- [ ] 폰트 크기가 적절한가?
- [ ] 긴 텍스트가 올바르게 줄바꿈되었는가?
- [ ] 텍스트 정렬이 올바른가? (중앙, 왼쪽 등)

## Current Known Issues (실제 결과물 검증 결과)

**No known issues.** As of v0.1.110, all 2107 tests pass (+ 30 skipped = 2137 collected), all 26 examples (01-26) execute successfully and produce correct output, and mypy/ruff pass.

## Implementation Strategy

### Phase 1: 레이아웃 시스템 수정 (최우선)

**문제**: `auto_layout()` 후 패널별 콘텐츠가 올바른 위치에 렌더링되지 않음

**검증 방법**:
1. 간단한 2x2 그리드 테스트 예제 작성
2. 각 패널에 다른 색 사각형 추가
3. 렌더링 후 PNG 확인
4. 4개 사각형이 각 패널 중앙에 있어야 함
5. 작동할 때까지 수정 반복

**수정 후 재검증**:
- [ ] examples/01_simple_dialogue.py 다시 실행
- [ ] PNG 확인: 2개 패널에 각각 캐릭터와 말풍선
- [ ] examples/04_expressions.py 다시 실행
- [ ] PNG 확인: 4개 패널에 각각 캐릭터

### Phase 2: 캐릭터 완전 렌더링

**문제**: Stickman이 머리만 렌더링됨

**검증 방법**:
1. 단일 Stickman 테스트 예제 작성
2. 렌더링 후 PNG 확인
3. 머리(원), 몸통(선), 팔 2개(선), 다리 2개(선) 모두 보여야 함
4. 작동할 때까지 `Stickman.generate_points()` 수정

### Phase 3: 말풍선 크기 및 위치 조정

**문제**: 말풍선이 패널 밖으로 나가거나 너무 큼

**검증 방법**:
1. 말풍선 테스트 예제 작성
2. 렌더링 후 PNG 확인
3. 말풍선이 패널 안에 들어가야 함
4. 텍스트에 맞는 적절한 크기여야 함

## Examples of Proper Validation

### Example: 올바른 검증 워크플로우

```python
# 1. 기능 구현
# comix/cobject/character/character.py 수정

# 2. 테스트 예제 실행
# uv run python test_character_full_body.py

# 3. Read tool로 PNG 확인
# Read("test_character_full_body.png")

# 4. 육안 검증:
# ✅ 머리: 원 보임
# ✅ 몸통: 수직선 보임
# ✅ 팔: 좌우 대각선 2개 보임
# ✅ 다리: 좌우 대각선 2개 보임
# → 완벽! 다음 작업으로

# 만약 문제 발견:
# ❌ 팔이 안보임
# → Stickman.generate_points()에서 팔 좌표 생성 코드 수정
# → 다시 2번으로 돌아가 재검증
```

### Example: 레이아웃 검증

```python
# 2x2 그리드 테스트
page = Page(width=800, height=800)
page.set_layout(rows=2, cols=2)

# 각 패널에 다른 색 원 추가
colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
for i, color in enumerate(colors):
    panel = Panel()
    circle = Circle(radius=50, fill_color=color)
    circle.move_to((200, 200))  # 패널 중심 기준
    panel.add_content(circle)
    page.add(panel)

page.auto_layout()
page.render("test_grid.png")

# Read("test_grid.png")로 확인:
# 기대 결과:
# [Red]  [Green]
# [Blue] [Yellow]
#
# 실제 결과가 이렇게 나오지 않으면:
# → auto_layout() 또는 좌표 변환 버그
# → 수정 후 다시 검증
```

## Success Criteria

**이 스펙은 다음이 모두 충족될 때 성공:**

1. ✅ 모든 예제(01-13)가 시각적으로 올바르게 렌더링됨
2. ✅ 각 예제 PNG를 육안으로 확인했음
3. ✅ 레이아웃 버그 없음 (모든 패널에 콘텐츠 올바르게 배치)
4. ✅ 캐릭터 완전 렌더링 (머리, 몸통, 팔, 다리)
5. ✅ 말풍선 테두리와 꼬리 보임
6. ✅ 텍스트 겹침 없음
7. ✅ 패널 밖으로 나가는 요소 없음
8. ✅ 모든 수정 후 재검증 완료

## For Ralph Agent: Mandatory Workflow

**모든 구현 작업에 이 워크플로우 적용:**

```bash
# 1. 코드 수정
vim comix/some_file.py

# 2. 예제 실행
uv run python examples/01_simple_dialogue.py

# 3. 결과 확인 (필수!)
# Read tool로 examples/output/01_simple_dialogue.png 열기

# 4. 체크리스트 검증
# - 레이아웃 OK?
# - 캐릭터 완전?
# - 말풍선 테두리?
# - 텍스트 겹침 없음?

# 5a. 완벽하면 → 다음 작업
# 5b. 문제 있으면 → 1번으로 돌아가 수정

# 모든 예제에 대해 반복
```

**절대 잊지 말 것:**
- 코드만 작성하고 끝내지 말 것
- 테스트 통과로 만족하지 말 것
- 반드시 PNG를 눈으로 확인할 것
- 문제는 즉시 수정할 것

---

**이 문서는 모든 다른 스펙보다 우선한다.**
**시각적 검증 없이 작업 완료 불가.**
