from abc import ABC, abstractclassmethod
from typing import List
from invmonInfra.models import InventorySqlModel
from invmonInfra.domain.jobsInterface import JobsInterface


class JobsInventoryInterface(JobsInterface, ABC):
    _urlPattern: str

    @abstractclassmethod
    def __collectInventoryRecords__(self, likeUrl: str) -> List[InventorySqlModel]:
        """
        This talks to sql to find the records that need be pulled for this Job.  
        This can be found in JobsInventoryBase.
        """
        pass

    @abstractclassmethod
    def __checkInventoryStatus__(self, item: InventorySqlModel) -> None:
        """
        This checks each indiviual item and validates the inventory status.
        This is added to each job, not from Base.
        """
        pass

    @abstractclassmethod
    def __checkIfOutOfStock__(self, tag: str, key: str, value: str) -> bool:
        """
        This checks to find the attribute that tells us that item is out of stock.
        This can be found in JobsInventoryBase
        
        Example:
        __checkIfOutOfStock__(tag='div', key='class', value='product-oos-info-title')
        """
        pass

    @abstractclassmethod
    def __updateInventoryRecord__(self, activeRecord: InventorySqlModel) -> None:
        pass

    @abstractclassmethod
    def __addAlerts__(self, activeRecord: InventorySqlModel) -> None:
        """
        This will generate the records to tell the other jobs that an alert needs to be sent out for the the item sent.
        This can be found in JobsInventoryBase.
        """
