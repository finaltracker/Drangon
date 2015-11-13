kill -INT `cat /tmp/project-master.pid`
uwsgi --stop /tmp/project-master.pid
/etc/init.d/nginx stop
