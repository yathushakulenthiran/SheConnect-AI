from django.core.management.base import BaseCommand
from mentors.models import Mentor


SAMPLE_MENTORS = [
    {
        'name': 'Dr. Sarah Perera',
        'expertise': 'Business Strategy & Digital Marketing',
        'years_experience': 15,
        'short_bio': 'Experienced business strategist specializing in digital transformation and marketing for women-led businesses in Sri Lanka.',
        'key_focus_areas': 'Digital Marketing, Business Strategy, Brand Development, Market Entry',
        'industry': 'Technology',
        'business_stage_expertise': 'growth',
        'email': 'sarah.perera@example.com',
        'phone': '+94 11 234 5678',
        'linkedin_profile': 'https://linkedin.com/in/sarahperera',
        'is_verified': True,
        'is_active': True,
        'availability_status': 'available',
        'average_rating': 4.8,
        'rating_count': 37,
    },
    {
        'name': 'Nimali Fernando',
        'expertise': 'Financial Planning & Investment',
        'years_experience': 12,
        'short_bio': 'Certified financial planner with expertise in helping women entrepreneurs manage finances and secure funding.',
        'key_focus_areas': 'Financial Planning, Investment Strategy, Funding, Budget Management',
        'industry': 'Finance',
        'business_stage_expertise': 'startup',
        'email': 'nimali.fernando@example.com',
        'phone': '+94 11 234 5679',
        'linkedin_profile': 'https://linkedin.com/in/nimalifernando',
        'is_verified': True,
        'is_active': True,
        'availability_status': 'available',
        'average_rating': 4.6,
        'rating_count': 22,
    },
]


class Command(BaseCommand):
    help = "Seed sample mentors for development"

    def handle(self, *args, **options):
        created = 0
        for data in SAMPLE_MENTORS:
            if not Mentor.objects.filter(email=data['email']).exists():
                Mentor.objects.create(**data)
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} mentor(s)."))


