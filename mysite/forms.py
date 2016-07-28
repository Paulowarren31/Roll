from django import forms

class BetForm(forms.Form):
  name = forms.CharField(label='name', max_length=20)
