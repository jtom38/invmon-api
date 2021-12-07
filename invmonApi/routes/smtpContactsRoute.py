from fastapi import APIRouter
from fastapi_sqlalchemy import db
from typing import List
from invmonInfra.models import SmtpContactsModel, SmtpContactsApiModel, SmtpContactsSqlModel


SmtpContactsRouter = APIRouter(prefix='/smtpcontacts', tags=['SmtpContacts'])
SmtpContactsTags = { 
    "name": "SmtpContacts"
    ,"description": "This contains objects that define who to send alerts to."
}

@SmtpContactsRouter.get('/get/all')
def testEmail() -> List[SmtpContactsSqlModel]:
    r = db.session.query(SmtpContactsSqlModel).all()
    return r
    

@SmtpContactsRouter.post('/new')
def newSmtpContact(email: str) -> None:
    exists = db.session.query(SmtpContactsSqlModel).filter(SmtpContactsSqlModel.address == email).first()
    if exists != None:
        db.session.close()
        raise Exception("Requested email address already exists.")
    
    r = SmtpContactsModel(address=email)
    db.session.add(r.getSqlModel())
    db.session.commit()
    db.session.close()


@SmtpContactsRouter.delete('/delete')
def deleteSemptContact(email: str) -> None:
    res = db.session.query(SmtpContactsSqlModel).filter(SmtpContactsSqlModel.address == email).first()
    db.session.delete(res)
    db.session.commit()
    db.session.close()

