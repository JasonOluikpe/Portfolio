"""Finds the newest BetterIDE download for each platform from GitHub Releases.

Uses only the standard library. Results are cached so the site stays well under
GitHub's unauthenticated API limit (60 requests/hour), and if GitHub can't be
reached the last good result (or the hardcoded fallback) is used instead.
"""

import json
import re
import threading
import time
import urllib.request

REPO = 'JasonOluikpe/Portfolio'
API_URL = f'https://api.github.com/repos/{REPO}/releases?per_page=30'

# Which release file belongs to which platform (see BetterIDE's build.py).
PATTERNS = {
    'mac': re.compile(r'arm64.*\.dmg$', re.IGNORECASE),
    'windows': re.compile(r'\.zip$', re.IGNORECASE),
}

# Used only if GitHub can't be reached and nothing has been cached yet.
FALLBACK = {
    'mac': f'https://github.com/{REPO}/releases/download/v1.4.4/BetterIDE-arm64-v1.4.4.dmg',
    'windows': f'https://github.com/{REPO}/releases/download/v1.4.2/BetterIDE-1.4.2.zip',
}

CACHE_SECONDS = 600
RETRY_SECONDS = 60
TIMEOUT = 3

_lock = threading.Lock()
_cache: dict[str, str] = {}
_next_refresh = 0.0


def _version(tag: str) -> tuple:
    return tuple(int(part) for part in re.findall(r'\d+', tag))


def fetch_latest() -> dict[str, str]:
    """{'mac': url, 'windows': url} using the newest release that has each file."""
    request = urllib.request.Request(
        API_URL, headers={'User-Agent': 'portfolio-site', 'Accept': 'application/vnd.github+json'},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        releases = json.load(response)

    best: dict[str, tuple[tuple, str]] = {}
    for release in releases:
        if release.get('draft') or release.get('prerelease'):
            continue
        version = _version(release.get('tag_name', ''))
        for asset in release.get('assets', []):
            for platform, pattern in PATTERNS.items():
                if pattern.search(asset['name']) and (platform not in best or version > best[platform][0]):
                    best[platform] = (version, asset['browser_download_url'])
    return {platform: url for platform, (_, url) in best.items()}


def latest_urls() -> dict[str, str]:
    global _cache, _next_refresh
    with _lock:
        if time.monotonic() >= _next_refresh:
            try:
                _cache = {**_cache, **fetch_latest()}
                _next_refresh = time.monotonic() + CACHE_SECONDS
            except Exception:
                _next_refresh = time.monotonic() + RETRY_SECONDS  # keep last good data
        return {**FALLBACK, **_cache}
