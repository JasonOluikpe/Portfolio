import os

from nicegui import ui

from src.content import PROFILE
from src.setup import configure_app
import src.pages


configure_app()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title=f"{PROFILE['name']} | {PROFILE['role']}",
        dark=True,
        reload=False,
        show=False,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 3000)),
    )