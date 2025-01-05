from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=150)
    ticket_price = models.FloatField(default=0.00)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_organizer')

    def clean(self):
        if self.date.date() <= now().date():
            raise ValidationError("The event date must be set at least one day in the future.")
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() before saving
        super().save(*args, **kwargs)