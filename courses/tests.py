from django.test import TestCase
from django.core import mail

from django.test.client import Client
from django.urls import reverse

from .models import Course

# Create your tests here.


class HomeViewTest(TestCase):

	def test_home_status_code(self):

		client = Client()
		response = client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)

