from rest_framework.permissions import BasePermission
from people.models import Customer, Moderator


# This class allows only the customer who created the task to edit or delete
class TasksPermission(BasePermission):
    def has_permission(self,request,view):
        user = request.user
        if Customer.objects.filter(user=user).exists():
            return True
        elif request.method == 'GET':
            return True
        return False
        
# This class allows only the moderator to edit the work/comment they submitted
class CompletedTasksPermission(BasePermission):
    def has_permission(self,request,view):
        user = request.user
        if Moderator.objects.filter(user=user).exists():
            return True
        elif request.method == 'GET':
            return True
        return False