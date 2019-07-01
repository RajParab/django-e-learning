"""View for a student registration form"""

from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class StudentRegistrationForm(CreateView):
	template_name='students/student/registration.html'
	success_url=reverse_lazy('student_course_list')
	form_class=UserCreationForm

	def form_valid(self, form):
		result=super(StudentRegistrationForm, self).form_valid(form)
		cd= form.cleaned_data
		user=authenticate(username=cd['username'],
						  password=cd['password1'])

		login(self.request, user)
		return result

"""View to get the list of the enrolled courses"""

from .forms import CourseEnrollForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentEnrollCourseView(LoginRequiredMixin,FormView):
	course=None
	form_class=CourseEnrollForm

	def form_valid(self, form):
		self.course=form.cleaned_data['course']
		self.course.students.add(self.request.user)
		return super(StudentEnrollCourseView,self).form_valid(form)

	def get_sucess_url(self):
		return reverse_lazy('student_course_detail',
							args=[self.course.id])


"""View to Student Courses List View and its Details view"""
from django.views.generic.list import ListView
from courses.models import Course

class StudentCourseListView(LoginRequiredMixin, ListView):
	template_name='students/course/list.html'
	model=Course

	def get_queryset(self):
		qs=super(StudentCourseListView,self).get_queryset()
		return qs.filter(students__in=[self.request.user])



from django.views.generic.detail import DetailView

class StudentCourseDetailView(LoginRequiredMixin, DetailView):
	model=Course
	template_name='students/course/detail.html'

	def get_queryset(self):
		qs=super(StudentCourseDetailView,self).get_queryset()
		return qs.filter(students__in=[self.request.user])

	def get_context_data(self, **kwargs):
		context=super(StudentCourseDetailView, self).get_context_data(**kwargs)

		course=self.get_object()
		if 'module_id' in self.kwargs:
			context['module']=course.modules.get(id=self.kwargs['module_id'])

		else:
			context['module']=course.modules.all().first()

		return context