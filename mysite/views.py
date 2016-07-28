from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from bet.models import Bet
from django.contrib.auth import logout
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest

from allauth.socialaccount.models import SocialToken

import requests

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
  args['bet'] = Bet.objects.filter(id=id_in)[0]
  return render(request, 'bet.html', args)

def logout_view(request):
  if request.user.is_authenticated():
    logout(request)
  return redirect('/')

def friends(request):
  if not request.user.is_authenticated():
    #TODO:
    #redirect to login page or error page or somethin
    return redirect('/')

  args = {}
  args['friends'] = Friend.objects.friends(request.user)
  args['friend_img_urls'] = request.user.socialaccount_set.all()

  print(request.user.socialaccount_set.all()[0].extra_data['friends']['data'])
  return render(request, 'friends.html', args)

def friend_detail(request, id_in):
  if not request.user.is_authenticated():
    #TODO:
    #redirect to login page or error page or somethin
    return redirect('/')
  args = {}
  args['friend'] = Friend.objects.friends(request.user)[int(id_in) - 1]
  return render(request, 'friend.html', args)

def add_friend(request, id_in):
  friend = User.objects.filter(id=id_in)[0]
  Friend.objects.add_friend(request.user, friend).accept()
  print(Friend.objects.friends(request.user))

  return redirect('/friends')

def test(request):
  print(request.user)
  social_user = request.user.socialaccount_set.all()
  return redirect('/')

