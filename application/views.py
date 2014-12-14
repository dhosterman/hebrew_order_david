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
    return redirect('poll.views.new')
