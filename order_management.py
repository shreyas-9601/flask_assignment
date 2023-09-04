from datetime import datetime
from flask import *
app = Flask(__name__)
from orders_model import OrdersModel
from order_validation import Order
from order_services import OrderServices
import re

@app.route('/order', methods=['POST'])
def create_order():
    order_data = request.json
    required_fields = ['Name', 'Birthday', 'Email', 'State', 'ZipCode']

    missing_fields = [field for field in required_fields if field not in order_data]
    if missing_fields:
        error_messages = [f"Missing required field: {field}" for field in missing_fields]
        return jsonify({"errors": error_messages}), 400

    birthday = order_data['Birthday']
    try:
        birthday = datetime.strptime(birthday, '%m/%d/%Y')
    except ValueError:
        return jsonify({"error": "Invalid date format for Birthday"}), 400

    email = order_data['Email']
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return jsonify({"error": "Invalid email format"}), 400

    zipcode = order_data['ZipCode']
    if len(zipcode) > 10:
        return jsonify({"error": "Invalid zipcode format"}), 400

    name = order_data['Name']
    if type(name) != str or len(name) > 100:
        return jsonify({"error":"Invalid name format"}), 400
    
    state = order_data['State']
    if len(state) > 50:
        return jsonify({"error": "Invalid state format"}), 400
    
    order = Order(order_id= None ,name = name, birthday = order_data['Birthday'], email = email, state = state, zipcode = zipcode)
    
    order_model = OrdersModel(name = order.user.name, birthday = order.user.birthday, 
                                email = order.user.email, state = order.user.state, zipcode = order.user.zipcode)
    
    validation_error = OrderServices.validation_orders(order)
    if validation_error:
        return jsonify({"message": f"Order creation failed due to {validation_error['error']}"}), 400
    
    order_model = OrderServices.save_orders(order_data)

    return jsonify({"message": "Order created successfully", "order_id": str(order_model.id)}), 201

@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order_model = OrdersModel.objects(id=str(order_id)).get()
        if order_model.is_deleted == True:
            return jsonify({"message": "Order already deleted successfully"}), 400
        elif order_model: 
            order_model = OrderServices.delete_orders(order_id) 
            return jsonify({"message": "Order deleted successfully"}), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order_model = OrdersModel.objects(id=str(order_id)).get()
        if order_model.is_deleted == False:
            order_dict = order_model.to_dict()
            return jsonify(order_dict), 200
        else:
            return jsonify({"error": "Order not found"}), 404 
    except Exception as e:
        return jsonify({"error":str(e)}), 500 
    
@app.route('/order/<order_id>', methods=['PUT'])
def mark_order_as_delivered(order_id):
    try:
        order_model = OrdersModel.objects(id=str(order_id)).get()
        if order_model.is_deleted == False:
            if order_model.is_delivered == True:
                return jsonify({"message": "Order already marked as delivered"}), 400
            elif order_model:
                order_model = OrderServices.mark_orders_as_delivered(order_id) 
                return jsonify({"message": "Order marked as delivered"}), 200
            else:
                return jsonify({"error": "Order not found"}), 404
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
@app.route('/orders', methods=['GET'])
def list_orders_route():
    email = request.args.get('email')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    
    per_page = int(request.args.get('per_page', 10))
    sort_field = request.args.get('sort_field', 'created_time')
    sort_order = request.args.get('sort_order', 'asc')
    page = int(request.args.get('page', 1))
    
    filters = {}
    if email:
        filters['email'] = email
    if state:
        filters['state'] = state
    if zipcode:
        filters['zipcode'] = zipcode

    orders_list = OrderServices.list_orders(filters=filters, sort_field=sort_field,          
                                            sort_order=sort_order, page=page, per_page=per_page)

    return jsonify(orders_list), 200

if __name__ == '__main__':
    app.run(debug=True)