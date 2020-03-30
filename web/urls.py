from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home),
    path("about", views.about),
    path("gallery1", views.gallery1),
    path('login1',views.login1),
    path('verify1',views.verify1),
    path('resend',views.resend),
    path("contact1", views.contact1),
    path("savecontact", views.saveContact),
    path('register', views.register),
    path("loginuser", views.loginuser),
    path("resetpw",views.resetpw),
    path('logout',views.logout)
]