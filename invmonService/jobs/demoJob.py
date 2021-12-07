from invmonService.logger import getLogger

class DemoJobService():
    def __init__(self) -> None:
        self.logger = getLogger()
        pass

    def start(self) -> None:
        self.logger.info("Hello from DemoJobService!")