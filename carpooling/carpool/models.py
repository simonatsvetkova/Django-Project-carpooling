from django.db import models
from django.core.validators import MinValueValidator

from accounts.models import ProfileUser


# Create your models here.


class Offer(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
