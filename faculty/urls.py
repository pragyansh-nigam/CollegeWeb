from django.urls import path 
from . import views
urlpatterns = [
    path('home1', views.home1),
    path("answer1",views.answer1)    
]