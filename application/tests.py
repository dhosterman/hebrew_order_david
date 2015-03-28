from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from accounts.models import User
from application.forms import UserForm
from .validators import is_valid_tn
from .notify import on_new_user, on_updated_user


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
        self.valid_contact_data = {
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
            'mobile_phone': '123-456-7890'
        }

        self.valid_personal_data = {
            'date_of_birth_month': '1',
            'date_of_birth_day': '1',
            'date_of_birth_year': '1977',
            'city_of_birth': 'Dallas',
            'country_of_birth': 'USA',
            'married': 'on',
            'children': 'on'
        }

        self.valid_wife_data = {
            'name': 'Martha Smith',
            'hebrew_name': 'Hebrew Smith',
            'date_of_birth_month': '1',
            'date_of_birth_day': '1',
            'date_of_birth_year': '1977',
            'date_of_marriage_month': '1',
            'date_of_marriage_day': '1',
            'date_of_marriage_year': '1980',
            'email': 'wife@email.com',
            'country_of_marriage': 'USA',
            'city_of_marriage': 'Chicago',
            'mobile_phone': '123-456-7890',
        }

        self.valid_occupation_data = {
            'occupation-occupation': 'Carpenter',
            'occupation-business_name': 'Carpenters, Inc.',
            'occupation-address': '123 Main St',
            'occupation-city': 'Dallas',
            'occupation-state': 'TX',
            'occupation-zip': '12345',
            'occupation-phone': '123-456-7890'
        }

        self.valid_hod_data = {
            'synagogue_or_temple': 'Synagogue',
            'sponsor': 'Tom Thumb',
            'sponsor_phone': '123-456-7890',
            'previous_member_of_hod': '',
            'previous_lodges': '',
            'skills_or_hobbies': '',
            'other_organizations': ''
        }

        self.valid_user_data = {
            'email': 'valid@valid.com',
            'first_name': 'First',
            'last_name': 'Last'
        }

        self.valid_formset_management = {
            'children-TOTAL_FORMS': 0,
            'children-INITIAL_FORMS': 0,
            'children-MIN_NUM_FORMS': 0,
            'children-MAX_NUM_FORMS': 0,
            'committees-TOTAL_FORMS': 0,
            'committees-INITIAL_FORMS': 0,
            'committees-MIN_NUM_FORMS': 0,
            'committees-MAX_NUM_FORMS': 0
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

    def test_user_must_be_logged_in_to_view_update(self):
        url = reverse('application.views.update')
        response = self.c.post(url, self.valid_formset_management)
        expected_url = reverse('accounts.views.login_view')
        expected_url += '?next=/application/update/'
        self.assertRedirects(response, expected_url)
        self.c.login(email=self.user.email, password='test')
        response = self.c.post(url, self.valid_formset_management)
        expected_url = reverse('application.views.thank_you')
        self.assertRedirects(response, expected_url)

    # a complete application requires that an applicant enters information
    # for the User models as well as for ContactDeails, PersonalDetails,
    # and OtherDetails. If any of these models do not have the required
    # information, the form should not submit
    def test_post_saves_if_all_submissions_are_valid(self):
        valid_post_data = {}
        valid_post_data.update(self.valid_user_data)
        valid_post_data.update(self.valid_contact_data)
        valid_post_data.update(self.valid_personal_data)
        valid_post_data.update(self.valid_wife_data)
        valid_post_data.update(self.valid_occupation_data)
        valid_post_data.update(self.valid_hod_data)
        valid_post_data.update(self.valid_formset_management)
        url = reverse('application.views.post')
        expected_url = reverse('application.views.thank_you')
        response = self.c.post(url, valid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_contact_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_data)
        invalid_post_data.update(self.valid_contact_data)
        invalid_post_data.update(self.valid_personal_data)
        invalid_post_data.update(self.valid_wife_data)
        invalid_post_data.update(self.valid_occupation_data)
        invalid_post_data.update(self.valid_hod_data)
        invalid_post_data.update(self.valid_formset_management)
        invalid_post_data['home_address'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_personal_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_data)
        invalid_post_data.update(self.valid_contact_data)
        invalid_post_data.update(self.valid_personal_data)
        invalid_post_data.update(self.valid_wife_data)
        invalid_post_data.update(self.valid_occupation_data)
        invalid_post_data.update(self.valid_hod_data)
        invalid_post_data.update(self.valid_formset_management)
        invalid_post_data['date_of_birth_year'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_occupation_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_data)
        invalid_post_data.update(self.valid_contact_data)
        invalid_post_data.update(self.valid_personal_data)
        invalid_post_data.update(self.valid_wife_data)
        invalid_post_data.update(self.valid_occupation_data)
        invalid_post_data.update(self.valid_hod_data)
        invalid_post_data.update(self.valid_formset_management)
        invalid_post_data['occupation-occupation'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)
    
    def test_post_fails_if_hod_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_data)
        invalid_post_data.update(self.valid_contact_data)
        invalid_post_data.update(self.valid_personal_data)
        invalid_post_data.update(self.valid_wife_data)
        invalid_post_data.update(self.valid_occupation_data)
        invalid_post_data.update(self.valid_hod_data)
        invalid_post_data.update(self.valid_formset_management)
        invalid_post_data['sponsor'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

    def test_post_fails_if_user_invalid(self):
        invalid_post_data = {}
        invalid_post_data.update(self.valid_user_data)
        invalid_post_data.update(self.valid_contact_data)
        invalid_post_data.update(self.valid_personal_data)
        invalid_post_data.update(self.valid_wife_data)
        invalid_post_data.update(self.valid_occupation_data)
        invalid_post_data.update(self.valid_hod_data)
        invalid_post_data.update(self.valid_formset_management)
        invalid_post_data['first_name'] = ''
        url = reverse('application.views.post')
        expected_url = reverse('application.views.error')
        response = self.c.post(url, invalid_post_data)
        self.assertRedirects(response, expected_url)

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


class NotifyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            first_name = 'Steve',
            last_name = 'Smith',
            email = 'ssmith@fakeemail.com',
            password = 'password'
        )

        self.user.hebrew_name = 'Aaron'
        self.user.save()

        User.objects.create_superuser(
            first_name = 'Natasha',
            last_name = 'Romanov',
            email = 'natasha@avengers.com',
            password = 'password'
        )

    def tearDown(self):
        pass

    def test_on_new_user_subject_is_correct(self):
        expected = 'New Application'
        on_new_user(self.user)
        result = mail.outbox[0].subject
        self.assertIn(expected, result)

    def test_on_new_user_sends_proper_number(self):
        expected = 2
        on_new_user(self.user)
        result = len(mail.outbox)
        self.assertEqual(expected, result)

    def test_on_new_user_body_contains_applicant_name(self):
        expected = 'Applicant: Steve Smith'
        on_new_user(self.user)
        result = str(mail.outbox[0].message())
        self.assertIn(expected, result)

    def test_on_new_user_body_contains_applicant_email(self):
        expected = 'Email: ssmith@fakeemail.com'
        on_new_user(self.user)
        result = str(mail.outbox[0].message())
        self.assertIn(expected, result)

    def test_on_new_user_body_contains_appliant_hebrew_name(self):
        expected = 'Hebrew Name: Aaron'
        on_new_user(self.user)
        result = str(mail.outbox[0].message())
        self.assertIn(expected, result)

    def test_on_update_user_subject_is_correct(self):
        expected = 'Updated Application'
        on_updated_user(self.user, [])
        result = mail.outbox[0].subject
        self.assertIn(expected, result)

    def test_on_update_user_body_contains_applicant_name(self):
        expected = 'Applicant: Steve Smith'
        on_updated_user(self.user, [])
        result = str(mail.outbox[0].message())
        self.assertIn(expected, result)

    def test_on_update_body_contains_changed_field_names(self):
        post = {
            'first_name': 'Steve',
            'last_name': 'Smith',
            'email': 'ssmith@fakeemail.com',
            'hebrew_name': 'David'
        }
        form = UserForm(post, instance=self.user)
        form.is_valid()
        expected = '* Hebrew name: changed from Aaron to David'
        on_updated_user(self.user, [form])
        result = str(mail.outbox[0].message())
        self.assertIn(expected, result)
