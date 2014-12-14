from django.shortcuts import render, redirect
from django.db import transaction
from accounts.models import User
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


@transaction.atomic
def post(request):
    user = UserForm(request.POST)
    if user.is_valid():
        user_instance = user.save(commit=False)
        password = User.objects.make_random_password(length=8)
        user_instance.set_password(password)
        user_instance.save()
    else:
        print(user.errors)

    contact_details = ContactDetailsForm(request.POST)
    if contact_details.is_valid():
        contact_details_instance = contact_details.save(commit=False)
        contact_details_instance.user = user_instance
        contact_details_instance.save()

    personal_details = PersonalDetailsForm(request.POST)
    if personal_details.is_valid():
        personal_details_instance = personal_details.save(commit=False)
        personal_details_instance.user = user_instance
        personal_details_instance.save()

    other_details = OtherDetailsForm(request.POST)
    if other_details.is_valid():
        other_details_instance = other_details.save(commit=False)
        other_details_instance.user = user_instance
        other_details_instance.save()

    return redirect('application.views.thank_you')


def thank_you(request):
    return render(request, 'thank_you.html', {})
