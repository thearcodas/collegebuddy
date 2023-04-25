from django.contrib import admin
from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard,name='home'),
    path('profile', views.profile,name='profile'),
    path('schedules', views.schedules,name='schedules'),
    path('announcement', views.announcement,name='announcement'),
    path('map', views.map,name='map'),
    path('courses', views.courses,name='courses'),
    path('login', views.loginUser,name='login'),
    path('logout', views.logoutUser,name='logout')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
