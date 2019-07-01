"""Serialzers- For building a REST api, serializer decides on how the data 
is transfered"""

from rest_framework import serializers

#Serializer for subject
from ..models import Subject

class SubjectSerializer(serializers.ModelSerializer):

	class Meta:
		model=Subject
		fields =['id', 'title', 'slug']

#Serializer for Courses
from ..models import Course

#Serializer for Module
from ..models import Module

class ModuleSerializer(serializers.ModelSerializer):
	class Meta:
		model=Module
		fields=['order','title','description']

class CourseSerializer(serializers.ModelSerializer):
	modules=ModuleSerializer(many=True, read_only=True)
	#For many modules which cannot be edited

	class Meta:
		model=Course
		fields=['id','subject','title','slug','description',
				'created_on', 'owner', 'modules']

#Serializer for Content
from ..models import Content
class ItemRelatedField(serializers.RelatedField):
	def to_representation(self, value):
		return value.render()

class ContentSerializer(serializers.ModelSerializer):
	item = ItemRelatedField(read_only=True)
	class Meta:
		model = Content
		fields = ['order', 'item']

#alternate serailizer
class ModuleWithContentsSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)	
	class Meta:
		model = Module
		fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
	modules = ModuleWithContentsSerializer(many=True)
	class Meta:
		model = Course
		fields = ['id', 'subject', 'title', 'slug',
					'description', 'created_on', 'owner', 'modules']