# -*- coding: utf-8 -*-

categories=['Car','House','Misc.']
db.define_table('posts',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('interests'),
                Field('offers'),
                Field('category', requires=IS_IN_SET(categories)),
                Field('image', 'upload'),
                Field('User_ID', 'reference auth_user'),
                auth.signature)
                
db.define_table('messages',
                Field('body', 'text'),
                Field('User_ID2'),
                auth.signature)
db.define_table('rating',
                Field('User_ID', 'reference auth_user'),
                Field('Rcount', 'float'),
                Field('score', 'float'),
                Field('rating', 'float'))
db.rating.Rcount.default = 1;
db.define_table('votes',
                Field('Rater','reference auth_user'),
                Field('Ratee','reference auth_user'),
                Field('Vtype'),
                Field('score','float'))

db.define_table('profile',
                Field('User_ID','reference auth_user'),
                Field('image','upload',default='defaultprofile.png'),
                Field('zip_code'),
                Field('age','integer'),
                Field('about_me','text'),
                Field('extrafield'))
db.profile.zip_code.requires = IS_MATCH('^\d{5}(-\d{4})?$',
         error_message='not a zip code')
