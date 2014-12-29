from django.test import TestCase
from .models import User


# Create your tests here.
class AccountTest(TestCase):
    def setUp(self):
        self.user = User.objects.get_or_create(
            email='testguy@test.com'
        )[0]
        self.user.set_password('test')
        self.user.save()

    def test_custom_user_model(self):
        self.assertNotEqual(self.user, None)
