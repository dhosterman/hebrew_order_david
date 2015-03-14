from django.contrib import admin
from .models import User
from application.models import Contact, Personal, Wife


# Register your models here.
class ContactInline(admin.StackedInline):
    model = Contact


class PersonalInline(admin.StackedInline):
    model = Personal


class WifeInline(admin.StackedInline):
    model = Wife


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline,
        PersonalInline,
        WifeInline
    ]

admin.site.register(User, UserAdmin)
admin.site.site_header = 'Hebrew Order of David Administration'
