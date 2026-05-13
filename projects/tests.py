from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project
from skills.models import Skill

User = get_user_model()


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test',
            surname='User',
            password='pass'
        )
        self.skill = Skill.objects.create(name='Python')

    def test_create_project(self):
        project = Project.objects.create(
            name='Test Project',
            owner=self.user,
            status='open'
        )
        project.skills.add(self.skill)
        project.participants.add(self.user)
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.skills.count(), 1)
        self.assertEqual(project.participants.count(), 1)
