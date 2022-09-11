from __future__ import division
from distutils.command.upload import upload
from django.utils import timezone
from msilib.schema import Error
from django.db import models


# SPECTO MODELS - CONFIGURATION :

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, default="Default User")
    updated_by = models.CharField(max_length=50, default="Default User")

    class Meta :
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteManagerDel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null = True)
    deleted_by = models.CharField(max_length=50, blank = True, null=True)
    restored_at = models.DateTimeField(blank=True, null = True)
    restored_by = models.CharField(max_length=50, blank = True, null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted_objects = SoftDeleteManagerDel()

    def delete(self):
        raise Error()

    def soft_deleted(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = "Default User"
        self.save()

    def restore(self):
        self.is_deleted = False
        self.restored_at = timezone.now()
        self.restored_by = "Default User"
        self.save()

    class Meta : 
        abstract = True


class Division(BaseModel,SoftDeleteModel):

    name = models.CharField(max_length=30, default="Division name")
    location = models.CharField(max_length=30,default="Tunis")
    description = models.CharField(max_length=200,default="Division description")

    def __str__(self):
        return self.name


class Program(BaseModel,SoftDeleteModel):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="Program name")
    description = models.CharField(max_length=200,default="Program description")

    def __str__(self):
        return self.name


class Product(BaseModel,SoftDeleteModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="Product name")
    description = models.CharField(max_length=200,default="Product description")

    def __str__(self):
        return self.name


class Workshop(BaseModel,SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="Workshop name")
    description = models.CharField(max_length=200,default="Workshop description")

    def __str__(self):
        return self.name

class EmployeeFile(models.Model):
    employee_data_file = models.FileField(upload_to='configuration/handle_uploaded_file') # to create a file input in templates

class Employee(models.Model): # does not inherit from BaseModel/SoftDeleteModel because managed from upload

    matricule = models.IntegerField()
    names = models.CharField(max_length= 100)
    i_p = models.CharField(max_length=2)
    code = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop,on_delete=models.CASCADE)
    wording = models.CharField(max_length=100)
    cost_center = models.CharField(max_length=30)
    job_bulletin = models.CharField(max_length=100)
    resp_matricule_n1 = models.IntegerField()
    resp_names_n1 = models.CharField(max_length=100)
    resp_matricule_n2 = models.IntegerField()
    resp_names_n2 = models.CharField(max_length=100)
    staff_tab_afs = models.CharField(max_length=50)
    
    division = models.ForeignKey(Division,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.names)

