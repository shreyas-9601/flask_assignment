from datetime import datetime, date
import csv
import re  
        
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
        birthday_obj = datetime.strptime(self.birthday, '%m/%d/%Y')
        today = date.today()
        age = today.year-birthday_obj.year
        if (today.month < birthday_obj.month or (today.month == birthday_obj.month and today.day < birthday_obj.day)):
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
        birthday_obj = datetime.strptime(self.birthday, '%m/%d/%Y')
        return birthday_obj.weekday() != 0 or birthday_obj.day > 7

            
class Order:
    def __init__(self,order_id,name,birthday,email,state,zipcode):
        self.order_id=order_id
        self.user=User(name,birthday,email,state,zipcode)
        
    def validate_orders(self):
        return self.user.is_valid_state() and self.user.is_valid_zipcode() and self.user.is_valid_age() and self.user.is_valid_age() and self.user.is_valid_mail() and self.user.first_monday_born()           
        

    
    
class Acme:
    def __init__(self):
        self.valid_orders=[]
        self.invalid_orders=[]
    
    
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
                birthday = row[birthday_index]
                email = row[email_index]
                state = row[state_index]
                zipcode = row[zipcode_index]
                
                order=Order(order_id, name, birthday, email, state, zipcode)

                if (order.validate_orders()):
                    self.valid_orders.append(order)
                else:
                    self.invalid_orders.append(order)
                    
                    
    def write(self):
        with open('valid.csv', 'w', newline='') as valid_file: 
            writer = csv.writer(valid_file) 
            writer.writerows([[Order.order_id]] for Order in self.valid_orders)
            
        with open('invalid.csv', 'w', newline='') as invalid_file: 
            writer = csv.writer(invalid_file) 
            writer.writerows([[Order.order_id]] for Order in self.invalid_orders)
            
            
if __name__ == '__main__':
    acme = Acme()
    acme.process()
    acme.write()          