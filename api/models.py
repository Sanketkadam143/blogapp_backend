from django.db import models
from django.contrib.auth.models import User

class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
