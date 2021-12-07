from invmonInfra.enum import InventoryLastStatusEnum
from invmonService import FirefoxDriverService, HtmlParser, BasicLoggerService
from invmonInfra.base import JobsInventoryBase
from invmonInfra.domain import JobsInventoryInterface, DriverInterface, LoggerInterface
from invmonInfra.models import InventorySqlModel


class JobShopDisneyService(JobsInventoryBase, JobsInventoryInterface): 
    _logger: LoggerInterface
    _driver: DriverInterface
    _parser: HtmlParser
    _urlPattern: str = '%shopdisney.com%'
    
    def __init__(self, logger: LoggerInterface, driver = DriverInterface) -> None:
        self._logger = logger
        self._driver = driver
        self._parser = HtmlParser()
        self._parser.setLogger(self._logger)

    def __checkInventoryStatus__(self, item: InventorySqlModel) -> None:
        # Set the URI
        self._logger.info(f"Checking '{item.url}'")
        self.setUri(item.url)

        self._driver.driverGoTo(self.getUri())
        self.parser = HtmlParser(sourceCode=self._driver.driverGetContent())

        # validate the HTML format didnt change

        # Check if 'out of stock' is present
        outOfStock = self.__checkIfOutOfStock__(tag='div', key='class', value='product-oos-info-title')
        #inStock = self.checkIfInStock()

        if outOfStock == True:
            # if the lastStatus didnt change, move on
            self._logger.debug("Item is out of stock")
            if item.lastStatus == InventoryLastStatusEnum.OUTOFSTOCK.value:
                self._logger.debug("Inventory Status didnt change, checking the next item.")
                return None
            item.lastStatus = InventoryLastStatusEnum.OUTOFSTOCK.value

        if outOfStock == False:
            # if the lastStatus didnt change, move on
            self._logger.debug("Item is in stock!")
            if item.lastStatus == InventoryLastStatusEnum.INSTOCK.value:
                self._logger.debug("Inventory Status didnt change, checking the next item.")
                return None
            item.lastStatus = InventoryLastStatusEnum.INSTOCK.value

        self.__updateInventoryRecord__(item)
        self.__addAlerts__(item)

    def checkIfInStock(self) -> bool:
        invStatus: str = self.parser.findSingle(name='div', attrKey='class', attrValue='col-12 prices-add-to-cart-actions'
        )

