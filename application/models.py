from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from .validators import is_valid_tn


# Create your models here.
class ContactDetails(models.Model):
    user = models.OneToOneField(User)
    home_address = models.CharField(max_length=255)
    home_city = models.CharField(max_length=255)
    home_state = models.CharField(max_length=2)
    home_zip = models.PositiveIntegerField()
    postal_same_as_home = models.BooleanField(default=True)
    postal_address = models.CharField(max_length=255, blank=True)
    postal_city = models.CharField(max_length=255, blank=True)
    postal_state = models.CharField(max_length=2, blank=True)
    postal_zip = models.PositiveIntegerField(blank=True, null=True)
    home_phone = models.CharField(max_length=20)
    work_phone = models.CharField(max_length=20)
    mobile_phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_city = models.CharField(max_length=255)
    business_state = models.CharField(max_length=2)
    business_zip = models.PositiveIntegerField()

    def clean(self):
        if not is_valid_tn(self.home_phone):
            raise ValidationError('Home phone must be a valid phone number.')
        if not is_valid_tn(self.mobile_phone):
            raise ValidationError('Mobile phone must be a valid phone number.')
        if not is_valid_tn(self.work_phone):
            raise ValidationError('Work phone must be a valid phone number.')
        if not is_valid_tn(self.fax, blank=True):
            raise ValidationError('Fax number must be a valid phone number.')
        self.postal_state = self.postal_state.upper()
        self.home_state = self.home_state.upper()
        self.business_state = self.business_state.upper()

    class Meta:
        verbose_name = 'Contact Detail'


class PersonalDetails(models.Model):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    city_of_birth = models.CharField(max_length=255)
    country_of_birth = models.CharField(max_length=255)
    date_of_marriage = models.DateField(blank=True, null=True)
    wife_name = models.CharField(max_length=255, blank=True)
    wife_email = models.EmailField(max_length=254, blank=True)
    country_where_married = models.CharField(max_length=255, blank=True)
    wife_mobile_phone = models.CharField(max_length=20, blank=True)

    def clean(self):
        if not is_valid_tn(self.wife_mobile_phone, blank=True):
            raise ValidationError("Wife's mobile phone must be a valid " +
                                  "phone number.")

    class Meta:
        verbose_name = 'Personal Detail'


class OtherDetails(models.Model):
    user = models.OneToOneField(User)
    sponsor = models.CharField(max_length=255)
    previous_member_of_hod = models.BooleanField(default=False,
        verbose_name='Previous member of HOD')
    previous_lodges = models.CharField(max_length=255, blank=True)
    relatives_member_of_hod = models.BooleanField(default=False,
        verbose_name='Relatives member of HOD')
    relatives_names_and_mother_lodges = models.TextField(blank=True)
    member_of_other_organizations = models.BooleanField(default=False)
    other_organizations = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Other Detail'
