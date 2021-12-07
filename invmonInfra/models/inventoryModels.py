from logging import lastResort
from pydantic import BaseModel
from invmonApi.database import Base
from invmonInfra.enum import InventoryLastStatusEnum
from sqlalchemy import Column, String, Boolean
from uuid import uuid4


class InventorySqlModel(Base):
    __tablename__ = "inventory"
    id = Column(String, primary_key=True)
    enabled: bool = Column(Boolean)
    itemName: str = Column(String)
    lastStatus: str = Column(String)
    url: str = Column(String)    
    

class InventoryApiModel(BaseModel):
    id: str
    enabled: bool
    itemName: str
    lastStatus: str
    url: str


class InventoryModel():
    id: str
    enabled: bool
    itemName: str
    lastStatus: str
    url: str

    def __init__(self, enabled: str, itemName: str, url: str, lastStatus: InventoryLastStatusEnum, id: str = '') -> None:
        self.id: str = id
        if self.id == '':
            self.id = str(uuid4())
            
        self.enabled = enabled
        self.itemName = itemName
        self.lastStatus = lastStatus.value
        self.url = url
        pass

    def getApiModel(self) -> InventoryApiModel:
        r = InventoryApiModel()
        r.id = self.id
        r.enabled = self.enabled
        r.itemName = self.itemName
        r.lastStatus = self.lastStatus
        r.url = self.url
        return r

    def getSqlModel(self) -> InventorySqlModel:
        r = InventorySqlModel()
        r.id = self.id
        r.enabled = self.enabled
        r.itemName = self.itemName
        r.lastStatus = self.lastStatus
        r.url = self.url
        return r

