from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from poll.models import Poll


# Create your tests here.
class PollTest(TestCase):
    """Test that model Poll functions properly."""
    def setUp(self):
        self.user = User.objects.get_or_create(
            username='testguy',
            email='testguy@test.com'
        )[0]
        self.user.set_password('test')
        self.user.save()

    def test_that_poll_saves(self):
        poll = Poll(
            user=self.user,
            home_phone='123-456-7890',
            cell_phone='987-654-3210',
            street_address='123 Main St',
            city='Dallas',
            state='TX',
            zip_code=75205,
            birthdate=now().date()
        )
        poll.save()

        self.assertNotEqual(poll.pk, None)

    def test_phone_number_validation(self):
        poll = Poll(
            user=self.user,
            home_phone='123456-7890',
            cell_phone='987-654-3210',
            street_address='123 Main St',
            city='Dallas',
            state='TX',
            zip_code=75205,
            birthdate=now().date()
        )
        self.assertRaises(ValidationError, poll.clean)
        poll.home_phone = '23-456-7890'
        self.assertRaises(ValidationError, poll.clean)
        poll.home_phone = '123-456-789A'
        self.assertRaises(ValidationError, poll.clean)
        poll.home_phone = '123-456-7890'
        self.assertEquals(poll.clean(), None)
