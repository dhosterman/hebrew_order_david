from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from accounts.models import User
from application.forms import ContactDetailsForm, PersonalDetailsForm, \
    OtherDetailsForm, UserForm


# Create your views here.
def new(request):
    if request.user.is_active:
        return redirect('application.views.show')
    else:
        return render(request, 'new.html', {
            'user_form': UserForm(),
            'contact_details_form': ContactDetailsForm(),
            'personal_details_form': PersonalDetailsForm(),
            'other_details_form': OtherDetailsForm()
        })


@login_required(login_url='/accounts/login/')
def show(request):
    user = request.user
    contact_details = user.contactdetails_set.first()
    personal_details = user.personaldetails_set.first()
    other_details = user.otherdetails_set.first()
    return render(request, 'new.html', {
        'user_form': UserForm(instance=user),
        'contact_details_form': ContactDetailsForm(instance=contact_details),
        'personal_details_form': PersonalDetailsForm(instance=personal_details),
        'other_details_form': OtherDetailsForm(instance=other_details)
    })


@login_required(login_url='/accounts/login')
@transaction.atomic
def update(request):
    user_details = request.user
    contact_details = user_details.contactdetails_set.first()
    personal_details = user_details.personaldetails_set.first()
    other_details = user_details.otherdetails_set.first()

    user = UserForm(request.POST, instance=user_details)
    if user.is_valid():
        user.save()

    contact = ContactDetailsForm(request.POST, instance=contact_details)
    if contact.is_valid():
        contact.save()

    personal = PersonalDetailsForm(request.POST, instance=personal_details)
    if personal.is_valid():
        personal.save()

    other = OtherDetailsForm(request.POST, instance=other_details)
    if other.is_valid():
        other.save()

    return redirect('application.views.thank_you')


@transaction.atomic
def post(request):
    user = UserForm(request.POST)
    if user.is_valid():
        user_instance = user.save(commit=False)
        password = User.objects.make_random_password(length=8)
        user_instance.set_password(password)
        user_instance.save()

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
