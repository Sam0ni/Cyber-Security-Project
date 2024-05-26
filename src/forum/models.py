from django.db import models

# Create your models here.

class Thread(models.Model):
    title = models.TextField()
    msg = models.TextField()

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message = models.TextField()

class ForumUser(models.Model):
    username = models.TextField()
    password = models.TextField()