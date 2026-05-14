import random
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models

from PIL import Image, ImageDraw, ImageFont
from users.managers import UserManager

from config.constants import (
    MAX_LENGTH_ABOUT,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_USER_NAME,
    MAX_LENGTH_USER_SURNAME,
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=MAX_LENGTH_USER_NAME, verbose_name='Имя')
    surname = models.CharField(max_length=MAX_LENGTH_USER_SURNAME, verbose_name='Фамилия')
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^(\+7|8)\d{10}$')],
        verbose_name='Телефон'
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True, verbose_name='О себе')
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*args, **kwargs)

    def generate_avatar(self):
        colors = [
            '#4A90E2', '#50E3C2', '#F5A623', '#D0021B',
            '#8B572A', '#417505', '#F8E71C', '#BD10E0',
            '#7ED321', '#FF6B6B', '#4ECDC4', '#45B7D1'
        ]
        color = random.choice(colors)
        size = 200
        image = Image.new('RGB', (size, size), color)
        draw = ImageDraw.Draw(image)
        letter = self.name[0].upper()
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 100)
        except (OSError, IOError):
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) / 2, (size - text_height) / 2)
        draw.text(position, letter, fill='white', font=font)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), f'avatar_{self.email}.png')
