from nicegui import ui

from .components import div, heading, label, link, media, paragraph
from .content import ABOUT, ABOUT_CLIPS, FEATURABLE_WIDGET_ID, PROFILE, PROJECT, REFERENCES
from .setup import add_clip_lightbox, add_featurable, add_fonts, add_video_pause


def render_topbar() -> None:
    with div('wrap'):
        with div('topbar'):
            with div('brand'):
                ui.image('/static/logo.png').props("alt='logo'")
                label(PROFILE['name'])
            with div('nav'):
                link('Projects', '#projects')
                link('About', '#about')
                link('References', '#references')
                link('Contact', '#contact')


def render_hero() -> None:
    with div('wrap hero'):
        with div('prompt'):
            div('chev')
            label(PROFILE['name'], 'hero-name')
            div('cursor')
        label(PROFILE['role'], 'role')
        label(PROFILE['tagline'], 'tagline')
        with div('actions'):
            link('Resume', PROFILE['resume'], 'btn primary', new_tab=True)
            link('LinkedIn', PROFILE['linkedin'], 'btn', new_tab=True)


def render_clips(clips) -> None:
    with div('clips'):
        for title, caption, file in clips:
            with div('clip'):
                media(file, 'Insert video here')
                label(title, 'clip-title')
                label(caption, 'clip-caption')


def render_projects() -> None:
    pr = PROJECT
    with ui.element('section').props('id=projects'):
        with div('wrap'):
            heading('Projects')
            with div('proj-head'):
                with div():
                    label(pr.name, 'proj-name')
                    label(pr.summary, 'proj-sum')
                with div('proj-links'):
                    for text, href in pr.links:
                        link(text, href, download=True)
            paragraph(pr.description, 'desc')
            with div('chips'):
                for tech in pr.stack:
                    label(tech, 'chip')

            media(*pr.overview, hero=True)

            render_clips(pr.clips)

            label(pr.more, 'more-title')
            label(pr.joke)
            render_clips(pr.more_clips)


def render_reviews() -> None:
    label('Reviews', 'sub-title')
    with div('reviews-embed'):
        if FEATURABLE_WIDGET_ID:
            ui.element('div').props(f'id="featurable-{FEATURABLE_WIDGET_ID}" data-featurable-async')
            add_featurable()
        else:
            with div('placeholder'):
                div('ph-chev')
                ui.label('Add your Featurable widget ID in content.py')

def render_references() -> None:
    with ui.element('section').props('id=references'):
        with div('wrap'):
            heading('References')
            with div('refs'):
                for name, job, phone in REFERENCES:
                    with div('ref'):
                        label(name, 'ref-name')
                        label(job, 'ref-job')
                        label(phone, 'ref-phone')


def render_about() -> None:
    with ui.element('section').props('id=about'):
        with div('wrap'):
            heading('About me')
            for para in ABOUT:
                paragraph(para, 'about-text')
            render_clips(ABOUT_CLIPS)
            render_reviews()


def render_footer() -> None:
    with ui.element('footer').props('id=contact'):
        with div('wrap foot'):
            label(f"© {PROFILE['name']} 2026")
            with div():
                link("Email", f"mailto:{PROFILE['email']}", new_tab=True)
                link('LinkedIn', PROFILE['linkedin'], new_tab=True)


@ui.page('/')
def index() -> None:
    add_fonts()
    add_video_pause()
    add_clip_lightbox()
    ui.dark_mode().enable()
    render_topbar()
    render_hero()
    render_projects()
    render_about()
    render_references()
    render_footer()