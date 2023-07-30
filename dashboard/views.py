from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from django.db.models import Count,Sum

# Create your views here
@login_required(login_url="login")
def dashboard(request):
    is_admin=False
    is_prof=False
    is_student=False
    attendance=""
    name=""
    profile=""
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        is_student=True
        profile = Student.objects.get(roll_no=request.user)
        name=profile.name
        at=Attendance.objects.filter(student=profile).aggregate(Sum('weightage'))
        tat=Attendance.objects.filter(student=profile).aggregate(Sum('total_weightage'))
        attendance=(at['weightage__sum']/tat['total_weightage__sum'])*100
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        is_prof=True
        profile = Professor.objects.get(professor_id=request.user)
        name= profile.name
    else:
       is_admin=True
       name='Admin'
    context={   
            'profile':profile,
            'name':name,
            'isadmin':is_admin,
            'is_student':is_student,
            'is_prof': is_prof,
            'attendance': attendance
             }
    return render(request,'dashboard.html',context)

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
            messages.info(request, 'Invalid Id or Password!')
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
    is_admin=False
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
       is_admin=True
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
            if is_admin:
                new_announcement= Announcement.objects.create(department=Department.objects.get(name="Admin"),id=request.POST['a_id'],announcement_title=request.POST['a_title'],announcement_body=request.POST['a_body'])
                new_announcement.save()  
            else:
                new_announcement= Announcement.objects.create(department=professor.department,id=request.POST['a_id'],announcement_title=request.POST['a_title'],announcement_body=request.POST['a_body'])
                new_announcement.save()  
            
    return render(request,'announcements.html',context)

def encyclopedia(request):
    profile=display=is_student=""
    msg="Search for any student/professor"
    context = {
        'profile': profile,
        'display': display,
        'is_student': is_student,
        'message': msg,
    }
    return render(request,'viewprofile.html',context)

def viewprofile(request,id):
    #fetch the profiles
    profile=display=is_student=""
    if request.method == "POST":
        id1=request.POST.get('id')
        return redirect(viewprofile,id=id1)
    try:
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
    except:
        msg="No User with this ID/roll"
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
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        professor = Professor.objects.get(professor_id=request.user)
        courses = Course.objects.filter(instructors__in=[professor]) 
    elif request.user.is_authenticated:
       courses = Course.objects.all
    else:
        return redirect('login')
    
    context = {
        'courses': courses,
    } 
    return render(request,'courses.html',context)

@login_required(login_url="login")
def coursedetails(request,code):
    course= Course.objects.get(course_id=code)
    professors= Professor.objects.filter(courses_taught=course)
    students= Student.objects.filter(enrolled_courses=course)
    materials= StudyMaterial.objects.filter(course=course)
    questions= PYQ.objects.filter(course=course)
    is_professor= request.user.groups.filter(name='Professor').exists()
    is_student= request.user.groups.filter(name='Student').exists()
        
    if request.method == "POST":
        id=request.POST.get('id')
        msg= request.POST.get('message')
        
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
        'is_professor': is_professor,
        'is_student' : is_student,
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

@login_required(login_url="login")
def attendance(request,code):
    attendance=message=""
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = Student.objects.get(roll_no=request.user)
        attendance= Attendance.objects.filter(course= Course.objects.get(course_id=code),student=student)
        is_student=True
    else:
        message='You guys dont have attendance!'
        is_student=False
    
    context={
        'code' :    code,
        'is_student' : is_student,
        'attendances': attendance,
        'message': message
    }
    return render(request,'attendance.html',context)

@login_required(login_url="login")
def updateattendance(request,code):
    is_student=False
    course= Course.objects.get(course_id=code)
    students = Student.objects.filter(enrolled_courses__in=[course])
    message=""
    attendance=[]
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        is_student=True
        message='You dont have permission to be here!'
    
    if request.method=='POST':
        date= request.POST['date']
        total_weightage=request.POST['total']
        for student in students:
            id=f'weight{student.roll_no}'
            weightage=request.POST[id]
            attendance.append(Attendance(date=date,course=course,student=student,weightage=weightage,total_weightage=total_weightage))
        instance=Attendance.objects.bulk_create(attendance)
        
    context={
        'is_student' : is_student,
        'students': students,
        'message': message
    }
    return render(request,'updateattendance.html',context)
    
@login_required(login_url="login")
def attendancedetails(request):
    attendances={}
    tat=at={}
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        
        profile = Student.objects.get(roll_no=request.user)
        courses= profile.enrolled_courses
        for course in courses.all():
            name= course.course_id+'-'+course.name
            at=Attendance.objects.filter(student=profile,course=course).aggregate(Sum('weightage'))
            tat=Attendance.objects.filter(student=profile,course=course).aggregate(Sum('total_weightage'))
            try:
                attendances[name]=(at['weightage__sum']/tat['total_weightage__sum'])*100
            except:
                attendances[name]=0
    elif request.user.is_authenticated and request.user.groups.filter(name='Professor').exists():
        
        profile = Professor.objects.get(professor_id=request.user)
        courses= profile.courses_taught
        for course in courses.all():
            name= course.course_id+'-'+course.name
            at=Attendance.objects.filter(course=course).aggregate(Sum('weightage'))
            tat=Attendance.objects.filter(course=course).aggregate(Sum('total_weightage'))
            try:
                attendances[name]=(at['weightage__sum']/tat['total_weightage__sum'])*100
            except:
                attendances[name]=0
    context={
        
        'attendances': attendances,
    }
    return render(request,'attendancedetails.html',context)