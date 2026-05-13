from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import User
from .forms import LoginForm, RegisterForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import ProfileEditForm


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'
    success_url = None  # будет переопределено

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return f'/users/{self.request.user.pk}/'


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = 12
    ordering = ['id']


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.owned_projects.all()
        return context


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('project-list')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.name = form.cleaned_data['name']
        user.surname = form.cleaned_data['surname']
        user.save()
        return redirect(self.success_url)


def logout_view(request):
    logout(request)
    return redirect('project-list')


class ChangePasswordView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('project-list')
