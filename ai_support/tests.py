from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import MentalHealthSession, ChatMessage
from .chatbot_service import MentalHealthChatbot
from mentees.models import Mentee
import json

User = get_user_model()


class MentalHealthChatTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.mentee = Mentee.objects.create(
            user=self.user,
            business_name='Test Business',
            industry='Technology',
            years_in_business=2,
            team_size=3,
            revenue_range='Under $50K',
            preferred_meeting_mode='Online',
            languages='English',
            onboarding_complete=True
        )

    def test_mental_health_chat_page_loads(self):
        """Test that the mental health chat page loads correctly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('ai_support:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ai_support/chat.html')
        self.assertContains(response, 'Entrepreneur Mental Health Chat')

    def test_send_message_endpoint(self):
        """Test the AJAX message sending endpoint"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'message': 'I am feeling anxious today',
            'mood_rating': 3,
            'stress_level': 7
        }
        
        response = self.client.post(
            reverse('ai_support:send_message'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertIn('ai_response', response_data)

    def test_chat_session_creation(self):
        """Test that chat sessions are created properly"""
        self.client.login(username='testuser', password='testpass123')
        
        # Send a message
        data = {
            'message': 'Hello, I need help',
            'mood_rating': 5,
            'stress_level': 5
        }
        
        response = self.client.post(
            reverse('ai_support:send_message'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check that session was created
        session = MentalHealthSession.objects.filter(user=self.user).first()
        self.assertIsNotNone(session)
        self.assertEqual(session.mood_rating, 5)
        self.assertEqual(session.stress_level, 5)
        self.assertEqual(session.session_type, 'daily_checkin')

    def test_chat_messages_creation(self):
        """Test that chat messages are saved properly"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'message': 'I am feeling sad',
            'mood_rating': 2,
            'stress_level': 8
        }
        
        response = self.client.post(
            reverse('ai_support:send_message'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check that messages were created
        session = MentalHealthSession.objects.filter(user=self.user).first()
        messages = ChatMessage.objects.filter(session=session)
        self.assertEqual(messages.count(), 2)  # User message + AI response
        
        user_message = messages.filter(role='user').first()
        ai_message = messages.filter(role='assistant').first()
        
        self.assertEqual(user_message.content, 'I am feeling sad')
        self.assertIsNotNone(ai_message.content)


class ChatbotServiceTests(TestCase):
    def setUp(self):
        self.chatbot = MentalHealthChatbot()

    def test_entrepreneur_mood_analysis(self):
        """Test entrepreneur mood analysis functionality"""
        # Test business-specific indicators
        mood = self.chatbot.analyze_entrepreneur_mood("My business is doing great, sales are up")
        self.assertEqual(mood, 'happy')
        
        mood = self.chatbot.analyze_entrepreneur_mood("My business is failing, no sales")
        self.assertEqual(mood, 'sad')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I'm worried about cash flow")
        self.assertEqual(mood, 'anxious')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I'm overwhelmed with work")
        self.assertEqual(mood, 'stressed')
        
        # Test general mood indicators
        mood = self.chatbot.analyze_entrepreneur_mood("I am feeling happy and excited today")
        self.assertEqual(mood, 'happy')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I am feeling sad and depressed")
        self.assertEqual(mood, 'sad')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I am anxious and worried")
        self.assertEqual(mood, 'anxious')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I am stressed and overwhelmed")
        self.assertEqual(mood, 'stressed')
        
        mood = self.chatbot.analyze_entrepreneur_mood("I am okay")
        self.assertEqual(mood, 'neutral')

    def test_entrepreneur_response_generation(self):
        """Test AI response generation for entrepreneurs"""
        # Test greeting response
        response = self.chatbot.generate_entrepreneur_response("Hello")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Test business-specific response
        response = self.chatbot.generate_entrepreneur_response("I'm worried about my business finances")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_entrepreneur_challenge_identification(self):
        """Test entrepreneur challenge identification"""
        challenges = self.chatbot.identify_entrepreneur_challenges("I'm worried about money and cash flow")
        self.assertIn('financial_worries', challenges)
        
        challenges = self.chatbot.identify_entrepreneur_challenges("I can't balance work and family")
        self.assertIn('work_life_balance', challenges)
        
        challenges = self.chatbot.identify_entrepreneur_challenges("I feel lonely running my business")
        self.assertIn('loneliness', challenges)

    def test_mood_trends_tracking(self):
        """Test mood trends analysis"""
        sessions_data = [
            {'mood_rating': 3, 'stress_level': 7, 'date': timezone.now().date()},
            {'mood_rating': 5, 'stress_level': 6, 'date': timezone.now().date()},
            {'mood_rating': 7, 'stress_level': 4, 'date': timezone.now().date()},
        ]
        
        trends = self.chatbot.track_mood_trends(sessions_data)
        self.assertIn('trend', trends)
        self.assertIn('average_mood', trends)
        self.assertIn('sessions_count', trends)


class MoodAnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.mentee = Mentee.objects.create(
            user=self.user,
            business_name='Test Business',
            industry='Technology',
            years_in_business=2,
            team_size=3,
            revenue_range='Under $50K',
            preferred_meeting_mode='Online',
            languages='English',
            onboarding_complete=True
        )

    def test_mood_analytics_page_loads(self):
        """Test that the mood analytics page loads correctly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('ai_support:mood_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ai_support/mood_analytics.html')
        self.assertContains(response, 'Entrepreneur Mood Analytics')

    def test_mood_analytics_with_data(self):
        """Test mood analytics with session data"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create test sessions
        session1 = MentalHealthSession.objects.create(
            user=self.user,
            session_type='daily_checkin',
            mood_rating=7,
            stress_level=3,
            notes='Feeling good',
            ai_response='Great to hear you are feeling good!'
        )
        
        session2 = MentalHealthSession.objects.create(
            user=self.user,
            session_type='daily_checkin',
            mood_rating=8,
            stress_level=2,
            notes='Feeling great',
            ai_response='Excellent!'
        )
        
        response = self.client.get(reverse('ai_support:mood_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '7.5')  # Average mood
        self.assertContains(response, '2.5')  # Average stress
        self.assertContains(response, '2')    # Total sessions


class MentalHealthModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_mental_health_session_creation(self):
        """Test MentalHealthSession model"""
        session = MentalHealthSession.objects.create(
            user=self.user,
            session_type='daily_checkin',
            mood_rating=6,
            stress_level=4,
            notes='Feeling okay',
            ai_response='Thanks for sharing'
        )
        
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.session_type, 'daily_checkin')
        self.assertEqual(session.mood_rating, 6)
        self.assertEqual(session.stress_level, 4)
        self.assertEqual(str(session), f"{self.user.email} - daily_checkin ({session.created_at.date()})")

    def test_chat_message_creation(self):
        """Test ChatMessage model"""
        session = MentalHealthSession.objects.create(
            user=self.user,
            session_type='daily_checkin',
            mood_rating=5,
            stress_level=5,
            notes='',
            ai_response=''
        )
        
        message = ChatMessage.objects.create(
            session=session,
            content='Hello, I need help',
            role='user'
        )
        
        self.assertEqual(message.session, session)
        self.assertEqual(message.content, 'Hello, I need help')
        self.assertEqual(message.role, 'user')
        self.assertEqual(str(message), f"{self.user.email} - user ({message.created_at})")
