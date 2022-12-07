from django.forms import ModelForm
from .models import Criteria, HoldingGrid, HoldingGridCriteria


class CriteriaForm(ModelForm):
    class Meta:
        model = Criteria
        fields = ['name','description']


class HoldingGridForm(ModelForm):
    class Meta:
        model = HoldingGrid
        fields = ['user','workshop']


class HoldingGridCriteriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HoldingGridCriteriaForm, self).__init__(*args, **kwargs)
        self.fields['response'].label = False
        self.fields['comment'].label = False
    class Meta:
        model= HoldingGridCriteria
        fields = ['response','comment']


