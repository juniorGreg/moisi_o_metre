from django.forms import ModelForm
from .models import TaintedLemma

class TaintedLemmaForm(ModelForm):
    class Meta:
        model = TaintedLemma
        fields = '__all__'
