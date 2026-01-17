# Preview Server - Live Reload Development Server

## What

A development server that renders comic scripts to SVG and serves them via HTTP with automatic hot-reload when files change, enabling real-time preview during comic development.

## Why

Developing comics iteratively requires frequent render-preview cycles. Without a live preview:

1. **Slow iteration**: Must manually re-run scripts and open files
2. **Context switching**: Developer leaves editor to view results
3. **No immediate feedback**: Changes feel disconnected from results

The preview server enables:
1. **Instant feedback**: See changes immediately in browser
2. **Side-by-side editing**: Editor and preview together
3. **Rapid iteration**: Faster creative workflow
4. **Error visibility**: Render errors displayed in browser

## Acceptance Criteria

### Must Have
- [x] HTTP server serving rendered SVG
- [x] HTML wrapper page with embedded preview
- [x] File change detection
- [x] Auto-reload on file changes
- [x] Browser auto-open on server start
- [x] Graceful shutdown handling
- [x] CLI command (`comix serve`)
- [x] Error display in browser (styled error SVG)

### Should Have
- [x] Port configuration with auto-increment fallback
- [x] Host binding configuration
- [x] Optional watchdog file system monitoring
- [x] Polling fallback when watchdog unavailable
- [x] Version tracking for change detection
- [x] Cache-busting for browser refresh
- [x] Status indicator in UI (connected/reloading/error)
- [x] `--no-browser` option to skip auto-open

### Won't Have (This Iteration)
- [ ] Multiple file watching (single script only)
- [ ] Live CSS/theme editing
- [ ] WebSocket-based updates (uses polling)
- [ ] Mobile device preview
- [ ] Remote access beyond localhost

## Context

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Comic Script   │────▶│  Preview Server │────▶│     Browser     │
│   (Python)      │     │   (HTTP + Poll) │     │   (SVG View)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │
         │ file change          │ /poll endpoint
         │                      │ (30s long-poll)
         ▼                      ▼
┌─────────────────┐     ┌─────────────────┐
│    Watchdog     │────▶│  Re-render SVG  │
│  (optional)     │     │  + bump version │
└─────────────────┘     └─────────────────┘
```

### HTTP Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` or `/index.html` | GET | HTML page with embedded JavaScript |
| `/comic.svg` | GET | Rendered SVG with cache-control headers |
| `/version` | GET | JSON with current render version |
| `/poll` | GET | Long-poll (30s) for file changes |

### Hot Reload Mechanism

1. Client fetches initial version from `/version`
2. Client polls `/poll` endpoint (long-poll, 30s timeout)
3. Server detects file change (mtime or watchdog event)
4. Server re-renders SVG, increments version
5. `/poll` returns new version
6. Client updates SVG src with cache-busting timestamp
7. Repeat from step 2

### File Change Detection

Two mechanisms (watchdog preferred if available):

1. **Watchdog** (optional): File system event monitoring with 100ms debounce
2. **Polling**: mtime comparison during `/poll` requests

### UI Status Indicators

- **Green pulsing dot**: Connected and watching
- **Yellow dot**: Reloading in progress
- **Red dot**: Connection lost or render error

## Examples

### Example 1: Basic Usage

```bash
# Start preview server for a script
comix serve my_comic.py

# Output:
# Starting preview server at http://localhost:8000
# Watching my_comic.py for changes...
# Press Ctrl+C to stop
```

Browser automatically opens to `http://localhost:8000`.

### Example 2: Custom Port and Host

```bash
comix serve my_comic.py --port 3000 --host 0.0.0.0
```

### Example 3: Without Auto-Open Browser

```bash
comix serve my_comic.py --no-browser
```

### Example 4: Programmatic Server Usage

```python
from comix.preview import PreviewServer

server = PreviewServer("my_comic.py", port=8000)
server.start()  # Blocks until Ctrl+C

# Or for non-blocking:
server.start(block=False)
# ... do other things ...
server.stop()
```

### Example 5: Script That Gets Previewed

```python
# my_comic.py
from comix import Page, Stickman

page = Page(width=400, height=300)
char = Stickman(name="Test").move_to((200, 150))
page.add(char)

# The page variable is auto-discovered by the server
```

### Example 6: Using with Templates

```python
# my_template_comic.py
from comix import FourKoma, Stickman

page = FourKoma()

# Add content to panels
page.panels[0].add_content(
    Stickman(name="A").say("Panel 1")
)
# ... more panels ...
```

## Open Questions

- [x] Watch directory or single file? **Decision**: Single file for simplicity
- [x] WebSocket vs polling? **Decision**: Polling for broader compatibility
- [x] Multiple browser tabs? **Decision**: Each tab polls independently
- [x] Handle script syntax errors? **Decision**: Display error SVG with message

## Test Requirements

1. **Server Lifecycle**:
   - Test: Server starts on specified port
   - Test: Server tries next port if occupied
   - Test: Graceful shutdown cleans up resources
   - Test: Browser opens on start (when enabled)

2. **Endpoints**:
   - Test: `/` returns HTML with JavaScript
   - Test: `/comic.svg` returns valid SVG
   - Test: `/version` returns JSON with version number
   - Test: `/poll` blocks until timeout or change
   - Test: 404 for unknown paths

3. **Hot Reload**:
   - Test: Version increments on file change
   - Test: SVG re-renders on file change
   - Test: Error displayed when render fails
   - Test: Recovery from errors on fix

4. **File Watching**:
   - Test: Watchdog events trigger reload (when available)
   - Test: Mtime polling works as fallback
   - Test: Debouncing prevents rapid re-renders

5. **Error Handling**:
   - Test: Script with syntax error shows error SVG
   - Test: Missing Page object shows helpful message
   - Test: HTML entities escaped in error messages

## Implementation Status

Fully implemented in `/comix/preview/server.py` with 56 tests in `/tests/test_preview.py`.

Optional dependency - requires `uv sync --extra web` for watchdog file watching (falls back to polling without it).
