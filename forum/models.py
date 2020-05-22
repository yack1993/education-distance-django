from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager

from django.urls import reverse

class Thread(models.Model):
	title = models.CharField('Titulo', max_length=100)
	slug = models.SlugField('Identificador', max_length=100, unique=True)
	body = models.TextField('Mensagem')
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Autor', related_name='threads')
	views = models.IntegerField('Visualizações', blank=True, default=0)
	answers = models.IntegerField('Respostas', blank=True, default=0)
	tags = TaggableManager()

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	modified_at = models.DateTimeField('Modificado em', auto_now=True)

	def __str__(self):
		return self.title

	
	def get_absolute_url(self):
		#return "topico/%s/" %(self.slug)
		return "/forum/%s/" %(self.slug)

	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
		ordering = ['-modified_at']


class Reply(models.Model):

	thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='Tópico', related_name='repliess')

	reply = models.TextField('Resposta')
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Autor', related_name='replies')

	correct = models.BooleanField('Correta?', blank=True, default=False)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	modified_at = models.DateTimeField('Modificado em', auto_now=True)

	def __str__(self):
		return self.reply[:100]

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
		ordering = ['-correct', 'created_at']


def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.repliess.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.repliess.exclude(pk=instance.pk).update(
            correct=False
        )

#quando adciona e remove, faz a contagem de quantos repostas tem
def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)