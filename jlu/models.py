from django.db import models

# Create your models here.


class UserInfo(models.Model):
    nickName = models.CharField(max_length=50)
    openID = models.TextField(unique=True, default=0)
    avatarUrl = models.TextField()