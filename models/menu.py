# -*- coding: utf-8 -mail = auth.settings.mailer
mail.settings.server = "stmp.gmail.com:587"
mail.settings.sender= "autoweb2py@gmail.com"
mail.settings.login = "autoweb2py@gmail.com:waolokssqdipvbkp"

auth.settings.registration_requires_verification = True

def send_email(user, subject):
    message = "Multi Line string for %string(first_name)s"# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Thingder'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="/thingder/default/index",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Create Post'), False, URL('default', 'create'), []),
    (T('My Profile'), False, URL('default', 'my_profile'), []),
    
    
]
if auth.has_membership('managers'):
    response.menu.append((T('Manage Posts'), False, URL('default', 'manage')))


DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()

mail = auth.settings.mailer
mail.settings.server = "smtp.gmail.com:587"
mail.settings.sender= "autoweb2py@gmail.com"
mail.settings.login = "autoweb2py@gmail.com:waolokssqdipvbkp"

auth.settings.registration_requires_verification = True

def send_email(user, subject):
    message = " Multi line string for %string(first_name)s"
    message = open("somefile.html", "r").read()
    mail.send(to=user.email,
              subject=subject,
              message=message % user)
