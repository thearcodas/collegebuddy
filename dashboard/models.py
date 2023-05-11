from django.db import models
from django.contrib.auth.models import User


    
    
class Student(models.Model):
    roll_no = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=20,default='Anonymous')
    semester = models.IntegerField()
    stream= models.ForeignKey('Stream' , on_delete=models.SET_NULL, blank=True, null=True, related_name='stream')
    phone_no = models.CharField(max_length=20)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='student_profile_pics/', blank=True, null=True)
    enrolled_courses = models.ManyToManyField('Course', related_name='enrolled_students')

    def __str__(self):
        return self.name


class Professor(models.Model):
    professor_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    name = models.CharField(max_length=20, default='Anonymous')
    phone_no = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='professor_profile_pics/', blank=True, null=True)
    highest_qualification = models.CharField(max_length=50)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='professors')
    courses_taught = models.ManyToManyField('Course', related_name='instructors')

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.name

class Stream(models.Model):
    code= models.CharField(max_length=10)
    name= models.CharField(max_length=50)
    department=models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='department')
    
    def __str__(self):
        return self.name
        
class Department(models.Model):
    name = models.CharField(max_length=50)
    hod = models.OneToOneField(Professor, on_delete=models.SET_NULL, blank=True, null=True, related_name='department_head')
    def __str__(self):
        return self.name

class Announcement(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id= models.IntegerField(primary_key=True)
    announcement_title = models.CharField(max_length=100)
    announcement_body = models.TextField()
    date_published = models.DateField(auto_now_add=True)

class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='study_materials/')

    def __str__(self):
        return self.title


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_attendance')
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} - {self.course} - {self.date} - {self.present}'


class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_tests')
    date = models.DateField()
    marks = models.IntegerField()
    full_marks = models.IntegerField()
    def __str__(self):
        return f'{self.student} - {self.course} - {self.date} - {self.marks}'


class Query(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='queries')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='asked_queries')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='answered_queries')
    query = models.TextField()
    answer = models.TextField(blank=True,null=True)

class Maps(models.Model):
    name = models.TextField()
    location=models.TextField()
