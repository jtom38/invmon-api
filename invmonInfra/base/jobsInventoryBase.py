from typing import List
from invmonInfra.domain import DriverInterface
from invmonInfra.domain.loggerInterface import LoggerInterface
from invmonInfra.models import InventorySqlModel, EmailAlertsSqlModel, ActiveAlertModel
from fastapi_sqlalchemy import db


class JobsInventoryBase():
    """
    This class contains the basics required to run a Inventory
    """
    _driver: DriverInterface
    _logger: LoggerInterface

    def setUri(self, uri: str) -> None:
        self.__jobUri__: str = uri
    
    def getUri(self) -> str:
        return self.__jobUri__

    def runJob(self) -> None:
        # Query db for records
        res = self.__collectInventoryRecords__(self._urlPattern)
        self.driver = self._driver.driverStart(True)
        for item in res:
            self.__checkInventoryStatus__(item)

        self.driver.close()

    def __collectInventoryRecords__(self, likeUrl: str) -> List[InventorySqlModel]:
        res: List
        with db():
            res = db.session.query(InventorySqlModel) \
                .filter(InventorySqlModel.url.like(likeUrl)) \
                .filter(InventorySqlModel.enabled == True) \
                .all()
        if len(res) == 0:
            raise Exception("Failed to find any records.")
        return res

    def __checkIfOutOfStock__(self, tag: str, key: str, value: str) -> bool:
        #invStatus: str = self.parser.findSingle(name='div', attrKey='class', attrValue="product-oos-info-title").text
        invStatus: str = self.parser.findSingle(name=tag, attrKey=key, attrValue=value).text
        if invStatus == "Out of Stock":
            return True
        return False

    def __updateInventoryRecord__(self, activeRecord: InventorySqlModel) -> None:
        with db():
            res = db.session.query(InventorySqlModel).filter(InventorySqlModel.id == activeRecord.id).first()
            #res.enabled == False
            db.session.add(res)
            db.session.commit()
            db.session.close()

    def __addAlerts__(self, activeRecord: InventorySqlModel) -> None:
        with db():
            res = db.session.query(EmailAlertsSqlModel).filter(EmailAlertsSqlModel.inventoryId == activeRecord.id).all()
            for alert in res:
                i = ActiveAlertModel(smtpContactId=alert.smtpContactsId, inventoryId=activeRecord.id)
                db.session.add(i.getSqlModel())
                db.session.commit()

            print(res)

