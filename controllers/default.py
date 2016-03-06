# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    #pagination from web2py manual
    if len(request.args): page=int(request.args[0])
    else: page=0
    items_per_page=5
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db().select(db.posts.ALL,limitby=limitby)
    return locals()
    #rows = db(db.posts).select()

    #if form.accepted:
        #redirect(URL('other', vars={ 'your_name':form.vars.your_name}))
    return locals()

def user(): 
    return dict(form=auth())

@auth.requires_login()
def create():
    
    db.posts.User_ID.default = auth.user.id
    form = SQLFORM(db.posts).process()
    db.posts.User_ID.readable = False
    if form.accepted: 
        
        rows = db(db.rating.User_ID==auth.user.id).select()
        
        if(not rows):
            db.rating.insert(User_ID=auth.user.id, rating=0, Rcount=0, score=0)
            
        redirect(URL('index'))
        
    return locals()

def show():
    post = db.posts(request.args(0, cast=int))
    voter = db((db.votes.Rater==auth.user)&(db.votes.Ratee==post.created_by)).select()
    
    return locals()

def showByCategory():
    var1 = request.vars.filter1
    rows = db(db.posts.category==var1).select()
    
    return locals()

def showByLocations():
    var2 = request.vars.filter2
    rows= db(db.posts.locations==var2).select()
    
    return locals()

@auth.requires_login()
def messaging():
    rows = db(db.messages.recepient==auth.user.first_name).select(orderby=~db.messages.created_on)
    form3 = SQLFORM(db.messages).process()
    if form3.accepted:
        redirect('messaging')
        
    return locals()    

@auth.requires_login()
def my_profile():
    fname = auth.user.first_name
    lname = auth.user.last_name
    infos = db(db.profile.User_ID==auth.user.id).select()
    rows = db(db.posts.User_ID==auth.user.id).select()
    rates = db(db.rating.User_ID==auth.user.id).select()
    
    return locals()


def show_profile():
    if request.args:
        get_ID = request.args[0]
        infos = db(db.profile.User_ID==get_ID).select()
        rows = db(db.posts.User_ID==get_ID).select()
        rates = db(db.rating.User_ID==get_ID).select()
        thing = db.auth_user(id=get_ID)
        voter = db((db.votes.Rater==auth.user)&(db.votes.Ratee==get_ID)).select()
    if request.vars:
        name = request.vars.search_filter
        person = db(db.auth_user.first_name == name).select()
        if person:
            person = person[0]
            x = person.id
            infos = db(db.profile.User_ID==x).select()
            rows = db(db.posts.User_ID==x).select()
            thing = db.auth_user(id=x)
        else:
            session.flash = "sorry, we couldn't find what you were looking for :("
            redirect(URL('index'))
            
    return locals()

def test_map():
    location = request.args(0, cast=str)
    return locals()

@auth.requires_login()
def profile():
    user_id = request.args(0)
    profile_row = db(db.profile.User_ID==user_id).select()[0]
    #exists_info = db(db.profile(db.profile.User_ID==user_id))
    
    #if (exists_info):
    #    response.flash="THIS USER HAS A PROFILE"
    #else:
    #    response.flash="THIS USER DOESN'T"
    form = SQLFORM(db.profile).process()
    
    return locals()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.posts)
    return locals()

@auth.requires_login()
def rating_callback():
    vars = request.post_vars
    voted = False
    
    if vars:
        #make another table tracking who voted for who; then in the conditional check to see if the current user already has a vote logged for the user
        user = vars.user
        rate = (float (vars.rate))
        Rating = db(db.rating.User_ID==user).select()[0]
        
        voter = db((db.votes.Rater==auth.user.id)&(db.votes.Ratee==user)).select()
        if voter:
            voter = voter[0]
            score = voter.score
            Rating.update_record(score=Rating.score-score)
            Rating.update_record(score=Rating.score+rate)
            Rating.update_record(rating=((Rating.score)/Rating.Rcount))
            voter.update_record(score = rate)
            response.flash="You changed your vote"
            
        else:
            
            Rating.update_record(Rcount=Rating.Rcount+ 1)
            Rating.update_record(score=Rating.score+rate)
            Rating.update_record(rating=((Rating.score)/Rating.Rcount))
            db.votes.insert(Rater=auth.user.id, Ratee=user, Vtype='profile', score=rate)
            response.flash="new vote"
    return locals()
def testCss():
    
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
    auth.settings.register_onaccept.append(lambda form: db.profile.insert(User_ID=auth.user.id))
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

def delete_post():
    post_id = request.post_vars.post_id
    query = db.posts.id==post_id
    db(query).delete()
    response.flash = "Post deleted"

def getItems(items):
    items = items.replace(" ", "")
    items = items.lower()
    items = items.split(",")
    return items

#input_list == rows
#intersts_list == all tokens of curr_item.intersts

def checkMatch(input_list):
    interst_list = getItems(input_list.interests)
    match = db(db.posts.created_by != input_list.created_by)
    match = db(db.posts.interests == input_list.offers )
    '''for item in interst_list:
        match =  db(db.posts.offers == item).select()'''
    return match

def item():
    curr_item = db.posts(request.args(0,cast=int))
    '''
    rows = db(db.posts.created_by != curr_item.created_by).select()
    rows = db(db.posts.interests == curr_item.offers ).select()
    rows = db(db.posts.offers == curr_item.interests ).select()
    '''
    rows = checkMatch(curr_item).select()
    incomplete_rows = rows
    return locals()
