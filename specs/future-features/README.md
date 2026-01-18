# Future Features (Advanced, Optional)

이 디렉토리의 spec들은 구현되어 있지만, 프로젝트를 **정적 만화 제작**에 집중하기 위해 core 기능에서 제외되었습니다.

## 포함된 기능들

### [HTML Export](html-export.md)
- Interactive HTML export with zoom, pan controls
- Dark/light theme toggle
- Multi-page navigation
- Touch/mobile support

### [Animation Export](animation-export.md)
- Timeline-based GIF animation system
- 28 easing functions
- Property/Effect/Object animations
- AnimationGroup composition

### [Video Export](video-export.md)
- MP4/WebM video export via ffmpeg
- Quality settings (low/medium/high)
- Audio track support
- Frame extraction for post-processing

### [AI Images](ai-images.md)
- OpenAI DALL-E integration
- Replicate API support
- Background generation

### [Preview Server](preview-server.md)
- Live reload development server
- Hot reload with watchdog
- Web-based preview

### [Parser DSL](parser-dsl.md)
- Markup language for rapid comic creation
- Declarative syntax for panels and characters
- Text-based comic scripting

## 왜 보류되었나?

Comicode의 핵심 가치는 **코드로 그림을 그려서 만화를 만드는 것**입니다.
다음 이유로 위 기능들을 보류했습니다:

1. **복잡성 증가**: HTML/Video/Animation은 정적 이미지 생성과 다른 관심사
2. **의존성 증가**: ffmpeg, imageio, watchdog 등 추가 의존성 필요
3. **유지보수 부담**: 여러 출력 포맷을 지원하면 테스트와 버그 수정 부담 증가
4. **초점 분산**: "만화 그리기"에서 "멀티미디어 생성"으로 초점 이동

## 언제 사용하나?

다음과 같은 경우 이 기능들을 고려할 수 있습니다:

- **HTML Export**: 웹에서 인터랙티브하게 만화를 보여주고 싶을 때
- **Animation Export**: 캐릭터에 간단한 움직임을 추가하고 싶을 때
- **Video Export**: 만화를 동영상으로 변환하고 싶을 때
- **AI Images**: 배경이나 복잡한 이미지를 AI로 생성하고 싶을 때
- **Preview Server**: 개발 중 실시간으로 결과를 확인하고 싶을 때
- **Parser DSL**: 코드 대신 마크업으로 빠르게 만화를 작성하고 싶을 때

## 구현 상태

모든 기능은 완전히 구현되어 있으며 테스트도 통과합니다.
코드베이스에서 제거되지 않았으므로 필요시 언제든 사용할 수 있습니다.

다만, 프로젝트의 **공식 문서와 예제**에서는 핵심 기능만 다룹니다.

## 사용 방법

각 spec 문서를 참고하여 해당 기능을 사용할 수 있습니다.
예를 들어:

```python
# HTML Export
from comix import Page
page = Page()
# ... build page ...
page.render("output.html", format="html")

# Animation Export
from comix.animation import Timeline, PropertyAnimation
timeline = Timeline(fps=24, duration=2.0)
anim = PropertyAnimation(char, "opacity", start=0, end=1, duration=1.0)
timeline.add(anim)
timeline.render("animated.gif")

# Video Export
timeline.render("animated.mp4", format="video", quality="high")
```

---

**Updated**: 2026-01-18
**Status**: Available but not core
