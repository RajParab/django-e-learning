from django.urls import path
from . import views

urlpatterns=[
			path('register/', views.StudentRegistrationForm.as_view(), name='student_registration'),
			path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_course_enroll'),
			path('courses/', views.StudentCourseListView.as_view(),name='student_course_list'),
			path('course/<pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
			path('course/<pk>/<module_id>/',views.StudentCourseDetailView.as_view(),name='student_course_detail_module'),

			]