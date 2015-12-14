from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone
from django.contrib.auth.models import User
from user.models import UserInfo
import json
import logging

class userTests(TestCase):

	def setUp(self):
		user_1 = User.objects.create(username='12345993',password='123456',is_staff=False,is_active=True,is_superuser=False)
		user_info_1 = UserInfo.objects.create(user=user_1, nickname='test 01')

	def test_1_register_with_user(self):
		json_data = {
			"mobile": 18601612682,
			"password": "123456",
			"confirmpass": "123456",
			'imsi': 12345993,
			'nick_name': "test"
		}
	
		response = self.client.post(reverse('user:register'), json_data)

		self.assertEqual(response.content, "ok")

	def test_1_register_with_diff_password(self):
		json_data = {
			"mobile": 18601612682,
			"password": "123456",
			"confirmpass": "125456",
			'imsi': 12345993,
		}
	
		response = self.client.post(reverse('user:register'), json_data)

		self.assertEqual(response.content, "ok")		

	def test_2_login_with_user(self):
		json_data = {
			"mobile": 12345993,
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

	def test_4_delete_user(self):
		json_data = {
			"mobile": 12345993,
			"password": "123456",
		}
	
		response = self.client.post(reverse('user:delete_user'), json_data) 

		self.assertEqual(response.content, "ok")		

