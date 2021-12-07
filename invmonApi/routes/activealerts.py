from fastapi import APIRouter
from fastapi_sqlalchemy import db
from typing import List
from invmonInfra.models import ActiveAlertSqlModel


ActiveAlertsRouter = APIRouter(prefix='/activealerts' ,tags=['Active Alerts'])
ActiveAlertsTags = {
    "name": "Active Alerts",
    "description": "This is the queue of active alerts to be sent out"
}


@ActiveAlertsRouter.get('/get/all')
def getAllActiveAlerts() -> List[ActiveAlertSqlModel]:
    r = db.session.query(ActiveAlertSqlModel).all()
    return r

