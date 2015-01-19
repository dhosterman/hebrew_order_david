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


class AccountsModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            first_name='first',
            last_name='last',
            password='password'
        )

    def test_create_user_creates_valid_user(self):
        self.assertEquals(self.user.is_active, True)
        self.assertNotEqual(self.user.is_staff, True)
        self.assertNotEqual(self.user.is_admin, True)

    def test_create_superuser_creates_valid_superuser(self):
        superuser = User.objects.create_superuser(
            email='super@user.com',
            first_name='first',
            last_name='last',
            password='password'
        )
        self.assertEquals(superuser.is_active, True)
        self.assertEquals(superuser.is_staff, True)
        self.assertEquals(superuser.is_admin, True)

    def test_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                first_name='first',
                last_name='last',
                password='password'
            )

    def test_user_unicode_returns_email_address(self):
        self.assertEquals(self.user.__unicode__(), 'test@test.com')

    def test_user_get_short_name_returns_first_name(self):
        self.assertEquals(self.user.get_short_name(), 'first')

