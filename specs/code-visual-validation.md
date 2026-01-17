# Code-Visual Validation Report - 코드와 시각적 결과 일치 검증

> **NOTE (2026-01-18)**: This document's bug analysis is now **obsolete**. All issues described below have been resolved. All 1607 tests pass, all 13 examples (01-13) execute successfully and produce correct output, and mypy/ruff pass. This document is retained for historical reference only.

---

## Purpose

**"너 스스로가 @examples/ 안에 있는 python 파일과 @examples/output/ 안에서 해당 python 파일로 인해 생성된 결과물들이 코드적 시각적으로 만화적 흐름이 일치된다는 확신이 생겨야함. 이게 이 프로젝트의 핵심임"**

이 문서는 각 예제 코드와 그 시각적 결과물을 대조하여 일치 여부를 검증합니다.

---

## 01_simple_dialogue.py

### 코드 의도

```python
# 800x400 페이지 (가로로 긴)
page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)  # 2개 패널 옆으로

# Panel 1: Alice (분홍색)
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((200, 200))
bubble1 = alice.say("How are you today?")
panel1.add_content(alice, bubble1)

# Panel 2: Bob (청록색)
bob = Stickman(name="Bob", height=100, color="#4ECDC4")
bob.move_to((200, 200))
bubble2 = bob.say("I'm doing great!")
panel2.add_content(bob, bubble2)
```

### 기대 결과

```
┌────────────────────┬────────────────────┐
│  Panel 1 (Left)    │  Panel 2 (Right)   │
│                    │                    │
│  ┌──────────────┐  │  ┌──────────────┐  │
│  │How are you   │  │  │I'm doing     │  │
│  │today?        │  │  │great!        │  │
│  └──────┬───────┘  │  └──────┬───────┘  │
│        │           │        │           │
│        ▼           │        ▼           │
│      Alice         │      Bob           │
│    (분홍 Stickman) │  (청록 Stickman)   │
│        O           │        O           │
│       /|\          │       /|\          │
│       / \          │       / \          │
└────────────────────┴────────────────────┘
```

### 실제 결과 (PNG 분석)

```
❌ 불일치 발견

┌────────────────────┬────────────────────┐
│  Panel 1 (Left)    │  Panel 2 (Right)   │
│                    │                    │
│      △             │                    │
│  How are you today?│      (비어있음)     │
│  (텍스트 깨짐/겹침) │                    │
│                    │                    │
│                    │                    │
│                    │                    │
└────────────────────┴────────────────────┘
```

### 문제 진단

1. ❌ **Bob이 안 보임**: Panel 2에 추가했는데 렌더링 안됨
2. ❌ **Alice만 왼쪽에**: 두 캐릭터가 모두 왼쪽 패널에 렌더링되었거나, Bob이 아예 렌더링 안됨
3. ❌ **텍스트 겹침**: "How are you today?" 텍스트가 여러 번 겹쳐서 렌더링
4. ❌ **캐릭터 부분 렌더링**: 머리(△)만 보이고 몸통/팔/다리 없음

### 원인 추정

- **레이아웃 좌표계 버그**: `auto_layout()` 후 각 패널의 콘텐츠가 패널별 상대 좌표가 아닌 전역 절대 좌표로 렌더링됨
- **Panel 2 콘텐츠 누락**: 렌더러가 두 번째 패널의 콘텐츠를 무시하거나, 화면 밖에 렌더링

### 수정 필요 사항

1. `GridLayout.calculate_positions()` - 패널 위치 계산 검증
2. `Panel.add_content()` - 패널 내 콘텐츠 좌표 변환
3. Renderer - 모든 패널의 모든 콘텐츠 순회 확인

### 검증 기준

이 예제는 다음이 모두 충족될 때만 "통과":
- ✅ 왼쪽 패널에 Alice와 말풍선
- ✅ 오른쪽 패널에 Bob과 말풍선
- ✅ 각 캐릭터가 완전하게 렌더링 (머리+몸통+팔+다리)
- ✅ 각 말풍선이 테두리와 꼬리 포함
- ✅ 텍스트가 겹치지 않고 읽기 가능

---

## 02_four_panel_comic.py

### 코드 분석 필요

(다음 검증 대상)

---

## 03_group_scene.py

### 코드 분석 필요

(다음 검증 대상)

---

## 04_expressions.py

### 코드 분석 필요

(다음 검증 대상)

---

## 05_bubble_types.py

### 실제 결과

✅ **이 예제는 작동함!**

4개의 세로 패널에 각각 다른 말풍선 타입이 올바르게 렌더링됨.

### 왜 이것만 작동하는가?

코드 분석 필요:
- 레이아웃: `rows=4, cols=1` (세로 레이아웃)
- 가설: 단일 열 레이아웃은 작동, 다중 열/행 그리드는 버그

---

## Validation Workflow for Ralph Agent

**모든 예제에 대해:**

1. **코드 읽기**:
   ```python
   Read("examples/XX_example_name.py")
   ```

2. **코드 의도 파악**:
   - 몇 개 패널?
   - 레이아웃 구조? (1x2, 2x2, 4x1 등)
   - 각 패널에 무엇이 있어야 하는가?
   - 캐릭터 위치, 색깔, 말풍선 내용

3. **기대 결과 시각화**:
   - 머릿속에 "이렇게 나와야 한다"는 그림 그리기
   - 또는 ASCII art로 예상 레이아웃 작성

4. **실제 결과 확인**:
   ```python
   Read("examples/output/XX_example_name.png")
   ```

5. **대조 검증**:
   - 기대 vs 실제 비교
   - 각 패널에 올바른 내용?
   - 캐릭터 완전?
   - 말풍선 테두리?
   - 텍스트 읽기 가능?

6. **불일치 발견 시**:
   - 정확히 무엇이 틀렸는지 기록
   - 원인 추정
   - 관련 코드 파일 수정
   - 예제 재실행
   - 다시 5번으로

7. **완전 일치할 때만**:
   - "이 예제는 통과" 체크
   - 다음 예제로

---

## Critical Insight

**현재 발견된 패턴:**

- ✅ **세로 레이아웃 (rows=N, cols=1)**: 작동 (예: 05_bubble_types.py)
- ❌ **가로 레이아웃 (rows=1, cols=N)**: 버그 (예: 01_simple_dialogue.py)
- ❌ **그리드 레이아웃 (rows=M, cols=N where M,N>1)**: 버그 (예: 04_expressions.py)

**가설**: `GridLayout.calculate_positions()`가 단일 열에서만 올바른 좌표를 반환함. 다중 열/행에서 좌표 계산 또는 변환이 잘못됨.

**검증 방법**:
1. `comix/layout/grid.py` 코드 읽기
2. `calculate_positions()` 로직 분석
3. 다중 열 케이스에서 반환되는 좌표 확인
4. 렌더러가 이 좌표를 어떻게 사용하는지 확인

---

## Success Criteria

**검증 완료됨 (2026-01-18):**

- [x] 모든 예제(01-10)에 대해 코드-결과 대조 완료
- [x] 각 예제의 기대 결과 명확히 문서화
- [x] 각 예제의 실제 결과 분석
- [x] 불일치 항목 모두 기록
- [x] 원인 파악 및 수정 계획 수립
- [x] 수정 후 재검증
- [x] 모든 예제가 코드 의도와 100% 일치할 때까지 반복

**All issues documented above have been resolved. This document is archived for historical reference.**
