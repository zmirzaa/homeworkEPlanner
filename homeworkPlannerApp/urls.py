from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.login), 
    path('register', views.register),
    path('dashboard', views.dashboard), 
    path('addTask', views.addTask), 
    path('add', views.add), 
    path('delete/<int:id>', views.delete, name="delete"),
    path('assignments/<int:id>', views.viewClass), 
    path('logout', views.logout)
]