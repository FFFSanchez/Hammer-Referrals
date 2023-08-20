from http import HTTPStatus

from django.test import Client, TestCase


class RefsAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_sign_up(self):
        """ Smoke check """

        data = {'phone': '+71112220000'}
        response = self.guest_client.post('/api/v1/auth/signup/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
