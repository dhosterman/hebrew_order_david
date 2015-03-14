from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.mail import send_mail
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email address', unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    hebrew_name = models.CharField(max_length=255, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, html_message=None,
                   from_email=None, **kwargs):
        return send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [self.email],
            html_message=html_message
        )
