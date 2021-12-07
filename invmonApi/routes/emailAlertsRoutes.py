from fastapi import APIRouter
from fastapi_sqlalchemy import db
from invmonInfra.models import EmailAlertsSqlModel, EmailAlertsModel
from typing import List


EmailAlertsRouter = APIRouter(prefix='/emailalerts' ,tags=['Email Alerts'])
EmailAlertTags = {
    "name": "Email Alerts", 
    "description": "This contains the relationship between SmtpContacts and Inventory.  When an inventory item become available, these objects are reviewed to see who wants to be alerted."
}

@EmailAlertsRouter.get('/get/all')
def getAllEmailAlerts() -> List[EmailAlertsSqlModel]:
    r = db.session.query(EmailAlertsSqlModel).all()
    return r
    

@EmailAlertsRouter.post('/new')
def newEmailAlert(smtpContactId: str, inventoryId: str) -> None:
    e = EmailAlertsModel(smtpContactId, inventoryId)    
    db.session.add(e.getSqlModel())
    db.session.commit()
    db.session.close()


@EmailAlertsRouter.delete('/delete')
def deleteEmailAlert(id: str) -> None:
    res = db.session.query(EmailAlertsSqlModel).filter(EmailAlertsSqlModel.id == id).first()
    db.session.delete(res)
    db.session.commit()
    db.session.close()