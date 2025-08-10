#!/usr/bin/env python
"""
Demo data creation script for SheConnect AI
Run this to create test users and mentors for demo purposes
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheconnect_ai.settings')
django.setup()

from django.contrib.auth import get_user_model
from mentors.models import Mentor
from mentees.models import Mentee
from django.db import transaction

User = get_user_model()

def create_demo_data():
    """Create demo users and mentors for presentation"""
    
    with transaction.atomic():
        # Create demo mentee user
        print("Creating demo mentee...")
        demo_user = User.objects.create_user(
            username='demo_mentee',
            email='demo@sheconnect.ai',
            password='demo123456',
            first_name='Sarah',
            last_name='Johnson',
            is_active=True
        )
        
        # Create mentee profile
        mentee = Mentee.objects.create(
            user=demo_user,
            bio='Tech startup founder looking for mentorship in business growth and marketing.',
            goals='Scale my business from $50K to $500K ARR',
            challenges='Marketing strategy, team building, investor relations',
            preferred_meeting_mode='video',
            years_in_business=2,
            team_size=5,
            revenue_range='$50K-$100K',
            languages='English, Sinhala',
            onboarding_complete=True
        )
        
        print(f"✅ Created demo mentee: {demo_user.email} (password: demo123456)")
        
        # Create sample mentors
        mentors_data = [
            {
                'name': 'Dr. Priya Fernando',
                'expertise': 'Business Strategy & Growth',
                'bio': 'Former CEO of LankaTech with 15+ years scaling startups. Helped 50+ companies reach $1M+ revenue.',
                'years_experience': 15,
                'availability': 'Weekdays 6-8 PM',
                'hourly_rate': 150,
                'is_active': True,
                'average_rating': 4.8,
                'rating_count': 12
            },
            {
                'name': 'Nimali Silva',
                'expertise': 'Digital Marketing & Branding',
                'bio': 'Marketing Director at Global Brands Lanka. Expert in social media marketing and brand development.',
                'years_experience': 8,
                'availability': 'Weekends 10 AM-2 PM',
                'hourly_rate': 120,
                'is_active': True,
                'average_rating': 4.6,
                'rating_count': 8
            },
            {
                'name': 'Kumara Perera',
                'expertise': 'Finance & Investment',
                'bio': 'CFO with 20+ years in financial management. Specializes in startup funding and financial planning.',
                'years_experience': 20,
                'availability': 'Weekdays 7-9 PM',
                'hourly_rate': 200,
                'is_active': True,
                'average_rating': 4.9,
                'rating_count': 15
            }
        ]
        
        for mentor_data in mentors_data:
            mentor = Mentor.objects.create(**mentor_data)
            print(f"✅ Created mentor: {mentor.name} - {mentor.expertise}")
        
        print("\n🎉 Demo data created successfully!")
        print("\n📋 Demo Login Credentials:")
        print("   Email: demo@sheconnect.ai")
        print("   Password: demo123456")
        print("\n🔗 Access URLs:")
        print("   Home: http://127.0.0.1:8000/")
        print("   Login: http://127.0.0.1:8000/accounts/login/")
        print("   Mentee Dashboard: http://127.0.0.1:8000/mentees/dashboard/")
        print("   AI Matching: http://127.0.0.1:8000/ai-support/matching/")
        print("   Mentor List: http://127.0.0.1:8000/mentors/")

if __name__ == '__main__':
    try:
        create_demo_data()
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        sys.exit(1)

