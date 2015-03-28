from io import BytesIO
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import User
from application import notify
from .models import (Contact, Personal, Wife, Occupation, Children, Hod,
                     UserCommittee, Committee, Legal)
from .forms import (ContactForm, PersonalForm, WifeForm, OccupationForm,
                    ChildrenForm, HodForm, UserForm, CurrentCommitteeForm,
                    DesiredCommitteesForm)
import xlsxwriter


# Create your views here.
def new(request):
    if request.user.is_active:
        return redirect('application.views.show')
    else:
        ChildrenFormset = formset_factory(ChildrenForm, extra=0, can_delete=True)
        CurrentCommitteesFormset = formset_factory(CurrentCommitteeForm,
                                                     extra=0, can_delete=True)
        children_formset = ChildrenFormset(prefix='children')
        current_committees_formset = CurrentCommitteesFormset(prefix='committees')
        return render(request, 'new.html', {
            'user_form': UserForm(),
            'contact_form': ContactForm(),
            'personal_form': PersonalForm(),
            'wife_form': WifeForm(prefix="wife"),
            'occupation_form': OccupationForm(prefix="occupation"),
            'children_formset': children_formset,
            'hod_form': HodForm(),
            'current_committees_formset': current_committees_formset,
            'desired_committees_form': DesiredCommitteesForm(),
            'pills': 'inactive',
            'data_toggle': 'none',
            'legal': Legal.objects.first()
        })


@login_required(login_url='/accounts/login/')
def show(request):
    user = request.user
    try:
        contact = user.contact
    except ObjectDoesNotExist:
        contact = Contact(user=user)
    try:
        personal = user.personal
    except ObjectDoesNotExist:
        personal = Personal(user=user)
    try:
        wife = user.wife
    except ObjectDoesNotExist:
        wife = Wife(user=user)
    try:
        occupation = user.occupation
    except ObjectDoesNotExist:
        occupation = Occupation(user=user)
    try:
        hod = user.hod
    except ObjectDoesNotExist:
        hod = Hod(user=user)

    this_year = datetime.datetime.now().year
    years = [year for year in range(this_year + 1, this_year - 100, -1)]
    widgets = {'date_of_birth': SelectDateWidget(years=years)}
    ChildrenFormset = modelformset_factory(Children, extra=0, can_delete=True,
                                           exclude=['user'],
                                           widgets=widgets)
    children = user.children_set.all().values()
    CurrentCommitteesFormset = modelformset_factory(UserCommittee,
                                                    extra=0, can_delete=True,
                                                    exclude=['user', 'current'])
    committees = user.usercommittee_set.all().values()
    children_formset = ChildrenFormset(prefix='children', initial=children,
                                       queryset=user.children_set.all())
    current_committees_formset = CurrentCommitteesFormset(prefix='committees',
                                                          initial=committees,
                                                          queryset=user.usercommittee_set.all())   
    return render(request, 'new.html', {
        'user_form': UserForm(instance=user),
        'contact_form': ContactForm(instance=contact),
        'personal_form': PersonalForm(instance=personal),
        'wife_form': WifeForm(instance=wife, prefix='wife'),
        'occupation_form': OccupationForm(instance=occupation,
                                          prefix='occupation'),
        'hod_form': HodForm(instance=hod),
        'current_committees_formset': current_committees_formset,
        'children_formset': children_formset,
        'desired_committees_form': DesiredCommitteesForm(),
        'pills': 'active',
        'data_toggle': 'tab' 
    })


@login_required(login_url='/accounts/login/')
@transaction.atomic
def update(request):
    user_instance = request.user
    updated_forms = []
    try:
        contact_instance = user_instance.contact
    except ObjectDoesNotExist:
        contact_instance = Contact(user=request.user)
    try:
        personal_instance = user_instance.personal
    except ObjectDoesNotExist:
        personal_instance = Personal(user=request.user)
    try:
        wife_instance = user_instance.wife
    except ObjectDoesNotExist:
        wife_instance = Wife(user=request.user)
    try:
        occupation_instance = user_instance.occupation
    except ObjectDoesNotExist:
        occupation_instance = Occupation(user=request.user)
    try:
        hod_instance = user_instance.hod
    except ObjectDoesNotExist:
        hod_instance = Hod(user=request.user)

    user = UserForm(request.POST, instance=user_instance)
    if user.is_valid() and user.changed_data:
        updated_forms.append(user)
        user.save()

    contact = ContactForm(request.POST, instance=contact_instance)
    if contact.is_valid() and contact.changed_data:
        updated_forms.append(contact)
        contact.save()
    else:
        print(contact.errors)

    personal = PersonalForm(request.POST, instance=personal_instance)
    if personal.is_valid() and personal.changed_data:
        updated_forms.append(personal)
        personal.save()

    wife = WifeForm(request.POST, instance=wife_instance, prefix='wife')
    if wife.is_valid() and wife.changed_data:
        updated_forms.append(wife)
        wife.save()
    
    occupation = OccupationForm(request.POST, instance=occupation_instance,
                                prefix='occupation')
    if occupation.is_valid() and occupation.changed_data:
        updated_forms.append(occupation)
        occupation.save()
    
    hod = HodForm(request.POST, instance=hod_instance)
    if hod.is_valid() and hod.changed_data:
        updated_forms.append(hod)
        hod.save()

    ChildrenFormset = modelformset_factory(Children, exclude=['user'],
                                           can_delete=True)
    children_formset = ChildrenFormset(request.POST, prefix='children')
    if children_formset.is_valid():
        for child in children_formset:
            if child not in children_formset.deleted_forms and child.changed_data:
                updated_forms.append(child)
                child_instance = child.save(commit=False)
                child_instance.user = user_instance
                child_instance.save()
        for child in children_formset.deleted_forms:
            child_instance = child.save(commit=False)
            if child_instance.id:
                child_instance.delete()
    else:
        print(children_formset.errors)
        
    CurrentCommitteesFormset = modelformset_factory(UserCommittee,
                                                    exclude=['user'],
                                                    can_delete=True)
    committees_formset = CurrentCommitteesFormset(request.POST,
                                                  prefix='committees')
    if committees_formset.is_valid():
        for committee in committees_formset:
            if committee not in committees_formset.deleted_forms and committee.changed_data:
                updated_forms.append(committee)
                committee_instance = committee.save(commit=False)
                committee_instance.user = user_instance
                committee_instance.current = True
                committee_instance.save()
        for committee in committees_formset.deleted_forms:
            committee_instance = committee.save(commit=False)
            if committee_instance.id:
                committee_instance.delete()
    else:
        print(committees_formset.errors)

    notify.on_updated_user(user_instance, updated_forms)
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
        print('user')
        print(user.errors)
        submission_valid = False

    contact = ContactForm(request.POST)
    if contact.is_valid() and user.is_valid() and submission_valid:
        contact_instance = contact.save(commit=False)
        submission_valid = True
    else:
        print('contact')
        print(contact.errors)
        submission_valid = False

    personal = PersonalForm(request.POST)
    if personal.is_valid() and user.is_valid() and submission_valid:
        personal_instance = personal.save(commit=False)
        submission_valid = True
    else:
        print('personal')
        print(personal.errors)
        submission_valid = False

    wife = WifeForm(request.POST, prefix='wife')
    if wife.is_valid() and user.is_valid() and submission_valid:
        wife_instance = wife.save(commit=False)
        submission_valid = True
    else:
        print('wife')
        print(wife.errors)
        submission_valid = False

    occupation = OccupationForm(request.POST, prefix='occupation')
    if occupation.is_valid() and user.is_valid() and submission_valid:
        occupation_instance = occupation.save(commit=False)
        submission_valid = True
    else:
        print('occupation')
        print(occupation.errors)
        submission_valid = False

    hod = HodForm(request.POST)
    if hod.is_valid() and user.is_valid() and submission_valid:
        hod_instance = hod.save(commit=False)
        submission_valid = True
    else:
        print('hod')
        print(hod.errors)
        submission_valid = False

    ChildrenFormset = formset_factory(ChildrenForm)
    children_formset = ChildrenFormset(request.POST, prefix='children')
    if children_formset.is_valid() and user.is_valid() and submission_valid:
        submission_valid = True
    else:
        print('children')
        print(children_formset.errors)
        submission_valid = False

    CurrentCommitteesFormset = formset_factory(CurrentCommitteeForm)
    committees_formset = CurrentCommitteesFormset(request.POST, prefix='committees')
    if committees_formset.is_valid() and user.is_valid() and submission_valid:
        submission_valid = True
    else:
        print('committees')
        print(committees_formset.errors)
        submission_valid = False

    if submission_valid:
        user.save()
        contact_instance.user = user_instance
        contact_instance.save()
        personal_instance.user = user.instance
        personal_instance.save()
        wife_instance.user = user.instance
        wife_instance.save()
        occupation_instance.user = user.instance
        occupation_instance.save()
        hod_instance.user = user.instance
        hod_instance.save()
        for child in children_formset:
            child_instance = child.save(commit=False)
            child_instance.user = user_instance
            child_instance.save()
        for committee in committees_formset:
            committee_instance = committee.save(commit=False)
            committee_instance.user = user_instance
            committee_instance.save()
        message = "Welcome to HoD Shimon Peres! "
        message += "If you want to view or change the information you "
        message += "submitted, please log in using your email address "
        message += "and the password: "
        message += password
        user_instance.email_user('Welcome!', message)
        notify.on_new_user(user_instance)
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
        ('Hebrew Name', 'hebrew_name'),
        ('Email', 'email'),
        ('Home Address', 'contact__home_address'),
        ('City', 'contact__home_city'),
        ('State', 'contact__home_state'),
        ('Zip', 'contact__home_zip'),
        ('Postal Address', 'contact__postal_address'),
        ('City', 'contact__postal_city'),
        ('State', 'contact__postal_state'),
        ('Zip', 'contact__postal_zip'),
        ('Home Phone', 'contact__home_phone'),
        ('Work Phone', 'contact__work_phone'),
        ('Mobile Phone', 'contact__mobile_phone'),
        ('Birth Date', 'personal__date_of_birth'),
        ('Birth City', 'personal__city_of_birth'),
        ('Birth Country', 'personal__country_of_birth'),
        ("Wife's Name", 'wife__name'),
        ("Wife's Hebrew Name", 'wife__hebrew_name'),
        ("Wife's Birth Date", 'wife__date_of_birth'),
        ("Wife's Email", 'wife__email'),
        ("Wife's Mobile Phone", 'wife__mobile_phone'),
        ('Date of Marriage', 'wife__date_of_marriage'),
        ('Country of Marriage', 'wife__country_of_marriage'),
        ('City of Marriage', 'wife__city_of_marriage'),
        ('Occupation', 'occupation__occupation'),
        ('Business Name', 'occupation__business_name'),
        ('Address', 'occupation__address'),
        ('City', 'occupation__city'),
        ('State', 'occupation__state'),
        ('Zip', 'occupation__zip'),
        ('Phone', 'occupation__phone'),
        ('Synagogue or Temple', 'hod__synagogue_or_temple'),
        ('Sponsor', 'hod__sponsor'),
        ('Sponsor Phone', 'hod__sponsor_phone'),
        ('Previous Member?', 'hod__previous_member_of_hod'),
        ('Previous Lodges', 'hod__previous_lodges'),
        ('Skills or Hobbies', 'hod__skills_or_hobbies'),
        ('Other Orgs', 'hod__other_organizations')
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
