# -*- coding: utf-8 -*-


db.define_table('posts',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('interests'),
                Field('offers'),
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
