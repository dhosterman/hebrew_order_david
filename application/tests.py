from django.test import TestCase
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
