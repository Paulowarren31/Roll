from django.shortcuts import render, redirect
from bet.models import Bet

def bets(request):
  if request.user.is_authenticated():
    args = {}
    args['bets'] = Bet.objects.all()
    return render(request, 'bets.html', args)
  else:
    return redirect('/')

def bet_detail(request, id_in):
  args = {}
  args['bet'] = Bet.objects.filter(id=id_in)[0]
  return render(request, 'bet.html', args)

