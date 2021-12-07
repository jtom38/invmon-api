import smtplib
from email.message import EmailMessage
from typing import List
from invmonInfra.domain import EmailInterface
from invmonInfra.enum.envReaderEnum import EnvReaderEnum
from invmonService import EnvReaderService


class EmailService(EmailInterface):
    _env: EnvReaderService
    __to__: List[str]
    __cc__: List[str]
    __bcc__: List[str]

    def __init__(self) -> None:
        self.__to__ = list()
        self.__cc__ = list()
        self.__bcc__ = list()
        self.__subject__ = ''
        self.__body__ = ''
        self._env = EnvReaderService()
        self.msg = EmailMessage()
        
        self.client = smtplib.SMTP(
            host=self._env.getValue(EnvReaderEnum.SMTPHOST)
            ,port=self._env.getValue(EnvReaderEnum.SMTPPORT)
        )
        self.client.starttls()
        self.client.ehlo()
        self.__login__()
        pass

    def __login__(self) -> None:
        self.client.login(
            user=self._env.getValue(EnvReaderEnum.SMTPUSERNAME)
            ,password=self._env.getValue(EnvReaderEnum.SMTPPASSWORD)
        )

    def __generateMsg__(self) -> EmailMessage:
        msg = EmailMessage()
        if self.__body__ == '':
            raise Exception("Body is missing from email.")
        msg.set_content(self.__body__)

        if self._env.getValue(EnvReaderEnum.SMTPUSERNAME) == '':
            raise Exception("From is missing from the email.")
        msg['From'] = self._env.getValue(EnvReaderEnum.SMTPUSERNAME)

        if self.__to__ == '':
            raise Exception("To is missing from the email.")
        msg['To'] = self.__to__

        if self.__subject__ == '':
            raise Exception("Subject is missing from the email.")
        msg['Subject'] = self.__subject__
        return msg

    def setTo(self, to: str) -> None:
        self.__to__.append(to)

    def setCc(self, cc: str) -> None:
        self.__cc__.append(cc)

    def setBcc(self, bcc: str) -> None:
        self.__bcc__.append(bcc)

    def setSubject(self, subject: str) -> None:
        self.__subject__ = subject

    def setBody(self, body: str) -> None:
        self.__body__ = body

    def send(self) -> None:
        try:
            msg = self.__generateMsg__()
            self.client.send_message(msg=msg)
        except Exception as e:
            print(e)