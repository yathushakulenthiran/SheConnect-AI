from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mentees.models import Mentee
from mentors.models import Mentor

User = get_user_model()

class Command(BaseCommand):
    help = 'Create demo user and mentors for presentation'

    def handle(self, *args, **options):
        # Create demo mentee
        if not User.objects.filter(email='demo@sheconnect.ai').exists():
            demo_user = User.objects.create_user(
                username='demo_mentee',
                email='demo@sheconnect.ai',
                password='demo123456',
                first_name='Sarah',
                last_name='Johnson',
                is_active=True
            )
            
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
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created demo mentee: {demo_user.email} (password: demo123456)')
            )
        else:
            self.stdout.write('Demo user already exists!')

        # Create sample mentors
        mentors_data = [
            {
                'name': 'Dr. Priya Fernando',
                'expertise': 'Business Strategy & Growth',
                'bio': 'Former CEO of LankaTech with 15+ years scaling startups.',
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
                'bio': 'Marketing Director at Global Brands Lanka.',
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
                'bio': 'CFO with 20+ years in financial management.',
                'years_experience': 20,
                'availability': 'Weekdays 7-9 PM',
                'hourly_rate': 200,
                'is_active': True,
                'average_rating': 4.9,
                'rating_count': 15
            }
        ]
        
        for mentor_data in mentors_data:
            if not Mentor.objects.filter(name=mentor_data['name']).exists():
                mentor = Mentor.objects.create(**mentor_data)
                self.stdout.write(f'✅ Created mentor: {mentor.name}')
            else:
                self.stdout.write(f'Mentor {mentor_data["name"]} already exists!')

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Demo data ready!')
        )
        self.stdout.write('\n📋 Demo Login:')
        self.stdout.write('   Email: demo@sheconnect.ai')
        self.stdout.write('   Password: demo123456')

