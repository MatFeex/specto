from dataclasses import field
from django.forms import ModelForm
from .models import Division, Program, Product, Workshop


class DivisionForm(ModelForm):
    class Meta:
        model = Division
        fields = '__all__'


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = '__all__'