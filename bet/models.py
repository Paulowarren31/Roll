from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Bet(models.Model):
  author = models.ForeignKey('auth.User', related_name='true_author')
  people = models.ManyToManyField('auth.User', related_name='people_in_bet')
  title = models.CharField(max_length=200)
  text = models.TextField()
  price = models.IntegerField()
  created_date = models.DateTimeField(default=timezone.now().strftime('%x'))
  end_date = models.DateTimeField(blank=True)
  def publish(self):
    self.save()

  def __str__(self):
    return self.title


class BetComment(models.Model):
  author = models.ForeignKey('auth.User', related_name='author')
  comment = models.CharField(max_length=200)
  date = models.DateTimeField(default=timezone.now)
  bet = models.ForeignKey(Bet, on_delete=models.CASCADE, default=2)

  def publish(self):
    self.save()
  
  def __str__(self):
    return self.comment
