from __future__ import unicode_literals

from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User
import boto3
import botocore

# Create your models here.
class Hub(models.Model):
    alias = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    room = models.ForeignKey(Room, blank=True, null=True)
    serial_number = models.CharField(max_length=30, unique=True)
    def is_updated(self):
        client = boto3.client('iot-data', region_name='us-east-1')
        response = client.get_thing_shadow(thingName=self.serial_number)
        return "\"delta\":" not in response['payload'].read()
