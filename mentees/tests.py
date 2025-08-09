from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Mentee


User = get_user_model()


class RegistrationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='t', email='t@example.com', password='pass12345', is_active=True)

    def test_register_view_get(self):
        self.client.login(username='t', password='pass12345')
        resp = self.client.get(reverse('mentees:register'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mentee Registration')

    def test_register_submit(self):
        self.client.login(username='t', password='pass12345')
        data = {
            'business_stage': 'startup',
            'industry': 'Tech',
            'business_name': 'Acme',
            'main_challenges': 'X',
            'mentorship_goals': 'Y',
            'phone': '',
            'location': '',
            'linkedin_profile': '',
        }
        resp = self.client.post(reverse('mentees:register'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Mentee.objects.filter(user=self.user).exists())

    def test_onboarding_submit(self):
        self.client.login(username='t', password='pass12345')
        # Create mentee via register first
        data = {
            'business_stage': 'startup',
            'industry': 'Tech',
            'business_name': 'Acme',
            'main_challenges': 'X',
            'mentorship_goals': 'Y',
            'phone': '',
            'location': '',
            'linkedin_profile': '',
        }
        self.client.post(reverse('mentees:register'), data)
        resp = self.client.post(reverse('mentees:onboarding'), {
            'years_in_business': 2,
            'team_size': 3,
            'revenue_range': '0-10k',
            'preferred_meeting_mode': 'online',
            'languages': 'English,Tamil',
        })
        self.assertEqual(resp.status_code, 302)
        mentee = Mentee.objects.get(user=self.user)
        self.assertTrue(mentee.onboarding_complete)

    def test_profile_update(self):
        self.client.login(username='t', password='pass12345')
        self.client.post(reverse('mentees:register'), {
            'business_stage': 'startup',
            'industry': 'Tech',
            'business_name': 'Acme',
            'main_challenges': 'X',
            'mentorship_goals': 'Y',
            'phone': '',
            'location': '',
            'linkedin_profile': '',
        })
        resp = self.client.post(reverse('mentees:profile'), {
            'business_stage': 'growth',
            'industry': 'Finance',
            'business_name': 'Acme2',
            'main_challenges': 'Z',
            'mentorship_goals': 'W',
            'phone': '123',
            'location': 'Colombo',
            'linkedin_profile': '',
            'years_in_business': 5,
            'team_size': 10,
            'revenue_range': '10k-100k',
            'preferred_meeting_mode': 'offline',
            'languages': 'English',
        })
        self.assertEqual(resp.status_code, 302)
        mentee = Mentee.objects.get(user=self.user)
        self.assertEqual(mentee.business_stage, 'growth')

    def test_dashboard_renders(self):
        self.client.login(username='t', password='pass12345')
        # Ensure mentee exists
        self.client.post(reverse('mentees:register'), {
            'business_stage': 'startup',
            'industry': 'Tech',
            'business_name': 'Acme',
            'main_challenges': 'X',
            'mentorship_goals': 'Y',
            'phone': '',
            'location': '',
            'linkedin_profile': '',
        })
        resp = self.client.get(reverse('mentees:dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Pending Connections')

# Create your tests here.
