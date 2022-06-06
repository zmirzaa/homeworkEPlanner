from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class UserManager(models.Manager): 
    def validate(self, form): 
        errors = {}

        emailCheck =self.filter(email=form['email']) 
        if emailCheck: 
            errors['email'] = 'Email has been taken.'

        if not EMAIL_REGEX.match(form['email']): 
            errors['email'] = 'Please use valid email format.'
        
        if len(form['name']) < 1: 
            errors['name'] = 'Please provide name.'
        
        if len(form['password']) < 8: 
            errors['password'] = 'Password must be atleast 8 characters.'
        
        if form['password'] != form['confirm']: 
            errors['password'] = 'Passwords do not match.'

        return errors 


class ClassManager(models.Manager): 
    def validateClass(self, classData): 
        errors = {} 
        if len(classData['subject']) < 1: 
            errors['subject'] = "Please provide subject."
        if len(classData['day']) < 1: 
            errors['day'] = "Please provide the days you have class."
        return errors 



class HomeworkManager(models.Manager): 
    def validateWork(self, homeworkData): 
        errors = {} 
        if len(homeworkData['subject']) < 1: 
            errors['subject'] = "Please provide subject."
        if len(homeworkData['dueDate']) < 1: 
            errors['dueDate'] = "Please provide due date."
        if len(homeworkData['description']) < 1: 
            errors['subject'] = "Please provide description."
        if len(homeworkData['type']) < 1: 
            errors['type'] = "Please specify what type of action."
        return errors 




class User(models.Model): 
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    userCreatedAt = models.DateTimeField(auto_now_add=True)
    userUpdatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager() 




class Class(models.Model):  
    subject = models.CharField(max_length=255)
    day = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='userClasses', on_delete=CASCADE) 
    objects = ClassManager() 



class Homework(models.Model): 
    description = models.CharField(max_length=255)
    dueDate = models.DateField()
    type = models.CharField(max_length=255)
    subject = models.ForeignKey(Class, related_name='homeworkSubject', on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='userHomework', on_delete=CASCADE)
    objects = HomeworkManager() 

