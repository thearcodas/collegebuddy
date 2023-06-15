from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *


import os
from langchain.agents import *
from langchain import LLMChain, SQLDatabase,SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# Create your views here
@login_required(login_url="login")
def dashboard(request):
    os.environ['OPENAI_API_KEY'] = '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'
    db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
    llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True,memory=memory)
    
    if request.method == "POST":
        question=request.POST.get('userInput')
        try:
            response= db_chain.run(question)
        except Exception as e:
            response= e
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
    is_admin=False
    profile=''
    is_student = False
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        profile = Student.objects.get(roll_no=request.user)
        is_student = True
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        profile = Professor.objects.get(professor_id=request.user)
        is_student = False
    elif request.user.is_authenticated:
       is_admin=True
    else:
        return redirect('login')

    # Display the current profile information
    context = {
        'profile': profile,
        'is_admin': is_admin,
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
    is_admin=False
    schedule=''
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        profile = Student.objects.get(roll_no=request.user)
        semester=profile.semester
        schedule= Schedule.objects.get(stream=profile.stream,name= f'semester {semester}')
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        profile = Professor.objects.get(professor_id=request.user)
        schedule = Schedule.objects.filter(name= profile.name)
    else:
       is_admin=True
    
    context={
        'schedule': schedule,
        'is_admin': is_admin
    }
    return render(request,'schedules.html',context)

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

def viewprofile(request,id):
    #fetch the profiles
    user=User.objects.get(username=id)
    if Student.objects.filter(roll_no=user).exists():
        profile = Student.objects.get(roll_no=user)
        is_student=True
        display=True
        msg="Showing student's profile with roll "+id
    elif Professor.objects.filter(professor_id=user).exists():
        profile = Professor.objects.get(professor_id=user)
        is_student = False
        display=True
        msg="Showing professor's profile with Id "+id
    else:
        display=False
        msg='No profiles are present with this Id'

    # Display the current profile information
    context = {
        'profile': profile,
        'display': display,
        'is_student': is_student,
        'message': msg,
    }
    return render(request,'viewprofile.html',context)

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

@login_required(login_url="login")
def coursedetails(request,code):
    course= Course.objects.get(course_id=code)
    professors=Professor.objects.filter(courses_taught=course)
    students=Student.objects.filter(enrolled_courses=course)
    materials=StudyMaterial.objects.filter(course=course)
    questions=PYQ.objects.filter(course=course)
    is_student=request.user.groups.filter(name='Student').exists()
    
    if request.method == "POST":
        id=request.POST.get('id')
        msg= request.POST.get('message')
        print(id)
        print(msg)
        
        if 'material' in msg:
            material= StudyMaterial.objects.get(pk=int(id))
            material.delete()
        else:
            question= PYQ.objects.get(pk=int(id))
            question.delete()
    
    context={
        'course' : course,
        'professors' : professors,
        'students' : students,
        'materials' : materials,
        'questions' : questions,
        'is_student': is_student
    }
    return render(request,'coursedetails.html',context)

@login_required(login_url="login")
def addmaterial(request,code,material):
    is_student=False
    
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        is_student=True
    if request.method == 'POST':
        form = MaterialForm(request.POST,request.FILES)
        title=request.POST['title']
        file=request.FILES['fileupload']
        desc=request.POST['desc']
        print(file.name)
        course= Course.objects.get(course_id=code)
        if (material=='question'):
            instance = PYQ.objects.create(title=title,file=file,course=course,description=desc)
            instance.save()
        elif(material=='material'):
            instance = StudyMaterial.objects.create(title=title,file=file,course=course,description=desc)
            instance.save()
    else:
        form= MaterialForm()
    context={
        'form' : form,
        'is_student' : is_student,
        'material': material,
        'code' : code
    }
    return render(request,'addmaterial.html',context)

    