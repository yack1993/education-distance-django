from django.urls import path,re_path
#from django.contrib.auth.decorators import login_required

from .import views

urlpatterns = [
	path('', views.index, name='index'),
	path('tag/<tag>/', views.index, name='index_tagged'),
	#path('respostas/correta/<int:id>', views.reply_correct, name='reply-correct'),
	#path('respostas/incorreta/<int:id>', views.reply_incorrect, name='reply-incorrect'),

	re_path(r'^respostas/(?P<pk>\d+)/correta/$', views.reply_correct,name='reply_correct'),
    re_path(r'^respostas/(?P<pk>\d+)/incorreta/$', views.reply_incorrect, name='reply_incorrect'),

	path('<slug>/', views.thread, name='thread'),
	#path('topico/<slug>/', views.thread, name='thread'),
]