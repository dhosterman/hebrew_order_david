from accounts.models import User


def on_new_user(user):
    # notify administrators if a new user has completed an application
    admins = User.objects.filter(is_admin=True)    
    subject = 'New Application'
    message = 'Applicant: {} {}\r\n'.format(user.first_name, user.last_name) 
    message += 'Email: {}\r\n'.format(user.email)
    message += 'Hebrew Name: {}\r\n'.format(user.hebrew_name)
   
    for admin in admins:
        admin.email_user(subject=subject, message=message)

def on_updated_user(user, forms):
    # notify adminstrators if an existing user has updated an application
    admins = User.objects.filter(is_admin=True)
    subject = 'Updated Application'
    message = 'Applicant: {} {}\r\n'.format(user.first_name, user.last_name) 
    message += 'Updated Fields:\r\n'
    for form in forms:
        if form.prefix:
            message += '[{}]\r\n'.format(form.prefix)
        for key in form.changed_data:
            old_value = form.initial.get(key, 'blank')
            if old_value == '':
                old_value = 'blank'
            new_value = form.cleaned_data.get(key, 'blank')
            label = form.fields[key].label
            message += '* {}: changed from {} to {}\r\n'.format(label,
                                                              old_value,
                                                              new_value)

    for admin in admins:
        admin.email_user(subject=subject, message=message)
