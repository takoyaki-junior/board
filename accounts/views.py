from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from . import forms
from django.views import generic
from accounts.forms import LoginForm, SignUpForm


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class IndexView(TemplateView):
    template_name = "board/index.html"


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
