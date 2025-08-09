from django.test import TestCase
from django.urls import reverse
from .models import Mentor


class MentorListTests(TestCase):
    def setUp(self):
        Mentor.objects.create(
            name="A One", expertise="Biz", years_experience=5, short_bio="bio", key_focus_areas="f",
            availability_status="available", industry="Tech", business_stage_expertise="growth",
            email="a@example.com", is_verified=True, is_active=True,
        )
        Mentor.objects.create(
            name="B Two", expertise="Sales", years_experience=7, short_bio="bio", key_focus_areas="f",
            availability_status="busy", industry="Finance", business_stage_expertise="startup",
            email="b@example.com", is_verified=True, is_active=True,
        )

    def test_list_page_ok(self):
        resp = self.client.get(reverse('mentors:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Our Expert Mentors")

    def test_search_filters(self):
        resp = self.client.get(reverse('mentors:list'), {"search": "Sales"})
        self.assertContains(resp, "B Two")
        self.assertNotContains(resp, "A One")


class MentorDetailTests(TestCase):
    def setUp(self):
        self.mentor = Mentor.objects.create(
            name="Detail Test", expertise="Marketing", years_experience=10, short_bio="bio", key_focus_areas="f",
            availability_status="available", industry="Tech", business_stage_expertise="growth",
            email="detail@example.com", is_verified=True, is_active=True,
        )

    def test_detail_page_ok(self):
        resp = self.client.get(reverse('mentors:detail', args=[self.mentor.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Detail Test")
