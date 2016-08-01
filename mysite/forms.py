from django import forms

from friendship.models import Friend, Follow

class BetForm(forms.Form):
  def __init__(self, user, *args, **kwargs):
    super(BetForm, self).__init__(*args, **kwargs)
    self.fields['people'] = forms.ChoiceField(
        choices=[(o, str(o)) for o in Friend.objects.friends(user)] 
    )
