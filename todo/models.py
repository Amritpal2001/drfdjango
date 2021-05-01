from django.db import models
from django.contrib.auth.models import User
from people.models import Moderator,Customer
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100, default='Task')
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    deadline_time = models.DateTimeField(null=True, blank=True)
    customer  = models.ForeignKey(Customer, on_delete=models.CASCADE)
    moderator  = models.ForeignKey(Moderator, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class CompletedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description_by_moderator = models.TextField(null=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    moderator  = models.ForeignKey(Moderator, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.task.title

