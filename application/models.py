from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from .validators import is_valid_tn


# Create your models here.
class Contact(models.Model):
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

    def clean(self):
        if not is_valid_tn(self.home_phone):
            raise ValidationError('Home phone must be a valid phone number.')
        if not is_valid_tn(self.mobile_phone):
            raise ValidationError('Mobile phone must be a valid phone number.')
        if not is_valid_tn(self.work_phone):
            raise ValidationError('Work phone must be a valid phone number.')
        self.postal_state = self.postal_state.upper()
        self.home_state = self.home_state.upper()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Contact'


class Personal(models.Model):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    city_of_birth = models.CharField(max_length=255)
    country_of_birth = models.CharField(max_length=255)
    married = models.BooleanField(default=False)
    children = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Personal'


class Wife(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=255, blank=True)
    hebrew_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_marriage = models.DateField(null=True, blank=True)
    country_of_marriage = models.CharField(max_length=255, blank=True)
    city_of_marriage = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.email

    def clean(self):
        if not is_valid_tn(self.mobile_phone, blank=True):
            print(self.mobile_phone)
            raise ValidationError('Mobile phone must be a valid phone number.')


class Occupation(models.Model):
    user = models.OneToOneField(User)
    occupation = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.PositiveIntegerField()
    phone = models.CharField(max_length=20, blank=True)

    def clean(self):
        if not is_valid_tn(self.phone, blank=True):
            raise ValidationError('Phone must be a valid phone number.')
        self.state = self.state.upper()

    def __str__(self):
        return self.user.email


class Children(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    hebrew_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name + ' '+ self.user.last_name


class Hod(models.Model):
    user = models.OneToOneField(User)
    synagogue_or_temple = models.CharField(max_length=255, blank=True)
    sponsor = models.CharField(max_length=255)
    sponsor_phone = models.CharField(max_length=20, blank=True)
    previous_member_of_hod = models.BooleanField(default=False,
        verbose_name='Previous member of HOD')
    previous_lodges = models.CharField(max_length=255, blank=True)
    skills_or_hobbies = models.TextField(blank=True)
    other_organizations = models.TextField(blank=True)
    
    def clean(self):
        if not is_valid_tn(self.sponsor_phone, blank=True):
            raise ValidationError('Sponsor phone must be a valid phone number.')

    def __str__(self):
        return self.user.email


class Committee(models.Model):
    members = models.ManyToManyField(User, through='UserCommittee', through_fields=('committee', 'user'))
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserCommittee(models.Model):
    user = models.ForeignKey(User)
    committee = models.ForeignKey(Committee)
    position = models.CharField(max_length=255)
    current = models.BooleanField(default=False)
    years = models.PositiveIntegerField()

    def __str__(self):
        return self.user.email + ':' + self.committee.name


class Legal(models.Model):
    terms_and_conditions = models.TextField()
    privacy_policy = models.TextField()
