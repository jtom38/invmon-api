from invmonInfra.domain import LoggerInterface, JobsInventoryInterface
from invmonInfra.enum import EnvReaderEnum, SchedulerTriggerEnum
from invmonInfra.models import SchedulerJobModel
from invmonService.firefoxDriverService import FirefoxDriverService
from invmonService.jobs import JobShopDisneyService, JobAlertService
from invmonService import SchedulerService, EnvReaderService, BasicLoggerService


class ApiEventsService():
    _env = EnvReaderService()
    _logger: LoggerInterface
    _isDebug: bool

    def __init__(self) -> None:
        if self._env.getValue(EnvReaderEnum.LOCALDEV) == True:
            self._isDebug = True
        else: self._isDebug = False

    def startup(self) -> None:
        self._logger = BasicLoggerService()
        self._logger.info("Running startup tasks")

        ss = SchedulerService()
        ss.addJob(self.__enableDisneyWatcher__())
        ss.addJob(self.__enableAlertEmail__())
        ss.start()

    def __enableDisneyWatcher__(self) -> SchedulerJobModel:
        _disneyService = JobShopDisneyService(
            logger=self._logger, 
            driver=FirefoxDriverService(logger=self._logger)
        )
        i = SchedulerJobModel(
            functionName=_disneyService.runJob
            ,trigger=SchedulerTriggerEnum.INTERVAL
            ,minutes=30)
        if self._isDebug == True:
            i.minutes = 30
        return i

    def __enableAlertEmail__(self) -> SchedulerJobModel:
        _emailAlertService = JobAlertService(logger=self._logger)
        return SchedulerJobModel(
            functionName=_emailAlertService.runJob
            ,trigger=SchedulerTriggerEnum.INTERVAL
            ,minutes=2
        )

    def shutdown(self) -> None:
        pass