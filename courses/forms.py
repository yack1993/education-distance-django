from django import forms

from django.core.mail import send_mail
from django.conf import settings

from core.mail import send_mail_template

from .models import Comment

#Classe Formulario do curso
class ContactCourse(forms.Form):

	name = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='E-mail')
	message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

	#Metodo esponsavel pelo envio de email
	def send_mail(self, course):
		subject = '[%s] Contato' % course
		context = {
			'name': self.cleaned_data['name'],
			'email': self.cleaned_data['email'],
			'message': self.cleaned_data['message'],
		}
		template_name = 'courses/contact_email.html'
		send_mail(subject, template_name, context, [settings.CONTACT_EMAIL])


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		#os campos do formulario
		fields = ['comment']