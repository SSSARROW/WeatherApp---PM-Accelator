from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



urlpatterns = [
    path('', views.weather_list, name='weather_list'),
    path('get_weather_api/', views.get_weather_api, name='get_weather_api'),
    path('new/', views.weather_create, name='weather_create'),
    path('<int:pk>/edit/', views.weather_update, name='weather_update'),
    path('<int:pk>/delete/', views.weather_delete, name='weather_delete'),
    path('<int:pk>/youtube/', views.weather_youtube, name='weather_youtube'),
]