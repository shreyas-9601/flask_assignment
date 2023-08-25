from mongoengine import *
from datetime import datetime
connect('ordersdb')

class OrdersModel(Document):   
    name = StringField( required = True, max_length =100)
    birthday = DateTimeField( required = True)
    email = StringField( required = True)
    state = StringField( required = True, max_length =50)
    zipcode = StringField( required = True, max_length =10)
    is_deleted = BooleanField( default = False)
    deletion_time = DateTimeField()
    created_time = DateTimeField( default = datetime.utcnow)
    updated_time = DateTimeField( default = datetime.utcnow)
    is_delivered = BooleanField( default = False)