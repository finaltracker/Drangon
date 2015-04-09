from django.test import TestCase
from django.core.urlresolvers import reverse
from user.models import UserInfo
from tips.models import Tip
from django.contrib.auth.models import User

class tipTests(TestCase):

	def setUp(self):
		user_1 = User.objects.create(username='12345993')
		user_info_1 = UserInfo.objects.create(user=user_1, nickname='test 01')
		user_2 = User.objects.create(username='13636630387')
		user_info_2 = UserInfo.objects.create(user=user_2, nickname='test 02')

		tip = Tip.objects.create(user=user_2,receiver="12345993",message="test4test",create_time="2015-4-9",audio="",photo="")

	def test_get_tip(self):
		json_data = {
			"mobile": 12345993,
			"friend_mobile": "13636630387",
			"mesg_id": 1,
		}
	
		response = self.client.post(reverse('tips:get_tip'), json_data)

		self.assertEqual(response.content, "ok")	