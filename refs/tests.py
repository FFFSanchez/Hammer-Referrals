from http import HTTPStatus

from django.test import Client, TestCase


class RefsTestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_sign_up(self):
        """ Smoke check """

        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
