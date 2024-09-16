from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class BetaProgram(models.Model):
    name=models.CharField(max_length=20, null=True, unique=True)

class Access(models.Model):
    beta_key=models.CharField(max_length=20, null=True, unique=True)

class Assign(models.Model):
    manager=models.ForeignKey(User,max_length=20)
    access=models.ForeignKey(Access,max_length=20)

