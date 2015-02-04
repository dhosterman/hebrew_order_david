from io import BytesIO
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User
from .models import ContactDetails, PersonalDetails, OtherDetails
from .forms import ContactDetailsForm, PersonalDetailsForm, \
    OtherDetailsForm, UserForm
import xlsxwriter


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
    try:
        contact_details = user.contactdetails
    except ObjectDoesNotExist:
        contact_details = ContactDetails(user=user)
    try:
        personal_details = user.personaldetails
    except ObjectDoesNotExist:
        personal_details = PersonalDetails(user=user)
    try:
        other_details = user.otherdetails
    except ObjectDoesNotExist:
        other_details = OtherDetails(user=user)
    return render(request, 'new.html', {
        'user_form': UserForm(instance=user),
        'contact_details_form': ContactDetailsForm(instance=contact_details),
        'personal_details_form': PersonalDetailsForm(instance=personal_details),
        'other_details_form': OtherDetailsForm(instance=other_details)
    })


@login_required(login_url='/accounts/login/')
@transaction.atomic
def update(request):
    user_details = request.user
    try:
        contact_details = user_details.contactdetails
    except ObjectDoesNotExist:
        contact_details = ContactDetails(user=request.user)
    try:
        personal_details = user_details.personaldetails
    except ObjectDoesNotExist:
        personal_details = PersonalDetails(user=request.user)
    try:
        other_details = user_details.otherdetails
    except ObjectDoesNotExist:
        other_details = OtherDetails(user=request.user)

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
    submission_valid = False
    if user.is_valid():
        user_instance = user.save(commit=False)
        password = User.objects.make_random_password(length=8)
        user_instance.set_password(password)
        submission_valid = True
    else:
        submission_valid = False

    contact_details = ContactDetailsForm(request.POST)
    if contact_details.is_valid() and user.is_valid() and submission_valid:
        contact_details_instance = contact_details.save(commit=False)
        submission_valid = True
    else:
        submission_valid = False

    personal_details = PersonalDetailsForm(request.POST)
    if personal_details.is_valid() and user.is_valid() and submission_valid:
        personal_details_instance = personal_details.save(commit=False)
        submission_valid = True
    else:
        submission_valid = False

    other_details = OtherDetailsForm(request.POST)
    if other_details.is_valid() and user.is_valid() and submission_valid:
        other_details_instance = other_details.save(commit=False)
        submission_valid = True
    else:
        submission_valid = False

    if submission_valid:
        user_instance.save()
        contact_details_instance.user = user_instance
        contact_details_instance.save()
        personal_details_instance.user = user.instance
        personal_details_instance.save()
        other_details_instance.user = user.instance
        other_details_instance.save()
        message = "Welcome to HoD Shimon Peres! "
        message += "If you want to view or change the information you "
        message += "submitted, please log in using your email address "
        message += "and the password: "
        message += password
        user_instance.email_user('Welcome!', message)
        return redirect('application.views.thank_you')

    else:
        return redirect('application.views.error')


def thank_you(request):
    return render(request, 'thank_you.html', {})


def error(request):
    return render(request, 'error.html', {})


def is_staff(user):
    return user.is_staff or user.is_admin or user.is_superuser


@user_passes_test(is_staff, login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def export_as_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'mm/dd/yy'})

    # tuples of column names, model field names
    columns = [
        ('First Name', 'first_name'),
        ('Last Name', 'last_name'),
        ('Email', 'email'),
        ('Home Address', 'contactdetails__home_address'),
        ('City', 'contactdetails__home_city'),
        ('State', 'contactdetails__home_state'),
        ('Zip', 'contactdetails__home_zip'),
        ('Postal Address', 'contactdetails__postal_address'),
        ('City', 'contactdetails__postal_city'),
        ('State', 'contactdetails__postal_state'),
        ('Zip', 'contactdetails__postal_zip'),
        ('Home Phone', 'contactdetails__home_phone'),
        ('Work Phone', 'contactdetails__work_phone'),
        ('Mobile Phone', 'contactdetails__mobile_phone'),
        ('Fax', 'contactdetails__fax'),
        ('Occupation', 'contactdetails__occupation'),
        ('Business Name', 'contactdetails__business_name'),
        ('Business Address', 'contactdetails__business_address'),
        ('City', 'contactdetails__business_city'),
        ('State', 'contactdetails__business_state'),
        ('Zip', 'contactdetails__business_zip'),
        ('Birth Date', 'personaldetails__date_of_birth'),
        ('Birth City', 'personaldetails__city_of_birth'),
        ('Country', 'personaldetails__country_of_birth'),
        ('Marriage Date', 'personaldetails__date_of_marriage'),
        ("Wife's Name", 'personaldetails__wife_name'),
        ("Wife's Email", 'personaldetails__wife_email'),
        ('Place of Marriage', 'personaldetails__place_of_marriage'),
        ("Wife's Mobile Phone", 'personaldetails__wife_mobile_phone'),
        ('Previous Member?', 'otherdetails__previous_member_of_hodi'),
        ('Previous Lodges', 'otherdetails__previous_lodges'),
        ('Relatives?', 'otherdetails__relatives_member_of_hodi'),
        ('Relatives', 'otherdetails__relatives_names_and_mother_lodges'),
        ('Other Orgs?', 'otherdetails__member_of_other_organizations'),
        ('Other Orgs', 'otherdetails__other_organizations')
    ]

    normal_users = User.objects.exclude(is_staff=True).exclude(is_superuser=True)
    applications = normal_users.select_related().values_list(
        *[x[1] for x in columns])

    row = 0
    col = 0
    for key in [x[0] for x in columns]:
        worksheet.write(row, col, key)
        col += 1
    col = 0
    row = 1
    for application in applications:
        for value in application:
            if type(value) == datetime.date:
                worksheet.write_datetime(row, col, value, date_format)
            else:
                worksheet.write(row, col, value)
            col += 1
        col = 0
        row += 1

    workbook.close()

    output.seek(0)
    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(output.read(), content_type=mime)
    response['Content-Disposition'] = "attachment; filename=applications.xlsx"

    return response
