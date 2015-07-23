from django.test import TestCase
from django.core.urlresolvers import reverse
from feed.models import PosInfo
from django.contrib.auth.models import User

class feedTests(TestCase):

	def setUp(self):
		user_1 = User.objects.create(username='12345993')
		pos1 = PosInfo(user=user_1)
		pos1.lat = 31.20707817
		pos1.lng = 121.592949
		pos1.save()

	def testUpload(self):
		json_data = {
			'mobile': '12345993',
			"lat": 131.20707817,
			"lng": 21.592949,
		}

		response = self.client.post(reverse('feed:locate_upload'), json_data)
		self.assertEqual(response.content, "ok")		

	def testUpdate(self):
		json_data = {
			'mobile': '12345993',
			'friend_mobile': '12345993',
			'require_type': 'one',
		}

		response = self.client.post(reverse('feed:locate_get'), json_data)
		self.assertEqual(response.content, "ok")			