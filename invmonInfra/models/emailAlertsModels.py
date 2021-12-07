from pydantic import BaseModel
from invmonApi.database import Base
from sqlalchemy import Column, String
from uuid import uuid4


class EmailAlertsSqlModel(Base):
    __tablename__ = "emailalerts"
    id = Column(String, primary_key=True)
    smtpContactsId: str = Column(String)
    inventoryId: str = Column(String)
    

class EmailAlertsApiModel(BaseModel):
    id: str
    smtpContactsId: str
    inventoryId: str


class EmailAlertsModel():
    id: str
    smtpContactsId: str
    inventoryId: str

    def __init__(self, smtpContactsId: str, inventoryId: str, id: str = '') -> None:
        self.id: str = id
        if self.id == '':
            self.id = str(uuid4())
            
        self.smtpContactsId = smtpContactsId
        self.inventoryId = inventoryId
        pass

    def getApiModel(self) -> EmailAlertsApiModel:
        r = EmailAlertsApiModel()
        r.id = self.id
        r.smtpContactsId = self.smtpContactsId
        r.inventoryId = self.inventoryId
        return r

    def getSqlModel(self) -> EmailAlertsSqlModel:
        r = EmailAlertsSqlModel()
        r.id = self.id
        r.smtpContactsId = self.smtpContactsId
        r.inventoryId = self.inventoryId
        return r

