# manydoors
access script for manylabs door

use rfid to trigger actions at the manylabs door.

update ids in the github repo when new ones are available

raspberry pi setup sync github repo every minute to keep ids up to date.

# setup

1. login to pi
2. clone github repo using ```git clone https://github.com/jhpoelen/manydoors.git access_control```
3. create symlink to start service ```sudo ln -s /home/pi/rfid/access_control/access_control.conf /etc/init/access_control.conf```
4. restart service using ```sudo service access_control restart```
5. edit crontab for synching github repo ```crontab -e```
6. add ```* * * * * cd /home/pi/rfid/access_control && git pull --rebase
```

