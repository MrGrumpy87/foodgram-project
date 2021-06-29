from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class Login(LoginView):
    template_name = 'users/login.html'


class Logout(LogoutView):
    template_name = 'users/logout.html'


class PasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'users/password_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
