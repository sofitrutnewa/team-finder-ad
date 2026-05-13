from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from skills.models import Skill
from .forms import ProjectForm
import json


@require_POST
@csrf_exempt
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)

    if request.user == project.owner:
        return JsonResponse({'error': 'Владелец не может откликнуться'}, status=400)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participating = False
    else:
        project.participants.add(request.user)
        is_participating = True

    # Возвращаем обновлённые данные
    return JsonResponse({
        'status': 'ok',
        'is_participating': is_participating,
        'participants_count': project.participants.count()
    })


@require_POST
@csrf_exempt
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse({'error': 'Нет прав'}, status=403)

    if project.status != 'open':
        return JsonResponse({'error': 'Проект уже завершён'}, status=400)

    project.status = 'closed'
    project.save()

    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


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
        return reverse_lazy('project-detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.pk})


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
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
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_participant'] = self.request.user in self.object.participants.all()
        return context


@require_GET
def skill_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(name__icontains=q).order_by('name')[:10]
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)


@require_POST
@csrf_exempt
def add_skill_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse({'error': 'Нет прав'}, status=403)

    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    skill_name = data.get('name')

    created = False
    if skill_name and not skill_id:
        skill, created = Skill.objects.get_or_create(name=skill_name)
        skill_id = skill.id
    else:
        skill = get_object_or_404(Skill, pk=skill_id)

    if project.skills.filter(id=skill.id).exists():
        return JsonResponse({
            'skill_id': skill.id,
            'created': created,
            'added': False
        })

    project.skills.add(skill)
    return JsonResponse({
        'skill_id': skill.id,
        'created': created,
        'added': True
    })


@require_POST
@csrf_exempt
def remove_skill_from_project(request, pk, skill_id):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        return JsonResponse({'error': 'Нет прав'}, status=403)

    skill = get_object_or_404(Skill, pk=skill_id)
    project.skills.remove(skill)

    return JsonResponse({'status': 'ok'})
