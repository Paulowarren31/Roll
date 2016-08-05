from django.db import models
from django.contrib.auth.models import User

class PointCount(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  points = models.IntegerField()

  def __str__(self):
    return self.user.username + ' ' + str(self.points)


