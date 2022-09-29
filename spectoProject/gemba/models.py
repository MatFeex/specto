from django.utils import timezone
from django.db import models
from configuration.models import BaseModel, SoftDeleteModel
from django.contrib.auth.models import User

# SPECTO MODELS - GEMBA :

class GembaService(BaseModel,SoftDeleteModel):

    name = models.CharField(max_length=100, default="Gemba service name")
    description = models.TextField(default="Gemba service description")

    def __str__(self):
        return self.name


class GembaItem(BaseModel,SoftDeleteModel):
    
    gemba_service = models.ForeignKey(GembaService, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Gemba Item name")
    description = models.TextField(default="Gemba item description")

    def __str__(self):
        return self.name


class Gemba(BaseModel, SoftDeleteModel):

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    gemba_date = models.DateField(default=timezone.now)
    gemba_items = models.ManyToManyField(GembaItem, through='GembaItemItem',blank=True)

    def __str__(self):
        return self.gemba_date


class GembaItemItem(models.Model):
    answers = [
        ('OK', 'OK'),
        ('NK', 'NK')
    ]
    gemba_item = models.ForeignKey(GembaItem, on_delete=models.CASCADE)
    gemba = models.ForeignKey(Gemba, on_delete=models.CASCADE)
    answer = models.CharField(max_length=30,choices=answers)
    problem = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.action


