from django.contrib import admin
from .models import Division, Employee, Program, Product, Workshop, VMS_Planning

# Register your models here.
admin.site.register(Division)
admin.site.register(Program)
admin.site.register(Product)
admin.site.register(Workshop)
admin.site.register(Employee)
admin.site.register(VMS_Planning)


