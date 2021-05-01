from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,  null=True)
    contact = models.CharField(max_length=20, null=True)
    email = models.EmailField( null=True)
    bio = models.TextField(null=True)
    def __str__(self):
        return "Moderator : " + self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,  null=True)
    contact = models.CharField(max_length=20, null=True)
    email = models.EmailField( null=True)
    bio = models.TextField(null=True)
    def __str__(self):
        return "Customer : " + self.user.username


