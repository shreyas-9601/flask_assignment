from mongoengine import *

connect("ordersdb")

class OrdersModel(Document):   
    order_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    birthday = DateTimeField(required=True)
    email = StringField(required=True)
    state = StringField(required=True)
    zipcode = StringField(required=True)
    isvalid = BooleanField(default=False)