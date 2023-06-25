from abc import ABC, abstractmethod

from src.presenter.AbstractPresenter import AbstractPresenter
from ..error.AppError import AppError
from flask import request, jsonify

class AbstractController(ABC):
    __presenter: AbstractPresenter

    def __init__(self, presenter: AbstractPresenter) -> None:
        self.__presenter = presenter

    def execController(self, **args) -> any:
        data = {
            **args,
            **request.args,
            **self.__presenter.payload()
        }
        try:
            return self.__presenter.send(self.handle(data))
        except AppError as err:
            return  self.__presenter.send(err.message)
        except Exception as err:
            return jsonify(err), 500
        

    @abstractmethod
    def handle(self, controllerInput: dict) -> any:
        pass