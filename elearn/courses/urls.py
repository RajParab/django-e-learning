"""Create urls for this app which connects each view to the html page"""

from django.urls import path

from . import views

urlpatterns=[

	path('mine/',views.ManageCourseListView.as_view(), name='manage_course_list'),
	path('create/',views.CreateCourseView.as_view(), name='create_course'),
	path('<pk>/delete/',views.DeleteCourseView.as_view(), name='delete_course'),
	path('<pk>/edit/',views.EditCourseView.as_view(),name='edit_course'),
	path('<pk>/module',views.CreateModuleUpdateView.as_view(),name='course_module_update'),
	path('module/<int:module_id>/content/<model_name>/create/',views.CreateContentUpdateView.as_view(),name='module_content_create'),
	path('module/<int:module_id>/content/<model_name>/<id>/',views.CreateContentUpdateView.as_view(),name='module_content_update'),
	path('content/<int:id>/delete/',views.CourseContentDeleteView.as_view(),name='module_content_delete'),
	path('module/<int:module_id>/',views.ModuleContentView.as_view(),name='module_content_list'),
	path('module/order/',views.ModuleOrderView.as_view(),name='module_order'),
	path('content/order/',views.ContentOrderView.as_view(),name='content_order'),
	path('',views.CourseListView.as_view(), name='course_list'),
	path('subject/<slug:subject>', views.CourseListView.as_view(), name='course_list_subject'),
	path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail')

]