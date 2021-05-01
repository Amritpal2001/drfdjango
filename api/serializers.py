from rest_framework import serializers
from todo.models import Task, CompletedTask
from people.models import Customer, Moderator
from django.contrib.auth.models import User

# Necessary Serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=('id','title', 'description', 'deadline_time', 'moderator')

class CompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompletedTask
        fields= ('task', 'description_by_moderator')

class CompletedTaskListSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    class Meta:
        model=CompletedTask
        fields= ('id','task', 'description_by_moderator', 'completed_time', 'moderator')




class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        x = Customer.objects.create(user = user)
        x.save()
        return user

class ModeratorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        x = Moderator.objects.create(user = user)
        x.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id','username', 'contact', 'email', 'bio')

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'contact', 'email', 'bio')

class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ('id','username', 'contact', 'email', 'bio')

class ModeratorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ('username', 'contact', 'email', 'bio')