from django.forms import ModelForm
from .models import TaintedLemma

class TaintedLemmaForm(ModelForm):
    class Meta:
        model = TaintedLemma
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TaintedLemmaForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['class'] = 'select'
        self.fields['lang'].widget.attrs['class'] = 'select'
        self.fields['lang'].disabled = True
        self.fields['name'].widget.attrs['class'] = 'input'
        self.fields['name'].disabled = True
        self.fields['is_evaluated'].widget.attrs['class'] = 'checkbox'
