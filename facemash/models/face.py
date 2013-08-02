
## Database to hold the faces that will be mashed 
db.define_table('face',
                 Field('name', 'string', length=40, required=True),
                 Field('image', 'upload', required=True, requires=IS_IMAGE(extensions=('bmp','gif','jpeg','png'))),
                 Field('created_on','datetime',default=request.now, readable=False, writable=False),
                 Field('created_by',db.auth_user, default=auth.user_id , readable=False, writable=False ),
                 Field('upload_addr', 'string', default=request.env.remote_addr, readable=False, writable=False),
                 Field('won','integer',default=0,readable=False , writable=False),
                 Field('lost','integer',default=0,readable=False, writable=False),
                 Field('elo_rating','decimal(6,4)',readable=False, default=1600.00,writable=False),
                 )

