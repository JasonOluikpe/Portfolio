import os

from nicegui import app, ui
from fastapi.responses import RedirectResponse

from src.content import PROFILE
from src.setup import configure_app
import src.pages



configure_app()

LOGO_URL = PROFILE['logo']

@app.get('/apple-touch-icon.png')
@app.get('/apple-touch-icon-precomposed.png')
@app.get('/media/logo.png')
async def logo_redirect():
    return RedirectResponse(LOGO_URL, status_code=301)

@app.get('/health')
async def health():
    return {'status': 'ok'}


if __name__ in {'__main__', '__mp_main__'}:
    try:
        ui.run(
            title=f"{PROFILE['name']} | {PROFILE['role']}",
            dark=True,
            reload=False,
            show=False,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 3000)),
        )
    except PermissionError:
        pass
