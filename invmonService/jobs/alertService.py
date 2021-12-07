from logging import log
from invmonInfra.domain import JobsInterface, LoggerInterface
from invmonInfra.models import ActiveAlertModel, SmtpContactsSqlModel, InventorySqlModel
from invmonInfra.models.activeAlertModels import ActiveAlertSqlModel
from invmonService.email import EmailService
from fastapi_sqlalchemy import db
from typing import List
from time import sleep


class JobAlertService(JobsInterface):
    """When this service runs, it checks the DB to see if any alerts need to be sent out, and will handle that processing."""

    _logger: LoggerInterface

    def __init__(self, logger: LoggerInterface) -> None:
        self._logger = logger
        pass

    def runJob(self) -> None:
        # Check the table to see what records we find.
        alerts = self.collectAlerts()
        if len(alerts) == 0: return None

        for alert in alerts:
            # Find the SmtpContact we will send an alert to.
            smtpContact = self.collectSmtpContact(alert.smtpContactId)
            item = self.collectInventory(alert.inventoryId)
            
            email = EmailService()
            email.setTo(smtpContact.address)
            email.setSubject(f"ALERT - '{item.itemName}' was in stock!")
            email.setBody(f"Click here to view the current stock. {item.url}")
            email.send()
            self._logger.debug(f"Sent message to {email.__to__}")

            self.removeAlert(alert.id)

            sleep(3)


    def collectAlerts(self) -> List[ActiveAlertSqlModel]:
        with db():
            res = db.session.query(ActiveAlertSqlModel).all()
            db.session.close()
        return res

    def collectSmtpContact(self, findId: str) -> SmtpContactsSqlModel:
        with db():
            res = db.session.query(SmtpContactsSqlModel).filter(SmtpContactsSqlModel.id == findId).first()
            db.session.close()
        
        if res.id == '':
            raise Exception(f"Failed to find the requested SmtpContactId of '{findId}'.")
        return res
            
    def collectInventory(self, findId: str) -> InventorySqlModel:
        with db():
            res = db.session.query(InventorySqlModel).filter(InventorySqlModel.id == findId).first()
            db.session.close()

        if res.id == '':
            raise Exception(f"Failed to find the requested InventoryId of '{findId}'.")
        return res

    def removeAlert(self, alertId: str) -> None:
        with db():
            res = db.session.query(ActiveAlertSqlModel).filter(ActiveAlertSqlModel.id == alertId).first()
            db.session.delete(res)
            db.session.commit()
            db.session.close()

