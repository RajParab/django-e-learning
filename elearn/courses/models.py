from django.db import models
from django.contrib.auth.models import User

#Ordering for a specific integer value
from .fields import OrderField

"""THis model consists of a proper elearning software. The layear are arranged as follows-
Subject- The subject 
	Courses - A course related t the subject
		Module- a module for a selected course for a specific subject
			course video content will be uploade inside of the module
			Content - Any type of content whether video, image, text, or file can be added for
						a specific module
"""

#For uploading the content to a specific module
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Subject(models.Model):
	title=models.CharField(max_length=250)
	slug=models.SlugField(max_length=250,unique=True)

	class Meta:
		ordering=['title']

	def __str__(self):
		return self.title


class Course(models.Model):
	user=models.ForeignKey(User, related_name='courses_created',on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
	title=models.CharField(max_length=250)
	slug=models.SlugField(max_length=250,unique=True)
	description=models.TextField(blank=True)
	created_on=models.DateTimeField(auto_now_add=True)
	updated_on=models.DateTimeField(auto_now=True)


	class Meta:
		ordering=['title','user','subject']

	def __str__(self):
		return self.title


class Module(models.Model):
	course=models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
	order=OrderField(blank=True,for_fields=['courses'])
	title=models.CharField(max_length=250)
	description=models.TextField(blank=True)


	class Meta:
		ordering=['order']

	def __str__(self):
		return '%s %s'  %(self.order,self.title)


#model for every type of content
class Content(models.Model):
	module=models.ForeignKey(Module,related_name='modules',on_delete=models.CASCADE,
		                                    limit_choices_to={'model__in':('text','file','image','video')})
	order=OrderField(blank=True,for_fields=['module'])
	content_type= models.ForeignKey(ContentType,related_name='content_type', on_delete=models.CASCADE)
	object_id=models.PositiveIntegerField()
	items=GenericForeignKey('content_type','object_id')

	class Meta:
		ordering=['order']

	def __str__(self):
		return '%s %s'  %(self.order,self.title)


""""Content models -
	There are three typres of content model - Absract models, Multi- Table models, Proxy models

Here is a example of Abstract models"""


class ItemBase(models.Model):
	owner= models.ForeignKey(User, related_name='%(class)s_related',on_delete=models.CASCADE)
	title=models.CharField(max_length=250)
	created_on=models.DateTimeField(auto_now_add=True)
	updated_on=models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True

	def __str__(self):
		return self.title

class TextItem(ItemBase):
	text=models.TextField()

class FileItem(ItemBase):
	file=models.FileField(upload_to='files')

class ImageItem(ItemBase):
	image=models.FileField(upload_to='images')

class VideoItem(ItemBase):
	url=models.URLField()