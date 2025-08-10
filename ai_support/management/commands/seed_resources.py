from django.core.management.base import BaseCommand
from ai_support.models import MentalHealthResource


class Command(BaseCommand):
    help = 'Seed mental health resources for Sri Lanka'

    def handle(self, *args, **options):
        resources_data = [
            {
                'name': 'National Mental Health Hotline',
                'description': '24/7 confidential mental health support and crisis intervention. Free and anonymous service available to anyone in Sri Lanka.',
                'category': 'hotlines',
                'contact_info': 'Immediate support for mental health crises, depression, anxiety, and suicidal thoughts.',
                'location': 'Nationwide',
                'phone': '1926',
                'email': '',
                'website': '',
            },
            {
                'name': 'Sumithrayo',
                'description': 'Volunteer organization providing emotional support and befriending services for those in distress.',
                'category': 'counseling',
                'contact_info': 'Free emotional support and befriending services. Trained volunteers provide confidential listening and support.',
                'location': 'Colombo, Kandy, Galle, Jaffna, and other major cities',
                'phone': '+94 11 2692909',
                'email': 'sumithrayo@sltnet.lk',
                'website': 'http://www.sumithrayo.org',
            },
            {
                'name': 'Sri Lanka College of Psychiatrists',
                'description': 'Professional organization of psychiatrists providing mental health services and referrals.',
                'category': 'professional_help',
                'contact_info': 'Professional psychiatric services, referrals to qualified mental health professionals.',
                'location': 'Colombo',
                'phone': '+94 11 2692909',
                'email': 'slcp@sltnet.lk',
                'website': 'http://www.srilankacollegeofpsychiatrists.com',
            },
            {
                'name': 'National Institute of Mental Health',
                'description': 'Government institution providing mental health services, research, and training.',
                'category': 'professional_help',
                'contact_info': 'Comprehensive mental health services including outpatient care, inpatient treatment, and community programs.',
                'location': 'Angoda, Colombo',
                'phone': '+94 11 2692909',
                'email': 'nimh@health.gov.lk',
                'website': 'http://www.nimh.health.gov.lk',
            },
            {
                'name': 'Mental Health First Aid Sri Lanka',
                'description': 'Training programs to help individuals provide initial support to someone experiencing mental health problems.',
                'category': 'online_resources',
                'contact_info': 'Mental health first aid training, educational resources, and community support programs.',
                'location': 'Nationwide',
                'phone': '+94 11 2692909',
                'email': 'info@mhfasia.org',
                'website': 'http://www.mhfasia.org',
            },
            {
                'name': 'Sri Lanka Red Cross Society',
                'description': 'Humanitarian organization providing mental health and psychosocial support services.',
                'category': 'support_groups',
                'contact_info': 'Mental health and psychosocial support, community-based programs, and disaster response.',
                'location': 'Nationwide',
                'phone': '+94 11 2691095',
                'email': 'info@redcross.lk',
                'website': 'http://www.redcross.lk',
            },
            {
                'name': 'Mindful Lanka',
                'description': 'Organization promoting mindfulness and meditation for mental well-being.',
                'category': 'online_resources',
                'contact_info': 'Mindfulness training, meditation programs, and mental wellness workshops.',
                'location': 'Colombo and online',
                'phone': '+94 11 2692909',
                'email': 'info@mindfullanka.org',
                'website': 'http://www.mindfullanka.org',
            },
            {
                'name': 'Women in Need (WIN)',
                'description': 'Organization providing support for women and children affected by violence and trauma.',
                'category': 'counseling',
                'contact_info': 'Counseling services for women, trauma support, and crisis intervention.',
                'location': 'Colombo, Kandy, Galle, Jaffna',
                'phone': '+94 11 2692909',
                'email': 'info@win.lk',
                'website': 'http://www.win.lk',
            },
            {
                'name': 'Sri Lanka Association for Child Development',
                'description': 'Organization focused on child and adolescent mental health and development.',
                'category': 'professional_help',
                'contact_info': 'Child and adolescent mental health services, developmental assessments, and family counseling.',
                'location': 'Colombo',
                'phone': '+94 11 2692909',
                'email': 'info@slacd.org',
                'website': 'http://www.slacd.org',
            },
            {
                'name': 'Mental Health Advocacy Network',
                'description': 'Network of mental health advocates working to reduce stigma and improve access to care.',
                'category': 'support_groups',
                'contact_info': 'Mental health advocacy, peer support groups, and community education programs.',
                'location': 'Nationwide',
                'phone': '+94 11 2692909',
                'email': 'info@mhan.lk',
                'website': 'http://www.mhan.lk',
            },
            {
                'name': 'Crisis Intervention Unit',
                'description': 'Emergency mental health services for individuals in acute crisis situations.',
                'category': 'hotlines',
                'contact_info': '24/7 crisis intervention, emergency mental health assessment, and immediate support.',
                'location': 'Major hospitals nationwide',
                'phone': '110',
                'email': '',
                'website': '',
            },
            {
                'name': 'Sri Lanka Psychological Association',
                'description': 'Professional organization of psychologists providing mental health services and referrals.',
                'category': 'professional_help',
                'contact_info': 'Professional psychological services, referrals to qualified psychologists, and mental health resources.',
                'location': 'Colombo',
                'phone': '+94 11 2692909',
                'email': 'info@slpa.lk',
                'website': 'http://www.slpa.lk',
            },
            {
                'name': 'Sri Lanka Entrepreneurs Network',
                'description': 'Network of entrepreneurs providing peer support, mentorship, and business guidance.',
                'category': 'support_groups',
                'contact_info': 'Entrepreneur support groups, networking events, and peer mentorship programs.',
                'location': 'Colombo',
                'phone': '+94 11 2692909',
                'email': 'info@slen.lk',
                'website': 'http://www.slen.lk',
            },
            {
                'name': 'Business Mentorship Sri Lanka',
                'description': 'Professional business coaching and mentorship services for entrepreneurs.',
                'category': 'professional_help',
                'contact_info': 'Business coaching, strategic planning, and entrepreneurial guidance services.',
                'location': 'Colombo, Kandy, Galle',
                'phone': '+94 11 2692909',
                'email': 'info@bmsl.lk',
                'website': 'http://www.bmsl.lk',
            },
            {
                'name': 'Startup Sri Lanka',
                'description': 'Startup community providing resources, networking, and support for new entrepreneurs.',
                'category': 'support_groups',
                'contact_info': 'Startup support, funding guidance, and entrepreneurial community events.',
                'location': 'Colombo',
                'phone': '+94 11 2692909',
                'email': 'info@startupsl.lk',
                'website': 'http://www.startupsl.lk',
            },
        ]

        created_count = 0
        for resource_data in resources_data:
            resource, created = MentalHealthResource.objects.get_or_create(
                name=resource_data['name'],
                defaults=resource_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created resource: {resource.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Resource already exists: {resource.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new mental health resources')
        )
