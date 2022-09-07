from django.db import models
from configuration.models import BaseModel, SoftDeleteModel

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
