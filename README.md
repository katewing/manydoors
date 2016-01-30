# manydoors
access script for manylabs door

features:

1. use rfid to record entry/exit at the manylabs door.
2. automatically updates ids from this github repo when new ones are available
3. keeps a local event log on the pi
4. posts a enter/exit events on the #door channel of manylabs slack

# setup

1. login to pi
2. clone github repo using ```git clone https://github.com/jhpoelen/manydoors.git access_control```
3. create symlink to start service ```sudo ln -s /home/pi/rfid/access_control/access_control.conf /etc/init/access_control.conf```
4. restart service using ```sudo service access_control restart```
5. edit crontab for synching github repo ```crontab -e```
6. add ```* * * * * cd /home/pi/rfid/access_control && git pull --rebase```

