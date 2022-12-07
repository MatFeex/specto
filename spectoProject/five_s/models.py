from django.db import models
from configuration.models import BaseModel, SoftDeleteModel, Workshop
from django.contrib.auth.models import User
from django.utils import timezone

# 5S models

class Criteria(BaseModel, SoftDeleteModel):

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150,blank=True, null=True)

    def __str__(self):
        return self.name


class HoldingGrid(BaseModel, SoftDeleteModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    criterias = models.ManyToManyField(Criteria,through="HoldingGridCriteria",blank=True)

    def __str__(self):
        return f"Holding grid {self.id}"

class HoldingGridCriteria(models.Model):

    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    holding_grid = models.ForeignKey(HoldingGrid, on_delete= models.CASCADE)
    response = models.BooleanField(default=False)
    comment = models.CharField(max_length=150,blank=True, null=True)

    def __str__(self):
        return self.comment