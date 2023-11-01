from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from .models import *


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        # print(response)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertEqual(response.context_data['title'], 'title_name')
        self.assertTemplateUsed(response, 'index.html')


