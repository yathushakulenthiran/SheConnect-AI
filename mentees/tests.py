from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Mentee, ConnectionRequest
from mentors.models import Mentor


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

class ConnectionRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123',
            is_active=True
        )
        self.mentee = Mentee.objects.create(
            user=self.user,
            business_stage='startup',
            industry='Tech',
            main_challenges='marketing',
            mentorship_goals='growth'
        )
        self.mentor = Mentor.objects.create(
            name='Test Mentor',
            expertise='Business Strategy',
            years_experience=5,
            short_bio='Experienced business strategist',
            key_focus_areas='marketing, growth',
            availability_status='available',
            industry='Tech',
            business_stage_expertise='startup',
            email='mentor@example.com',
            is_verified=True,
            is_active=True
        )

    def test_send_connection_request(self):
        """Test sending a connection request to a mentor"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('mentees:send_connection', args=[self.mentor.id]),
            {'message': 'I would like to connect with you'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ConnectionRequest.objects.filter(
            mentee=self.mentee,
            mentor=self.mentor,
            status='pending'
        ).exists())

    def test_send_connection_request_duplicate(self):
        """Test that duplicate connection requests are prevented"""
        # Create existing connection
        ConnectionRequest.objects.create(
            mentee=self.mentee,
            mentor=self.mentor,
            status='pending'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('mentees:send_connection', args=[self.mentor.id]),
            {'message': 'Another request'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect with warning
        self.assertEqual(ConnectionRequest.objects.filter(
            mentee=self.mentee,
            mentor=self.mentor
        ).count(), 1)  # Only one connection should exist

    def test_cancel_connection_request(self):
        """Test canceling a pending connection request"""
        connection = ConnectionRequest.objects.create(
            mentee=self.mentee,
            mentor=self.mentor,
            status='pending'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('mentees:cancel_connection', args=[connection.id])
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(ConnectionRequest.objects.filter(id=connection.id).exists())

    def test_connections_page_renders(self):
        """Test that the connections page renders correctly"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('mentees:connections'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Connections')

    def test_connections_with_different_statuses(self):
        """Test connections page shows different status types correctly"""
        # Create connections with different statuses
        ConnectionRequest.objects.create(
            mentee=self.mentee,
            mentor=self.mentor,
            status='pending'
        )
        
        accepted_mentor = Mentor.objects.create(
            name='Accepted Mentor',
            expertise='Finance',
            years_experience=3,
            short_bio='Finance expert',
            key_focus_areas='finance',
            availability_status='available',
            industry='Finance',
            business_stage_expertise='growth',
            email='finance@example.com',
            is_verified=True,
            is_active=True
        )
        
        ConnectionRequest.objects.create(
            mentee=self.mentee,
            mentor=accepted_mentor,
            status='accepted'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mentees:connections'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pending Requests (1)')
        self.assertContains(response, 'Active Connections (1)')
        self.assertContains(response, 'Rejected Requests (0)')

# Create your tests here.
