from django.contrib import admin
from .models import User
from application.models import (Contact, Personal, Wife, Occupation, Children,
                                Hod, Committee, UserCommittee, Legal)


# Register your models here.
class ContactInline(admin.StackedInline):
    model = Contact


class PersonalInline(admin.StackedInline):
    model = Personal


class WifeInline(admin.StackedInline):
    model = Wife


class OccupationInline(admin.StackedInline):
    model = Occupation


class HodInline(admin.StackedInline):
    model = Hod


class ChildrenInline(admin.StackedInline):
    model = Children


class UserCommitteeInline(admin.StackedInline):
    model = UserCommittee


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline,
        PersonalInline,
        WifeInline,
        OccupationInline,
        HodInline,
        ChildrenInline,
        UserCommitteeInline
    ]

class LegalAdmin(admin.ModelAdmin):
    model = Legal

admin.site.register(User, UserAdmin)
admin.site.register(Legal, LegalAdmin)
admin.site.site_header = 'Hebrew Order of David Administration'
