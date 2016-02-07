# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    rows = db(db.posts).select()

    #if form.accepted:
        #redirect(URL('other', vars={ 'your_name':form.vars.your_name}))
    return locals()

@auth.requires_login()
def create():
    db.posts.User_ID.default = auth.user.id
    form = SQLFORM(db.posts).process()
    db.posts.User_ID.readable = False
    if form.accepted: redirect(URL('index'))
    return locals()

def show():
    post = db.posts(request.args(0, cast=int))
    return locals()

def messaging():
    userID = request.args(0, cast=int)
    db.messages.User_ID2.default = userID
    #db.messages.User_ID2.readable = False
    db.messages.User_ID2.writable = False
    
    rows = db(db.messages.User_ID2==auth.user.id).select()

    form3 = SQLFORM(db.messages).process()
    return locals()
    if form3.accepted:
        redirect('messaging')

@auth.requires_login()
def my_profile():
    name = auth.user.first_name
    rows = db(db.posts.User_ID==auth.user.id).select()
    return locals()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.posts)
    return locals()

def login():
    form2 = SQLFORM(db.auth_user).process()
    return locals()

def other():
    #add sql data entry form in this page.. maybe some flash messages
    message = 'Welcome %s' % request.vars.your_name
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def item():
    rows = db(db.posts.id != request.args(0,cast=int)).select()
    curr_item = db.posts(request.args(0,cast=int))
    return locals()
