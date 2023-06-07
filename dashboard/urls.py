from django.contrib import admin
from django.urls import path,re_path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('profile', views.profile,name='profile'),
    path('profile/<str:id>',views.viewprofile,name='viewprofile'),
    path('changepassword',views.change_password,name='changepassword'),
    path('schedules', views.schedules,name='schedules'),
    path('announcement', views.announcement,name='announcement'),
    path('courses', views.courses,name='courses'),
    path('course/<str:code>', views.coursedetails,name='coursedetails'),
    path('login', views.loginUser,name='login'),
    path('logout', views.logoutUser,name='logout')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)