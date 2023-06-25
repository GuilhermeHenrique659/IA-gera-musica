from src.music.router.MusicRouter import music_router
from src.server.application import Application


application = Application()
application.add_router(music_router)

application.run('0.0.0.0', 3000)