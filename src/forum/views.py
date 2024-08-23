from django.shortcuts import render, redirect
from .models import ForumUser, Thread, Message
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
#from django.contrib.auth.models import User

#remove @csrf_exempt to fix csrf vulnerability
@csrf_exempt
def handleLogin(request):
    requser = request.POST.get("username")
    reqpass = request.POST.get("password")
    try:
        user = ForumUser.objects.get(username=requser)
        # user = User.objects.get(username=requser)
    except:
        user = None
    if user:
        if user.password == reqpass:
            request.session["username"] = requser
            request.session["password"] = reqpass
            #delete previous line
    else:
        new_user = ForumUser.objects.create(username=requser, password=reqpass)
        #new_user = User.objects.create_user(username=requser, password=reqpass)
        request.session["username"] = requser
        request.session["password"] = reqpass
        #delete previous line to not store password in session
    return redirect(homePageView)
#replace ForumUser model with django inbuilt User model, which hashes the passwords

#remove @csrf_exempt to fix csrf vulnerability
@csrf_exempt
def handleCreate(request):
    title = request.POST.get("title")
    msg = request.POST.get("msg")
    try:
        if request.session["username"]:
            user = request.session["username"]
            user = ForumUser.objects.get(username=user)
            #user = User.objects.get(username=user)
    except:
        return redirect(homePageView)
    #replace the following 3 lines with "Thread.objects.create(title=title, msg=msg, user=user)" to fix sql injection vulnerability
    query = f"INSERT INTO forum_thread (title, user_id, msg) VALUES ('{title}', '{user.id}', '{msg}')"
    with connection.cursor() as cursor:
        cursor.executescript(query)
    return redirect(homePageView)

#remove @csrf_exempt to fix csrf vulnerability
@csrf_exempt
def handleMsg(request):
    id = request.POST.get("id")
    msg = request.POST.get("message")
    try:
        if request.session["username"]:
            user = request.session["username"]
            user = ForumUser.objects.get(username=user)
            #user = User.objects.get(username=user)
    except:
        return redirect(homePageView)
    thread = Thread.objects.get(id=id)
    Message.objects.create(message=msg, thread=thread, user=user)
    return redirect(homePageView)


def homePageView(request):
    try:
        if request.session["username"]:
            user = request.session["username"]
    except:
        user = None
    threads = Thread.objects.all()
    all_threads = [(thread.id, thread.title) for thread in threads]
    return render(request, "homePage.html", {"threads": all_threads, "username": user})

def threadView(request, id):
    thread = Thread.objects.get(id=id)
    allmessages = Message.objects.filter(thread=thread)
    messages = [(message.id, message.message) for message in allmessages]
    try:
        if request.session["username"]:
            user = request.session["username"]
    except:
        user = None
    return render(request, "thread.html", {"id": thread.id, "title": thread.title, "msg": thread.msg, "messages": messages, "op": thread.user.username, "user": user})

def loginView(request):
    return render(request, "login.html")

def createView(request):
    return render(request, "newThread.html")

def logoutHandle(request):
    del request.session["username"]
    del request.session["password"]
    return redirect(homePageView)

def threadDeletionHandle(request, id):
    #thread = Thread.objects.get(id=id)
    #if thread.user.username = request.session["username"]:
    #assuming the usernames are unique
    Thread.objects.filter(id=id).delete()
    return redirect(homePageView)