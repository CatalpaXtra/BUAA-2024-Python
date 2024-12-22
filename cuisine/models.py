from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Cuisine(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=32)
    cafeteria = models.CharField(max_length=32)
    floor = models.CharField(max_length=32)
    window = models.CharField(max_length=32)
    star_ave = models.FloatField(default=-1)
    cost = models.FloatField(default=-1)
    image = models.ImageField()
    tag1 = models.CharField(max_length=32)
    tag2 = models.CharField(max_length=32)
    tag3 = models.CharField(max_length=32,default='')
    

    def __str__(self):
        return self.name


class CuisineComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-pub_time']


class StarCuisine(models.Model):
    star = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='stars')
    created_or_update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_or_update_at']


class FavoriteCuisine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cuisine')
        ordering = ['-created_at']


class EatenCuisine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='eatens')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cuisine')
        ordering = ['-created_at']