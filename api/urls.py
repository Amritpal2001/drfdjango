from django.urls import path,include
from .views import TasksAPI, CompletedTasksAPI, CustomerCreateAPI , ModeratorCreateAPI, CustomersAPI, CustomersUpdateAPI,ModeratorsAPI, ModeratorsUpdateAPI
from rest_framework.routers import DefaultRouter

routers=DefaultRouter()
routers.register('todo',TasksAPI,basename='todo')
routers.register('completed',CompletedTasksAPI,basename='completed')


urlpatterns = [
    path('customers/',CustomersAPI.as_view() ),
    path('customers/<int:pk>',CustomersAPI.as_view() ),
    path('updatecustomer/',CustomersUpdateAPI.as_view() ),

    path('moderators/',ModeratorsAPI.as_view() ),
    path('moderators/<int:pk>',ModeratorsAPI.as_view() ),
    path('updatemoderators/',ModeratorsUpdateAPI.as_view() ),

    path('',include(routers.urls)),
    # path('createcustomers/', CreateCustomersAPI.as_view()),
    path('register_customer', CustomerCreateAPI.as_view()),
    path('register_moderator', ModeratorCreateAPI.as_view()),
]