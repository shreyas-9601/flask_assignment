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

    for field in required_fields:
        if field not in order_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    birthday = None
    try:
        birthday = datetime.strptime(order_data['Birthday'], '%m/%d/%Y')
    except ValueError:
        return jsonify({"error": "Invalid date format for Birthday"}), 400

    email = order_data['Email']
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return jsonify({"error": "Invalid email format"}), 400

    zipcode = order_data['ZipCode']
    if len(zipcode) != 5:
        return jsonify({"error": "Invalid zipcode format"}), 400

    name = order_data['Name']
    if type(name) != str:
        return jsonify({"error":"Name must be a string"}), 400
    
    state = order_data['State']
    if len(state) != 2 or not state.isalpha() or state.islower():
        return jsonify({"error": "Invalid state format"}), 400
    
    order = Order(order_id= None ,name = name, birthday = order_data['Birthday'], email = email, state = state, zipcode = zipcode)
    
    order_model = OrdersModel(name = order.user.name, birthday = order.user.birthday, 
                                email = order.user.email, state = order.user.state, zipcode = order.user.zipcode)
    
    if order.validate_orders():
        order_model = OrderServices.save_orders(order_data)
        return jsonify({"message":"Order created successfully", "order_id": str(order_model.id)}),201
    else:
        if(order.user.is_valid_mail() == False):
            return jsonify({"message":"Order creation failed due to invalid mail"}), 400
        if(order.user.is_valid_state() == False):
            return jsonify({"message":"Order creation failed due to invalid state"}), 400
        if(order.user.is_valid_age() == False):
            return jsonify({"message":"Order creation failed due to invalid age"}), 400
        if(order.user.is_valid_zipcode() == False):
            return jsonify({"message":"Order creation failed due to invalid zipcode"}), 400
        if(order.user.first_monday_born() == False):
            return jsonify({"message":"Order creation failed due to invalid day of birthday"}), 400
    return jsonify({"message":"Order creation failed"}), 400

@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order_model = OrdersModel.objects(id=str(order_id)).get()
    if order_model.is_deleted == True:
        return jsonify({"message": "Order already deleted successfully"}), 400
    elif order_model: 
        order_model = OrderServices.delete_orders(order_id) 
        return jsonify({"message": "Order deleted successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order_model = OrdersModel.objects(id=str(order_id)).get()
    if order_model.is_deleted == False:
        order_dict = order_model.to_dict()
        return jsonify(order_dict), 200
    else:
        return jsonify({"error": "Order not found"}), 404  
    
@app.route('/order/<order_id>', methods=['PUT'])
def mark_order_as_delivered(order_id):
    order_model = OrdersModel.objects(id=str(order_id)).get()
    if order_model.is_deleted == False:
        if order_model.is_delivered == True:
            return jsonify({"message": "Order already marked as delivered"}), 400
        elif order_model:
            order_model = OrderServices.update_orders(order_id) 
            return jsonify({"message": "Order marked as delivered"}), 200
        else:
            return jsonify({"error": "Order not found"}), 404
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
        order = query.order_by(sort_field)
    elif sort_order == 'desc':
        order = query.order_by('-' + sort_field)
    else:
        return jsonify({"error": "Invalid sort_order value"}), 400
    
    order = order.skip(skip).limit(per_page)
    orders_list = []
    for order_model in order:
        order_dict = order_model.to_dict()
        orders_list.append(order_dict)
    return jsonify(orders_list), 200

if __name__ == '__main__':
    app.run(debug=True)