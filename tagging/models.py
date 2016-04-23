# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Labellog(models.Model):
    instance_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'LabelLog'


class Records(models.Model):
    event_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    event_date = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    actor1 = models.CharField(max_length=45, blank=True, null=True)
    actor2 = models.CharField(max_length=45, blank=True, null=True)
    event_type = models.CharField(max_length=45, blank=True, null=True)
    event_subtype = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Records'


class Taskinstances(models.Model):
    instance_id = models.IntegerField(primary_key=True)
    task_id = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TaskInstances'


class Tasks(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Tasks'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Users'

