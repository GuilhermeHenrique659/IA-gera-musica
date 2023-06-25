from flask import Flask
from .router import Router
from typing import List
from flask_cors import CORS


class Application:
    __app: Flask
    __routers: List[Router] = []

    def __init__(self) -> None:
        self.__app = Flask(__name__,  template_folder='../../templates', static_folder='../../static')
        CORS(self.__app)

    def get_app(self) -> Flask:
        return self.__app

    def add_router(self, router: Router) -> None:
        router.set_app(self.__app)
        self.__routers.append(router)

    def __setup_routers(self) -> None:
        for router in self.__routers:
            router.setup_routers()

    def run(self, host:str, port:int) -> None:
        self.__setup_routers()
        self.__app.run(host = host, port = port, debug = True)
