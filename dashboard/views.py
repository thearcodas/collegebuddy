from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from dashboard.models import *
import folium
from folium import plugins

import os
from langchain.agents import *
from langchain import SQLDatabase,SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
# Create your views here
@login_required(login_url="login")
def dashboard(request):
    os.environ['OPENAI_API_KEY'] = "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"
    db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
    llm = ChatOpenAI(temperature=0.9,model_name='gpt-3.5-turbo')
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True,memory= memory)
    response=""
    if request.method == "POST":
        question=request.POST.get('userInput')
        response= db_chain.run(question)
        return HttpResponse(response)

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
