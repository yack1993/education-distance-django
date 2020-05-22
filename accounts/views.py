from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.conf import settings
from django.contrib import messages

from courses.models import Enrollment

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

#importar o forms para usar o campo emai
from .forms import RegisterForm, EditAccountForm

@login_required #só vai ter acesso que estiver logado
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	#acessando as incrições do aluno
	context = {}
	#context['enrollments'] = Enrollment.objects.filter(user=request.user)
	return render(request, template_name, context)


def register(request):
	template_name = 'registration/register.html'
	if request.method == 'POST':
		#em vez de UserCreationForm(usar form do email,RegisterForm)
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(
				username=user.username, password=form.cleaned_data['password1']
			)
			login(request, user)
			return redirect(settings.LOGIN_REDIRECT_URL)
	else:
		form = RegisterForm()
	context = {
		'form':form
	}
	return render(request, template_name, context)

@login_required
def edit(request):
	template_name = 'accounts/edit.html'
	form = EditAccountForm()
	context = {}
	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			#form = EditAccountForm(instance=request.user)
			#context['success'] = True
			messages.success(request, 'Os dados foram alterados com sucesso')
			return redirect('/accounts')
	else:
		form = EditAccountForm(instance=request.user)
	context['form'] = form
	return render(request, template_name, context)


@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			context['success'] = True
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form
	return render(request, template_name, context)
	
