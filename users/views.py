from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from users.constants import USERS_PAGINATE_BY
from users.forms import LoginForm, ProfileEditForm, RegisterForm
from users.models import User


def redirect_to_profile_edit(request):
    if request.user.is_authenticated:
        return redirect('users:profile_edit', pk=request.user.id)
    return redirect('users:login')


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('projects:project_list')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.owned_projects.all()
        return context


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = USERS_PAGINATE_BY
    ordering = ['id']


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.request.user.pk})


class ChangePasswordView(PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('projects:project_list')


def logout_view(request):
    logout(request)
    return redirect('projects:project_list')
