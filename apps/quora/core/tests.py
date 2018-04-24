from django.test import TestCase
from .models import User

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': "demo",
            'email': 'demo@gmail.com',
            'password': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        User.objects.create_user(**self.credentials)

    def test_register(self):
        response = self.client.post('/core/register/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        user = User.objects.get(username="demo")
        self.assertEqual(user.username, "demo")