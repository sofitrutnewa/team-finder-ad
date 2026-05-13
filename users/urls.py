from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('edit-profile/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
]
