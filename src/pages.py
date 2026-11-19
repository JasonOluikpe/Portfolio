from nicegui import ui

from .components import div, label, link, media, paragraph, rich
from .content import (ABOUT, ABOUT_CLIPS, FACTS, FEATURABLE_WIDGET_ID, INTERESTS, PROFILE,
                      PROJECT, REFERENCES, ROLES, betteride_links)
from .layout import page_frame
from .setup import add_featurable


# ───────────────────────── shared bits ─────────────────────────
def eyebrow(text: str) -> None:
    label(f'<span class="chev-s">&gt;</span> {text}', 'eyebrow reveal')


def section_title(text: str, sub: str = '') -> None:
    with div('sec-title reveal'):
        ui.html(f'<h2>{text}</h2>', sanitize=False)
        if sub:
            paragraph(sub, 'sec-sub')


def clip_card(title: str, caption: str, src: str) -> None:
    with div('clip card tilt reveal'):
        media(src)
        with div('clip-body'):
            label(title, 'clip-title')
            label(caption, 'clip-caption')
        label('click to expand ↗', 'clip-hint')


def carousel(track_id: str, clips) -> None:
    with div('carousel'):
        with div('car-ctrl'):
            ui.html(f'<button class="car-btn" data-target="{track_id}" data-scroll="-1" aria-label="Previous">←</button>'
                    f'<button class="car-btn" data-target="{track_id}" data-scroll="1" aria-label="Next">→</button>',
                    sanitize=False).classes('car-btns')
        with div('track').props(f'id={track_id}'):
            for t, c, s in clips:
                clip_card(t, c, s)


def rail(items: list[tuple[str, str]]) -> None:
    """Fixed dot-rail on the right; highlights the section in view."""
    with div('rail'):
        for sid, text in items:
            ui.html(f'<a href="#{sid}" aria-label="{text}"><span>{text}</span><i></i></a>', sanitize=False)


# ───────────────────────── HOME ─────────────────────────
@ui.page('/')
def home() -> None:
    with page_frame('Home'):
        rail([('top', 'Intro'), ('featured', 'Featured'), ('numbers', 'Snapshot')])

        with ui.element('section').props('id=top').classes('snap-sec hero-sec'):
            with div('wrap hero'):
                label('<span class="dot"></span> Open to Internships', 'status reveal')
                with div('prompt reveal'):
                    div('chev')
                    label(PROFILE['name'], 'hero-name')
                    div('cursor')
                with div('typed-line reveal'):
                    ui.html('<span class="muted">~/jason $</span> <span class="typed" data-words=\''
                            + str(ROLES).replace("'", '"') + '\'></span><span class="caret"></span>',
                            sanitize=False)
                paragraph(PROFILE['tagline'], 'tagline reveal')
                with div('actions reveal'):
                    link('See my work', '/projects', 'btn primary')
                    link('About me', '/about', 'btn')
                    link('GitHub', PROFILE['github'], 'btn ghost', new_tab=True)
                label('scroll ↓', 'scroll-hint')

        with ui.element('section').props('id=featured').classes('snap-sec'):
            with div('wrap'):
                eyebrow('featured project')
                with ui.link(target='/projects').classes('feature card tilt reveal'):
                    with div('feature-text'):
                        label(PROJECT.name, 'proj-name')
                        label(PROJECT.summary, 'proj-sum')
                        paragraph(PROJECT.description, 'desc')
                        with div('chips'):
                            for tech in PROJECT.stack:
                                label(tech, 'chip')
                        label('Explore every feature →', 'more-link')
                    media(PROJECT.overview)

        with ui.element('section').props('id=numbers').classes('snap-sec'):
            with div('wrap'):
                eyebrow('snapshot')
                with div('stats'):
                    for num, suffix, text in FACTS:
                        with div('stat card reveal'):
                            ui.html(f'<span class="num" data-count="{num}" data-suffix="{suffix}">0</span>',
                                    sanitize=False)
                            label(text, 'stat-label')


# ───────────────────────── PROJECTS ─────────────────────────
@ui.page('/projects')
def projects() -> None:
    pr = PROJECT
    groups = [('Essentials', pr.clips), ('Power features', pr.more_clips)]
    flat = [c for _, g in groups for c in g]

    with page_frame('Projects', 'Projects'):
        with div('wrap page-head'):
            eyebrow('projects')
            with div('reveal'):
                ui.html(f'<h1>{pr.name}</h1>', sanitize=False)
            paragraph(pr.summary, 'lead reveal')
            paragraph(pr.description, 'desc reveal')
            with div('chips reveal'):
                for tech in pr.stack:
                    label(tech, 'chip')
            with div('proj-links reveal'):
                label('Download', 'muted dl-label')
                for text, href in betteride_links():  # re-resolved per page load (cached 10 min)
                    link(text, href, 'btn dl', download=True)

        with div('wrap'):
            with div('overview reveal'):
                media(pr.overview)

        with div('wrap explorer-wrap'):
            section_title('Features', 'Did I mention these were built from ==***SCRATCH***==')
            with div('explorer'):
                # list
                with div('ex-list'):
                    idx = 0
                    for gname, clips in groups:
                        label(gname, 'ex-group')
                        for t, c, s in clips:
                            btn = div('ex-item').props(f'data-i={idx}')
                            with btn:
                                label(f'{idx + 1:02d}', 'ex-num')
                                label(t, 'ex-name')
                            btn.on('click', lambda _, i=idx: select(i))
                            idx += 1
                # stage
                with div('ex-stage card'):
                    player = ui.video(flat[0][2], controls=False, muted=True, loop=True, autoplay=True) \
                        .classes('ex-video').props('playsinline')
                    with div('ex-caption'):
                        title_l = label(flat[0][0], 'clip-title')
                        cap_l = label(flat[0][1], 'clip-caption')
                    with div('ex-nav'):
                        ui.button('← Prev', on_click=lambda: select((state['i'] - 1) % len(flat))).props('flat no-caps')
                        counter = ui.label(f'1 / {len(flat)}').classes('muted')
                        ui.button('Next →', on_click=lambda: select((state['i'] + 1) % len(flat))).props('flat no-caps')

            state = {'i': 0}

            def select(i: int) -> None:
                state['i'] = i
                t, c, s = flat[i]
                player.set_source(s)
                title_l.content = rich(t)
                cap_l.content = rich(c)
                counter.text = f'{i + 1} / {len(flat)}'
                ui.run_javascript(
                    f"document.querySelectorAll('.ex-item').forEach((e,k)=>e.classList.toggle('on',k=={i}));"
                    "setTimeout(()=>{const v=document.querySelector('.ex-video'); if(v){v.muted=true; v.load(); v.play().catch(()=>{});}},120);")

            ui.timer(0.2, lambda: select(0), once=True)


# ───────────────────────── ABOUT ─────────────────────────
@ui.page('/about')
def about() -> None:
    with page_frame('About', 'About'):
        rail([('who', 'Who I am'), ('life', 'Off the clock'), ('reviews', 'Reviews')])

        with ui.element('section').props('id=who').classes('snap-sec'):
            with div('wrap page-head'):
                eyebrow('about me')
                with div('reveal'):
                    ui.html('<h1>More than a programmer.</h1>', sanitize=False)
                with div('about-grid'):
                    with div():
                        for para in ABOUT:
                            paragraph(para, 'about-text reveal')
                    with div('card interests reveal'):
                        label('Currently', 'muted')
                        with div('chips'):
                            for i in INTERESTS:
                                label(i, 'chip')

        with ui.element('section').props('id=life').classes('snap-sec'):
            with div('wrap'):
                section_title('Off the clock', 'Swipe or use the arrows. Tap a clip to expand it.')
                carousel('life-track', ABOUT_CLIPS)

        with ui.element('section').props('id=reviews').classes('snap-sec'):
            with div('wrap'):
                section_title('What customers say')
                with div('reviews-embed reveal'):
                    if FEATURABLE_WIDGET_ID:
                        ui.element('div').props(f'id="featurable-{FEATURABLE_WIDGET_ID}" data-featurable-async')
                        add_featurable()
                    else:
                        label('Add your Featurable widget ID in content.py', 'placeholder')


# ───────────────────────── CONTACT ─────────────────────────
@ui.page('/contact')
def contact() -> None:
    def copy_email() -> None:
        ui.run_javascript(f"navigator.clipboard.writeText('{PROFILE['email']}')")
        ui.notify('Email copied to clipboard', type='positive', position='bottom')

    with page_frame('Contact', 'Contact'):
        with div('wrap page-head'):
            eyebrow('contact')
            with div('reveal'):
                ui.html("<h1>Let's talk.</h1>", sanitize=False)
            paragraph(PROFILE['tagline'], 'lead reveal')

            with div('contact-grid'):
                with ui.element('button').classes('card tilt big-mail reveal').on('click', copy_email):
                    label('Email', 'muted')
                    label(PROFILE['email'], 'mail-addr')
                    label('click to copy', 'clip-hint')
                for name, href, desc in [
                    ('LinkedIn', PROFILE['linkedin'], 'Connect with me'),
                    ('GitHub', PROFILE['github'], 'Browse the code'),
                    ('Resume', PROFILE['resume'], 'PDF, one page'),
                ]:
                    with ui.link(target=href, new_tab=True).classes('card tilt social reveal'):
                        label(name, 'social-name')
                        label(desc, 'muted')
                        label('↗', 'arrow')

            eyebrow('references')
            with div('refs'):
                for name, job, phone in REFERENCES:
                    with ui.link(target='tel:' + ''.join(ch for ch in phone if ch.isdigit() or ch == '+')) \
                            .classes('ref card tilt reveal'):
                        label(name, 'ref-name')
                        label(job, 'ref-job')
                        label(phone, 'ref-phone')
