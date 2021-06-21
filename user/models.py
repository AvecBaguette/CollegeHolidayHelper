from django.db import models


# Create your models here.
class Activity(models.Model):
    activity_type = models.CharField(null=True, blank=True, max_length=50)
    teacher_name = models.CharField(null=True, blank=True, max_length=50)
    course_name = models.CharField(null=True, blank=True, max_length=200)
    time_interval = models.CharField(null=True, blank=True, max_length=10)
    groups = models.CharField(null=True, blank=True, max_length=100)
    day = models.CharField(null=True, blank=True, max_length=20)
