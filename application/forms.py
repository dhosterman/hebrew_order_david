import datetime
from django.forms import ModelForm, Form, ModelMultipleChoiceField
from accounts.models import User
from django.forms.extras.widgets import SelectDateWidget
from .models import (Contact, Personal, Wife, Occupation, Children, Hod,
                     Committee, UserCommittee)

this_year = datetime.datetime.now().year
years = [year for year in range(this_year + 1, this_year - 100, -1)]


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
            'home_address',
            'home_city',
            'home_state',
            'home_zip',
            'postal_same_as_home',
            'postal_address',
            'postal_city',
            'postal_state',
            'postal_zip',
            'home_phone',
            'work_phone',
            'mobile_phone'
        ]


class PersonalForm(ModelForm):
    class Meta:
        model = Personal
        fields = [
            'date_of_birth',
            'city_of_birth',
            'country_of_birth',
            'married',
            'children'
        ]

        widgets = {
            'date_of_birth': SelectDateWidget(years=years),
        }


class WifeForm(ModelForm):
    class Meta:
        model = Wife
        fields = [
            'name',
            'hebrew_name',
            'date_of_birth',
            'email',
            'mobile_phone',
            'date_of_marriage',
            'country_of_marriage',
            'city_of_marriage'
        ]

        widgets = {
            'date_of_marriage': SelectDateWidget(years=years) 
        }


class OccupationForm(ModelForm):
    class Meta:
        model = Occupation
        fields = [
            'occupation',
            'business_name',
            'address',
            'city',
            'state',
            'zip',
            'phone'
        ]


class ChildrenForm(ModelForm):
    class Meta:
        model = Children
        fields = [
            'name',
            'hebrew_name',
            'date_of_birth'
        ]

        widgets = {
            'date_of_birth': SelectDateWidget(years=years) 
        }


class CurrentCommitteeForm(ModelForm):
    class Meta:
        model = UserCommittee
        fields = [
            'committee',
            'position',
            'years'
        ]


class DesiredCommitteesForm(Form):
    queryset = Committee.objects.all()
    committee = ModelMultipleChoiceField(queryset, required=False)


class HodForm(ModelForm):
    class Meta:
        model = Hod
        fields = [
            'synagogue_or_temple',
            'sponsor',
            'sponsor_phone',
            'previous_member_of_hod',
            'previous_lodges',
            'skills_or_hobbies',
            'other_organizations'
        ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'hebrew_name'
        ]
