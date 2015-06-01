from django.db import models


class Job(models.Model):

    INTERVAL_CHOICES = (
        ('Y', 'Yearly'),
        ('M', 'Monthly'),
        ('W', 'Weekly'),
        ('D', 'Daily'),
        ('H', 'Hourly'),
        ('m', 'Minutely')
    )

    name = models.TextField(max_length=32)
    description = models.TextField(max_length=128)
    interval = models.CharField(max_length=1, choices=INTERVAL_CHOICES, default='D')
    interval_options = models.TextField(max_length=32)
    last_run = models.DateTimeField(null=True)
    next_run = models.DateTimeField(null=True)
    arguments = models.TextField(default='')
    active = models.BooleanField(default=False)
    file_name = models.TextField(default='')


class JobLog(models.Model):
    job = models.ForeignKey(Job)
    submit_time = models.DateTimeField()
