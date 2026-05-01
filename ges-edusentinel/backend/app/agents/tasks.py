import os
from celery import Celery
from .orchestrator import run_deepscan

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("edusentinel", broker=REDIS_URL, backend=REDIS_URL)

@celery.task
def deepscan_task(scope_org_unit_id: int, term_id: int, dataset: str):
    result = run_deepscan(scope_org_unit_id, term_id, dataset)
    return result.__dict__
