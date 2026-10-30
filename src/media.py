import mimetypes

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse
from nicegui import app
from starlette.background import BackgroundTask

from .config import MEDIA_ORIGIN

ALLOWED = ('.mp4', '.png')
FORWARD = ('content-length', 'content-range')
client = httpx.AsyncClient(follow_redirects=True, timeout=30)


def media_url(src: str) -> str:
    return f'/media/{src.rsplit("/", 1)[-1]}'


@app.api_route('/media/{name}', methods=['GET', 'HEAD'])
async def serve_media(name: str, request: Request):
    if not name.endswith(ALLOWED):
        raise HTTPException(404)
    headers = {'Range': request.headers['range']} if 'range' in request.headers else {}
    upstream = await client.send(
        client.build_request('GET', f'{MEDIA_ORIGIN}/{name}', headers=headers), stream=True
    )
    if upstream.status_code >= 400:
        await upstream.aclose()
        raise HTTPException(upstream.status_code)
    out = {k: upstream.headers[k] for k in FORWARD if k in upstream.headers}
    out['Accept-Ranges'] = 'bytes'
    out['Cache-Control'] = 'public, max-age=86400'
    return StreamingResponse(
        upstream.aiter_raw(),
        status_code=upstream.status_code,
        media_type=mimetypes.guess_type(name)[0],
        headers=out,
        background=BackgroundTask(upstream.aclose),
    )
