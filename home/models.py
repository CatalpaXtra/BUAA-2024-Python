from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class FavoriteWindow(models.Model):
    name = models.CharField(max_length=32, default='')
    path = models.CharField(max_length=128, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ('user', 'cuisine')
        ordering = ['-created_at']
