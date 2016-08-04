from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from bet.models import Bet, BetComment
from django.contrib.auth import logout
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest
from allauth.socialaccount.models import SocialToken
import json

from .forms import BetForm, CommentForm

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

  bet = Bet.objects.get(pk=id_in)
  print(bet.people)

  if request.method == 'POST':
    #adding a comment...
    if request.user not in bet.people.all():
      #or 404?
      return redirect('/')
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.cleaned_data['comment']
      new_comment = BetComment(comment=comment, author=request.user, bet=bet)
      new_comment.save()

      return redirect('/bet/'+id_in)
  else:
    context = {}

    context['bet'] = bet
    context['comments'] = BetComment.objects.filter(bet=bet)
    context['form'] = CommentForm()
    return render(request, 'bet.html', context)

def remove_comment(request, bet_id_in, comment_id_in):

  bet = Bet.objects.get(pk=bet_id_in)
  #if they are not in the bet
  if request.user not in bet.people.all():
    #or 404?
    return redirect('/')

  comment = BetComment.objects.get(pk=comment_id_in)
  #if they are not the author
  if request.user != comment.author:
    return redirect('/')
  comment.delete()

  return redirect('/bet/'+bet_id_in)


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
  friend = User.objects.get(pk=int(id_in))

  #if they are friends
  if Friend.objects.are_friends(request.user, friend):
    args['friend'] = friend
    return render(request, 'friend.html', args)
  else:
    #not friends
    return redirect('/')

def add_friend(request, id_in):
  friend = User.objects.get(pk=id_in)
  Friend.objects.add_friend(request.user, friend).accept()
  return redirect('/bets')

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
        friend = User.objects.get(pk=id)
        newForm.people.add(friend)
      newForm.people.add(request.user)
      newForm.save()

      return redirect('/bets')
  else:
    form = BetForm(request.user)
  return render(request, 'add_bet.html', {'form': form}) 
