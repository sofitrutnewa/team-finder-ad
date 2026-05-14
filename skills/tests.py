from django.test import TestCase

from .models import Skill


class SkillModelTest(TestCase):
    def test_create_skill(self):
        skill = Skill.objects.create(name='Django')
        self.assertEqual(str(skill), 'Django')
