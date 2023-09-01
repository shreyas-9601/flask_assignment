from orders_model import OrdersModel
from datetime import datetime

class OrderServices:
    def save_orders(order_data):
        order_model = OrdersModel(name=order_data['Name'],birthday=order_data['Birthday'], 
                                  email=order_data['Email'], state=order_data['State'], zipcode=order_data['ZipCode'])
        order_model= order_model.save()
        return order_model
    
    def delete_orders(order_id):
        order_model = OrdersModel.objects(id=str(order_id), is_deleted = False).get()
        order_model = order_model.update(set__is_deleted=True, set__deletion_time=datetime.utcnow())
        return order_model
    
    def update_orders(order_id):
        order_model = OrdersModel.objects(id=str(order_id), is_deleted = False).get()
        order_model = order_model.update(set__is_delivered= True, set__updated_time = datetime.utcnow())
        return order_model
    
    def validation_orders(order):
        if not order.user.is_valid_mail():
            return {"error": "Invalid mail"}
        if not order.user.is_valid_state():
            return {"error": "Invalid state"}
        if not order.user.is_valid_age():
            return {"error": "Invalid age"}
        if not order.user.is_valid_zipcode():
            return {"error": "Invalid zipcode"}
        if not order.user.first_monday_born():
            return {"error": "Invalid day of birthday"}
        return None