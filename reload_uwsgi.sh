#! /bin/bash
for id in `sudo cat /var/run/cdn.pid`;
do
    sudo kill -9 $id
done
sleep 1

exec sudo uwsgi --ini uwsgi.ini
