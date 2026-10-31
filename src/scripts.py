VIDEO_PAUSE = '''
<script>
(() => {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.play().catch(() => {});
      else e.target.pause();
    });
  }, { rootMargin: '200px' });

  const watch = () => {
    document.querySelectorAll('video').forEach(v => { v.defaultMuted = true; v.muted = true; });
    document.querySelectorAll('video.watch-video:not([data-watched])')
      .forEach(v => { v.dataset.watched = '1'; io.observe(v); });
  };

  new MutationObserver(watch).observe(document.body, { childList: true, subtree: true });
  watch();
})();
</script>
'''

FEATURABLE = '''
<script>
(() => {
  const inject = () => {
    if (document.querySelector('script[data-featurable]')) return;
    const s = document.createElement('script');
    s.src = 'https://cdn.featurable.com/widget/v2/embed.js';
    s.charset = 'UTF-8';
    s.defer = true;
    s.dataset.featurable = '1';
    document.body.appendChild(s);
  };

  const watch = () => {
    const el = document.querySelector('[data-featurable-async]');
    if (!el) return false;
    new IntersectionObserver((entries, io) => {
      if (entries.some(e => e.isIntersecting)) { io.disconnect(); inject(); }
    }, { rootMargin: '400px' }).observe(el);
    return true;
  };

  if (!watch()) {
    const mo = new MutationObserver(() => { if (watch()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
'''

CLIP_LIGHTBOX = '''
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
      '<video class="lb-video" playsinline loop disablepictureinpicture disableremoteplayback></video>' +
      '<div class="lb-title"></div><div class="lb-caption"></div></div>';
    document.body.appendChild(box);
    vid = box.querySelector('.lb-video');
    titleEl = box.querySelector('.lb-title');
    capEl = box.querySelector('.lb-caption');
    vid.addEventListener('pause', () => {
      if (box.classList.contains('open')) vid.play().catch(() => {});
    });
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