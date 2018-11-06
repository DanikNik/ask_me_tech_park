from django.contrib.auth.models import User
from django.db import models

class Person(User):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)

