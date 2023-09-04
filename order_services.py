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
    
    def mark_orders_as_delivered(order_id):
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
    
    def list_orders(filters= None, sort_field='created_time', sort_order='asc', page=1, per_page=10):
        skip = (page - 1) * per_page
        query = OrdersModel.objects(is_deleted=False)

        if filters:
            if 'email' in filters:
                query = query.filter(email=filters['email'])
            if 'state' in filters:
                query = query.filter(state=filters['state'])
            if 'zipcode' in filters:
                query = query.filter(zipcode=filters['zipcode'])

        if sort_order == 'asc':
            order = query.order_by(sort_field)
        elif sort_order == 'desc':
            order = query.order_by('-' + sort_field)
        else:
            return {"error":"Invalid sort_order value"}

        order = order.skip(skip).limit(per_page)
        orders_list = []
        for order_model in order:
            order_dict = order_model.to_dict()
            orders_list.append(order_dict)

        return orders_list