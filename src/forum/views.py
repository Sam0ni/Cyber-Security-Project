from django.shortcuts import render, redirect
from .models import ForumUser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handleLogin(request):
    requser = request.POST.get("username")
    reqpass = request.POST.get("password")
    try:
        user = ForumUser.objects.get(username=requser)
    except:
        user = None
    if user:
        if user.password == reqpass:
            request.session["username"] = requser
            request.session["password"] = reqpass
    else:
        new_user = ForumUser.objects.create(username=requser, password=reqpass)
        request.session["username"] = requser
        request.session["password"] = reqpass
    return redirect(homePageView)

def homePageView(request):
    try:
        if request.session["username"]:
            return render(request, "homePage.html", {"username": request.session["username"]})
    except:
        return render(request, "homePage.html")

def threadView(request):
    return render(request, "thread.html")

def loginView(request):
    return render(request, "login.html")