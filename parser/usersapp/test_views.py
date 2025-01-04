from django.test import Client
from django.test import TestCase
from faker import Faker


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.faker = Faker('ru_RU')

    def test_statuses(self):
        # get pages
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
