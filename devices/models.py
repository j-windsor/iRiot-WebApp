from __future__ import unicode_literals

from django.db import models
from rooms.models import Room

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=30)
    room = models.ForeignKey(Room)

class Function(models.Model):
    function = models.CharField(max_length=30)
    prontohex = models.CharField(max_length=800)
    device = models.ForeignKey(Device)
