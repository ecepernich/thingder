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

@auth.requires_login()
def messaging():
    
    rows = db(db.messages.User_ID2==auth.user.id).select()
    
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
    
    return locals()


def show_profile():
    x = request.args[0]
    #x=1
    infos = db(db.profile.User_ID==x).select()
    rows = db(db.posts.User_ID==x).select()
    thing = db.auth_user(id=x)
    
    return locals()

@auth.requires_login()
def profile():
    
    form = SQLFORM(db.profile).process()
    
    return locals()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.posts)
    return locals()

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

def getItems(items):
    items = items.replace(" ", "")
    items = items.lower()
    items = items.split(",")
    return items

#input_list == rows
#intersts_list == all tokens of curr_item.intersts

def getMatchLists(input_list, match_list, curr_item):
    curr_interest_list = getItems(curr_item.intersts)
  #  for row in input_list:
     #   input_interst_list = getItems(input_list.intersts);
       # for index in interest_list:
          #  if((curr_interest_list[index] == input_list.offer):
           #    return
            
    return

def item():
    curr_item = db.posts(request.args(0,cast=int))
    rows = db(db.posts.created_by != curr_item.created_by).select()
    return locals()
