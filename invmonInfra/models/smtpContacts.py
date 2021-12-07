from pydantic import BaseModel
from invmonApi.database import Base
from sqlalchemy import Column, String
from uuid import uuid4


class SmtpContactsSqlModel(Base):
    __tablename__ = "smtpContacts"
    id = Column(String, primary_key=True)
    address: str = Column(String)
    

class SmtpContactsApiModel(BaseModel):
    id: str
    address: str


class SmtpContactsModel():
    def __init__(self, address:str, id: str = '') -> None:
        self.id: str = id
        if self.id == '':
            self.id = str(uuid4())
            
        self.address: str = address
        pass

    def getApiModel(self) -> SmtpContactsApiModel:
        r = SmtpContactsApiModel(id=self.id, address=self.address)
        return r

    def getSqlModel(self) -> SmtpContactsSqlModel:
        r = SmtpContactsSqlModel()
        r.id = self.id
        r.address = self.address
        return r

