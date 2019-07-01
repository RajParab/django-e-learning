'''Fo the views we us the below view
 Class Based View- We build a class for each type of view but in this we cannot restrict one user from changing courses 
					 posted by some other user.

To solve this we have using mixins for a class based view

Mixixn are a special kind of multipl inheritance for a class 
There are manny types of mixins in Django '''

from django.views.generic.list import ListView # to display as a list
from django.views.generic.edit import CreateView,UpdateView,DeleteView # View To make changes to any course
from django.urls import reverse_lazy

""""To make sure that the logged in user has the permission to see the view we use the below Mixins """
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# To take tha effect we need to add the above mixins in each class as the parent class

#import the model
from .models import Course, Module, Content, Subject



#Creating a mixin class for each view 
class OwnerMixin(object):
	def get_queryset(self):
		qs = super(OwnerMixin, self).get_queryset()
		return qs.filter(owner= self.request.user)

class OwnerEditMixin(object):
	def form_valid(self, form):
		form.instance.owner=self.request.user
		return super(OwnerEditMixin, self).form_valid(form)
# abve classes are for the getting the exact owner of the course so that no one apart from him touches the file

class OwnerCourseMixin(OwnerMixin , LoginRequiredMixin):
	model=Course   #Callin the model in the picture
	fields = ['subject', 'title', 'slug', 'description']
	success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
	"""fields=['subject','title','slug','description']
	success_url=reverse_lazy('manage_course_list')"""
	template_name="manage/course/form.html"

class ManageCourseListView(OwnerCourseMixin,ListView):
	template_name="manage/course/list.html"

class CreateCourseView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
	permission_required= "courses.add_course"

class EditCourseView( PermissionRequiredMixin,OwnerCourseEditMixin,UpdateView):
	permission_required= 'courses.change_course'

class DeleteCourseView(PermissionRequiredMixin,OwnerCourseMixin,DeleteView):
	template_name="manage/course/delete.html"
	success_url=reverse_lazy("manage_course_list")
	permission_required='courses.delete_course'


""" To setup the views for the modules 
"""
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404, redirect
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps

class CreateModuleUpdateView(TemplateResponseMixin, View):
	template_name="manage/module/formset.html"
	course=None


	def get_form(self,data=None):
		return ModuleFormSet(instance=self.course,data=data)

	def dispatch(self,request,pk):
		self.course=get_object_or_404(Course,id=pk,owner=request.user)

		return super(CreateModuleUpdateView,self).dispatch(request, pk)

	def get(self,request, *args,**kwargs):
		formset=self.get_form()

		return self.render_to_response({'course':self.course,
									'formset':formset
			})

	def post(self,request,*args,**kwargs):
		formset=self.get_form(data=request.POST)

		if formset.is_valid():
			formset.save()

			return redirect('manage_course_list')
		return self.render_to_response({'course':self.course,
										'formset':formset
										})

"""Setting up views for content upload 
"""

from django.forms.models import modelform_factory
from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps
from .models import Content,Module

class CreateContentUpdateView(TemplateResponseMixin,View):
	module=None
	model=None
	obj=None
	template_name="manage/content/form.html"


	def get_model(self,model_name):
		if model_name in ['text','video','image','file']:
			return apps.get_model(app_label='courses',model_name=model_name)
		return None

	def get_form(self, model, *args, **kwargs):
		Form =modelform_factory(model,exclude=['owner','order','created_on',
											'updated_on'])
		return Form(*args,**kwargs)

	def dispatch(self,request,module_id,model_name,id=None):
		self.module=get_object_or_404(Module,id=module_id,
									course__owner=request.user)

		self.model=self.get_model(model_name)

		if id:
			self.obj=get_object_or_404(self.model,
								id=id, owner=request.user)

		return super(CreateContentUpdateView, self).dispatch(request,module_id,model_name,id)

	def get(self,request,model_name,module_id, id=None):
		form=self.get_form(self.model, instance=self.obj)
		return self.render_to_response({'form':form,
									'object':self.obj})

	def post(self,request, module_id,model_name,id=None):
		form=self.get_form(self.model, instance=self.obj,
							data=request.POST, files=request.FILES)

		if form.is_valid():
			obj=form.save(commit=False)
			obj.owner=request.user
			obj.save()
			if not id:
				Content.objects.create(module=self.module,item=obj)
			return redirect('module_content_list', self.module.id)

		return self.render_to_response({'form':form,
										'object':self.obj})

#To delete content
class CourseContentDeleteView(View):

	def post (self,request,id):
		content=get_object_or_404(Content,id=id,
			module__course__owner=request.user)
		module=content.module
		content.item.delete()
		content.delete()
		return redirect('module_content_list', module.id)

#View to view the content in a particular model
class ModuleContentView(TemplateResponseMixin,View):
	template_name="manage/module/content_list.html"

	def get(self,request,module_id):
		module=get_object_or_404(Module,
							id=module_id,
							course__owner=request.user)
		return self.render_to_response({'module':module})

"""MAke a view that receives the new order of modules ID encoded in JSON"""

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):

	def post(self):
		for id, order in self.request_json.items():
			Module.objects.filter(id=id, 
				course__owner=request.user).update(oder=order)
		return self.render_json_response({'saved':'OK'})


class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
	def post(self):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id,
				module__course__owner=request.user).update(order=order)
	
		return self.render_json_response({'saved':'OK'})


"""View to list out courses as per subjects"""

from django.db.models import Count
from .models import Subject

class CourseListView(TemplateResponseMixin,View):
	model=Course
	template_name='course/list.html'

	def get(self,request,subject=None):
		subjects=Subject.objects.annotate(total_courses=Count('courses'))
		courses=Course.objects.annotate(total_modules=Count('modules'))


		if subject:
			subject=get_object_or_404(Subject,slug=subject)
			courses=courses.filter(subject=subject)

		return self.render_to_response({'subjects':subjects,
										'subject':subject,
										'courses':courses})

"""View to give a detail view"""
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm


class CourseDetailView(DetailView):
	model=Course
	template_name='course/detail.html'
	"""Changes to show the enrolled courses of students"""

	def get_context_data(self, **kwargs):
		context =super(CourseDetailView,self).get_context_data(**kwargs)

		context['enroll_form']=CourseEnrollForm(initial={'course':self.object})
		return context
		
