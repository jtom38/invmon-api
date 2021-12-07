from abc import ABC, abstractclassmethod


class JobsInterface(ABC):
    """
    The JobsInterface is the root interface for all jobs.
    """

    @abstractclassmethod
    def runJob(self) -> None:
        """This is the primay entry point for all jobs."""
        pass
