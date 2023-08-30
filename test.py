import unittest 
from process_orders_data import User
from datetime import datetime,date

class TestUser(unittest.TestCase):
    def setUp(self):
        self.dummy_data = User('Kathleen','3/10/1931','KathleenDGuzman@dodgit.com','NY','99654')
        
    def test_return_true_if_is_valid_state(self):
        user=self.dummy_data.is_valid_state()
        self.assertTrue(user)
        
    def test_return_false_if_is_not_valid_state(self):
        self.dummy_data.state='NJ'
        user=self.dummy_data.is_valid_state()
        self.assertFalse(user)
        
    def test_return_true_if_is_valid_age(self):
        date_obj = datetime.strptime('7/1/1996', '%m/%d/%Y')
        self.dummy_data.birthday=date_obj
        user=self.dummy_data.is_valid_age()
        self.assertTrue(user)
        
    def test_return_false_if_is_not_valid_age(self):
        date_obj = datetime.strptime('5/3/2003', '%m/%d/%Y')
        self.dummy_data.birthday=date_obj
        user=self.dummy_data.is_valid_age()
        self.assertFalse(user)
        
    def test_return_true_if_is_valid_zipcode(self):
        self.dummy_data.zipcode='37209'
        user=self.dummy_data.is_valid_zipcode()
        self.assertTrue(user)
        
    def test_return_false_if_is_not_valid_zipcode(self):
        user=self.dummy_data.is_valid_zipcode()
        self.assertFalse(user)
        
    def test_return_true_if_not_born_on_first_monday_of_month(self):
        date_obj = datetime.strptime('5/3/2003', '%m/%d/%Y')
        self.dummy_data.birthday=date_obj
        user=self.dummy_data.first_monday_born()
        self.assertTrue(user)
        
    def test_return_false_if_born_on_first_monday_of_month(self):
        date_obj = datetime.strptime('7/1/1996', '%m/%d/%Y')
        self.dummy_data.birthday=date_obj
        user=self.dummy_data.first_monday_born()
        self.assertFalse(user)
        
    def test_return_true_if_is_valid_mail(self):
        user=self.dummy_data.is_valid_mail()
        self.assertTrue(user)
        
    def test_return_false_if_is_not_valid_mail(self):
        self.dummy_data.email='JacquelynRHic.ksmailinator.com'
        user=self.dummy_data.is_valid_mail()
        self.assertFalse(user)