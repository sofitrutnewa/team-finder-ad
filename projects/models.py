from django.db import models
from users.models import User
from skills.models import Skill


class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default='open')
    participants = models.ManyToManyField(
        User, related_name='participated_projects', blank=True)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
