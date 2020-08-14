# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import pytz

# Main cronjob function.
from main import cronjob

date = datetime.datetime(2020, 8, 14, 7, 0, 0)
timezone = pytz.timezone('Canada/Eastern')
date = timezone.localize(date)

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cronjob, 'date', run_date=date)

scheduler.start()