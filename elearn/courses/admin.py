from django.contrib import admin
from .models import Course, Module, Subject


"""After creating models we need to the admin view here, for every model"""

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display=['title','slug']
	prepopulated_fields={'slug':('title',)}

class ModuleAdmin(admin.StackedInline):
	model=Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display=['title','user','subject','created_on','updated_on']
	list_filter=['title','user','subject','created_on']
	prepopulated_fields={'slug':('title',)}
	search_fields=['title','user']
	inlines=[ModuleAdmin]