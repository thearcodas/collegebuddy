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
    if request.method=='POST':
        start= request.POST['start']
        end=request.POST['end']
        hauseOutline = Maps.objects.get(name=start)
        folium.GeoJson(hauseOutline.location, name="1").add_to(m)
        hauseOutline = Maps.objects.get(name=end)
        folium.GeoJson(hauseOutline.location, name="2").add_to(m)
        #folium.plugins.AntPath([[22.58826749694964, 88.36978025176631]..
        #Ant Paths
        if(start=='Main Building' and end=='Millenium Building'):
            folium.plugins.AntPath([[22.58825741381537, 88.36977309152951],
            [22.5882901363904, 88.36965569215971],
            [22.588556007022802, 88.36978195185912],
            [22.588337175077456, 88.37041103527503],
            [22.58823287187886, 88.37037116379082],
            [22.58818992348047, 88.37052621956377],
            [22.587531379467165, 88.37032021634269],
            [22.587838154918288, 88.36940095712288],
            [22.587078442002735, 88.36912452209913],
            [22.586953686046698, 88.36906028470707],
            [22.586896420980338, 88.36923527622218]]).add_to(m)
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
