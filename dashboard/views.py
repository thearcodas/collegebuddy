from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from dashboard.models import *
import folium
from folium import plugins
from ipywidgets import *
import os
import openai

# Create your views here
@login_required(login_url="login")
def dashboard(request):
    return render(request,'dashboard.html')

def loginUser(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return redirect("/login")
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

@login_required(login_url="login")
def profile(request):
    # Get the current user's profile based on their authentication status
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        print(request.user)
        profile = Student.objects.get(roll_no=request.user)
        is_student = True
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        profile = Professor.objects.get(professor_id=request.user)
        is_student = False
    elif request.user.is_authenticated:
       return HttpResponse("admin dont have profiles")
    else:
        return redirect('login')

    # Display the current profile information
    context = {
        'profile': profile,
        'is_student': is_student,
    }

    if request.method == 'POST':
        # Update the profile if the form has been submitted
        if is_student:
            profile.name = request.POST['name']
            profile.phone_number = request.POST['phone_number']
            profile.facebook_link = request.POST['facebook_link']
            profile.instagram_link = request.POST['instagram_link']
            profile.bio = request.POST['bio']
            
            profile.save()
        else:
            profile.name = request.POST['name']
            profile.phone_number = request.POST['phone_number']
            profile.highest_qualification = request.POST['highest_qualification']
            
            profile.save()

    return render(request, 'profile.html', context)
    
@login_required(login_url="login")
def schedules(request):
    return render(request,'schedules.html')

@login_required(login_url="login")
def announcement(request):
    #Authentication_Status
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = Student.objects.get(roll_no=request.user)
        announcements = Announcement.objects.filter(department=student.stream.department) 
        is_student = True
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        professor = Professor.objects.get(professor_id=request.user)
        announcements = Announcement.objects.filter(department=professor.department) 
        is_student = False
    elif request.user.is_authenticated:
       announcements = Announcement.objects.all
       is_student = False
    else:
        return redirect('login')
    
     # Display the current profile information
    context = {
        'announcements': announcements,
        'is_student': is_student,
    }
    
    if not is_student:
        if request.method == 'POST':
            new_announcement= Announcement.objects.create(department=professor.department,id=request.POST['a_id'],announcement_title=request.POST['a_title'],announcement_body=request.POST['a_body'])
            new_announcement.save()  
            
    return render(request,'announcements.html',context)

@login_required(login_url="login")
def map(request):
    maplocation = (22.58834117253593, 88.37003485253165)
    m = folium.Map(location = maplocation, width = "100%", zoom_start = 17) # max zoom: 18
    hauseOutline = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"coordinates":[[88.36925418969236,22.587214788302376],[88.3694517376025,22.58715159576029],[88.36938708014992,22.58697604029122],[88.36918509095563,22.587038580038893],[88.36925495581363,22.587214076966532]],"type":"LineString"}}]}
    folium.GeoJson(hauseOutline, name="1").add_to(m)
    folium.plugins.AntPath([[22.58826749694964, 88.36978025176631],
    [22.58829906393933, 88.3696687635312],
    [22.588552972074922, 88.36978173827646],
    [22.58833474836929, 88.37041350489221],
    [22.588230440053565, 88.37037188261735],
    [22.58818652073957, 88.37052499312733],
    [22.588380040113222, 88.37061121069615],
    [22.58868472969833, 88.36970889832872],
    [22.588307298210268, 88.36957065371098],
    [22.588065741899328, 88.36948481064627],
    [22.58717912238926, 88.36916089413626],
    [22.587157162565873, 88.36923521962592]]).add_to(m)
    context={
        'map' : m._repr_html_ 
    }
    return render(request,'map.html',context)

@login_required
def courses(request):
     #Authentication_Status
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = Student.objects.get(roll_no=request.user)
        courses = Course.objects.filter(enrolled_students__in=[student])
        is_student = True
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        professor = Professor.objects.get(professor_id=request.user)
        courses = Course.objects.filter(instructors__in=[professor]) 
        is_student = False
    elif request.user.is_authenticated:
       courses = Course.objects.all
       is_student = False
    else:
        return redirect('login')
    
    context = {
        'courses': courses,
    } 
    return render(request,'courses.html',context)

def coursedetails(request,code):
    course= Course.objects.get(course_id=code)
    professors=Professor.objects.filter(courses_taught=course)
    students=Student.objects.filter(enrolled_courses=course)
    is_student=request.user.groups.filter(name='Student').exists()
    context={
        'course' : course,
        'professors' : professors,
        'students' : students,
        'is_student': is_student
    }
    return render(request,'coursedetails.html',context)
