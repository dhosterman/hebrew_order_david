from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from accounts.models import User
from .validators import is_valid_tn


# Create your tests here.
class TestTNValidation(TestCase):
    def test_valid_non_blank_tn(self):
        valid_tn = '123-456-7890'
        is_valid = is_valid_tn(valid_tn)
        self.assertEqual(is_valid, True)

    def test_non_valid_non_blank_tn(self):
        invalid_tn = '1234-345-1234'
        is_valid = is_valid_tn(invalid_tn)
        self.assertEqual(is_valid, False)

    def test_valid_blank_tn(self):
        valid_tn = ''
        is_valid = is_valid_tn(valid_tn, blank=True)
        self.assertEqual(is_valid, True)

    def test_non_valid_blank_tn(self):
        invalid_tn = ''
        is_valid = is_valid_tn(invalid_tn)
        self.assertEqual(is_valid, False)


class ApplicationViewsTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            first_name='first',
            last_name='last',
            password='test'
        )

    def tearDown(self):
        self.c.logout()

    def test_new_redirects_to_show_if_user_active(self):
        self.c.login(email=self.user.email, password='test')
        url = reverse('application.views.new')
        expected_url = reverse('application.views.show')
        response = self.c.get(url)
        self.assertRedirects(response, expected_url)

    def test_new_shows_registration_form_if_user_not_active(self):
        url = reverse('application.views.new')
        response = self.c.get(url)
        self.assertTemplateUsed(response, 'new.html')

    def test_user_must_be_logged_in_to_view_show(self):
        url = reverse('application.views.show')
        response = self.c.get(url)
        expected_url = reverse('accounts.views.login_view')
        expected_url += '?next=/application/show/'
        self.assertRedirects(response, expected_url)
        self.c.login(email=self.user.email, password='test')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_must_be_logged_in_to_view_upate(self):
        url = reverse('application.views.update')
        response = self.c.post(url)
        expected_url = reverse('accounts.views.login_view')
        expected_url += '?next=/application/update/'
        self.assertRedirects(response, expected_url)
        self.c.login(email=self.user.email, password='test')
        response = self.c.post(url)
        expected_url = reverse('application.views.thank_you')
        self.assertRedirects(response, expected_url)
