from django.urls import path

from . import views

urlpatterns = [
    path("", views.homePageView, name="homePage"),
    path("thread", views.threadView, name="thread"),
    path("login", views.loginView, name="login"),
    path("loginHandle", views.handleLogin, name="loginHandle")
]