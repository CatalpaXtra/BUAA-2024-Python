from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('login', views.mylogin, name='login'),
    path('login/check/<str:email>/<str:password>/<int:remember>', views.check_login, name='check_login'),
    path('logout', views.mylogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
    path('forget', views.forget, name='forget'),
    path('password', views.send_email_reset, name='reset_password'),
    path('modify', views.modify, name='modify'),
    path('modify_password', views.modify_password, name='modify_password'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('handle_avatar', views.handle_avatar, name='handle_avatar'),
    
    path('center', views.center, name='center'),
    path('history/pub', views.history_pub, name='history_pub'),
    path('history/like', views.history_like, name='history_like'),
    path('history/favorite', views.history_favorite, name='history_favorite'),
    path('history/eaten', views.history_eaten, name='history_eaten'),
    path('history/window', views.history_window, name='history_window'),
]