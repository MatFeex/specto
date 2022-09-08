from django.utils import timezone
from django.db import models
from configuration.models import BaseModel, SoftDeleteModel, Workshop
from django.contrib.auth.models import User

# SPECTO MODELS - VMQ :

class Theme(BaseModel,SoftDeleteModel):

    name = models.CharField(max_length=30, default="Theme name")
    description = models.TextField(default="Theme description")

    def __str__(self):
        return self.name


class Item(BaseModel,SoftDeleteModel):
    
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="Item name")
    description = models.TextField(default="Item description")

    def __str__(self):
        return self.name


class Vmq(BaseModel, SoftDeleteModel):
    results = [
        ('Conforme', 'Conforme'),
        ('Non Conforme', 'Non Conforme')
    ]
    types = [
        ('Application', 'Application'),
        ('Disposition', 'Disposition')
    ]

    reference = models.CharField(max_length=100, default="REF")
    visit_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    employee = models.IntegerField(default=1)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    result = models.CharField(max_length=30,choices=results,default=results[0])
    type = models.CharField(max_length=30, choices=types, default=types[0])
    comment = models.TextField(default="Comment")

    def __str__(self):
        return self.reference





