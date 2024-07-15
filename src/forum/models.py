from django.db import models

# Create your models here.

class ForumUser(models.Model):
    username = models.TextField()
    password = models.TextField()

class Thread(models.Model):
    title = models.TextField()
    msg = models.TextField()
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message = models.TextField()
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)