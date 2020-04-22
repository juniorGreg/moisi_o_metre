from django import forms

class CommentForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
