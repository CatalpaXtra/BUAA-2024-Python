from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('map', views.map, name='map'),
    path('window/favor/<str:window>/<path:path>', views.favor_window, name='favor_window'),
    
    path('window/meal/<str:cafeteria>/<int:floor>/<str:window>', views.meal_window_detail, name='meal_window_detail'),
    path('window/drink/<str:cafeteria>/<int:floor>/<str:window>', views.drink_window_detail, name='drink_window_detail'),
    path('window/breakfast', views.breakfast_window_detail, name='breakfast_window_detail'),
    path('window/selfselect/<str:window>', views.selfselect_window_detail, name='selfselect_window_detail'),
]