from django import forms

class CommentForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
    email = forms.EmailField(required=False)
