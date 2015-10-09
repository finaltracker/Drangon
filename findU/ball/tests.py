from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone

from friend.models import Friend
from user.models import UserInfo
from django.contrib.auth.models import User

import json
import logging
import time

class ballTests(TestCase):

	def setUp(self):
		user_1 = User.objects.create(username='12345993')
		user_info_1 = UserInfo.objects.create(user=user_1, nickname='test 01')
		user_2 = User.objects.create(username='13636630387')
		user_info_2 = UserInfo.objects.create(user=user_2, nickname='test 02')
		self.start()

	def start(self):
		json_data = {
			'mobile': '13636630387',
			"type": 1,
			"content": 'funzy',
			"duration": 1,
			"begin_lat":31.2477310000,
			"begin_lng":121.6405930000,
			"end_lat":31.1993100000,
			"end_lng":121.6451920000,
		}

		response = self.client.post(reverse('ball:start'), json_data)

		#self.assertEqual(response.content, "ok")


	def test_locate_get(self):
		time.sleep(15)
		json_data = {
			'mobile': '13636630387',
			"mask": 3,
			"lat":31.229977,
			"lng":121.642279,	
			"distance": 100,		
		}

		response = self.client.post(reverse('ball:locate_get'), json_data)

		self.assertEqual(response.content, "ok")

	def test_current_loc(self):
		time.sleep(15)
		json_data = {
			'mobile': '13636630387',
			"ball_id": 1,	
		}

		response = self.client.post(reverse('ball:current_loc'), json_data)

		self.assertEqual(response.content, "ok")		
