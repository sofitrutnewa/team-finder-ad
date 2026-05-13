from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('list/', views.ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/skills/add/', views.add_skill_to_project, name='add-skill'),
    path('<int:pk>/skills/<int:skill_id>/remove/',
         views.remove_skill_from_project, name='remove-skill'),
    path('skills/', views.skill_autocomplete, name='skill-autocomplete'),
    path('create-project/', views.ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/complete/', views.complete_project, name='project-complete'),
    path('<int:pk>/toggle-participate/',
         views.toggle_participate, name='toggle-participate'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
]
