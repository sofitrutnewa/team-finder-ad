from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/projects/list/'), name='home'),
    path('projects/', include('projects.urls', namespace='projects')),
    path('users/', include('users.urls', namespace='users')),
    path('users/skills/', include('skills.urls', namespace='user_skills')),
    path('projects/skills/', include('skills.urls', namespace='project_skills')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
