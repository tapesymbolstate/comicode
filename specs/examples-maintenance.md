# Examples Maintenance - 예제 정리 및 관리 기준

> **Note**: This document contains **process guidelines** for future maintenance.
> All 23 examples (01-23) are currently working correctly as of v0.1.61.

## What
examples/ 디렉토리를 주기적으로 정리하여 **실제로 작동하는 예제만 유지**하고, 버그가 있는 예제는 명확히 표시하거나 임시 제거한다.

## Why
**망가진 예제가 있으면 사용자가 혼란스럽다.**

현재 상황 (2026-01-18):
- ✅ 01-23 예제 파일 모두 존재
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

**All 23 examples are working.** As of 2026-01-18, all examples execute successfully and produce correct output.

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
| 16_character_types.py | ✅ Working |
| 17_ai_image_generation.py | ✅ Working |
| 18_flow_layout.py | ✅ Working |
| 19_constraint_layout.py | ✅ Working |
| 20_themes_and_styles.py | ✅ Working |
| 21_text_and_narration.py | ✅ Working |
| 22_advanced_templates.py | ✅ Working |
| 23_preview_server.py | ✅ Working |

## Maintenance Process (For Future Use)

> **Note**: This section describes what to do IF examples break in the future.
> Currently all 23 examples are working correctly.

### If An Example Breaks

1. **Document the issue** in this file's status table above
2. **Create an issue** describing the problem
3. **Fix the example** or the underlying library code
4. **Verify the fix** by running the example and checking output
5. **Update status** back to ✅ Working

### Validation Workflow

**When modifying examples:**

1. Run the example: `uv run python examples/XX_example.py`
2. Check the output in `examples/output/`
3. Visually verify the output matches the code's intent
4. Update status table if needed

### Source of Truth

- **examples/README.md** - Authoritative list of all examples with descriptions
- **Status table above** - Quick reference for example health
- **specs/code-visual-validation.md** - Historical validation notes (archived)
