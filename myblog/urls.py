from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('home', views.home, name='home'),
    path('detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('like/<int:blog_id>', views.like_blog, name='like_blog'),
    path('pub', views.pub_blog, name='pub_blog'),
    path('comment/pub', views.pub_comment, name='pub_comment'),
    path('search', views.search, name='search'),
    path('delete/<int:blog_id>', views.delete_blog, name='delete'),
]