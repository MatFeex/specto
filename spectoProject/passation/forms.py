from django.forms import ModelForm
from .models import Passation


class PassationForm(ModelForm):
    class Meta:
        model = Passation
        fields = [
            'transmitter','receiver']





