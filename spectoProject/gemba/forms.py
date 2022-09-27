from django.forms import ModelForm
from .models import GembaService, GembaItem, Gemba, GembaItemItem


# SPECTO FORMS : GEMBA WALK

class GembaServiceForm(ModelForm):
    class Meta:
        model = GembaService
        fields = ['name','description']


class GembaItemForm(ModelForm):
    class Meta:
        model = GembaItem
        fields = ['name','description']


class GembaForm(ModelForm):
    class Meta:
        model = Gemba
        fields = ['user','gemba_date','gemba_items']
        labels = {
            'user': 'Auditor',
            'gemba_date': 'DATE',
        }


class GembaItemItemForm(ModelForm):
    class Meta:
        model= GembaItemItem
        fields = ['answer','problem','action']



