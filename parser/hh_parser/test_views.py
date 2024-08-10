from django.test import Client
from django.test import TestCase
from faker import Faker


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.faker = Faker('ru_RU')

    def test_statuses(self):
        vacancy = self.faker.job()
        city = self.faker.city_name()

        # get pages
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/results/'+vacancy+'/'+city)
        self.assertEqual(response.status_code, 301)

        # post pages
        response = self.client.post('/form/', vacancy=vacancy, city=city)
        self.assertEqual(response.status_code, 200)

        # Данные на настранице
        response = self.client.get('/results/')
        self.assertTrue('obj', 'skills' in response.context)