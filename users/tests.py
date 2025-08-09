from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class SignupAndVerifyTests(TestCase):
    def test_signup_page_renders(self):
        resp = self.client.get(reverse('users:signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Create your account')

    def test_email_verify_flow(self):
        user = User.objects.create_user(username='v', email='v@example.com', password='x', is_active=False)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        resp = self.client.get(reverse('users:verify', args=[uid, token]))
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
from django.test import TestCase

# Create your tests here.
