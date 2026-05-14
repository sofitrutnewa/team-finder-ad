from django.db import models
from django.urls import reverse

from config.constants import MAX_LENGTH_SKILL_NAME


class Skill(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_SKILL_NAME,
        unique=True,
        verbose_name='Название навыка'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skill_detail', args=[str(self.id)])
