# Examples Maintenance - 예제 정리 및 관리 기준

> **Note**: This document contains **process guidelines** for future maintenance.
> All 15 examples (01-15) are currently working correctly as of v0.1.42.

## What
examples/ 디렉토리를 주기적으로 정리하여 **실제로 작동하는 예제만 유지**하고, 버그가 있는 예제는 명확히 표시하거나 임시 제거한다.

## Why
**망가진 예제가 있으면 사용자가 혼란스럽다.**

현재 상황 (2026-01-18):
- ✅ 01-10 예제 파일 모두 존재
- ✅ 모든 예제가 정상 작동
- ✅ 시각적 출력 검증 완료

**참고: 아래 정리 기준은 향후 예제가 깨질 경우를 위한 것입니다.**

## Acceptance Criteria

### Must Have

- [ ] examples/README.md에 각 예제의 상태 표시 (✅ 작동 / 🔴 버그 / 🚧 작업중)
- [ ] 버그 있는 예제는 파일명에 `.BROKEN.py` 추가하거나 `_broken/` 디렉토리로 이동
- [ ] 작동하는 예제만 메인 examples/ 디렉토리에 유지
- [ ] 각 예제 파일 상단에 상태 주석 추가
- [ ] Ralph Agent가 수정 작업 시 예제 상태 업데이트

### Should Have

- [ ] examples/working/ - 완벽히 작동하는 예제
- [ ] examples/broken/ - 버그로 작동 안 하는 예제
- [ ] examples/wip/ - 작업 중인 예제

## Current Examples Status

**All 15 examples are working.** As of 2026-01-18, all examples execute successfully and produce correct output.

| Example | Status |
|---------|--------|
| 01_simple_dialogue.py | ✅ Working |
| 02_four_panel_comic.py | ✅ Working |
| 03_group_scene.py | ✅ Working |
| 04_expressions.py | ✅ Working |
| 05_bubble_types.py | ✅ Working |
| 06_multi_page_pdf.py | ✅ Working |
| 07_custom_layout.py | ✅ Working |
| 08_manual_positioning.py | ✅ Working |
| 09_using_templates.py | ✅ Working |
| 10_error_handling.py | ✅ Working |
| 11_html_export.py | ✅ Working |
| 12_parser_dsl.py | ✅ Working |
| 13_visual_effects.py | ✅ Working |
| 14_animation_export.py | ✅ Working |
| 15_video_export.py | ✅ Working |

## Immediate Action Plan

### Step 1: 예제 디렉토리 재구성

```bash
mkdir -p examples/working examples/broken examples/wip

# 작동하는 예제
mv examples/03_group_scene.py examples/working/
mv examples/05_bubble_types.py examples/working/

# 버그 있는 예제
mv examples/01_simple_dialogue.py examples/broken/
mv examples/02_four_panel_comic.py examples/broken/
mv examples/04_expressions.py examples/broken/

# 미검증 예제는 wip/로
mv examples/06_multi_page_pdf.py examples/wip/
mv examples/07_custom_layout.py examples/wip/
mv examples/08_manual_positioning.py examples/wip/
mv examples/09_using_templates.py examples/wip/
mv examples/10_error_handling.py examples/wip/
```

### Step 2: examples/README.md 업데이트

```markdown
# Comix Examples

## ✅ Working Examples (신뢰 가능)

### 03_group_scene.py
단일 패널에 여러 캐릭터 배치
- **Status**: ✅ 작동 (캐릭터 머리만 렌더링, 레이아웃은 OK)
- **Run**: `uv run python examples/working/03_group_scene.py`
- **Output**: `examples/output/03_group_scene.png`

### 05_bubble_types.py
다양한 말풍선 타입 (Speech, Thought, Shout, Whisper)
- **Status**: ✅ 완벽히 작동!
- **Run**: `uv run python examples/working/05_bubble_types.py`
- **Output**: `examples/output/05_bubble_types.png`

## 🔴 Broken Examples (버그로 사용 불가)

### broken/01_simple_dialogue.py
- **Issue**: 레이아웃 버그 - 왼쪽 패널에만 내용
- **Blocker**: GridLayout 1x2 (가로 레이아웃) 버그
- **DO NOT USE** until fixed

### broken/02_four_panel_comic.py
- **Issue**: 모든 내용이 첫 패널에 몰림
- **Blocker**: GridLayout 4x1 세로 + auto_layout 버그
- **DO NOT USE** until fixed

### broken/04_expressions.py
- **Issue**: 2x2 그리드에서 한 패널에만 내용
- **Blocker**: GridLayout 2x2 버그
- **DO NOT USE** until fixed

## 🚧 Work in Progress (검증 중)

나머지 예제들은 아직 시각적 검증이 완료되지 않았습니다.
사용 전에 반드시 출력 결과를 확인하세요.
```

### Step 3: 각 파일 상단에 상태 주석

```python
# examples/working/05_bubble_types.py
"""
STATUS: ✅ WORKING
VERIFIED: 2026-01-18
OUTPUT: examples/output/05_bubble_types.png

Different speech bubble types demonstration.
This example works correctly and can be used as reference.
"""

# examples/broken/01_simple_dialogue.py
"""
STATUS: 🔴 BROKEN - Layout bug
ISSUE: Content clusters in left panel only
BLOCKER: GridLayout horizontal layout (1x2) not working
DO NOT USE until GridLayout is fixed

Expected: Two panels side by side with Alice and Bob
Actual: Only left panel has content
"""
```

## Validation Workflow for Ralph Agent

**예제 작업 시 반드시:**

1. **수정 전**:
   - 예제 실행
   - PNG 확인
   - 작동 여부 파악
   - 상태 기록

2. **수정 중**:
   - 코드 수정
   - 예제 재실행
   - PNG 재확인
   - 여전히 안 되면 broken/에 유지
   - 작동하면 working/으로 이동

3. **수정 후**:
   - 상태 주석 업데이트
   - examples/README.md 업데이트
   - specs/code-visual-validation.md 업데이트

## Directory Structure

```
examples/
├── README.md                 # 전체 예제 상태 요약
├── working/                  # ✅ 작동하는 예제만
│   ├── 03_group_scene.py
│   └── 05_bubble_types.py
├── broken/                   # 🔴 버그 있는 예제
│   ├── 01_simple_dialogue.py
│   ├── 02_four_panel_comic.py
│   └── 04_expressions.py
├── wip/                      # 🚧 검증 중
│   ├── 06_multi_page_pdf.py
│   ├── 07_custom_layout.py
│   ├── 08_manual_positioning.py
│   ├── 09_using_templates.py
│   └── 10_error_handling.py
└── output/                   # 생성된 PNG/PDF
    ├── 03_group_scene.png
    ├── 05_bubble_types.png
    └── ...
```

## Success Criteria

**이 정리가 완료되면:**

- ✅ 사용자가 examples/working/만 보면 작동하는 예제 확인 가능
- ✅ broken/ 디렉토리를 보면 무엇이 안 되는지 명확
- ✅ 각 파일의 상태가 파일 자체에 주석으로 기록됨
- ✅ Ralph Agent가 수정 시 예제를 올바른 디렉토리로 이동
- ✅ 혼란 최소화

## For Ralph Agent: Checklist

**예제 수정 작업 시:**

- [ ] 수정할 예제 실행 → PNG 확인 → 현재 상태 파악
- [ ] 상태에 따라 working/broken/wip/ 중 올바른 위치로 이동
- [ ] 파일 상단에 STATUS 주석 추가/업데이트
- [ ] 수정 후 재실행 → PNG 재확인
- [ ] 작동하면 working/으로, 여전히 안 되면 broken/에 유지
- [ ] examples/README.md 업데이트
- [ ] specs/code-visual-validation.md에 검증 결과 기록

**절대 하지 말 것:**
- ❌ 작동 안 하는 예제를 working/에 두지 말 것
- ❌ 검증 없이 예제를 이동하지 말 것
- ❌ 상태 주석 없이 파일을 커밋하지 말 것
