from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone

from friend.models import Friend
from user.models import UserInfo
from django.contrib.auth.models import User

import json
import logging

class friendTests(TestCase):

	def setUp(self):
		pass

	def test_add_friend(self):
		json_data = {
			'mobile': 12345993,
			"add friend": 13636630387,
		}

		response = self.client.post(reverse('friend:add_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_get_friend(self):
		
		self.prepare_data()

		json_data = {
			"mobile": 12345993,
			"mobile_friend_version": 2,
		}

		response = self.client.post(reverse('friend:get_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_accept_friend(self):
		json_data = {
			"mobile": 12345993,
			"nok": 1,
			"to friend": 13636630387,
		}

		response = self.client.post(reverse('friend:accept_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_update_friend(self):

		self.prepare_data()

		json_data = {
			"mobile": 12345993,
			"update friend": 13636630387,
			"comment": 'penut',
			"group": 'cat_pic',
			"description": 'cross finger',
		}

		response = self.client.post(reverse('friend:update_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_search_friend(self):

		self.prepare_data()

		json_data = {
			"mobile": 12345993,
			"search_str": 13636630387,
		}

		response = self.client.post(reverse('friend:search_friend'), json_data)

		self.assertEqual(response.content, "ok")		

	def prepare_data(self):
		test1 = User.objects.create(username='12345993')
		dog = UserInfo.objects.create(user=test1,nickname='dog')
		cat = Friend.objects.create(user=test1,phone='13636630387', nickname='cat',version_id=1)
		dog.version_count  = 1
		dog.save()
		cow = Friend.objects.create(user=test1, phone='13636630388', nickname='cow',version_id=2)
		dog.version_count = 2
		dog.save()