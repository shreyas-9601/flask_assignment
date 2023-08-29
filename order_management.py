from datetime import datetime
from flask import *
app = Flask(__name__)
from orders_model import OrdersModel
from bson.objectid import ObjectId
from order_validation import Order

@app.route('/order', methods=['POST'])
def create_order():
    order_data = request.json
    orders=Order(order_id=id, name=order_data['Name'], birthday = order_data['Birthday'], 
                        email = order_data['Email'], state = order_data['State'], zipcode = order_data['ZipCode'])
    order = OrdersModel(name = orders.user.name, birthday = orders.user.birthday, 
                        email = orders.user.email, state = orders.user.state, zipcode = orders.user.zipcode)
    if orders.validate_orders():
        order = order.save()
        return jsonify({"message":"Order created successfully", "order_id": str(order.id)}),201
    else:
        if(orders.user.is_valid_mail() == False):
            return jsonify({"message":"Order creation failed due to invalid mail"}), 400
        if(orders.user.is_valid_state() == False):
            return jsonify({"message":"Order creation failed due to invalid state"}), 400
        if(orders.user.is_valid_age() == False):
            return jsonify({"message":"Order creation failed due to invalid age"}), 400
        if(orders.user.is_valid_zipcode() == False):
            return jsonify({"message":"Order creation failed due to invalid zipcode"}), 400
        if(orders.user.first_monday_born() == False):
            return jsonify({"message":"Order creation failed due to invalid day of birthday"}), 400
    return jsonify({"message":"Order creation failed"}), 400

@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = OrdersModel.objects(id=ObjectId(order_id)).first()
    if order:
        order.is_deleted = True  
        order.deletion_time = datetime.utcnow()  
        order.save()  
        return jsonify({"message": "Order deleted successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order = OrdersModel.objects(id=ObjectId(order_id), is_deleted = False).first()
    if order:
        order_dict = order.to_dict()
        return jsonify(order_dict), 200
    else:
        return jsonify({"error": "Order not found"}), 404  
    
@app.route('/order/<order_id>', methods=['PUT'])
def mark_order_as_delivered(order_id):
    order = OrdersModel.objects(id=ObjectId(order_id)).first()
    if order:
        order.is_delivered = True  
        order.updated_time = datetime.utcnow()
        order.save()  
        return jsonify({"message": "Order marked as delivered"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404
    
@app.route('/orders', methods=['GET'])
def list_orders():
    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page

    email = request.args.get('email')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    
    sort_field = request.args.get('sort_field', 'created_time')  
    sort_order = request.args.get('sort_order', 'asc')  

    query = OrdersModel.objects(is_deleted = False)

    if email:
        query = query.filter(email=email)
    if state:
        query = query.filter(state=state)
    if zipcode:
        query = query.filter(zipcode=zipcode)

    if sort_order == 'asc':
        orders = query.order_by(sort_field).skip(skip).limit(per_page)
    elif sort_order == 'desc':
        orders = query.order_by('-' + sort_field).skip(skip).limit(per_page)
    else:
        return jsonify({"error": "Invalid sort_order value"}), 400
    orders_list = []
    for order in orders:
        order_dict = order.to_dict()
        orders_list.append(order_dict)
    return jsonify(orders_list), 200

if __name__ == '__main__':
    app.run(debug=True)