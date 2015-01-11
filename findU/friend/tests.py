from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone
import json
import logging

class friendTests(TestCase):

	def test_add_friend(self):
		json_data = {
			'imsi': 12345993,
			"target_user": 13636630387,
		}

		response = self.client.post(reverse('friend:add_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_get_friend(self):
		json_data = {
			"friend": 13636630387,
		}

		response = self.client.post(reverse('friend:get_friend'), json_data)

		self.assertEqual(response.content, "ok")

	def test_accept_friend(self):
		json_data = {
			"nok": 1,
			'imsi': 12345993,
			"target_user": 13636630387,
		}

		response = self.client.post(reverse('friend:accept_friend'), json_data)

		self.assertEqual(response.content, "ok")

	# todo: fix it
	def test_update_friend(self):
		json_data = {
			"friend": 13636630387,
		}

		response = self.client.post(reverse('friend:update_friend'), json_data)

		self.assertEqual(response.content, "ok")
