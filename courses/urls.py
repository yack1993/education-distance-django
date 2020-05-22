from django.urls import path
#from django.contrib.auth.decorators import login_required

from .import views

urlpatterns = [
	path('', views.index, name='index'),
	#re_path('(?P<slug>[\w_-]+)/inscricao/', views.enrollment, name='enrollment'),
	path('<slug>/inscricao/',views.enrollment, name='enrollment'),
	path('<slug>/cancelar-inscricao/', views.undo_enrollment, name='cancelar-inscricao'),
	path('<slug>/',views.details, name='details'),
	path('<slug>/anuncios/', views.announcements, name='anuncios'),
	path('<slug>/anuncios/<int:id>/', views.show_announcement, name='anuncios'),
	path('<slug>/aulas/', views.lessons, name='Aulas'),
	path('<slug>/aulas/<int:id>/', views.lesson, name='lesson'),
	path('<slug>/materiais/<int:id>/', views.material, name='material'),
]