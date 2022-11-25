from django.utils import timezone
from django.db import models
from configuration.models import BaseModel, SoftDeleteModel, Workshop, Employee
from django.contrib.auth.models import User

# SPECTO MODELS - VMQ :

class QualityReference(BaseModel,SoftDeleteModel):

    name = models.CharField(max_length=100, default="Quality reference name")
    description = models.TextField(default="Quality reference description")

    def __str__(self):
        return self.name

class Theme(BaseModel,SoftDeleteModel):

    quality_reference = models.ForeignKey(QualityReference, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Theme name")
    description = models.TextField(default="Theme description")

    def __str__(self):
        return self.name


class Item(BaseModel,SoftDeleteModel):
    
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Item name")
    description = models.TextField(default="Item description")

    def __str__(self):
        return self.name


class Vmq(BaseModel, SoftDeleteModel):

    visit_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,to_field="matricule", on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='VmqItem',blank=True)

    def __str__(self):
        return self.reference


class VmqItem(models.Model):
    results = [
        ('Conforme', 'Conforme'),
        ('Non Conforme', 'Non Conforme')
    ]
    types = [
        ('Application', 'Application'),
        ('Disposition', 'Disposition')
    ]
    choices = [
        ('Deferred', 'Deferred'),
        ('Immediate', 'Immediate')
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    vmq = models.ForeignKey(Vmq, on_delete=models.CASCADE)
    result = models.CharField(max_length=30,choices=results)
    type = models.CharField(max_length=30, choices=types)
    comment = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    defer_immediate = models.CharField(max_length=30, choices=choices, null=True, blank=True, default=None)
    responsible = models.ForeignKey(Employee,on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return self.comment


