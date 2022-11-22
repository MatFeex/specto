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
        fields = ['reference','visit_date','user']
        labels = {
            'user': 'Visitor',
            'reference': 'VMQ REF',
            'visit_date': 'DATE',
        }

class VmqItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VmqItemForm, self).__init__(*args, **kwargs)
        self.fields['defer_immediate'].label = False
        self.fields['responsible'].label = False
        self.fields['date'].label = False
    class Meta:
        model= VmqItem
        fields = ['defer_immediate','responsible','date']
        labels = {
            'defer_immediate': 'Defered/Immediate',
        }


