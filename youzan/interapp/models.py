from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UC(models.Model):
    user = models.OneToOneField(User)
    stack_ID = models.CharField(default="", help_text="股票编号", max_length=64)
