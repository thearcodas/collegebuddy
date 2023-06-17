from django.contrib import admin
from dashboard.models import *

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'semester', 'stream',  'phone_no')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'professor_id', 'phone_no', 'highest_qualification')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id','description')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('department', 'announcement_title')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'weightage')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department')

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'description','file')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('stream', 'name','image')
    
@admin.register(PYQ)
class PYQAdmin(admin.ModelAdmin):
    list_display = ('course', 'title','file')