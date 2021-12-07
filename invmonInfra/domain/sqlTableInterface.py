from abc import ABC, abstractclassmethod


class SqlTableInterface(ABC):
    @abstractclassmethod
    def getApiModel(self) -> object:
        pass

    @abstractclassmethod
    def getSqlModel(self) -> object:
        pass

    @abstractclassmethod
    def __validateInit__(self) -> None:
        pass