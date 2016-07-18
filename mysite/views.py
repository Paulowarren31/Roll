from django.shortcuts import render
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from bet.models import Bet

def index(request):
  context = RequestContext(request, {'user': request.user})
  return render_to_response('index.html', context_instance=context)

def bets(request):
  args = {}
  args['bets'] = Bet.objects.all()
  return render(request, 'bets.html', args)
