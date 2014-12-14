from django.shortcuts import render, redirect
from application.forms import ContactDetailsForm, PersonalDetailsForm, \
    OtherDetailsForm, UserForm


# Create your views here.
def new(request):
    return render(request, 'new.html', {
        'user_form': UserForm(),
        'contact_details_form': ContactDetailsForm(),
        'personal_details_form': PersonalDetailsForm(),
        'other_details_form': OtherDetailsForm()
    })


def post(request):
    user = UserForm(request.POST)
    if user.is_valid():
        print(user.cleaned_data)

    contact_details = ContactDetailsForm(request.POST)
    if contact_details.is_valid():
        print(contact_details.cleaned_data)

    personal_details = PersonalDetailsForm(request.POST)
    if personal_details.is_valid():
        print(personal_details.cleaned_data)

    other_details = OtherDetailsForm(request.POST)
    if other_details.is_valid():
        print(other_details.is_valid)

    return redirect('application.views.thank_you')


def thank_you(request):
    return render(request, 'thank_you.html', {})
