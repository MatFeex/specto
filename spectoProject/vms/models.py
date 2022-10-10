from django.utils import timezone
from django.db import models
from configuration.models import BaseModel, SoftDeleteModel, Workshop, Employee
from django.contrib.auth.models import User

from vmq.models import VmqItem

# SPECTO MODELS - VMS :

class Vms(BaseModel, SoftDeleteModel):

    reference = models.CharField(max_length=100, default="REF")
    visit_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference


class VmsItem(models.Model):

    condition_types = [
        ('PP', 'PP'),
        ('AD', 'AD'),
        ('CD', 'CD'),
    ]
    action_types = [
        ('IMM', 'IMM'),
        ('DIF', 'DIF')
    ]

    vms = models.ForeignKey(Vms, on_delete=models.CASCADE)
    observation = models.TextField()
    condition_type = models.CharField(max_length=10,choices=condition_types)
    dialogue_answer = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=10, choices= action_types, blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    manager = models.CharField(max_length=30,blank=True, null=True)
    delay = models.DateField(blank=True, null=True)

