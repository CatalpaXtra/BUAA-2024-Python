from django.urls import path
from . import views

app_name = 'cuisine'

urlpatterns = [
    path('<int:cuisine_id>', views.cuisine_detail, name='cuisine_detail'),
    path('pub', views.pub_comment, name='pub_comment'),
    path('search', views.search, name='search'),
    path('favor/<int:cuisine_id>', views.favor_cuisine, name='favor_cuisine'),
    path('eaten/<int:cuisine_id>', views.eaten_cuisine, name='eaten_cuisine'),
    path('recommend', views.recommend, name='recommend'),
]