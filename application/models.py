from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from .validators import is_valid_tn


# Create your models here.
class ContactDetails(models.Model):
    user = models.ForeignKey(User)
    home_address = models.CharField(max_length=255, blank=True)
    home_city = models.CharField(max_length=255, blank=True)
    home_state = models.CharField(max_length=2, blank=True)
    home_zip = models.PositiveIntegerField(blank=True)
    postal_address = models.CharField(max_length=255, blank=True)
    postal_city = models.CharField(max_length=255, blank=True)
    postal_state = models.CharField(max_length=2, blank=True)
    postal_zip = models.PositiveIntegerField(blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    work_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    business_name = models.CharField(max_length=255, blank=True)
    business_address = models.CharField(max_length=255, blank=True)
    business_city = models.CharField(max_length=255, blank=True)
    business_state = models.CharField(max_length=2, blank=True)
    business_zip = models.PositiveIntegerField(blank=True)

    def clean(self):
        if not is_valid_tn(self.home_phone):
            raise ValidationError('Home phone must be a valid phone number.')
        if not is_valid_tn(self.mobile_phone):
            raise ValidationError('Mobile phone must be a valid phone number.')
        if not is_valid_tn(self.work_phone):
            raise ValidationError('Work phone must be a valid phone number.')
        if not is_valid_tn(self.fax):
            raise ValidationError('Fax number must be a valid phone number.')
        self.postal_state = self.postal_state.upper()
        self.home_state = self.home_state.upper()
        self.business_state = self.business_state.upper()


class PersonalDetails(models.Model):
    user = models.ForeignKey(User)
    date_of_birth = models.DateField()
    city_of_birth = models.CharField(max_length=255, blank=True)
    country_of_birth = models.CharField(max_length=255, blank=True)
    is_jewish = models.BooleanField(default=False, blank=True)
    is_married = models.BooleanField(default=False, blank=True)
    date_of_marriage = models.DateField(blank=True)
    wife_name = models.CharField(max_length=255, blank=True)
    wife_email = models.EmailField(max_length=254, blank=True)
    place_of_marriage = models.CharField(max_length=255, blank=True)
    wife_mobile_phone = models.CharField(max_length=20, blank=True)

    def clean(self):
        if not is_valid_tn(self.wife_mobile_phone):
            raise ValidationError("Wife's mobile phone must be a valid " +
                                  "phone number.")


class OtherDetails(models.Model):
    user = models.ForeignKey(User)
    previous_member_of_hodi = models.BooleanField(default=False)
    previous_lodges = models.CharField(max_length=255, blank=True)
    relatives_member_of_hodi = models.BooleanField(default=False)
    relatives_names_and_mother_lodges = models.TextField(blank=True)
    member_of_other_organizations = models.BooleanField(default=False)
    other_organizations = models.TextField(blank=True)
