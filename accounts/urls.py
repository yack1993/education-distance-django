
from django.urls import path

from .import views

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='signup'),
    path('edit/', views.edit, name='edit'),
    path('edit_password/', views.edit_password, name='editar-senha'),
    #path('register/', views.SignUp.as_view(), name='signup'),
]