from flask import Flask
from ..controller.abstractController import AbstractController
from typing import List


class Router:
    __routers_config: list
    __prefix_name: str
    __app: Flask

    def __init__(self, prefixName: str, routersConfig) -> None:
        self.__routers_config = routersConfig
        self.__prefix_name = prefixName

    def set_app(self, app: Flask):
        self.__app = app

    def setup_routers(self) -> None:
        print(' * SetUp routers: {}'.format(self.__prefix_name))
        for router in self.__routers_config:
            print('     * SetUp router: {}'.format(self.__prefix_name + router['url']))
            self.__app.add_url_rule('/' + self.__prefix_name + router['url'],
                                                    endpoint=router['endpoint'],
                                                    view_func=router['controller'].execController,
                                                    methods = router['methods']
                                                   )
