from django.db import models
from django.contrib.auth import get_user_model

from core.mail import send_mail_template

from django.utils import timezone

from django.urls import reverse

# Create your models here.
class CourseManager(models.Model):

	def search(self, query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) | models.Q(description_icontains=query)
		)



class Course(models.Model):

	name = models.CharField('Nome', max_length=255)
	slug = models.SlugField('Atalho')
	description = models.TextField('Descrição Simples', blank=True)
	about = models.TextField('Sobre o Curso', blank=True)
	start_date = models.DateField('Data de Início', null=True, blank=True)
	#Objetos do tipo image, depende da biblioteca Pillow(pip manage.py Pillow)
	image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)
	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	objects = CourseManager()

	#Retonar os nomes dos cursos, em vez de course oblect 1
	def __str__(self):
		return self.name

	#metodo para saber as aulas disponiveis
	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__gte=today)

	class Meta():
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']



#Metodo para criação das aulas
class Lesson(models.Model):

	name = models.CharField('Nome', max_length=100)
	description = models.TextField('Descrição', blank=True)
	number = models.IntegerField('Número (ordem)', blank=True, default=0)
	release_date = models.DateField('Data da Liberação', blank=True, null=True)

	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso', related_name='lessons')

	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)
	
	def __str__(self):
		return self.name

	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today
		return False


	class Meta:
		verbose_name = 'Aula'
		verbose_name_plural = 'Aulas'
		ordering = ['number']

#Classe de criacão dos materias
class Material(models.Model):

	name = models.CharField('Nome', max_length=100)
	#campo responsavel pelos arquivos de midia
	embedded = models.TextField('Video embedded', blank=True)
	#Serão materias publicos
	#para privados teremos que fazer algumas modificações
	file = models.FileField(upload_to='lessons/materias', blank=True, null=True)

	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Aula', related_name='materials')

	def is_embedded(self):
		return bool(self.embedded)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Matérial'
		verbose_name_plural ='Materiais'


#classe de inscrição
class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Usuário', related_name='enrollments')

	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso', related_name='enrollments')

	status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)

	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def active(self):
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1

	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural ='Inscrições'
		unique_together = (('user', 'course'),)


class Announcement(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements', verbose_name='Curso')
	title = models.CharField('Titulo', max_length=100)
	content = models.TextField('Conteúdo')

	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-create_at']



class Comment(models.Model):
	announcement = models.ForeignKey(
		Announcement, on_delete=models.CASCADE, verbose_name='Anúncio', related_name='comments'
	)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Usuário')
	comment = models.TextField('Comentário')

	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['create_at']



#Alerta(quando enviar email no formulaio do anuncio)
def post_save_announcement(instance, created, **kwargs):
	if created:
		subject = instance.title
		context = {
			'announcement': instance
		}
		template_name = 'courses/announcement_mail.html'
		enrollments = Enrollment.objects.filter(
			course = instance.course, status=1
		)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
	post_save_announcement, sender=Announcement,
	dispatch_uid='post_save_announcement'
)

