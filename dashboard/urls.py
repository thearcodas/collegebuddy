from django.contrib import admin
from django.urls import path
from dashboard import views
urlpatterns = [
    path('', views.dashboard,name='home'),
    path('profile', views.profile,name='profile'),
    path('schedules', views.schedules,name='schedules'),
    path('notifications', views.notifications,name='notifications'),
    path('map', views.map,name='map'),
    path('courses', views.courses,name='courses')

]
