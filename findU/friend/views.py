from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import Friend
import time
from django.utils import timezone
import json
import jpush as jpush
import logging
from findU.conf import app_key, master_secret