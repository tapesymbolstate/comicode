# Comix - 만화 제작 라이브러리 아키텍처 설계

> Manim 구조를 벤치마킹한 코드 기반 만화 제작 프레임워크

---

## 1. Manim 핵심 구조 분석

### 1.1 Manim의 4대 핵심 개념

```
┌─────────────────────────────────────────────────────────────┐
│                        Scene                                 │
│  (캔버스 - 모든 요소를 조율하고 렌더링을 관리)                    │
├─────────────────────────────────────────────────────────────┤
│                        Mobject                               │
│  (수학적 객체 - 화면에 표시되는 모든 것)                         │
├─────────────────────────────────────────────────────────────┤
│                       Animation                              │
│  (애니메이션 - Mobject의 시간에 따른 변화를 정의)                 │
├─────────────────────────────────────────────────────────────┤
│                       Renderer                               │
│  (렌더러 - 실제 그리기 담당, Cairo/OpenGL 백엔드)                │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Manim 디렉토리 구조

```
manimlib/
├── __init__.py
├── __main__.py              # CLI 진입점
├── config.py                # 설정 처리
├── constants.py             # 상수 정의
│
├── scene/
│   ├── scene.py             # 기본 Scene 클래스
│   ├── scene_file_writer.py # 파일 출력
│   └── three_d_scene.py     # 3D 씬
│
├── mobject/
│   ├── mobject.py           # 기본 Mobject 클래스
│   ├── types/
│   │   ├── vectorized_mobject.py  # VMobject (벡터 기반)
│   │   └── image_mobject.py       # 이미지
│   ├── svg/
│   │   ├── svg_mobject.py
│   │   ├── tex_mobject.py   # LaTeX
│   │   └── text_mobject.py  # 텍스트
│   └── geometry.py          # 기하학적 도형
│
├── animation/
│   ├── animation.py         # 기본 Animation 클래스
│   ├── creation.py          # Create, Write 등
│   ├── transform.py         # Transform 계열
│   └── fading.py            # FadeIn/Out
│
├── camera/
│   └── camera.py            # 카메라 (뷰포트)
│
├── renderer/
│   ├── cairo_renderer.py    # 2D 벡터
│   └── opengl_renderer.py   # 3D/GPU
│
└── utils/
    ├── color.py
    ├── bezier.py
    ├── rate_functions.py    # 이징 함수
    └── space_ops.py         # 좌표 연산
```

### 1.3 Manim의 실행 흐름

```
CLI 실행 → Config 로드 → Scene 인스턴스화 → Renderer 초기화
    ↓
construct() 실행 → play() 호출 → Animation 처리 → 프레임 렌더링
    ↓
파일 출력 (mp4, gif, png)
```

---

## 2. Comix 아키텍처 설계

### 2.1 핵심 개념 매핑

| Manim | Comix | 설명 |
|-------|-------|------|
| Scene | Page / Strip | 만화 페이지 또는 한 줄 |
| Mobject | ComixObject | 화면에 표시되는 모든 것 |
| VMobject | Panel, Bubble, Character | 벡터 기반 만화 요소 |
| Animation | Effect | 웹툰용 효과 (선택적) |
| Camera | View | 패널 뷰 / 줌 |
| Renderer | Renderer | SVG, PNG, PDF 출력 |

### 2.2 Comix 디렉토리 구조

```
comix/
├── __init__.py
├── __main__.py              # CLI 진입점
├── config.py                # 전역 설정
├── constants.py             # 상수 (폰트, 색상, 크기)
│
├── page/                    # Scene에 대응
│   ├── page.py              # Page 클래스 (여러 패널)
│   ├── strip.py             # Strip 클래스 (한 줄)
│   └── page_writer.py       # 출력 담당
│
├── cobject/                 # Mobject에 대응 (Comix Object)
│   ├── cobject.py           # 기본 클래스
│   │
│   ├── panel/               # 패널 관련
│   │   ├── panel.py         # Panel 클래스
│   │   ├── gutter.py        # 패널 사이 간격
│   │   └── border.py        # 테두리 스타일
│   │
│   ├── bubble/              # 말풍선 관련
│   │   ├── bubble.py        # 기본 Bubble 클래스
│   │   ├── speech.py        # 일반 말풍선
│   │   ├── thought.py       # 생각 풍선 (구름)
│   │   ├── shout.py         # 외침 풍선 (뾰족)
│   │   ├── whisper.py       # 속삭임 (점선)
│   │   └── narrator.py      # 나레이션 박스
│   │
│   ├── text/                # 텍스트 관련
│   │   ├── text.py          # 기본 Text 클래스
│   │   ├── styled_text.py   # 스타일링된 텍스트
│   │   ├── sfx.py           # 효과음 (의성어/의태어)
│   │   └── font.py          # 폰트 관리
│   │
│   ├── character/           # 캐릭터 관련
│   │   ├── character.py     # 기본 Character 클래스
│   │   ├── stickman.py      # 스틱맨
│   │   ├── simple_face.py   # 단순 얼굴
│   │   ├── expression.py    # 표정 정의
│   │   └── pose.py          # 포즈 정의
│   │
│   ├── shapes/              # 기본 도형
│   │   ├── rectangle.py
│   │   ├── circle.py
│   │   └── line.py
│   │
│   └── image/               # 외부 이미지
│       ├── image.py         # 이미지 삽입
│       └── ai_image.py      # AI 생성 이미지 (확장)
│
├── effect/                  # Animation에 대응 (웹툰용)
│   ├── effect.py            # 기본 Effect 클래스
│   ├── appear.py            # 등장 효과
│   ├── shake.py             # 흔들림
│   ├── zoom.py              # 줌 인/아웃
│   └── motion_line.py       # 속도선
│
├── layout/                  # 레이아웃 시스템
│   ├── grid.py              # 그리드 레이아웃
│   ├── flow.py              # 자동 배치
│   └── constraints.py       # 제약 조건
│
├── style/                   # 스타일 시스템
│   ├── style.py             # Style 클래스
│   ├── presets/             # 프리셋
│   │   ├── manga.py         # 일본 만화 스타일
│   │   ├── comic.py         # 미국 코믹 스타일
│   │   ├── webtoon.py       # 한국 웹툰 스타일
│   │   └── minimal.py       # 미니멀 스타일
│   └── theme.py             # 테마 관리
│
├── renderer/                # 렌더링 백엔드
│   ├── renderer.py          # 기본 Renderer
│   ├── svg_renderer.py      # SVG 출력
│   ├── cairo_renderer.py    # PNG/PDF 출력
│   └── web_renderer.py      # HTML/웹 출력
│
├── parser/                  # 마크업 파서 (선택적)
│   ├── parser.py
│   └── markup.py            # 간단한 마크업 → 코드 변환
│
└── utils/
    ├── color.py             # 색상 유틸
    ├── geometry.py          # 기하학 연산
    ├── bezier.py            # 베지어 곡선 (말풍선용)
    ├── typography.py        # 타이포그래피 유틸
    └── positioning.py       # 위치 계산
```

---

## 3. 핵심 클래스 설계

### 3.1 CObject (Comix Object) - Mobject에 대응

```python
# comix/cobject/cobject.py

from __future__ import annotations
from typing import Self
import numpy as np

class CObject:
    """모든 만화 요소의 기본 클래스 (Manim의 Mobject 대응)"""
    
    def __init__(
        self,
        position: tuple[float, float] = (0, 0),
        scale: float = 1.0,
        rotation: float = 0,
        opacity: float = 1.0,
        z_index: int = 0,
        name: str | None = None,
    ):
        self.position = np.array(position)
        self.scale = scale
        self.rotation = rotation
        self.opacity = opacity
        self.z_index = z_index
        self.name = name or self.__class__.__name__
        
        self.submobjects: list[CObject] = []
        self.parent: CObject | None = None
        
        # 내부 상태
        self._points = np.zeros((0, 2))
        self._needs_update = True
    
    # === Manim 스타일 체이닝 메서드 ===
    
    def move_to(self, position: tuple[float, float]) -> Self:
        """절대 위치 이동"""
        self.position = np.array(position)
        return self
    
    def shift(self, delta: tuple[float, float]) -> Self:
        """상대 위치 이동"""
        self.position += np.array(delta)
        return self
    
    def set_scale(self, scale: float) -> Self:
        self.scale = scale
        return self
    
    def set_opacity(self, opacity: float) -> Self:
        self.opacity = opacity
        return self
    
    def rotate(self, angle: float) -> Self:
        """라디안 단위 회전"""
        self.rotation += angle
        return self
    
    def next_to(
        self, 
        other: CObject, 
        direction: str = "right",
        buff: float = 10
    ) -> Self:
        """다른 객체 옆에 배치"""
        # direction: "up", "down", "left", "right"
        ...
        return self
    
    def align_to(self, other: CObject, edge: str) -> Self:
        """다른 객체와 정렬"""
        ...
        return self
    
    # === 계층 구조 ===
    
    def add(self, *cobjects: CObject) -> Self:
        """하위 객체 추가"""
        for obj in cobjects:
            if obj not in self.submobjects:
                self.submobjects.append(obj)
                obj.parent = self
        return self
    
    def remove(self, *cobjects: CObject) -> Self:
        """하위 객체 제거"""
        for obj in cobjects:
            if obj in self.submobjects:
                self.submobjects.remove(obj)
                obj.parent = None
        return self
    
    def get_family(self) -> list[CObject]:
        """자신과 모든 하위 객체 반환"""
        family = [self]
        for child in self.submobjects:
            family.extend(child.get_family())
        return family
    
    # === 바운딩 박스 ===
    
    def get_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        """(min_point, max_point) 반환"""
        ...
    
    def get_width(self) -> float:
        bbox = self.get_bounding_box()
        return bbox[1][0] - bbox[0][0]
    
    def get_height(self) -> float:
        bbox = self.get_bounding_box()
        return bbox[1][1] - bbox[0][1]
    
    def get_center(self) -> np.ndarray:
        bbox = self.get_bounding_box()
        return (bbox[0] + bbox[1]) / 2
    
    # === 렌더링 (서브클래스에서 구현) ===
    
    def generate_points(self) -> None:
        """도형의 점들을 생성 (서브클래스에서 오버라이드)"""
        pass
    
    def get_render_data(self) -> dict:
        """렌더러에 전달할 데이터"""
        return {
            "points": self._points,
            "position": self.position,
            "scale": self.scale,
            "rotation": self.rotation,
            "opacity": self.opacity,
        }
```

### 3.2 Panel 클래스

```python
# comix/cobject/panel/panel.py

from ..cobject import CObject
from ..border import Border

class Panel(CObject):
    """만화 패널 (컷)"""
    
    def __init__(
        self,
        width: float = 300,
        height: float = 300,
        border: Border | None = None,
        background_color: str = "#FFFFFF",
        padding: float = 10,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.border = border or Border()
        self.background_color = background_color
        self.padding = padding
        
        self._content: list[CObject] = []
    
    def add_content(self, *cobjects: CObject) -> Self:
        """패널 내부에 콘텐츠 추가"""
        for obj in cobjects:
            self._content.append(obj)
            self.add(obj)
        return self
    
    def set_background(self, color: str = None, image: str = None) -> Self:
        """배경 설정"""
        if color:
            self.background_color = color
        if image:
            self.background_image = image
        return self
```

### 3.3 Bubble 클래스 (말풍선)

```python
# comix/cobject/bubble/bubble.py

from ..cobject import CObject
from ..text import StyledText
from ...utils.bezier import create_bubble_path

class Bubble(CObject):
    """말풍선 기본 클래스"""
    
    # 말풍선 타입
    SPEECH = "speech"      # 일반 대사
    THOUGHT = "thought"    # 생각 (구름 모양)
    SHOUT = "shout"        # 외침 (뾰족)
    WHISPER = "whisper"    # 속삭임 (점선)
    NARRATOR = "narrator"  # 나레이션 (사각형)
    
    def __init__(
        self,
        text: str = "",
        style: str = SPEECH,
        
        # 말풍선 모양
        width: float | None = None,      # None이면 자동
        height: float | None = None,
        padding: tuple[float, float, float, float] = (15, 20, 15, 20),  # top, right, bottom, left
        corner_radius: float = 20,
        
        # 꼬리 (tail)
        tail_direction: str = "bottom-left",  # 꼬리 방향
        tail_length: float = 30,
        tail_width: float = 20,
        tail_target: CObject | tuple[float, float] | None = None,  # 꼬리가 가리키는 대상
        
        # 테두리
        border_color: str = "#000000",
        border_width: float = 2,
        
        # 내부
        fill_color: str = "#FFFFFF",
        
        # 텍스트 스타일
        font_family: str = "나눔손글씨",
        font_size: float = 16,
        font_color: str = "#000000",
        text_align: str = "center",
        line_height: float = 1.4,
        
        # 특수 효과
        wobble: float = 0,        # 떨림 정도 (0-1)
        emphasis: bool = False,   # 강조 (두꺼운 테두리)
        
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.text = text
        self.style = style
        
        # 치수
        self._auto_width = width is None
        self._auto_height = height is None
        self.width = width or 0
        self.height = height or 0
        self.padding = padding
        self.corner_radius = corner_radius
        
        # 꼬리
        self.tail_direction = tail_direction
        self.tail_length = tail_length
        self.tail_width = tail_width
        self.tail_target = tail_target
        
        # 스타일
        self.border_color = border_color
        self.border_width = border_width
        self.fill_color = fill_color
        
        # 텍스트
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.text_align = text_align
        self.line_height = line_height
        
        # 효과
        self.wobble = wobble
        self.emphasis = emphasis
        
        # 내부 텍스트 객체
        self._text_object: StyledText | None = None
        self._generate_content()
    
    def _generate_content(self):
        """내부 텍스트 객체 생성"""
        self._text_object = StyledText(
            self.text,
            font_family=self.font_family,
            font_size=self.font_size,
            color=self.font_color,
            align=self.text_align,
            line_height=self.line_height,
            max_width=self.width - self.padding[1] - self.padding[3] if self.width else None
        )
        
        if self._auto_width or self._auto_height:
            text_bbox = self._text_object.get_bounding_box()
            if self._auto_width:
                self.width = text_bbox[1][0] - text_bbox[0][0] + self.padding[1] + self.padding[3]
            if self._auto_height:
                self.height = text_bbox[1][1] - text_bbox[0][1] + self.padding[0] + self.padding[2]
    
    def set_text(self, text: str) -> Self:
        """텍스트 변경"""
        self.text = text
        self._generate_content()
        return self
    
    def point_to(self, target: CObject | tuple[float, float]) -> Self:
        """꼬리가 대상을 가리키도록 설정"""
        self.tail_target = target
        return self
    
    def attach_to(self, character: CObject, anchor: str = "top") -> Self:
        """캐릭터에 말풍선 부착"""
        # anchor: "top", "top-left", "top-right", "side-left", "side-right"
        char_bbox = character.get_bounding_box()
        
        if anchor == "top":
            self.move_to((
                character.get_center()[0],
                char_bbox[1][1] + self.height / 2 + 20
            ))
            self.point_to(character)
        # ... 다른 anchor 처리
        
        return self
    
    def generate_points(self):
        """말풍선 외곽선 점 생성"""
        self._points = create_bubble_path(
            width=self.width,
            height=self.height,
            style=self.style,
            corner_radius=self.corner_radius,
            tail_direction=self.tail_direction,
            tail_length=self.tail_length,
            tail_width=self.tail_width,
            wobble=self.wobble
        )


# 편의 서브클래스들

class SpeechBubble(Bubble):
    """일반 대사 말풍선"""
    def __init__(self, text: str = "", **kwargs):
        super().__init__(text=text, style=Bubble.SPEECH, **kwargs)


class ThoughtBubble(Bubble):
    """생각 풍선 (구름 모양)"""
    def __init__(self, text: str = "", **kwargs):
        kwargs.setdefault("corner_radius", 999)  # 둥글게
        super().__init__(text=text, style=Bubble.THOUGHT, **kwargs)


class ShoutBubble(Bubble):
    """외침 풍선 (뾰족한 모양)"""
    def __init__(self, text: str = "", **kwargs):
        kwargs.setdefault("border_width", 3)
        kwargs.setdefault("font_size", 20)
        super().__init__(text=text, style=Bubble.SHOUT, **kwargs)


class WhisperBubble(Bubble):
    """속삭임 풍선 (점선)"""
    def __init__(self, text: str = "", **kwargs):
        kwargs.setdefault("font_size", 14)
        super().__init__(text=text, style=Bubble.WHISPER, **kwargs)
```

### 3.4 Character 클래스

```python
# comix/cobject/character/character.py

from ..cobject import CObject
from .expression import Expression
from .pose import Pose

class Character(CObject):
    """캐릭터 기본 클래스"""
    
    def __init__(
        self,
        name: str = "Character",
        style: str = "stickman",  # "stickman", "simple", "detailed"
        
        # 기본 속성
        color: str = "#000000",
        fill_color: str | None = None,
        
        # 크기
        height: float = 100,
        
        # 초기 상태
        expression: str | Expression = "neutral",
        pose: str | Pose = "standing",
        facing: str = "right",  # "left", "right", "front", "back"
        
        **kwargs
    ):
        super().__init__(name=name, **kwargs)
        
        self.style = style
        self.color = color
        self.fill_color = fill_color
        self.height = height
        self.facing = facing
        
        # 표정과 포즈
        self._expression = self._resolve_expression(expression)
        self._pose = self._resolve_pose(pose)
    
    def _resolve_expression(self, expr) -> Expression:
        if isinstance(expr, Expression):
            return expr
        return Expression.from_name(expr)
    
    def _resolve_pose(self, pose) -> Pose:
        if isinstance(pose, Pose):
            return pose
        return Pose.from_name(pose)
    
    def set_expression(self, expression: str | Expression) -> Self:
        """표정 변경"""
        self._expression = self._resolve_expression(expression)
        self._needs_update = True
        return self
    
    def set_pose(self, pose: str | Pose) -> Self:
        """포즈 변경"""
        self._pose = self._resolve_pose(pose)
        self._needs_update = True
        return self
    
    def face(self, direction: str) -> Self:
        """바라보는 방향 변경"""
        self.facing = direction
        return self
    
    def say(self, text: str, **bubble_kwargs) -> Bubble:
        """말풍선 생성 및 부착"""
        from ..bubble import SpeechBubble
        bubble = SpeechBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble
    
    def think(self, text: str, **bubble_kwargs) -> Bubble:
        """생각 풍선 생성 및 부착"""
        from ..bubble import ThoughtBubble
        bubble = ThoughtBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble


class Stickman(Character):
    """스틱맨 캐릭터"""
    
    def __init__(self, name: str = "Stickman", **kwargs):
        kwargs.setdefault("style", "stickman")
        super().__init__(name=name, **kwargs)
    
    def generate_points(self):
        """스틱맨 도형 생성"""
        # 머리, 몸통, 팔, 다리 점 생성
        ...


class SimpleFace(Character):
    """단순한 얼굴 캐릭터 (이모티콘 스타일)"""
    
    def __init__(self, name: str = "Face", **kwargs):
        kwargs.setdefault("style", "simple")
        super().__init__(name=name, **kwargs)
```

### 3.5 Page 클래스 (Scene에 대응)

```python
# comix/page/page.py

from typing import Self
from ..cobject import CObject, Panel
from ..layout import GridLayout
from .page_writer import PageWriter

class Page:
    """만화 페이지 (Manim의 Scene에 대응)"""
    
    def __init__(
        self,
        width: float = 800,
        height: float = 1200,
        background_color: str = "#FFFFFF",
        margin: float = 20,
        gutter: float = 10,  # 패널 사이 간격
    ):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.margin = margin
        self.gutter = gutter
        
        self._panels: list[Panel] = []
        self._cobjects: list[CObject] = []
        self._layout: GridLayout | None = None
    
    # === Panel 관리 (Manim의 add/remove 스타일) ===
    
    def add(self, *cobjects: CObject) -> Self:
        """CObject 추가"""
        for obj in cobjects:
            if isinstance(obj, Panel):
                self._panels.append(obj)
            self._cobjects.append(obj)
        return self
    
    def remove(self, *cobjects: CObject) -> Self:
        """CObject 제거"""
        for obj in cobjects:
            if obj in self._panels:
                self._panels.remove(obj)
            if obj in self._cobjects:
                self._cobjects.remove(obj)
        return self
    
    # === 레이아웃 ===
    
    def set_layout(self, rows: int, cols: int) -> Self:
        """그리드 레이아웃 설정"""
        self._layout = GridLayout(
            rows=rows,
            cols=cols,
            width=self.width - 2 * self.margin,
            height=self.height - 2 * self.margin,
            gutter=self.gutter
        )
        return self
    
    def auto_layout(self) -> Self:
        """패널 자동 배치"""
        if self._layout and self._panels:
            positions = self._layout.calculate_positions(len(self._panels))
            for panel, pos in zip(self._panels, positions):
                panel.move_to(pos["center"])
                panel.width = pos["width"]
                panel.height = pos["height"]
        return self
    
    # === 빌드 (Manim의 construct에 대응) ===
    
    def build(self) -> None:
        """페이지 구성 (서브클래스에서 오버라이드)"""
        pass
    
    # === 렌더링 ===
    
    def render(
        self,
        output_path: str = "output.png",
        format: str = "png",  # "png", "svg", "pdf"
        quality: str = "medium",  # "low", "medium", "high"
    ) -> str:
        """페이지 렌더링 및 저장"""
        self.build()
        self.auto_layout()
        
        writer = PageWriter(self, format=format, quality=quality)
        return writer.write(output_path)
    
    def show(self) -> None:
        """미리보기 (개발용)"""
        import tempfile
        import webbrowser
        
        path = self.render(
            output_path=tempfile.mktemp(suffix=".svg"),
            format="svg"
        )
        webbrowser.open(f"file://{path}")


# 편의 클래스: 싱글 패널
class SinglePanel(Page):
    """단일 패널 만화"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._main_panel = Panel(
            width=self.width - 2 * self.margin,
            height=self.height - 2 * self.margin
        )
        self.add(self._main_panel)
    
    @property
    def panel(self) -> Panel:
        return self._main_panel


# 편의 클래스: 스트립 (4컷 등)
class Strip(Page):
    """가로 또는 세로 스트립"""
    
    def __init__(
        self,
        panels: int = 4,
        direction: str = "horizontal",  # "horizontal", "vertical"
        **kwargs
    ):
        # 방향에 따라 크기 조정
        if direction == "horizontal":
            kwargs.setdefault("width", 1200)
            kwargs.setdefault("height", 300)
        else:
            kwargs.setdefault("width", 300)
            kwargs.setdefault("height", 1200)
        
        super().__init__(**kwargs)
        
        self.direction = direction
        self.num_panels = panels
        
        if direction == "horizontal":
            self.set_layout(rows=1, cols=panels)
        else:
            self.set_layout(rows=panels, cols=1)
        
        # 패널 자동 생성
        for i in range(panels):
            self.add(Panel(name=f"Panel_{i+1}"))
```

### 3.6 Style 시스템

```python
# comix/style/style.py

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Style:
    """스타일 정의 (CSS처럼 사용)"""
    
    # 테두리
    border_color: str = "#000000"
    border_width: float = 2
    border_style: str = "solid"  # "solid", "dashed", "dotted"
    
    # 채우기
    fill_color: str = "#FFFFFF"
    fill_opacity: float = 1.0
    
    # 텍스트
    font_family: str = "sans-serif"
    font_size: float = 16
    font_weight: str = "normal"  # "normal", "bold"
    font_style: str = "normal"  # "normal", "italic"
    font_color: str = "#000000"
    text_align: str = "left"
    line_height: float = 1.4
    
    # 그림자
    shadow: bool = False
    shadow_color: str = "#00000033"
    shadow_offset: tuple[float, float] = (2, 2)
    shadow_blur: float = 4
    
    def merge_with(self, other: "Style") -> "Style":
        """다른 스타일과 병합 (other가 우선)"""
        ...
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        ...


# 프리셋 스타일들
MANGA_STYLE = Style(
    border_color="#000000",
    border_width=2,
    font_family="M PLUS Rounded 1c",
    font_size=14,
)

WEBTOON_STYLE = Style(
    border_color="#333333",
    border_width=0,
    font_family="나눔바른고딕",
    font_size=16,
    shadow=True,
)

COMIC_STYLE = Style(
    border_color="#000000",
    border_width=3,
    font_family="Comic Sans MS",
    font_size=18,
    font_weight="bold",
)
```

---

## 4. 사용 예시

### 4.1 기본 사용법 (Manim 스타일)

```python
from comix import Page, Panel, Stickman, SpeechBubble, ShoutBubble

class MyComic(Page):
    def build(self):
        self.set_layout(rows=2, cols=2)
        
        # 패널 1
        p1 = Panel()
        char_a = Stickman("철수").move_to((100, 150))
        char_b = Stickman("영희").move_to((200, 150)).face("left")
        
        bubble1 = char_a.say("안녕!")
        
        p1.add_content(char_a, char_b, bubble1)
        
        # 패널 2
        p2 = Panel()
        char_b2 = Stickman("영희").move_to((150, 150))
        bubble2 = ShoutBubble("뭐라고?!").attach_to(char_b2)
        
        p2.add_content(char_b2, bubble2)
        
        # 패널 3, 4 ...
        p3 = Panel()
        p4 = Panel()
        
        self.add(p1, p2, p3, p4)

# 렌더링
comic = MyComic()
comic.render("my_comic.png")
```

### 4.2 세밀한 제어

```python
from comix import Page, Panel, Bubble, Font, Style
from comix.cobject.text import SFX

# 커스텀 말풍선
bubble = Bubble(
    text="이건 비밀인데...",
    style=Bubble.WHISPER,
    
    width=200,
    padding=(20, 25, 20, 25),
    corner_radius=30,
    
    tail_direction="bottom-right",
    tail_length=40,
    tail_width=15,
    
    border_color="#666666",
    border_width=1,
    border_style="dashed",
    
    fill_color="#F5F5F5",
    
    font_family="나눔손글씨 붓",
    font_size=14,
    font_color="#333333",
    font_style="italic",
    
    wobble=0.1,
)

# 효과음
sfx = SFX(
    "쾅!",
    font_size=48,
    font_family="배민 을지로체",
    color="#FF0000",
    rotation=15,
    outline=True,
    outline_color="#FFFFFF",
    outline_width=3,
)
```

### 4.3 마크업 파서 (선택적 기능)

```python
from comix.parser import parse_markup

markup = """
[page 2x2]

# panel 1
철수(left, surprised): "뭐라고?!"
영희(right, smug): "응, 진짜야"

# panel 2  
철수(closeup): "..."
sfx: 충격

# panel 3
[background: 카페 전경]
narrator: "그날 이후..."

# panel 4
철수(center): "믿을 수 없어"
"""

page = parse_markup(markup)
page.render("output.png")
```

---

## 5. 기술 스택 제안

### 5.1 핵심 의존성

| 라이브러리 | 용도 |
|-----------|------|
| `numpy` | 좌표 연산, 점 계산 |
| `pycairo` | PNG/PDF 렌더링 |
| `svgwrite` | SVG 출력 |
| `Pillow` | 이미지 처리 |
| `fonttools` | 폰트 메트릭 |
| `click` | CLI |
| `pydantic` | 설정 검증 |

### 5.2 선택적 의존성

| 라이브러리 | 용도 |
|-----------|------|
| `openai` / `replicate` | AI 이미지 생성 |
| `lark` | 마크업 파서 |
| `rich` | CLI 출력 꾸미기 |
| `watchdog` | 핫 리로드 |

---

## 6. 개발 로드맵

### Phase 1: 코어 (MVP)
- [ ] CObject 기본 클래스
- [ ] Panel, Bubble, Text
- [ ] Stickman 캐릭터
- [ ] SVG Renderer
- [ ] Page 클래스
- [ ] 기본 CLI

### Phase 2: 스타일링
- [ ] Style 시스템
- [ ] 프리셋 (manga, webtoon, comic)
- [ ] Font 관리
- [ ] 커스텀 말풍선 모양

### Phase 3: 레이아웃
- [ ] GridLayout
- [ ] FlowLayout
- [ ] 자동 말풍선 배치

### Phase 4: 확장
- [ ] AI 이미지 연동
- [ ] 마크업 파서
- [ ] 웹 미리보기
- [ ] 웹툰용 Effect 시스템

---

## 7. 참고

- [Manim Community Edition](https://github.com/ManimCommunity/manim)
- [ManimGL (3b1b)](https://github.com/3b1b/manim)
- [Manim 내부 구조 문서](https://3b1b.github.io/manim/getting_started/structure.html)
- [Manim Deep Dive](https://docs.manim.community/en/stable/guides/deep_dive.html)