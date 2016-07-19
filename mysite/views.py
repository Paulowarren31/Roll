from django.shortcuts import render
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from bet.models import Bet
from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
  context = RequestContext(request, {'user': request.user})
  return render_to_response('index.html', context_instance=context)

def bets(request):
  args = {}
  args['bets'] = Bet.objects.all()
  if request.user.is_authenticated():
    return render(request, 'bets.html', args)
  else:
    return redirect('/')

def bet_detail(request, id_in):
  args = {}
  args['bet'] = Bet.objects.filter(id=id_in)
  print(Bet.objects.filter(id=id_in))
  return render(request, 'bet.html', args)
    

def logout_view(request):
  if request.user.is_authenticated():
    logout(request)
  return redirect('/')




