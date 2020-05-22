from django.contrib import admin

from .models import Thread, Reply

# Register your models here.
class ThreadAdmin(admin.ModelAdmin):

	list_display = ['title', 'author', 'created_at', 'modified_at']
	search_fields = ['title', 'author__email', 'body']
	prepopulated_fields = {'slug': ('title',)}


class ReplyAdmin(admin.ModelAdmin):
	list_display = ['thread', 'author', 'correct', 'created_at', 'modified_at']
	search_fields = ['thread__title', 'author__email', 'reply']

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
