from django.db import models
from django.utils import timezone

# Create your models here.

class Bet(models.Model):
  author = models.ForeignKey('auth.User', related_name='true_author')
  people = models.ManyToManyField('auth.User', related_name='people_in_bet')
  title = models.CharField(max_length=200)
  text = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_date = models.DateTimeField(
          default=timezone.now)
  published_date = models.DateTimeField(
          blank=True, null=True)
  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def __str__(self):
    return 'bet made by ' + self.author.username

