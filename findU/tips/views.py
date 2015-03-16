from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json
import jpush as jpush
from findU.conf import app_key, master_secret
import logging
logger = logging.getLogger(__name__)

def send_tip(request):
	# save tip
	# notify receiver

def get_tip(request):
	# get tip
