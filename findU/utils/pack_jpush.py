import jpush as jpush
from findU.conf import app_key, master_secret
from jpush import common

def jpush_send_message(push_data, push_target, id):
	_jpush = jpush.JPush(app_key, master_secret)
	push = _jpush.create_push()
	push.audience = jpush.audience(
		# push_target may user account or phone number
		jpush.tag(push_target)
	)
	push.message = jpush.message(msg_content=id, extras=push_data)
	push.platform = jpush.all_
	push.options = {"time_to_live":86400}
	try:
		push.send()
	except common.Unauthorized:
	    raise common.Unauthorized("Unauthorized")
	except common.APIConnectionException:
	    raise common.APIConnectionException("conn error")
	except common.JPushFailure:
	    print ("JPushFailure")
	except:
	    print ("Exception")
