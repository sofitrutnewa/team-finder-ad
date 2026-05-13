from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import password_validation
from django.utils.safestring import mark_safe
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})


class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=124, label='Имя')
    surname = forms.CharField(max_length=124, label='Фамилия')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

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
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(max_length=124, label='Имя')
    surname = forms.CharField(max_length=124, label='Фамилия')
    about = forms.CharField(
        max_length=256,
        label='Обо мне',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'style': 'resize: vertical; min-height: 100px;'
        })
    )
    phone = forms.CharField(
        max_length=12, label='Номер телефона', required=False)
    github_url = forms.URLField(
        label='Ссылка на профиль GitHub', required=False)
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
                f'<div><img src="{self.instance.avatar.url}" width="100" style="border-radius: 10px;"></div>'
            )
