from django import template
from friendship.models import Friend

register = template.Library()

@register.simple_tag(takes_context=True)
def current_friends(context):
  user = context['user']
  return Friend.objects.friends(user)
