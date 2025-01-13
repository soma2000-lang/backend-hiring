import logging
from time import sleep
from django.db import transaction
from .models import Site, UserRecords
from celery import shared_task
from .models import Jobs
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@shared_task
def task_01(site_id: int):
    TIME_MULTIPLIER = 0.001 # very fast execution per record
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 01: {} processed".format(record.name))
    return True

@shared_task
def task_02(site_id: int):
    TIME_MULTIPLIER = 0.01
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 02: {} processed".format(record.name))
        
    return True

@shared_task
def task_03(site_id: int):
    TIME_MULTIPLIER = 0.1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 03: {} processed".format(record.name))
    return True

@shared_task
def task_04(site_id: int):
    TIME_MULTIPLIER = 1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 04: {} processed".format(record.name))
    return True

@shared_task
def task_05(site_id: int):
    TIME_MULTIPLIER = 10
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 05: {} processed".format(record.name))
    return True



@shared_task
def distributer():
   """
   Distributes pending jobs to appropriate task handlers based on priority.

   """

   TASK_HANDLERS = {
       Jobs.TASK_01: task_01,
       Jobs.TASK_02: task_02, 
       Jobs.TASK_03: task_03,
       Jobs.TASK_04: task_04,
       Jobs.TASK_05: task_05
   }

   prioritized_sites = (
       Site.objects.filter(
           jobs__status="pending"
       ).distinct().order_by(
           '-record_capacity' 
       ).prefetch_related(
           'jobs'
       )
   )

   job_count = 0
   with transaction.atomic():
       for site in prioritized_sites:
           pending_jobs = site.jobs.filter(status="pending")
       
           for task_type, task_handler in TASK_HANDLERS.items():
               task_jobs = pending_jobs.filter(task=task_type)
          
               job_ids = list(task_jobs.values_list('id', flat=True))
               if job_ids:
                   task_handler.delay_many(job_ids) if hasattr(task_handler, 'delay_many') else [task_handler.delay(job_id) for job_id in job_ids]
                   job_count += len(job_ids)

   return job_count

