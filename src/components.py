import re

from nicegui import ui

from .media import media_url


def div(classes: str = ''):
    return ui.element('div').classes(classes)

ICONS = {
    'apple': '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" style=\"height:.7em;width:auto;display:block;fill:currentColor\" aria-label=\"Apple\"><path d=\"M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701\"/></svg>',
    'windows': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 951 951" style="height:.7em;width:auto;display:block;fill:currentColor" aria-label="Windows"><path d="M390 502V874L0 820V502ZM390 77V454H0V131ZM951 502V951L433 880V502ZM951 0V454H433V72Z"/></svg>',
}

def link(text: str, href: str, classes: str = '', new_tab: bool = False, download: bool = False):
    with ui.link(target=href, new_tab=new_tab).classes(classes) as el:
        if text.startswith('icon:'):
            _html(ICONS[text[5:]], 'span', 'icon-svg')
        else:
            _html(text, 'span', '')
    if download:
        el.props('download')
    return el

def heading(text: str):
    with ui.element('h2').classes('title'):
        _html(text, 'span', '')

def rich(text: str) -> str:
    out = []
    for part in re.split(r'(`[^`]+`)', text):
        if len(part) > 2 and part.startswith('`') and part.endswith('`'):
            out.append(f'<code>{part[1:-1]}</code>')
            continue
        part = re.sub(r'==(?=\S)(.+?)(?<=\S)==', r'<span class="hl">\1</span>', part)
        part = re.sub(r'\*\*\*(?=\S)(.+?)(?<=\S)\*\*\*', r'<strong><em>\1</em></strong>', part)
        part = re.sub(r'\*\*(?=\S)(.+?)(?<=\S)\*\*', r'<strong>\1</strong>', part)
        part = re.sub(r'\*(?=\S)(.+?)(?<=\S)\*', r'<em>\1</em>', part)
        out.append(part)
    return ''.join(out)


def _html(text: str, tag: str, classes: str):
    html = rich(text)
    try:
        el = ui.html(html, tag=tag, sanitize=False)
    except TypeError:
        el = ui.html(html, tag=tag)
    return el.classes(classes)


def paragraph(text: str, classes: str = ''):
    return _html(text, 'p', f"paragraph {classes}".strip())


def label(text: str, classes: str = ''):
    return _html(text, 'div', classes)


def media(src: str):
    with div('media'):
        ui.video(media_url(src), controls=False, muted=True, loop=True) \
            .classes('watch-video') \
            .props('playsinline preload=none')