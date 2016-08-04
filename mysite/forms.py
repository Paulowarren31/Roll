from django import forms

from friendship.models import Friend, Follow

class BetForm(forms.Form):
  def __init__(self, user, *args, **kwargs):
    super(BetForm, self).__init__(*args, **kwargs)
    self.fields['people'] = forms.MultipleChoiceField(
        choices=[(o.id, str(o)) for o in Friend.objects.friends(user)] 
    )

  title = forms.CharField(max_length=30)
  description = forms.CharField(max_length=200)
  GBP = forms.IntegerField()
  end_date = forms.DateField()

class CommentForm(forms.Form):
  comment = forms.CharField()
