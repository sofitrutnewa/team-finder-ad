from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff', 'projects_count')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {'fields': ('name', 'surname', 'phone', 'github_url', 'about', 'avatar')}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            projects_count=Count('participated_projects')
        )

    @admin.display(description='Участий в проектах', ordering='projects_count')
    def projects_count(self, obj):
        return obj.projects_count
