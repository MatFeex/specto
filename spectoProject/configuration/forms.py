from dataclasses import field
from django.forms import ModelForm
from .models import Division, Program, Product, Workshop


class DivisionForm(ModelForm):
    class Meta:
        model = Division
        fields = ['name','location','description']


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['division','name','description']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['program','name','description']


class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = ['product','name','description']