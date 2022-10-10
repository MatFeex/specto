from django.forms import ModelForm
from .models import Vms


class VmsForm(ModelForm):
    class Meta:
        model = Vms
        fields = [
            'reference','visit_date','user','employee','workshop']
        labels = {
            'user': 'Visitor',
            'reference': 'VMQ REF',
            'visit_date': 'DATE',
            'employee': 'Visited',
        }




