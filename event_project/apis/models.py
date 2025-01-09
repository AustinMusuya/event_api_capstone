from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

# Create your models here.
User = get_user_model()
class Event(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=150)
    ticket_price = models.FloatField(default=0.00)
    tags = TaggableManager()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_organizer')
