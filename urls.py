from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
 	path('', views.home, name="home"),
 	path('dashboard/', views.dashboard, name="dashboard"),
 	path('dashboard/add', views.create, name="addnew"),
 	path('dashboard/search', views.search, name="search"),
 	path('dashboard/edit/<str:pk>', views.edit, name="edit"),
 	path('dashboard/delete/<str:pk>', views.delete, name="delete"),

 	path('dashboard/quiz', views.quiz, name="quiz"),
 	path('dashboard/startquiz/<int:i>/<int:is_flipped>/<int:include_all>', views.start_quiz, name="startquiz"),
 	path('dashboard/increment/<int:i>/<int:is_flipped>/<int:include_all>', views.increment, name="increment"),
 	path('dashboard/decrement/<int:i>/<int:is_flipped>/<int:include_all>', views.decrement, name="decrement"),
 	path('dashboard/flipcard/<int:i>/<int:is_flipped>/<int:include_all>', views.flipcard, name="flipcard"),

 	path('login/', views.do_login, name="login"),
 	path('logout/', views.logout_user, name="logout"),
 	path('register/', views.register, name="register"),

 	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="myenglishmate/password_reset.html"), name="reset_password"),
 	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="myenglishmate/password_reset_sent.html"), name="password_reset_done"),
 	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="myenglishmate/password_reset_form.html"), name="password_reset_confirm"),
 	path('reset_password/complete', auth_views.PasswordResetCompleteView.as_view(template_name="myenglishmate/password_reset_done.html"), name="password_reset_complete"),
]