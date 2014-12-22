from django.forms import ModelForm
from accounts.models import User
from django.forms.extras.widgets import SelectDateWidget
from .models import ContactDetails, PersonalDetails, OtherDetails


class ContactDetailsForm(ModelForm):
    class Meta:
        model = ContactDetails
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
            'mobile_phone',
            'fax',
            'occupation',
            'business_name',
            'business_address',
            'business_city',
            'business_state',
            'business_zip'
        ]


class PersonalDetailsForm(ModelForm):
    class Meta:
        model = PersonalDetails
        fields = [
            'date_of_birth',
            'city_of_birth',
            'country_of_birth',
            'date_of_marriage',
            'wife_name',
            'wife_email',
            'place_of_marriage',
            'wife_mobile_phone'
        ]

        widgets = {
            'date_of_birth': SelectDateWidget(),
            'date_of_marriage': SelectDateWidget()
        }


class OtherDetailsForm(ModelForm):
    class Meta:
        model = OtherDetails
        fields = [
            'previous_member_of_hodi',
            'previous_lodges',
            'relatives_member_of_hodi',
            'relatives_names_and_mother_lodges',
            'member_of_other_organizations',
            'other_organizations'
        ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]
