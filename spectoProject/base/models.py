from msilib.schema import Error
from multiprocessing.util import abstract_sockets_supported
from turtle import update
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, default="Unknown User")
    updated_by = models.CharField(max_length=50, default="Unknown User")

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
        self.deleted_at = models.DateTimeField(auto_now=True)
        self.deleted_by = models.ForeignKey(User,default=User,on_delete=models.CASCADE)
        self.save()

    def restore(self):
        self.is_deleted = False
        self.restored_at = models.DateTimeField(auto_now=True)
        self.restored_by = models.ForeignKey(User,default=User,on_delete=models.CASCADE)
        self.save()

    class Meta : 
        abstract = True




