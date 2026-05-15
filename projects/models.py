from django.db import models
from django.urls import reverse

from skills.models import Skill
from users.models import User

from config.constants import MAX_LENGTH_NAME, MAX_LENGTH_STATUS, STATUS_CHOICES, STATUS_OPEN


class Project(models.Model):
    STATUS_CHOICES = STATUS_CHOICES

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название проекта'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    participants = models.ManyToManyField(
        User,
        related_name='participated_projects',
        blank=True
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='projects',
        blank=True
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[str(self.id)])
