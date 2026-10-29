from nicegui import app, ui

from .config import ASSETS_DIR, MEDIA_DIR, STATIC_URL, STYLES_FILE


FONTS_HTML = '''
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@400;500;600&display=swap' rel='stylesheet'>
'''

# Lazy-video + pause-offscreen behaviour.
# - `.lazy-video` elements start with no src; the observer copies `data-src` -> `src`
#   once they are within ~200px of the viewport, then calls play().
# - Any `.watch-video` element is paused when it leaves that band, so only a
#   handful of videos decode at any given time.
# - A MutationObserver re-scans so late-rendered videos (e.g. after "Show more")
#   get picked up automatically.
VIDEO_LAZY_SCRIPT = '''
<script>
(() => {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      const v = e.target;
      if (e.isIntersecting) {
        if (!v.getAttribute('src') && v.dataset.src) v.src = v.dataset.src;
        v.play().catch(() => {});
      } else {
        v.pause();
      }
    });
  }, { rootMargin: '200px' });

  const watch = () => document.querySelectorAll('video.watch-video:not([data-watched])')
    .forEach(v => { v.dataset.watched = '1'; io.observe(v); });

  new MutationObserver(watch).observe(document.body, { childList: true, subtree: true });
  watch();
})();
</script>
'''

# Featurable needs its <div data-featurable-async> to exist before bundle.js runs.
# NiceGUI builds the DOM client-side, so a plain <script defer> can fire too early.
# This waits for the div, then injects the script once.
FEATURABLE_SCRIPT = '''
<script>
(() => {
  const load = () => {
    if (!document.querySelector('[data-featurable-async]')) return false;
    if (!document.querySelector('script[data-featurable]')) {
      const s = document.createElement('script');
      s.src = 'https://cdn.featurable.com/widget/v2/embed.js';
      s.charset = 'UTF-8';
      s.defer = true;
      s.dataset.featurable = '1';
      document.body.appendChild(s);
    }
    return true;
  };
  if (!load()) {
    const mo = new MutationObserver(() => { if (load()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
'''

# Clip lightbox: clicking a clip opens it centred over a dark backdrop with its title and
# caption. Closes via the X, a click outside the video/text, or the Escape key.
# Uses event delegation so clips rendered later (e.g. "Show more") work automatically.
CLIP_LIGHTBOX_SCRIPT = '''
<script>
(() => {
  let box, vid, titleEl, capEl, source;

  const build = () => {
    box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML =
      '<button class="lb-close" type="button" aria-label="Close video">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">' +
      '<path d="M5 5l14 14M19 5L5 19"/></svg></button>' +
      '<div class="lb-content">' +
      '<video class="lb-video" playsinline loop></video>' +
      '<div class="lb-title"></div><div class="lb-caption"></div></div>';
    document.body.appendChild(box);
    vid = box.querySelector('.lb-video');
    titleEl = box.querySelector('.lb-title');
    capEl = box.querySelector('.lb-caption');
    box.addEventListener('click', e => {
      if (e.target.closest('.lb-close') || !e.target.closest('.lb-content')) close();
    });
  };

  const open = (clip, v, src) => {
    if (!box) build();
    source = v;
    v.pause();
    titleEl.innerHTML = (clip.querySelector('.clip-title') || {}).innerHTML || '';
    capEl.innerHTML = (clip.querySelector('.clip-caption') || {}).innerHTML || '';
    vid.src = src;
    vid.muted = false;
    box.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    vid.play().catch(() => {});
  };

  const close = () => {
    if (!box || !box.classList.contains('open')) return;
    box.classList.remove('open');
    vid.pause();
    vid.removeAttribute('src');
    vid.load();
    document.documentElement.style.overflow = '';
    if (source) {
      const r = source.getBoundingClientRect();
      if (r.bottom > 0 && r.top < window.innerHeight) source.play().catch(() => {});
    }
  };

  document.addEventListener('click', e => {
    const clip = e.target.closest('.clip');
    if (!clip) return;
    const v = clip.querySelector('video');
    const src = v && (v.getAttribute('src') || v.dataset.src);
    if (src) open(clip, v, src);
  });

  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();
</script>
'''


def configure_app() -> None:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    app.add_static_files(STATIC_URL, str(ASSETS_DIR))
    ui.add_css(STYLES_FILE.read_text(encoding='utf-8'), shared=True)


def add_fonts() -> None:
    '''Call inside a page function.'''
    ui.add_head_html(FONTS_HTML)


def add_video_lazy() -> None:
    '''Call inside a page function. Installs the lazy-load + pause observer.'''
    ui.add_body_html(VIDEO_LAZY_SCRIPT)


def add_featurable() -> None:
    '''Call inside a page function. Loads the Featurable reviews widget script.'''
    ui.add_body_html(FEATURABLE_SCRIPT)

def add_clip_lightbox() -> None:
    '''Call inside a page function. Makes clips clickable (fullscreen viewer).'''
    ui.add_body_html(CLIP_LIGHTBOX_SCRIPT)