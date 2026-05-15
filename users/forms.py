import re

from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from users.models import User

from config.constants import (
    MAX_LENGTH_ABOUT,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_USER_NAME,
    MAX_LENGTH_USER_SURNAME,
)
from config.mixins import GitHubURLMixin


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    name = forms.CharField(
        max_length=MAX_LENGTH_USER_NAME,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    surname = forms.CharField(
        max_length=MAX_LENGTH_USER_SURNAME,
        label='Фамилия',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileEditForm(GitHubURLMixin, forms.ModelForm):
    name = forms.CharField(
        max_length=MAX_LENGTH_USER_NAME,
        label='Имя'
    )
    surname = forms.CharField(
        max_length=MAX_LENGTH_USER_SURNAME,
        label='Фамилия'
    )
    about = forms.CharField(
        max_length=MAX_LENGTH_ABOUT,
        label='Обо мне',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'style': 'resize: vertical; min-height: 100px;'
        })
    )
    phone = forms.CharField(
        max_length=MAX_LENGTH_PHONE,
        label='Номер телефона',
        required=False
    )
    github_url = forms.URLField(
        label='Ссылка на профиль GitHub',
        required=False
    )
    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        widget=forms.FileInput(attrs={'class': 'avatar-input'})
    )

    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.avatar:
            self.fields['avatar'].help_text = mark_safe(
                f'<div><img src="{self.instance.avatar.url}" '
                f'width="100" style="border-radius: 10px;"></div>'
            )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return None
        phone_clean = re.sub(r'[^\d+]', '', phone)
        if not re.match(r'^(\+7|8)\d{10}$', phone_clean):
            msg = 'Номер телефона должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX'
            raise ValidationError(msg)
        if phone_clean.startswith('8'):
            phone_clean = '+7' + phone_clean[1:]
        if User.objects.exclude(pk=self.instance.pk).filter(phone=phone_clean).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует')
        return phone_clean
