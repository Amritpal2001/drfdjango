from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from todo.models import Task, CompletedTask
from django.contrib.auth.models import User
from people.models import Moderator, Customer
from .serializers import TaskSerializer, CompletedTaskSerializer, CompletedTaskListSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .permissions import TasksPermission, CompletedTasksPermission

import datetime
from rest_framework import generics

from .serializers import CustomerCreateSerializer, ModeratorCreateSerializer
from .serializers import CustomerSerializer, CustomerUpdateSerializer, ModeratorSerializer, ModeratorUpdateSerializer

from electura.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError


# This class handles Pending Tasks for both moderators and Customers
class TasksAPI(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated & TasksPermission]
    # this function overrides get method to handle tasks for both moderator and customer
    def get_queryset(self):
        user = self.request.user
        if Moderator.objects.filter(user = user).exists():
            moderator = Moderator.objects.filter(user = user).first()
            return Task.objects.filter(moderator=moderator, is_completed=False)
        else:
            customer = Customer.objects.filter(user = user).first()
            return Task.objects.filter(customer=customer,  is_completed=False)

     # this function overrides create method as it needs to send email
    def perform_create(self, serializer):
        user = self.request.user
        customer = Customer.objects.filter(user = user).first()
        serializer.save(customer=customer)
        moderator = serializer.data['moderator']
        to_email = Moderator.objects.get(id = moderator).email
        msg = EmailMultiAlternatives("New Task", "New Task Created. Checkout!", from_email=EMAIL_HOST_USER, to=[to_email])
        msg.send()


#  This class handles Completed Tasks for both moderators and Customers
class CompletedTasksAPI(viewsets.ModelViewSet):
    queryset = CompletedTask.objects.all()
    serializer_class = CompletedTaskSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated & CompletedTasksPermission]
    def list(self, request):
        user = self.request.user
        if Moderator.objects.filter(user = user).exists():
            moderator = Moderator.objects.filter(user = user).first()
            data = CompletedTask.objects.filter(moderator=moderator)
            serializer  = CompletedTaskListSerializer(data,many=True)
            return Response(serializer.data)
        else:
            customer = Customer.objects.filter(user = user).first()
            tasks = Task.objects.filter(customer=customer)
            data = CompletedTask.objects.filter(task__in = tasks.all())
            serializer  = CompletedTaskListSerializer(data, many=True)
            return Response(serializer.data)

         # this function overrides create method as it needs to send email  and other validations 
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        moderator = Moderator.objects.filter(user = user).first()
        task = serializer.validated_data['task']
        task = Task.objects.filter(title=task).first()
        if task.moderator != moderator or task.is_completed == True:
            return Response({'Message': 'Task was not assigned to you or it was already done'})
        serializer.save(moderator = moderator, completed_time = datetime.datetime.now())
        task = serializer.data['task']
        Task.objects.filter(id=task).update(is_completed = 'True')
        customer = Task.objects.filter(id = task).first().customer.id
        to_email = Customer.objects.get(id = customer).email
        msg = EmailMultiAlternatives("Task Completed", "Your Task has been completed. Checkout!", from_email=EMAIL_HOST_USER, to=[to_email])
        msg.send()
        return Response({'Message': 'Marked done successfully'})




# This class handles for creating new customers
class CustomerCreateAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerCreateSerializer
    permission_classes = (AllowAny, )

# This class handles for creating new moderators
class ModeratorCreateAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ModeratorCreateSerializer
    permission_classes = (AllowAny, )


# This class handles list of all customers
class CustomersAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

# This class handles customers profiles updates
class CustomersUpdateAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        user = request.user
        customer = Customer.objects.get(user=user)
        serializer = CustomerUpdateSerializer(customer)
        return Response(serializer.data)

    def patch(self, request, pk=None, format=None):
        user = request.user
        customer = Customer.objects.get(user=user)
        serializer = CustomerUpdateSerializer(customer, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "User Updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This class handles list of all moderators

class ModeratorsAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            moderator = Moderator.objects.get(id=id)
            serializer = ModeratorSerializer(moderator)
            return Response(serializer.data)
        moderators = Moderator.objects.all()
        serializer = ModeratorSerializer(moderators, many=True)
        return Response(serializer.data)


# This class handles moderators profiles updates
class ModeratorsUpdateAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        user = request.user
        moderator = Moderator.objects.get(user=user)
        serializer = ModeratorUpdateSerializer(moderator)
        return Response(serializer.data)

    def patch(self, request, pk=None, format=None):
        user = request.user
        moderator = Moderator.objects.get(user=user)
        serializer = ModeratorUpdateSerializer(moderator, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "User Updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)