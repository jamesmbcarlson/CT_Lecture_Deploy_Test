# get app.py from parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from app import create_app

import unittest
from unittest.mock import MagicMock, patch
from faker import Faker

fake = Faker()

class TestProductEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # test successful creation of product
    @patch('services.productService.save')
    def test_create_product(self, mock_save):
        name = fake.name()
        price = fake.pyfloat(None, 2, None, 0.0, 999.99)
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = name
        mock_product.price = price
        mock_save.return_value = mock_product

        payload = {
                "name": name,
                "price": price
            }
        
        response = self.app.post('/products/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_product.id)

    # test creation of product without price
    @patch('services.productService.save')
    def test_missing_price_payload(self, mock_save):
        name = fake.name()
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = name
        mock_save.return_value = mock_product

        payload = {
            "name": name
        }

        response = self.app.post('/products/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.json)

    # test creation of product with superfluous data
    @patch('services.productService.save')
    def test_extra_data_product(self, mock_save):
        name = fake.name()
        price = fake.job()
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = name
        mock_product.price = price
        mock_save.return_value = mock_product

        payload = {
                "name": name,
                "price": price,
                "sku" : "KSRUFTT"
            }
        
        response = self.app.post('/products/', json=payload)

        self.assertEqual(response.status_code, 400)