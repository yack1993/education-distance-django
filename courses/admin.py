from django.contrib import admin

# Register your models here.
#Cadastrando os models no admin
from .models import (Course, Enrollment, Announcement, Comment,Lesson,
	Material)

#Campos que apareceram na area do adm do django
class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'create_at']
	search_fields = ['name', 'slug']
	#Preenche o campo slug automaticamente
	prepopulated_fields = {'slug':('name',)}


#admin.TabularInline ou Stacked
class MaterialInlineAdmin(admin.StackedInline):

	model = Material


class LessonAdmin(admin.ModelAdmin):
	list_display = ['name', 'number', 'course', 'release_date']
	search_fields = ['name', 'description']
	list_fielter = ['create_at']

	inlines = [
		MaterialInlineAdmin
	]

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)