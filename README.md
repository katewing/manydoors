# manydoors doorbot
purpose: tap-in, tap-out with a ISO 14443A keyfob/card to document workspace usage 

## usage
1. get a keyfob or keycard (if you have one already, you can use it)
2. add your rfid number and name/alias to https://github.com/jhpoelen/manydoors/blob/master/ids.csv 
3. help document space usage by making door buzz when entering and leaving by tapping on the inside/outside facing coils on the door.

## features

1. use rfid to record entry/exit at the manylabs door.
2. automatically updates ids from this github repo when new ones are available
3. keeps a local event log on the pi
4. posts a enter/exit events on the [#door channel of manylabs slack](https://manylabs.slack.com/archives/door/)

# setup

1. login to pi
2. clone github repo using ```git clone https://github.com/jhpoelen/manydoors.git access_control```
3. create symlink to start service ```sudo ln -s /home/pi/rfid/access_control/access_control.conf /etc/init/access_control.conf```
4. restart service using ```sudo service access_control restart```
5. edit crontab for synching github repo ```crontab -e```
6. add ```* * * * * cd /home/pi/rfid/access_control && git pull --rebase```

