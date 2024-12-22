from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now=True)


class UserDetail(models.Model):
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=16, default='不明')
    height = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/img/avatar/', default='static/img/logo.webp')