from abc import ABC, abstractclassmethod


class EmailInterface(ABC):
    @abstractclassmethod
    def setTo(self, to: str) -> None:
        pass

    @abstractclassmethod
    def setCc(self, cc: str) -> None:
        pass

    @abstractclassmethod
    def setBcc(self, bcc: str) -> None:
        pass

    @abstractclassmethod
    def setSubject(self, subject: str) -> None:
        pass

    @abstractclassmethod
    def setBody(self, body: str) -> None:
        pass

    @abstractclassmethod
    def send(self) -> None:
        pass