from django.contrib import admin
from .models import User
from application.models import ContactDetails, PersonalDetails, OtherDetails


# Register your models here.
class ContactDetailsInline(admin.StackedInline):
    model = ContactDetails


class PersonalDetailsInline(admin.StackedInline):
    model = PersonalDetails


class OtherDetailsInline(admin.StackedInline):
    model = OtherDetails


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ContactDetailsInline,
        PersonalDetailsInline,
        OtherDetailsInline
    ]

admin.site.register(User, UserAdmin)
