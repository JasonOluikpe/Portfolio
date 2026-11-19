from contextlib import contextmanager

from nicegui import ui

from .components import div, link
from .content import PROFILE
from .setup import add_analytics, add_clip_lightbox, add_favicon, add_fonts, add_interactions

NAV = [
    ('Home', '/'),
    ('Projects', '/projects'),
    ('About', '/about'),
    ('Contact', '/contact'),
]


@contextmanager
def page_frame(active: str, title: str | None = None):
    """Shared shell for every page: dark-only theme, fixed top bar, scroll progress, footer."""
    ui.dark_mode().enable()
    ui.page_title(f"{title + ' | ' if title else ''}{PROFILE['name']}")
    add_fonts()
    add_favicon(PROFILE['logo'])
    add_clip_lightbox()
    add_interactions()
    add_analytics()

    div('glow')            # cursor-following light (moved by script)
    div('progress')        # scroll progress bar (driven by script)

    with ui.header(fixed=True, elevated=False).classes('topbar-shell'):
        with div('topbar'):
            with ui.link(target='/').classes('brand'):
                ui.image(PROFILE['logo']).props("alt='logo'")
                ui.html('<span class="brand-name">jason<span class="slash">/</span>oluikpe</span>', sanitize=False)
            with div('nav'):
                for text, href in NAV:
                    cls = 'nav-link active' if text == active else 'nav-link'
                    link(text, href, cls)
            link('Resume', PROFILE['resume'], 'btn primary nav-cta', new_tab=True)

    with div('page-enter'):
        yield

    with ui.element('footer').classes('footer'):
        with div('wrap foot'):
            ui.label(f"© {PROFILE['name']} 2026").classes('muted')
            with div('foot-links'):
                link('Email', f"mailto:{PROFILE['email']}", new_tab=True)
                link('LinkedIn', PROFILE['linkedin'], new_tab=True)
                link('GitHub', PROFILE['github'], new_tab=True)
