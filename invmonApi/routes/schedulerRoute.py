from fastapi import APIRouter
from typing import List
from invmonService.scheduler import SchedulerService
from invmonInfra.models import SchedulerActveJobsModel


router = APIRouter(prefix='/scheduler', tags=['Scheduler'])


@router.get('/get/jobs')
def getJobs() -> List[SchedulerActveJobsModel]:
    ss = SchedulerService()
    jobs = ss.getjobs()
    print(jobs)
    return jobs