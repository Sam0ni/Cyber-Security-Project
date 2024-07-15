from django.urls import path

from . import views

urlpatterns = [
    path("", views.homePageView, name="homePage"),
    path("thread/<str:id>", views.threadView, name="thread"),
    path("login", views.loginView, name="login"),
    path("loginHandle", views.handleLogin, name="loginHandle"),
    path("create", views.createView, name="create"),
    path("createHandle", views.handleCreate, name="createHandle"),
    path("createMsg", views.handleMsg, name="createMessage"),
    path("logout", views.logoutHandle, name="logout"),
    path("deleteThread/<str:id>", views.threadDeletionHandle, name="deleteThread"),
]