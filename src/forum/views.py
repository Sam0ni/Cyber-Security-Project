from django.shortcuts import render, redirect
from .models import ForumUser, Thread, Message
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


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

@csrf_exempt
def handleCreate(request):
    title = request.POST.get("title")
    msg = request.POST.get("msg")
    query = f"INSERT INTO forum_thread (title, msg) VALUES ('{title}', '{msg}')"
    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect(homePageView)

@csrf_exempt
def handleMsg(request):
    id = request.POST.get("id")
    msg = request.POST.get("message")
    thread = Thread.objects.get(id=id)
    Message.objects.create(message=msg, thread=thread)
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
    return render(request, "thread.html", {"id": thread.id, "title": thread.title, "msg": thread.msg, "messages": messages})

def loginView(request):
    return render(request, "login.html")

def createView(request):
    return render(request, "newThread.html")