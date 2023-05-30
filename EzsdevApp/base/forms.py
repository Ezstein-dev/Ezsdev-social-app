from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = ['username', 'password']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('posts')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            create_profile(user)
        return super().form_valid(form)
    
    def create_profile(user):
        if not Profile.objects.filter(user=user).exists():
            new_profile = Profile.objects.create(user=user)
            new_profile.save()

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super().get(*args, **kwargs)
