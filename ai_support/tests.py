from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from mentees.models import Mentee
from mentors.models import Mentor
from .services import score_match, top_matches


User = get_user_model()


class MatchingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', email='u@example.com', password='pass', is_active=True)
        self.mentee = Mentee.objects.create(
            user=self.user, business_stage='startup', industry='Tech',
            main_challenges='marketing', mentorship_goals='growth'
        )
        self.m1 = Mentor.objects.create(
            name='A', expertise='X', years_experience=5, short_bio='b', key_focus_areas='marketing, sales',
            availability_status='available', industry='Tech', business_stage_expertise='startup',
            email='a@example.com', is_verified=True, is_active=True, average_rating=4.5
        )
        self.m2 = Mentor.objects.create(
            name='B', expertise='Y', years_experience=5, short_bio='b', key_focus_areas='finance',
            availability_status='busy', industry='Finance', business_stage_expertise='growth',
            email='b@example.com', is_verified=True, is_active=True, average_rating=3.0
        )

    def test_score_match(self):
        score, reasoning, comp = score_match(self.mentee, self.m1)
        self.assertTrue(score > 0)
        self.assertIn('Stage:', reasoning)

    def test_top_matches_ordering(self):
        results = top_matches(self.mentee)
        self.assertEqual(results[0][0].name, 'A')

    def test_matching_view(self):
        self.client.login(username='u', password='pass')
        resp = self.client.get(reverse('ai_support:matching'))
        self.assertEqual(resp.status_code, 200)

# Create your tests here.
