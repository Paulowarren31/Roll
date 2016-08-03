from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from bet.models import Bet
from django.contrib.auth import logout
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest

from allauth.socialaccount.models import SocialToken

from .forms import BetForm

import requests

def index(request):
  context = RequestContext(request, {'user': request.user})
  return render_to_response('index.html', context_instance=context)

def bets(request):
  if request.user.is_authenticated():
    context = {}
    bets = Bet.objects.all()
    context['bets'] = []
    for bet in bets:
      if request.user in bet.people.all():
        context['bets'].append(bet)
    return render(request, 'bets.html', context)
  else:
    return redirect('/')

def bet_detail(request, id_in):
  args = {}
  args['bet'] = Bet.objects.filter(id=id_in)[0]
  return render(request, 'bet.html', args)

def logout_view(request):
  if request.user.is_authenticated():
    logout(request)
  return redirect('/')

def friend_detail(request, id_in):
  if not request.user.is_authenticated():
    #TODO:
    #redirect to 404
    return redirect('/')
  args = {}
  friend_id = int(id_in)
  friend = User.objects.get(id=int(id_in))

  #if they are friends
  if Friend.objects.are_friends(request.user, friend):
    args['friend'] = friend
    return render(request, 'friend.html', args)
  else:
    #not friends
    return redirect('/')

def add_friend(request, id_in):
  friend = User.objects.get(id=id_in)
  Friend.objects.add_friend(request.user, friend).accept()
  return redirect('/friends')

def add_bet_form(request):
  if request.method == 'POST':
    form = BetForm(request.user, request.POST)
    if form.is_valid():

      author = request.user
      title = form.cleaned_data['title']
      people_ids = form.cleaned_data['people']
      gbp = form.cleaned_data['GBP']
      end_date = form.cleaned_data['end_date']
      text = form.cleaned_data['description']

      newForm = Bet(author=author, title=title, text=text, price=gbp, end_date=end_date)
      newForm.save()

      for id in people_ids:
        friend = User.objects.get(id=id)
        newForm.people.add(friend)
      newForm.people.add(request.user)
      newForm.save()

      return redirect('/bets')
  else:
    form = BetForm(request.user)
  return render(request, 'add_bet.html', {'form': form})
