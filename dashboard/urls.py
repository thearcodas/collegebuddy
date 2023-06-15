from django.contrib import admin
from django.urls import path,re_path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('profile', views.profile,name='profile'),
    path('profile/<str:id>',views.viewprofile,name='viewprofile'),
    path('schedules', views.schedules,name='schedules'),
    path('announcement', views.announcement,name='announcement'),
    path('courses', views.courses,name='courses'),
    path('course/<str:code>', views.coursedetails,name='coursedetails'),
    path('<str:code>/<str:material>', views.addmaterial,name='addmaterial'),
    path('login', views.loginUser,name='login'),
    path('logout', views.logoutUser,name='logout'),
    
    path("changepassword/", auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name="reset_password"),
    path("changepassword_sent/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("changepassword/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("changepassword_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)