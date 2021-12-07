from pydantic import BaseModel
from invmonApi.database import Base
from invmonInfra.domain.sqlTableInterface import SqlTableInterface
from sqlalchemy import Column, String
from uuid import uuid4


class ActiveAlertSqlModel(Base):
    __tablename__ = "activealerts"
    id = Column(String, primary_key=True)
    smtpContactId: str = Column(String)
    inventoryId: str = Column(String)
    
    
class ActiveAlertApiModel(BaseModel):
    id: str
    smtpContactId: str
    inventoryId: str


class ActiveAlertModel(SqlTableInterface):
    id: str
    smtpContactId: str
    inventoryId: str

    def __init__(self, smtpContactId: str, inventoryId: str, id: str = '') -> None:
        self.id: str = id
        if self.id == '':
            self.id = str(uuid4())
            
        self.smtpContactId = smtpContactId
        self.inventoryId = inventoryId
        self.__validateInit__()
        pass

    def __validateInit__(self) -> None:
        pass

    def getApiModel(self) -> ActiveAlertApiModel:
        r = ActiveAlertApiModel()
        r.id = self.id
        r.smtpContactId = self.smtpContactId
        r.inventoryId = self.inventoryId
        return r

    def getSqlModel(self) -> ActiveAlertSqlModel:
        r = ActiveAlertSqlModel()
        r.id = self.id
        r.smtpContactId = self.smtpContactId
        r.inventoryId = self.inventoryId
        return r
