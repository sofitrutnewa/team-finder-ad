from django.urls import path

from projects.views import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    add_skill_to_project,
    complete_project,
    remove_skill_from_project,
    skill_autocomplete,
    toggle_participate,
)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create-project/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/toggle-participate/', toggle_participate, name='toggle_participate'),
    path('<int:pk>/complete/', complete_project, name='complete_project'),
    path('skills/autocomplete/', skill_autocomplete, name='skill_autocomplete'),
    path('<int:pk>/skills/add/', add_skill_to_project, name='add_skill_to_project'),
    path(
        '<int:pk>/skills/<int:skill_id>/remove/',
        remove_skill_from_project,
        name='remove_skill_from_project'
    ),
]
