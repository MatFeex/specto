from dataclasses import field
from django.forms import ModelForm
from .models import Theme, Item


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['name','description']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['theme','name','description']

