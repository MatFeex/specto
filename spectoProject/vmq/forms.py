from dataclasses import field
from django.forms import ModelForm
from .models import Theme, Item, Vmq


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['name','description']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['theme','name','description']


class VmqForm(ModelForm):
    class Meta:
        model = Vmq
        fields = ['reference','visit_date','user','employee','workshop','items','result','type','comment']



