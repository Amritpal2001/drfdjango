# TODO List and Notifications API in DRF(Django Rest Framework)
This is the assignment made during the assignment phase of Electura Internship

## Requirements
- Django > 3.0.0 
- djangorestframework

## Setup
Install the above requirments and run
```
python manage.py runserver
```
## For demonstration purpose I will be using the following link
http://drfdjango.pythonanywhere.com

The API Route has two links
- one for todo tasks : http://drfdjango.pythonanywhere.com/todo/
- second for completed tasks : http://drfdjango.pythonanywhere.com/completed/

## Customer example
- username = 'customer1'
- password = '1234'
* Once a user is logged in as a customer in the todo section, there is a complete list of tasks that customer has created and are pending to be completed by the assigned moderator.
* Customer can also create new Tasks by sending a POST request to the URL http://drfdjango.pythonanywhere.com/todo/ once the user is logged in.
* Customer can also change or delete the task by sending a PATCH or DELETE request at http://drfdjango.pythonanywhere.com/todo/'id_of_the_post'
* Customer can also view the completed tasks through : http://drfdjango.pythonanywhere.com/completed/  along with the comments from moderators/
* POST request Example JSON
```
{
        "id": 18,
        "title": "Task3",
        "description": "Task3 Description",
        "deadline_time": null,
        "moderator": 4
 }
```

## Moderator example
- username = 'moderator1'
- password = '1234'
* Once a user is logged in as a moderator in the todo section, there is a complete list of tasks that has been assigned to that particular moderator at http://drfdjango.pythonanywhere.com/todo/
* Moderator can also mark the tasks as completed by sending a POST request to the URL http://drfdjango.pythonanywhere.com/completed/ once the user is logged in.
* Moderator can also change or delete the comments given on a particular tasks assigned by sending PATCH or DELETE request at http://drfdjango.pythonanywhere.com/completed/'id_of_the_post'
* Moderator can also view the completed tasks by sending GET request at : http://drfdjango.pythonanywhere.com/completed/
* POST request Example JSON
```
{
    "task": 15,
    "description_by_moderator": "Task1 Completed"
 }
```

## To create New Customer User
* Send a post request to : http://drfdjango.pythonanywhere.com/register_customer with username and password
* Example 
```
{
    "username": "Amritpal",
    "password": "1234a"
}
```

## Similarly, To create New Moderator User
* Send a post request to : http://drfdjango.pythonanywhere.com/register_moderator with username and password

## To get list of customers
* Send a GET request to : http://drfdjango.pythonanywhere.com/customers/

## To get list of Moderators
* Send a GET request to : http://drfdjango.pythonanywhere.com/moderators/

## To update Moderator's Profile
* Send PATCH request to : http://drfdjango.pythonanywhere.com/updatemoderators/ after logging in as a moderator else it will give error
* Example Code 
```
{
    "username": "Moderator1",
    "contact": "123456789",
    "email": "abc@gmail.com",
    "bio": "Moderator1 Bio"
}
```

## To update Customer's Profile
* Send PATCH request to : http://drfdjango.pythonanywhere.com/updatecustomer/ after logging in as a customer else it will give error
* Example Code 
```
{
    "username": "Customer1",
    "contact": "123456789",
    "email": "abc@gmail.com",
    "bio": "Customer1 Bio"
}
```
### The Moderator will get the email once the task is assigned by the customer
### The Customer will get the email once the task is completed by the moderator

