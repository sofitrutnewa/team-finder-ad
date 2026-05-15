import json
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.constants import PAGINATE_BY
from projects.forms import ProjectForm
from projects.models import Project
from skills.models import Skill

from config.constants import STATUS_CLOSED, STATUS_OPEN


@require_POST
@csrf_exempt
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Требуется авторизация'},
            status=HTTPStatus.UNAUTHORIZED
        )

    if request.user == project.owner:
        return JsonResponse(
            {'error': 'Владелец не может откликнуться'},
            status=HTTPStatus.BAD_REQUEST
        )

    if (is_participating := project.participants.filter(id=request.user.id).exists()):
        project.participants.remove(request.user)
        is_participating = False
    else:
        project.participants.add(request.user)
        is_participating = True

    return JsonResponse({
        'status': 'ok',
        'participant': is_participating,
        'participants_count': project.participants.count()
    })


@require_POST
@csrf_exempt
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse(
            {'error': 'Нет прав'},
            status=HTTPStatus.FORBIDDEN
        )

    if project.status != STATUS_OPEN:
        return JsonResponse(
            {'error': 'Проект уже завершён'},
            status=HTTPStatus.BAD_REQUEST
        )

    project.status = STATUS_CLOSED
    project.save()

    return JsonResponse({'status': 'ok', 'project_status': STATUS_CLOSED})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATE_BY
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name__iexact=skill_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_skills'] = Skill.objects.all().order_by('name')
        context['active_skill'] = self.request.GET.get('skill')
        if self.request.user.is_authenticated:
            context['user_id'] = self.request.user.id
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_participant'] = self.object.participants.filter(
            id=self.request.user.id
        ).exists()
        if self.request.user.is_authenticated:
            context['user_id'] = self.request.user.id
        return context


@require_GET
def skill_autocomplete(request):
    from skills.views import skill_autocomplete as skills_autocomplete
    return skills_autocomplete(request)


@require_POST
@csrf_exempt
def add_skill_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse(
            {'error': 'Нет прав'},
            status=HTTPStatus.FORBIDDEN
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    skill_id = data.get('skill_id')
    skill_name = data.get('name')

    created = False
    if skill_name and not skill_id:
        skill, created = Skill.objects.get_or_create(name=skill_name)
    else:
        skill = get_object_or_404(Skill, pk=skill_id)

    if not project.skills.filter(id=skill.id).exists():
        project.skills.add(skill)

    return JsonResponse({
        'id': skill.id,
        'name': skill.name,
        'created': created,
        'added': True
    })


@require_POST
@csrf_exempt
def remove_skill_from_project(request, pk, skill_id):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse(
            {'error': 'Нет прав'},
            status=HTTPStatus.FORBIDDEN
        )

    skill = get_object_or_404(Skill, pk=skill_id)
    project.skills.remove(skill)

    return JsonResponse({'status': 'ok', 'id': skill_id})
