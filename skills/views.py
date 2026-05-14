from django.http import JsonResponse
from django.views.decorators.http import require_GET

from projects.constants import SKILL_AUTOCOMPLETE_LIMIT
from skills.models import Skill


@require_GET
def skill_autocomplete(request):
    query = request.GET.get('q', '')
    skills = Skill.objects.filter(
        name__icontains=query
    ).order_by('name')[:SKILL_AUTOCOMPLETE_LIMIT]
    data = [{'id': skill.id, 'name': skill.name} for skill in skills]
    return JsonResponse(data, safe=False)
