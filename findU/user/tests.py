from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone
from bson.json_util import default, object_hook
import json
import logging

class userTests(TestCase):

	def test_register_with_user(self):
		json_data = {
			"mobile": 18601612682,
			"password": "123456",
			"confirmpass": "123456",
		}
	
		response = self.client.post(reverse('user:mobile'), 
			json.dumps(json_data, default=default), content_type='application/json')

		self.assertEqual(response.content, "ok")

