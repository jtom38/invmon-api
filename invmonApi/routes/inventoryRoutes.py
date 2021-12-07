from fastapi import APIRouter
from fastapi_sqlalchemy import db
from typing import List

from sqlalchemy.sql.expression import exists
from invmonInfra.enum import InventoryLastStatusEnum
from invmonInfra.models import InventoryApiModel, InventorySqlModel, InventoryModel


InventoryRouter = APIRouter(prefix='/inventory', tags=['Inventory'])
InventoryTag = {
    "name": "Inventory",
    "description": "This defines all the enabled items that will be watched by the API."
}


@InventoryRouter.get('/get/all')
def getAllInventory() -> List[InventorySqlModel]:
    r = db.session.query(InventorySqlModel).all()
    return r
    

@InventoryRouter.post('/new')
def newInventoryItem(enabled: bool, itemName: str, url: str) -> None:
    exists = db.session.query(InventorySqlModel).filter(InventorySqlModel.url == url).first()
    if exists != None:
        db.session.close()
        raise Exception("Requested item is already being monitored.")
        
    e = InventoryLastStatusEnum.OUTOFSTOCK
    r = InventoryModel(enabled=enabled, itemName=itemName, lastStatus=e, url=url)
    db.session.add(r.getSqlModel())
    db.session.commit()
    db.session.close()


@InventoryRouter.delete('/delete')
def deleteInventoryItem(url: str) -> None:
    res = db.session.query(InventorySqlModel).filter(InventorySqlModel.url == url).first()
    db.session.delete(res)
    db.session.commit()
    db.session.close()

