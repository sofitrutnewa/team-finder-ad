from django.urls import path

from skills.views import skill_autocomplete

app_name = 'skills'

urlpatterns = [
    path('', skill_autocomplete, name='autocomplete'),
]
