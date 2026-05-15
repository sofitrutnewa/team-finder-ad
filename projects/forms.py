from django import forms

from projects.models import Project

from config.constants import STATUS_CHOICES
from config.mixins import GitHubURLMixin


class ProjectForm(GitHubURLMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
            'name': forms.TextInput(attrs={
                'placeholder': 'Название проекта',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание проекта',
                'rows': 4,
                'class': 'form-control'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/username/repo',
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Название:',
            'description': 'Описание:',
            'github_url': 'Ссылка на GitHub:',
            'status': 'Статус:',
        }
