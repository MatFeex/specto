from django.db import models
from configuration.models import BaseModel, SoftDeleteModel, Employee
from django.contrib.auth.models import User
from django.utils import timezone

# PASSATION models

class Passation(BaseModel, SoftDeleteModel):

    transmitter = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Employee,to_field="matricule", on_delete=models.CASCADE)

    def __str__(self):
        return f"Passation {self.id}"


class PassationAction(BaseModel, SoftDeleteModel):
    actions = [
        ('Avancement', 'Avancement'),
        ('Qualité', 'Qualité'),
        ('Matière', 'Matière'),
        ('RH', 'RH'),
        ('Milieu', 'Milieu'),
        ('Méthode', 'Méthode'),
        ('Formation', 'Formation'),
    ]

    passation = models.ForeignKey(Passation, on_delete=models.CASCADE)

    msn = models.CharField(max_length=20,blank=True, null=True)
    action = models.CharField(max_length=20, choices=actions)
   
    def __str__(self):
        return f"Passation Action {self.id}"



class PassationStatus(BaseModel, SoftDeleteModel):
    statuses = [
        ('A faire', 'A faire'),
        ('En cours', 'En cours'),
        ('Cloturé', 'Cloturé'),
    ]

    action = models.ForeignKey(PassationAction, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=statuses)
   
    def __str__(self):
        return self.status