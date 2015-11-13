#!/bin/bash

# if first argument is 1, then start nginx; other stop nginx
if [ $1 == 1 ]; then
	#uwsgi --ini local_uwsgi.ini
	uwsgi --ini uwsgi.ini
	/etc/init.d/nginx restart
else
	kill -INT `cat /tmp/project-master.pid`
	/etc/init.d/nginx stop
fi
