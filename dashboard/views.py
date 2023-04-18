from django.shortcuts import render,HttpResponse

# Create your views here
def dashboard(request):
    return render(request,'dashboard.html')

def profile(request):
    return render(request,'profile.html')

def schedules(request):
    return render(request,'schedules.html')

def notifications(request):
    return render(request,'notifications.html')

def map(request):
    return render(request,'map.html')

def courses(request):
    return render(request,'courses.html')