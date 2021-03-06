from logging import Logger
from time import sleep
from os.path import exists
from os import remove

from invmonInfra.domain.loggerInterface import LoggerInterface


class DriverBase():
    _logger: LoggerInterface

    
    def __init__(self) -> None:
        self.uri: str = ''

    def driverGetContent(self) -> str:
        try:
            content = self.__driver__.page_source
            return content
        except Exception as e:
            if "Failed to decode response from marionette" in e.args[0]:
                self._logger.critical(f"Code: s01 - Failed to read from browser.  This can be due to not enough RAM on the system. Error: {e}")
            else:
                self._logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def driverGoTo(self, uri: str) -> None:
        """
        This tells the driver to change pages.
        It will check what the current page is before it sends the command to change pages.
        This helps to avoid extra calls/refreshes if they are not needed.
        """
        try:
            if uri != self.driverGetUrl():
                self._logger.debug(f"Requesting page: '{uri}'")
                self.__driver__.get(uri)
                sleep(5)
                newUrl = self.driverGetUrl()
                if newUrl != uri:
                    self._logger.debug(f"Was redirected to '{newUrl}'!")
            # self.driver.implicitly_wait(10)
        except Exception as e:
            self._logger.error(f"Driver failed to get {uri}. Error: {e}")

    def driverSaveScreenshot(self, path: str) -> None:
        try:
            if exists(path) is True:
                remove(path)
        except Exception as e:
            self._logger.error(f"Attempted to remove the old screenshot on disk, but failed. Error: {e}")

        try:
            self.__driver__.save_screenshot(path)
        except Exception as e:
            self._logger.error(f"Attempted to save a screenshot to '{path}', but failed to do so. Error: {e}")

    def driverGetUrl(self) -> str:
        try:
            res = self.__driver__.current_url
            return res
        except Exception as e:
            raise Exception(f"Failed to get the active loaded page. Error: {e}")

    def driverFindByXPath(self, xpath: str) -> object:
        try:
            ele = self.driver.find_element_by_xpath(xpath)
            return ele
        except Exception as e:
            self._logger.error(f"Firefox failed to select the item via xpath.  Something changed on the page. Error: {e}")

    def driverClose(self, displayMsg: bool = True) -> None:
        try:
            self._logger.debug("Driver is closing.")
            self.__driver__.close()
        except Exception as e:
            self._logger.error(f"Driver failed to close. Error: {e}")
