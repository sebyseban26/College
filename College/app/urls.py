from django.urls import path
from .import views

urlpatterns = [
    path('course',views.course,name='course'),
    path('add_course',views.add_course,name='add_course'),
    path('student',views.student,name='student'),
    path('add_student',views.add_student,name='add_student'),
    path('show_student',views.show_student,name='show_student'),
    path('edit/<int:pk>/',views.edit,name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('admin',views.admin_dashboard,name='Admin_dashboard'),
    path('show_teachers', views.show_teachers, name='show_teachers'),
    path('teacher_delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path('',views.home,name='Home_dashboard'),
    path('signup_page', views.add_teacher, name='signup_page'),
    path('login_page',views.login_fun,name='login_page'),
    path('teacher_dashboard',views.teacher_dashboard,name='teacher_dashboard'),
    path('profile', views.profile_card, name='profile_card'),
    path('teacher_edit/<int:pk>/',views.edit_teacher,name='teacher_edit'),
    path('logout/', views.logout_teacher, name='logout'),
]

