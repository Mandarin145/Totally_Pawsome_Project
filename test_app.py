import unittest
from app import app


class FlaskTest(unittest.TestCase):

    def test_base_route(self):
        """check if response is 200"""
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code

        self.assertEqual(statuscode, 200)

    def test_adoption_content(self):
        """check if return content is text/html rather than json"""
        tester = app.test_client(self)
        response = tester.get("/adopt")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_customer_content(self):
        """check if return content is text/html"""
        tester = app.test_client(self)
        response = tester.get("/customer")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_homepage_data(self):
        """check for data return"""
        tester = app.test_client(self)
        response = tester.get("/")

        self.assertTrue(b"Adopt a Pet" in response.data)
