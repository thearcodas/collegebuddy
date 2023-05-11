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
    list_display = ('name', 'hod')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id','description')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('department', 'announcement_title')

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('student', 'professor', 'course', 'query')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'present')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'full_marks')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department')

@admin.register(Maps)
class MapAdmin(admin.ModelAdmin):
    list_display=('name','location')