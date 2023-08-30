from datetime import datetime, date
import csv
import re  
from orders_model import OrdersModel
        
class User:
    def __init__(self,name,birthday,email,state,zipcode):
            self.name=name
            self.birthday=birthday
            self.email=email
            self.state=state
            self.zipcode=zipcode
    
    def is_valid_state(self):
        return self.state not in ['NJ', 'CT', 'PA', 'MA', 'IL', 'ID', 'OR']


    def is_valid_age(self):
        today = date.today()
        age = today.year-self.birthday.year
        if (today.month < self.birthday.month or (today.month == self.birthday.month and today.day < self.birthday.day)):
            age -= 1
        return age >= 21


    def is_valid_mail(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, self.email)):
            return True


    def is_valid_zipcode(self):
        for i in range(len(self.zipcode)-1):
            if (abs(int(self.zipcode[i])-int(self.zipcode[i+1])) == 1):
                return False
        return True


    def first_monday_born(self):
        return self.birthday.weekday() != 0 or self.birthday.day > 7

            
class Order:
    def __init__(self,order_id,name,birthday,email,state,zipcode):
        self.order_id=order_id
        self.user=User(name,birthday,email,state,zipcode)
        
    def validate_orders(self):
        return self.user.is_valid_state() and self.user.is_valid_zipcode() and self.user.is_valid_age() and self.user.is_valid_age() and self.user.is_valid_mail() and self.user.first_monday_born() 
    
    def save_orders(self):
        ordermodel= OrdersModel(order_id= self.order_id, name= self.user.name, birthday= self.user.birthday, email=self.user.email, state= self.user.state, zipcode= self.user.zipcode)
        OrdersModel.save(ordermodel)
        
    def mark_as_valid(self):
        if(self.validate_orders()):
            OrdersModel.objects(order_id=self.order_id).update_one(set__isvalid=True)

        
    
class Acme:
    def process(self):
        with open('orders.csv', 'r') as file:
            csvreader = csv.reader(file)
            headers = next(csvreader)

            id_index = headers.index('ID')
            name_index = headers.index('Name')
            birthday_index = headers.index('Birthday')
            email_index = headers.index('Email')
            state_index = headers.index('State')
            zipcode_index = headers.index('ZipCode')

            for row in csvreader:
                order_id = row[id_index]
                name = row[name_index]
                birthday=datetime.strptime(row[birthday_index], '%m/%d/%Y')
                email = row[email_index]
                state = row[state_index]
                zipcode = row[zipcode_index]
                
                newOrder=Order(order_id, name, birthday, email, state, zipcode)
                newOrder.save_orders()
            print('All orders transfered to database successfully')
            
    def update_orders(self):
        orders=OrdersModel.objects
        
        for order in orders:
            neworder=Order(order.order_id,order.name,order.birthday,order.email,order.state,order.zipcode)
            neworder.mark_as_valid()
        print('All orders updated to database successfully')
            
            
if __name__ == '__main__':
    acme = Acme()
    acme.process() 
    acme.update_orders()        