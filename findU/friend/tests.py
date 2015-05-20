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
		user_1 = User.objects.create(username='12345993')
		user_info_1 = UserInfo.objects.create(user=user_1, nickname='test 01')
		user_2 = User.objects.create(username='13636630387')
		user_info_2 = UserInfo.objects.create(user=user_2, nickname='test 02')

	def test_add_friend(self):
		json_data = {
			'mobile': '12345993',
			"friend_mobile": '13636630387',
		}

		response = self.client.post(reverse('friend:add_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_get_friend_less(self):
		self.prepare_data()

		json_data = {
			"mobile": '12345993',
			"local_friend_version": 1,
		}

		response = self.client.post(reverse('friend:get_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_get_friend_equality(self):
		self.prepare_data()

		json_data = {
			"mobile": '12345993',
			"local_friend_version": 2,
		}

		response = self.client.post(reverse('friend:get_friend'), json_data)

		self.assertEqual(response.content, "ok")		

	def test_accept_friend(self):
		json_data = {
			"mobile": 12345993,
			"nok": 1,
			"friend_mobile": 13636630387,
		}

		response = self.client.post(reverse('friend:accept_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_update_friend(self):
		self.prepare_data()

		json_data = {
			"mobile": 12345993,
			"friend_mobile": 13636630387,
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
		test1 = User.objects.get(username='12345993')
		test2 = User.objects.get(username='13636630387')
		dog = UserInfo.objects.get(user=test1)
		cat = Friend.objects.create(user=test1,friend=test2, nickname='cat',version_id=1)
		dog.version_count  = 1
		dog.save()
