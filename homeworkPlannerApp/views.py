from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt 


def index(request): 
    return render(request, "index.html")


def home(request): 
    return render(request, 'home.html') 


def dashboard(request): 
    if 'user_id' not in request.session:
        return redirect('/home')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'classes': Class.objects.all().values(),
        "tasks": Homework.objects.all().values() 
    }
    return render(request, 'dashboard.html', context)


def register(request): 
    if request.method == 'GET': 
        return redirect('/home')
    errors = User.objects.validate(request.POST) 
    if errors: 
        for err in errors.values(): 
            messages.error(request, err)
        return redirect('/home') 
    
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        name = request.POST['name'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/dashboard')



def login(request): 
    userEmail = User.objects.filter(email = request.POST['email'])
    if userEmail:
        userLogin = userEmail[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/dashboard')
        messages.error(request, 'Invalid email/password')
        return redirect('/home')
    messages.error(request, 'You are not in the system. Please register.')
    return redirect('/home')

# render homework add page
def addTask(request):
    if 'user_id' not in request.session:
        return redirect('/home')
    context = {
        'classes': Class.objects.all().values()
    } 
    return render (request, "task.html", context)

# add homework
def add(request): 
    if 'user_id' not in request.session:
        return redirect('/home')
    Homework.objects.create(
        description = request.POST['description'], 
        dueDate = request.POST['dueDate'], 
        type = request.POST['type'], 
        subject = Class.objects.get(id=request.POST['class_id']), 
        user = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/dashboard')

# view specific class homework 
def viewClass(request, id): 
    if 'user_id' not in request.session:
        return redirect('/home')
    context = {
        "class": Class.objects.get(id=id),
        "homework": Homework.objects.all()
    }
    return render(request, "class.html", context)



def delete(request, id): 
    Homework.objects.filter(id=id).delete()
    return redirect('/dashboard')



def logout(request): 
    request.session.clear()
    return redirect('/home')

