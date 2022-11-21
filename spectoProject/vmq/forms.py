from dataclasses import field
from django.forms import ModelForm
from .models import Theme, Item, Vmq, VmqItem, QualityReference


class QualityReferenceForm(ModelForm):
    class Meta:
        model = QualityReference
        fields = ['name','description']

class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['name','description']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name','description']


class VmqForm(ModelForm):
    class Meta:
        model = Vmq
        fields = ['reference','visit_date','user','employee','workshop']
        labels = {
            'user': 'Visitor',
            'reference': 'VMQ REF',
            'visit_date': 'DATE',
            'employee': 'Visited',
        }

class VmqItemForm(ModelForm):
    class Meta:
        model= VmqItem
        fields = ['result','type','comment']


