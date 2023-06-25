from abc import ABC, abstractclassmethod


class AbstractPresenter(ABC):

    @abstractclassmethod
    def payload(self):
        pass

    @abstractclassmethod
    def send(self, agrs):
        pass