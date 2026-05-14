from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import path

from users.views import (
    ChangePasswordView,
    LoginView,
    ProfileEditView,
    RegisterView,
    UserDetailView,
    UserListView,
)


def redirect_to_profile_edit(request):
    if request.user.is_authenticated:
        return redirect('users:profile_edit', pk=request.user.id)
    return redirect('users:login')


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/projects/list/'), name='logout'),
    path('edit-profile/', redirect_to_profile_edit, name='profile_edit_redirect'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
