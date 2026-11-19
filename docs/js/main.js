(() => {
  'use strict';

  const fine = matchMedia('(pointer:fine)').matches;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ───── scroll progress + cursor glow ───── */
  const onScroll = () => {
    const bar = document.querySelector('.progress');
    if (!bar) return;
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? h.scrollTop / max : 0) + ')';
  };
  addEventListener('scroll', onScroll, { passive: true });
  if (fine && !reduce) {
    addEventListener('pointermove', e => {
      const g = document.querySelector('.glow');
      if (g) g.style.transform = 'translate(' + (e.clientX - 300) + 'px,' + (e.clientY - 300) + 'px)';
    }, { passive: true });
  }

  /* ───── reveal on scroll ───── */
  const rev = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); rev.unobserve(e.target); }
  }), { threshold: .12 });

  /* ───── scroll-spy for the side rail ───── */
  const spy = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = e.target.id;
    document.querySelectorAll('.rail a').forEach(a =>
      a.classList.toggle('on', a.getAttribute('href') === '#' + id));
  }), { rootMargin: '-45% 0px -50% 0px' });

  /* ───── typed text ───── */
  const type = el => {
    const words = JSON.parse(el.dataset.words);
    let w = 0, i = 0, del = false;
    const tick = () => {
      const word = words[w];
      i += del ? -1 : 1;
      el.textContent = word.slice(0, i);
      let t = del ? 35 : 75;
      if (!del && i === word.length) { del = true; t = 1500; }
      else if (del && i === 0) { del = false; w = (w + 1) % words.length; t = 350; }
      setTimeout(tick, t);
    };
    reduce ? (el.textContent = words[0]) : tick();
  };

  /* ───── 3D tilt on cards ───── */
  const tilt = el => {
    if (!fine || reduce) return;
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.setProperty('--rx', (-y * 6).toFixed(2) + 'deg');
      el.style.setProperty('--ry', (x * 8).toFixed(2) + 'deg');
      el.style.setProperty('--mx', ((x + .5) * 100) + '%');
      el.style.setProperty('--my', ((y + .5) * 100) + '%');
    });
    el.addEventListener('pointerleave', () => {
      el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg');
    });
  };

  /* ───── count-up numbers ───── */
  const count = el => {
    const to = +el.dataset.count; let n = 0;
    const step = () => {
      n += Math.max(1, to / 30);
      el.textContent = Math.min(to, Math.round(n)) + (el.dataset.suffix || '');
      if (n < to) requestAnimationFrame(step);
    };
    step();
  };
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { count(e.target); cio.unobserve(e.target); }
  }));

  /* ───── carousel buttons ───── */
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-scroll]');
    if (!b) return;
    const track = document.getElementById(b.dataset.target);
    if (track) track.scrollBy({ left: +b.dataset.scroll * (track.clientWidth * .8), behavior: 'smooth' });
  });

  /* ───── scan DOM for interaction hooks ───── */
  const scan = () => {
    document.querySelectorAll('.reveal:not(.in):not([data-r])').forEach(el => { el.dataset.r = 1; rev.observe(el); });
    document.querySelectorAll('.snap-sec:not([data-s])').forEach(el => { el.dataset.s = 1; spy.observe(el); });
    document.querySelectorAll('[data-words]:not([data-t])').forEach(el => { el.dataset.t = 1; type(el); });
    document.querySelectorAll('.tilt:not([data-tl])').forEach(el => { el.dataset.tl = 1; tilt(el); });
    document.querySelectorAll('[data-count]:not([data-c])').forEach(el => { el.dataset.c = 1; cio.observe(el); });
    onScroll();
  };
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
  scan();

  /* ───── VIDEO_PAUSE: play only when visible ───── */
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

  /* ───── FEATURABLE lazy loader ───── */
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

  /* ───── CLIP LIGHTBOX ───── */
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

  /* ───── BetterIDE download links: pull newest releases from GitHub ───── */
  (() => {
    const nums = t => (String(t).match(/\d+/g) || []).map(Number);
    const newer = (a, b) => {
      for (let i = 0; i < Math.max(a.length, b.length); i++) {
        if ((a[i] || 0) !== (b[i] || 0)) return (a[i] || 0) > (b[i] || 0);
      }
      return false;
    };
    const targets = { 'dl-mac': /arm64.*\.dmg$/i, 'dl-win': /\.zip$/i };
    (async () => {
      try {
        const key = 'betteride_releases';
        let releases = null;
        try { releases = JSON.parse(sessionStorage.getItem(key) || 'null'); } catch (e) {}
        if (!releases) {
          const res = await fetch('https://api.github.com/repos/JasonOluikpe/Portfolio/releases?per_page=30');
          if (!res.ok) return;
          releases = await res.json();
          try { sessionStorage.setItem(key, JSON.stringify(releases)); } catch (e) {}
        }
        for (const [id, pattern] of Object.entries(targets)) {
          let best = null;
          for (const rel of releases) {
            if (rel.draft || rel.prerelease) continue;
            const asset = (rel.assets || []).find(a => pattern.test(a.name));
            if (asset && (!best || newer(nums(rel.tag_name), best.version))) {
              best = { version: nums(rel.tag_name), url: asset.browser_download_url };
            }
          }
          const link = document.getElementById(id);
          if (best && link) link.href = best.url;
        }
      } catch (e) { /* keep the fallback hrefs */ }
    })();
  })();

  /* ───── copy email button ───── */
  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-copy-email]');
    if (!btn) return;
    const email = btn.getAttribute('data-copy-email');
    navigator.clipboard.writeText(email).catch(() => {});
    const note = document.createElement('div');
    note.textContent = 'Email copied to clipboard';
    note.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);' +
      'background:#00ff3c;color:#0b0b0b;font-weight:600;padding:10px 18px;border-radius:10px;' +
      'z-index:99999;box-shadow:0 8px 24px rgba(0,255,60,.3);';
    document.body.appendChild(note);
    setTimeout(() => note.remove(), 2000);
  });
})();
