from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit/<ID>', views.edit),
    path('update', views.update),
    path('remove/<ID>', views.remove),
    path('grante/<ID>', views.Granted),
    path('like/<ID>', views.like),
    path('wishes', views.wishes),
    path('addWish', views.addWish),
    path('create', views.create),
    path('view', views.view),
]
