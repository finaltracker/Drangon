from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone
import json
import logging

class userTests(TestCase):

	def test_1_register_with_user(self):
		json_data = {
			"mobile": 18601612682,
			"password": "123456",
			"confirmpass": "123456",
			'imsi': 12345993,
		}
	
		response = self.client.post(reverse('user:register'), json_data)

		self.assertEqual(response.content, "ok")

	def test_2_login_with_user(self):
		json_data = {
			"mobile": 18601612682,
			"password": "123456",
		}
	
		response = self.client.post(reverse('user:login'), json_data)

		self.assertEqual(response.content, "ok")

	def test_3_check_register(self):
		json_data = {
			"imsi": 12345993,
		}
	
		response = self.client.post(reverse('user:check_register'), json_data) 

		self.assertEqual(response.content, "ok")

