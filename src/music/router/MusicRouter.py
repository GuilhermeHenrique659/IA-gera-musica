from src.music.controller.MusicController import MusicController
from src.music.presenter.MusicPresenter import MusicPresenter
from src.server.router import Router

music_router = Router(
    'music',
    [
        {
            'url': '/',
            'methods': ['GET'],
            'endpoint': 'music',
            'controller': MusicController(MusicPresenter())
        }
    ],
)