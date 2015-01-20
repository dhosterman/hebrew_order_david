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

        # all of this data must pass all validations in post view
        self.valid_contact_details_data = {
            'home_address': '123 Main St',
            'home_city': 'Dallas',
            'home_state': 'TX',
            'home_zip': '12345',
            'postal_same_as_home': 'on',
            'postal_address': '',
            'postal_city': '',
            'postal_state': '',
            'postal_zip': '',
            'home_phone': '123-456-7890',
            'work_phone': '123-456-7890',
            'mobile_phone': '123-456-7890',
            'fax': '',
            'occupation': 'CEO',
            'business_name': 'Business, LLC',
            'business_address': '123 Main St',
            'business_city': 'Dallas',
            'business_state': 'TX',
            'business_zip': '12345'
        }

        self.valid_personal_details_data = {
            'date_of_birth_month': '1',
            'date_of_birth_day': '1',
            'date_of_birth_year': '1977',
            'city_of_birth': 'Dallas',
            'country_of_birth': 'USA',
            'date_of_marriage_month': '0',
            'date_of_marriage_day': '0',
            'date_of_marriage_year': '0',
            'wife_name': '',
            'wife_email': '',
            'place_of_marriage': '',
            'wife_mobile_phone': '',
        }

        self.valid_other_details_data = {
            'previous_member_of_hodi': '',
            'previous_lodges': '',
            'relatives_member_of_hodi': '',
            'relatives_names_and_mother_lodges': '',
            'member_of_other_organizations': '',
            'other_organizations': ''
        }

        self.valid_user_details_data = {
            'email': 'valid@valid.com',
            'first_name': 'First',
            'last_name': 'Last'
        }

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

    # a complete application requires that an applicant enters information
    # for the User models as well as for ContactDetails, PersonalDetails,
    # and OtherDetails. If any of these models do not have the required
    # information, the form should not submit
    def test_post_saves_if_all_submissions_are_valid(self):
        valid_post_data = {}
        valid_post_data.update(self.valid_user_details_data)
        valid_post_data.update(self.valid_other_details_data)
        valid_post_data.update(self.valid_contact_details_data)
        valid_post_data.update(self.valid_personal_details_data)
        url = reverse('application.views.post')
        expected_url = reverse('application.views.thank_you')
        response = self.c.post(url, valid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_contact_details_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_details_data)
        invalid_post_data.update(self.valid_other_details_data)
        invalid_post_data.update(self.valid_contact_details_data)
        invalid_post_data.update(self.valid_personal_details_data)
        invalid_post_data['home_address'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_personal_details_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_details_data)
        invalid_post_data.update(self.valid_other_details_data)
        invalid_post_data.update(self.valid_contact_details_data)
        invalid_post_data.update(self.valid_personal_details_data)
        invalid_post_data['date_of_birth_year'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_user_details_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_details_data)
        invalid_post_data.update(self.valid_other_details_data)
        invalid_post_data.update(self.valid_contact_details_data)
        invalid_post_data.update(self.valid_personal_details_data)
        invalid_post_data['first_name'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_other_details_invalid(self):
        # there are no required values for validation in this form/model yet
        pass

    def test_user_must_be_logged_in_and_staff_to_export_excel(self):
        staff_user = User.objects.create_superuser(
            email='staff@user.com',
            first_name='Staff',
            last_name='User',
            password='test',
        )
        url = reverse('application.views.export_as_excel')
        expected_url = reverse('accounts.views.login_view')
        expected_url += '?next=/application/export_excel/'
        self.c.login(email=self.user.email, password='test')
        response = self.c.get(url)
        self.assertRedirects(response, expected_url)
        self.c.login(email=staff_user.email, password='test')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
