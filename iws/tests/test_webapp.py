#
# Author: Rohtash Lakra
#
from fastapi import FastAPI

from tests.base import AbstractTestCase


class WebAppTest(AbstractTestCase):

    def test_webapp(self):
        """Tests the FastAPI application object"""
        print("+test_webapp()")
        self.assertIsNotNone(self.app)
        self.assertIsInstance(self.app, FastAPI)
        print("-test_webapp()")
        print()

    def test_health_check(self):
        """Tests the health-check end-point"""
        print("+test_health_check()")
        response = self.client.get("/health-check")
        self.assertEqual(200, response.status_code)
        print("-test_health_check()")
        print()

    def test_not_found(self):
        """Tests the not-found error handler returns the JSON error model"""
        print("+test_not_found()")
        response = self.client.get("/no-such-end-point")
        self.assertEqual(404, response.status_code)
        self.assertEqual(404, response.json().get("status"))
        print("-test_not_found()")
        print()
