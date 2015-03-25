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
