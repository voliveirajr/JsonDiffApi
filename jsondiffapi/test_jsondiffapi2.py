import unittest
import app
import requests
from jsondiffapi import *

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def test_hello_world(self):
        response = self.app.get('/')

if __name__ == "__main__":
    unittest.main()
