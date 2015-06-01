from django_cron import CronJobBase, Schedule
from models import *

import datetime
import calendar
import subprocess

from SchPark.settings import SPARK_BIN_DIR
from SchPark.settings import BASE_DIR

def add_month(sourcedate):
    month = sourcedate.month - 1 + 1
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.datetime(year, month, day, sourcedate.hour, sourcedate.minute)


def next_weekday(now, weekday):
    days_ahead = weekday - now.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return now + datetime.timedelta(days_ahead)


def new_next_run(job):
    now = datetime.datetime.now()
    if job.interval == 'Y':
        interval_options = job.interval_options
        day = int(interval_options[0:2])
        month = int(interval_options[3:5])
        hour = int(interval_options[6:8])
        minute = int(interval_options[9:11])

        prev_run_datetime = datetime.datetime(now.year, month, day, hour, minute)
        if prev_run_datetime > now:
            job.next_run = prev_run_datetime
        else:
            job.next_run = datetime.datetime(now.year + 1, month, day, hour, minute)

    elif job.interval == 'M':
        interval_options = job.interval_options
        day = int(interval_options[0:2])
        hour = int(interval_options[3:5])
        minute = int(interval_options[6:8])

        prev_run_datetime = datetime.datetime(now.year, now.month, day, hour, minute)
        if prev_run_datetime > now:
            job.next_run = prev_run_datetime
        else:
            while prev_run_datetime<=now:
                prev_run_datetime = add_month(prev_run_datetime)
            job.next_run = prev_run_datetime

    elif job.interval == 'W':
        interval_options = job.interval_options
        weekday = int(interval_options[0:1])
        hour = int(interval_options[2:4])
        minute = int(interval_options[5:7])

        prev_run_datetime = datetime.datetime(now.year, now.month, now.day, hour, minute)
        if not now.weekday() == weekday:
            prev_run_datetime = next_weekday(prev_run_datetime, weekday)

        job.next_run = prev_run_datetime

    elif job.interval == 'D':
        interval_options = job.interval_options
        hour = int(interval_options[0:2])
        minute = int(interval_options[3:5])

        prev_run_datetime = datetime.datetime(now.year, now.month, now.day, hour, minute)
        if now > prev_run_datetime:
            prev_run_datetime = prev_run_datetime + datetime.timedelta(days=1)

        job.next_run = prev_run_datetime

    elif job.interval == 'H':
        interval_options = job.interval_options
        minute = int(interval_options[0:2])

        prev_run_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, minute)

        if now > prev_run_datetime:
            prev_run_datetime = prev_run_datetime + datetime.timedelta(hours=1)

        job.next_run = prev_run_datetime

    elif job.interval == 'm':
        interval_options = job.interval_options
        minutes = int(interval_options)

        prev_run_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute + minutes)
        job.next_run = prev_run_datetime

    job.save()


def next_run(job):
    now = datetime.datetime.now()
    if job.interval == 'Y':
        last_run = job.last_run
        job.next_run = datetime.datetime(last_run.year+1, last_run.month, last_run.day, last_run.hour, last_run.minute)

    elif job.interval == 'M':
        last_run = job.last_run
        if int(job.interval_options[0:2]) == 31:
            job.next_run = add_month(datetime.datetime(last_run.year, last_run.month, 31, last_run.hour, last_run.minute, last_run.second))
        else:
            job.next_run = add_month(last_run)

    elif job.interval == 'W':
        last_run = job.last_run
        job.next_run = last_run + datetime.timedelta(days=7)

    elif job.interval == 'D':
        last_run = job.last_run
        job.next_run = last_run + datetime.timedelta(days=1)

    elif job.interval == 'H':
        last_run = job.last_run
        job.next_run = last_run + datetime.timedelta(hours=1)

    elif job.interval == 'm':
        last_run = job.last_run
        minutes = int(job.interval_options)
        job.next_run = last_run
        while job.next_run < now:
            job.next_run = job.next_run + datetime.timedelta(minutes=minutes)

    job.save()


class SubmitJobs(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'core.submit_jobs'
    ALLOW_PARALLEL_RUNS = False

    def do(self):
        #Get active jobs
        jobs = Job.objects.filter(active=True)
        for job in jobs:
            if not job.next_run:
                 new_next_run(job)
            else:
                if job.next_run <= datetime.datetime.now():
                    subprocess.Popen(SPARK_BIN_DIR + '/spark-submit --master spark://localhost:7077 ' + BASE_DIR + '/job_files/' + job.file_name  , shell=True)

                    job.last_run = job.next_run
                    job.save()

                    next_run(job)

                    #JobLog
                    #...
