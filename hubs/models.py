from __future__ import unicode_literals

from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User

# Create your models here.
class Hub(models.Model):
    alias = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    room = models.ForeignKey(Room, blank=True, null=True)
    serial_number = models.CharField(max_length=30)
