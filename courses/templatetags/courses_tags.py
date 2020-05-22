from django.template import Library

register = Library()

from courses.models import Enrollment

#converte a minha função
#numa tag que pode ser usada pelo django(@register.inclusion_tag)
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
	enrollments = Enrollment.objects.filter(user=user)
	context = {
		'enrollments': enrollments
	}
	return context


#Atualizar minha tag - 
#assignment_tag, pra versões 2... já não existe
@register.simple_tag
def load_my_courses(user):
	return Enrollment.objects.filter(user=user)