from django.urls import path 
from . import views
urlpatterns = [
    path('home1', views.home1), 
    path('question1',views.question1),
    path('stuquestion1',views.stuquestion1),
    path("stuanswer1",views.stuanswer1) 
]