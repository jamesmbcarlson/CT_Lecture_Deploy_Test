# get app.py from parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from app import create_app

import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import logging

fake = Faker()

def create_test_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = first_name + " " + last_name
    email = fake.email()
    phone = fake.phone_number()
    username = first_name[0] + last_name
    password = "pass123"

    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = name
    mock_customer.email = email
    mock_customer.phone = phone
    mock_customer.username = username
    mock_customer.password = password
    return mock_customer

def customer_payload(mock_customer):
    return {
        "name": mock_customer.name,
        "phone": mock_customer.phone,
        "email": mock_customer.email,
        "username": mock_customer.username,
        "password": mock_customer.password
    }

class TestCustomerEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()


    # test successful creation of customer
    @patch('services.customerService.create_customer')
    def test_create_customer(self, mock_save):
        mock_customer = create_test_customer()
        mock_save.return_value = mock_customer
        payload = customer_payload(mock_customer)
        
        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_customer.id)

    # test get all customers
    @patch('services.customerService.get_all')
    def test_get_customers(self, mock_save):
        response = self.app.get('/customers/')
        self.assertEqual(response.status_code, 200)
    
    # test get one customer by id
    @patch('services.customerService.get_customer')
    def test_get_customer(self, mock_save):
        response = self.app.get(f'/customers/1')
        self.assertEqual(response.status_code, 200)

    # test update customer data
    @patch('services.customerService.update_customer')
    def test_update_customer(self, mock_update):
        # create customer
        mock_customer = create_test_customer()
        payload = customer_payload(mock_customer)
        response = self.app.post('/customers/', json=payload)

        # update data
        new_email = fake.email()
        mock_customer.email = new_email
        mock_update.return_value = mock_customer
        payload = {
                "email": new_email
            }
        response = self.app.put(f'/customers/{mock_customer.id}', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn('email', response.json)
        self.assertEqual(response.json["email"], new_email)
    
    # test update customer data
    @patch('services.customerService.delete_customer')
    def test_delete_customer(self, mock_save):      
        response = self.app.delete('/customers/1')
        self.assertEqual(response.status_code, 201)