from nicegui import ui

from .config import STYLES_FILE
from .scripts import CLIP_LIGHTBOX, FAVICON, FEATURABLE, VIDEO_PAUSE

ANALYTICS_HTML = '''
<!-- Cloudflare Web Analytics -->
<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "4376511b01e4463f9b28108396962ac1"}'></script>
<!-- End Cloudflare Web Analytics -->
'''

FONTS_HTML = '''
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@400;500;600&display=swap' rel='stylesheet'>
'''


def configure_app() -> None:
    ui.add_css(STYLES_FILE.read_text(encoding='utf-8'), shared=True)


def add_fonts() -> None:
    ui.add_head_html(FONTS_HTML)


def add_video_pause() -> None:
    ui.add_body_html(VIDEO_PAUSE)


def add_featurable() -> None:
    ui.add_body_html(FEATURABLE)


def add_clip_lightbox() -> None:
    ui.add_body_html(CLIP_LIGHTBOX)


def add_favicon(url: str) -> None:
    ui.add_head_html(FAVICON.replace('__ICON__', url))


def add_analytics() -> None:
    ui.add_body_html(ANALYTICS_HTML)
